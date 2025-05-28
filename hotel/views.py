from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import TemplateView, ListView, FormView, DeleteView, View, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from .models import Room, Booking, Service, ServiceBooking, Cart, Profile
from .forms import BookingForm, ServiceBookingForm, LoginForm, RegisterForm, ProfileForm

class HomeView(TemplateView):
    template_name = 'hotel/home.html'

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'hotel/booking_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-check_in')

class BookingCreateView(LoginRequiredMixin, FormView):
    template_name = 'hotel/book_room.html'
    form_class = BookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            context['rooms'] = Room.objects.filter(category=category)
        else:
            context['rooms'] = Room.objects.all()
        return context

    def form_valid(self, form):
        room_id = self.request.POST.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']

        if Booking.check_availability(room, check_in, check_out):
            Cart.objects.create(
                user=self.request.user,
                type='ROOM',
                room=room,
                check_in=check_in,
                check_out=check_out
            )
            messages.success(self.request, 'Phòng đã được thêm vào giỏ hàng. Vui lòng kiểm tra giỏ hàng để thanh toán.')
        else:
            messages.error(self.request, 'Phòng đã được đặt trong khoảng thời gian này.')

        return redirect('hotel:book_room')

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('hotel:dashboard')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class ServiceBookingListView(LoginRequiredMixin, ListView):
    model = ServiceBooking
    template_name = 'hotel/service_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return ServiceBooking.objects.filter(user=self.request.user).order_by('-time_call')

class ServiceBookingCreateView(LoginRequiredMixin, FormView):
    template_name = 'hotel/service_booking.html'
    form_class = ServiceBookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            context['services'] = Service.objects.filter(service_type=category)
        else:
            context['services'] = Service.objects.all()
        return context

    def form_valid(self, form):
        service_id = self.request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        quantity = form.cleaned_data['quantity']

        Cart.objects.create(
            user=self.request.user,
            type='SERVICE',
            service=service,
            quantity=quantity
        )
        messages.success(self.request, 'Dịch vụ đã được thêm vào giỏ hàng. Vui lòng kiểm tra giỏ hàng để thanh toán.')

        return redirect('hotel:service_booking')

class ServiceBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = ServiceBooking
    success_url = reverse_lazy('hotel:dashboard')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return ServiceBooking.objects.filter(user=self.request.user)

class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'hotel/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        service_id = request.POST.get('service_id')
        quantity = int(request.POST.get('quantity', 1))
        service = get_object_or_404(Service, id=service_id)

        cart_item, created = Cart.objects.get_or_create(user=request.user, service=service)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return JsonResponse({'message': 'Service added to cart successfully!'})

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
        cart_item.delete()

        return JsonResponse({'message': 'Service removed from cart successfully!'})

class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        total_points = 0
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        for item in cart_items:
            if item.type == 'ROOM':
                if Booking.check_availability(item.room, item.check_in, item.check_out):
                    booking = Booking.objects.create(
                        user=request.user,
                        room=item.room,
                        check_in=item.check_in,
                        check_out=item.check_out,
                        total_price=item.calculate_total_price()
                    )
                    # Tính điểm cho đặt phòng: 10% giá trị
                    points = int(booking.total_price * Decimal('0.10'))
                    total_points += points
                else:
                    messages.error(request, f"Phòng {item.room.number} không khả dụng.")
            elif item.type == 'SERVICE':
                service_booking = ServiceBooking.objects.create(
                    user=request.user,
                    service=item.service,
                    quantity=item.quantity,
                    total_price=item.calculate_total_price()
                )
                # Tính điểm cho đặt dịch vụ: 5% giá trị
                points = int(service_booking.total_price * Decimal('0.05'))
                total_points += points

        if total_points > 0:
            profile.add_loyalty_points(total_points)
            messages.success(request, f'Thanh toán thành công! Bạn nhận được {total_points} điểm tích lũy!')
        else:
            messages.success(request, 'Thanh toán thành công!')
            
        cart_items.delete()
        return redirect('hotel:cart')

class LoginView(FormView):
    template_name = 'hotel/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Đăng nhập thành công!')
        return redirect('hotel:home')

class RegisterView(FormView):
    template_name = 'hotel/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Đăng ký thành công!')
        return redirect('hotel:home')

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Đăng xuất thành công!')
        return redirect('hotel:login')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'hotel/profile.html'
    success_url = reverse_lazy('hotel:profile')

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Thông tin cá nhân đã được cập nhật thành công!')
        return response

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'hotel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['profile'] = Profile.objects.get_or_create(user=user)[0]
        context['recent_bookings'] = Booking.objects.filter(user=user).order_by('-check_in')[:5]
        context['recent_services'] = ServiceBooking.objects.filter(user=user).order_by('-time_call')[:5]
        return context

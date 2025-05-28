from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from .models import Room, Booking, Service, ServiceBooking
from .forms import RoomForm, ServiceForm, BookingForm, ServiceBookingForm, LoginForm, RegisterForm

class HomeView(TemplateView):
    """Hiển thị trang chủ của hệ thống quản lý khách sạn."""
    template_name = 'hotel/home.html'

class RoomListView(LoginRequiredMixin, ListView):
    """Hiển thị danh sách phòng khách sạn."""
    model = Room
    template_name = 'hotel/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        """Input: category           
            Output:danh sách Room đã lọc hoặc tất cả phòng.
        """
        category = self.request.GET.get('category')
        if category:
            return Room.objects.filter(category=category)
        return Room.objects.all()

class RoomCreateView(LoginRequiredMixin, CreateView):
    """Tạo mới thông tin phòng khách sạn."""
    model = Room
    form_class = RoomForm
    template_name = 'hotel/add_room.html'

    def get_success_url(self):
        """Output: URL /rooms/"""
        return reverse_lazy('hotel:room_list')

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    """Chỉnh sửa thông tin phòng khách sạn."""    
    model = Room
    form_class = RoomForm
    template_name = 'hotel/edit_room.html'

    def get_success_url(self):
        return reverse_lazy('hotel:room_list')

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    """Xóa thông tin phòng khách sạn."""
    model = Room
    template_name = 'hotel/delete_room.html'

    def get_success_url(self):
        return reverse_lazy('hotel:room_list')

class ServiceListView(LoginRequiredMixin, ListView):
    """Hiển thị danh sách các dịch vụ trong khách sạn."""
    model = Service
    template_name = 'hotel/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        """Input: category
            Output: Dách sách các dịch vụ được lọc hoặc toàn bộ dịch vụ."""
        category = self.request.GET.get('category')
        if category:
            return Service.objects.filter(service_type=category)
        return Service.objects.all()

class ServiceCreateView(LoginRequiredMixin, CreateView):
    """Thêm mới một dịch vụ vào hệ thống."""
    model = Service
    form_class = ServiceForm
    template_name = 'hotel/add_service.html'

    def get_success_url(self):
        return reverse_lazy('hotel:service_list')

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    """Chỉnh sửa thông tin dịch vụ."""
    model = Service
    form_class = ServiceForm
    template_name = 'hotel/edit_service.html'

    def get_success_url(self):
        return reverse_lazy('hotel:service_list')

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    """Xóa một dịch vụ khỏi hệ thống."""
    model = Service
    template_name = 'hotel/delete_service.html'

    def get_success_url(self):
        return reverse_lazy('hotel:service_list')

class BookingListView(LoginRequiredMixin, ListView):
    """Hiển thị danh sách lịch sử đặt phòng của người dùng."""
    model = Booking
    template_name = 'hotel/booking_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        """Output: Dách sách các Booking của người dùng."""
        return Booking.objects.filter(user=self.request.user).order_by('-check_in')

class BookingCreateView(LoginRequiredMixin, FormView):
    """Tạo mới đặt phòng khách sạn."""
    template_name = 'hotel/book_room.html'
    form_class = BookingForm

    def get_context_data(self, **kwargs):
        """Input:category 
            Output: Danh sách phòng đã lọc theo category hoặc toàn bộ phòng nếu không có lọc."""
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            context['rooms'] = Room.objects.filter(category=category)
        else:
            context['rooms'] = Room.objects.all()
        return context

    def form_valid(self, form):
        """Input: check_in, check_out.
        Output: Đăng kí thành công hoặc thất bị do bị trùng"""
        room_id = self.request.POST.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']

        if Booking.check_availability(room, check_in, check_out):
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=check_in,
                check_out=check_out
            )
            booking.full_clean()
            booking.calculate_total_price()
            messages.success(self.request, f'Đặt phòng thành công! Tổng tiền: {booking.get_total_price()} VND')
        else:
            messages.error(self.request, 'Phòng đã được đặt trong khoảng thời gian này.')

        return redirect('hotel:book_room')

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    """Xóa một đặt phòng của người dùng hiện tại."""
    model = Booking
    template_name = 'hotel/delete_booking.html'

    def get_queryset(self):
        """Input: HTTP request từ người dùng
            Output:danh sách các Booking của người dùng."""
        return Booking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('hotel:booking_history')

class ServiceBookingListView(LoginRequiredMixin, ListView):
    """Hiển thị lịch sử đặt dịch vụ của người dùng"""
    model = ServiceBooking
    template_name = 'hotel/service_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        """Output:Danh sách các ServiceBooking liên kết với người dùng hiện tại."""
        return ServiceBooking.objects.filter(user=self.request.user).order_by('-time_call')

class ServiceBookingCreateView(LoginRequiredMixin, FormView):
    """Tạo đặt dịch vụ mới."""
    template_name = 'hotel/service_booking.html'
    form_class = ServiceBookingForm

    def get_context_data(self, **kwargs):
        """Input:Chọn category.
            Output:Dách sach các ServiceBooking theo category"""
        context = super().get_context_data(**kwargs)
        category = self.request.GET.get('category')
        if category:
            context['services'] = Service.objects.filter(service_type=category)
        else:
            context['services'] = Service.objects.all()
        return context

    def form_valid(self, form):
        """Input: service_id, quantity.
            Output: Thông báo thành công và tổng tiền."""
        service_id = self.request.POST.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        quantity = form.cleaned_data['quantity']

        service_booking = ServiceBooking.objects.create(
            user=self.request.user,
            service=service,
            quantity=quantity
        )
        service_booking.calculate_total_price()
        messages.success(self.request, f'Dịch vụ đã được đặt thành công! Tổng tiền: {service_booking.get_total_price()} VND')

        return redirect('hotel:service_booking')

class ServiceBookingDeleteView(LoginRequiredMixin, DeleteView):
    """Xóa một bản ghi đặt dịch vụ của người dùng hiện tại."""
    model = ServiceBooking
    template_name = 'hotel/delete_service_booking.html'

    def get_queryset(self):
        """Input: HTTP request từ người dùng
            Output: Dach sách các ServiceBooking thuộc về người dùng hiện tại."""
        return ServiceBooking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('hotel:service_history')

class LoginView(FormView):
    """Xử lý chức năng đăng nhập người dùng."""
    template_name = 'hotel/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        """Input: `username`, `password`.
            Output: Đăng nhập người dùng và redirect đến trang chủ"""
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'Đăng nhập thành công!')
        return redirect('hotel:home')

class RegisterView(FormView):
    """Xử lý chức năng đăng ký người dùng mới."""
    template_name = 'hotel/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        """Input:user_name, password'
            Output: đăng kí thành công lưu dữ liệu người dùng"""
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Đăng ký thành công!')
        return redirect('hotel:home')

class LogoutView(TemplateView):
    """Xử lý chức năng đăng xuất người dùng"""
    def get(self, request, *args, **kwargs):
        """Input:HTTP GET request
            Output:Đăng xuất người dùng"""
        logout(request)
        messages.success(request, 'Đăng xuất thành công!')
        return redirect('hotel:login')

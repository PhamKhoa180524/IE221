from django.urls import path
from . import views
from .views import CartListView, AddToCartView, RemoveFromCartView

app_name = 'hotel' 

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 

    path('booking/', views.BookingCreateView.as_view(), name='book_room'),
    path('booking/history/', views.BookingListView.as_view(), name='booking_history'),
    path('booking/delete/<int:pk>/', views.BookingDeleteView.as_view(), name='delete_booking'),

    path('service-booking/', views.ServiceBookingCreateView.as_view(), name='service_booking'),
    path('service-booking/history/', views.ServiceBookingListView.as_view(), name='service_history'),
    path('service-booking/delete/<int:pk>/', views.ServiceBookingDeleteView.as_view(), name='delete_service_booking'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('cart/', CartListView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
]

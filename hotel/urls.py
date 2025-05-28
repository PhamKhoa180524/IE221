from django.urls import path
from . import views

app_name = 'hotel' 

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/add/', views.RoomCreateView.as_view(), name='add_room'),
    path('rooms/edit/<int:pk>/', views.RoomUpdateView.as_view(), name='edit_room'),
    path('rooms/delete/<int:pk>/', views.RoomDeleteView.as_view(), name='delete_room'),

    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/add/', views.ServiceCreateView.as_view(), name='add_service'),
    path('services/edit/<int:pk>/', views.ServiceUpdateView.as_view(), name='edit_service'),
    path('services/delete/<int:pk>/', views.ServiceDeleteView.as_view(), name='delete_service'),

    path('booking/', views.BookingCreateView.as_view(), name='book_room'),
    path('booking/history/', views.BookingListView.as_view(), name='booking_history'),
    path('booking/delete/<int:pk>/', views.BookingDeleteView.as_view(), name='delete_booking'),

    path('service-booking/', views.ServiceBookingCreateView.as_view(), name='service_booking'),
    path('service-booking/history/', views.ServiceBookingListView.as_view(), name='service_history'),
    path('service-booking/delete/<int:pk>/', views.ServiceBookingDeleteView.as_view(), name='delete_service_booking'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

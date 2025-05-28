from django import forms
from .models import Room, Service,Booking,ServiceBooking
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

class RoomForm(forms.ModelForm):
    """Form cho phép thêm hoặc chỉnh sửa thông tin phòng khách sạn."""
    class Meta:
        model = Room
        fields = ['number', 'category', 'beds', 'price', 'image_url']  # Các trường trong form

class ServiceForm(forms.ModelForm):
    """Form để thêm hoặc chỉnh sửa thông tin dịch vụ khách sạn."""
    class Meta:
        model = Service
        fields = ['service_name', 'service_type', 'price','image_url' ]
        
class BookingForm(forms.ModelForm):
    """Form để tạo đặt phòng khách sạn."""
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def clean(self):
        
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out and check_in >= check_out:
            raise ValidationError("Ngày Check-in phải trước ngày Check-out.")

class ServiceBookingForm(forms.ModelForm):
    """Form để tạo đặt dịch vụ."""
    class Meta:
        model = ServiceBooking
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Nhập số lượng'
            })
        }
        
class LoginForm(AuthenticationForm):
    """Form xác thực thông tin đăng nhập của người dùng."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tên đăng nhập',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mật khẩu',
    }))

class RegisterForm(UserCreationForm):
    """Form để tạo tài khoản người dùng mới."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tên đăng nhập',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Họ',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tên',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mật khẩu',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Xác nhận mật khẩu',
    }))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    
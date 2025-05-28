from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class BaseBooking(models.Model):
    """Lớp trừu tượng dùng chung cho Booking và ServiceBooking."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)

    class Meta:
        abstract = True

    def set_total_price(self, price):
        if price < 0:
            raise ValidationError('Tổng giá không thể nhỏ hơn 0')
        self.total_price = price

    def get_total_price(self):
        return self.total_price

    def calculate_total_price(self):
        pass

class Room(models.Model):
    """Lớp biến diễn thông tin phòng khách sạn."""
    ROOM_CATEGORIES = (
        ('SGL', 'SINGLE'),
        ('TWN', 'TWIN'),
        ('DBL', 'DOUBLE'),
        ('TPL', 'TRIPLE')
    )
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Room {self.number} - {self.category} - {self.beds} - {self.price} VND"

    def get_price(self):
        return self.price

    def set_price(self, price):
        if price < 0:
            raise ValidationError('Giá phòng không thể nhỏ hơn 0')
        self.price = price

class Service(models.Model):
    """Lớp biểu diễn thông tin dịch vụ khách sạn."""
    SERVICE_CATEGORIES = (
        ('FOOD', 'FOOD'),
        ('DRINK', 'DRINK'),
        ('SPA', 'SPA')
    )
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=5, choices=SERVICE_CATEGORIES)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Service {self.service_name} - {self.service_name} - {self.service_type} -  {self.price} VND"

    def get_price(self):
        return self.price

    def set_price(self, price):
        if price < 0:
            raise ValidationError('Giá dịch vụ không thể nhỏ hơn 0')
        self.price = price

class Booking(BaseBooking):
    """Lớp mô hình đại diện cho thông tin đặt phòng khách sạn kế thừa từ lớp BaseBooking"""
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f"Booking {self.user} - {self.room} - {self.check_in} - {self.check_out} - {self.total_price} VND"

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError({
                'check_in': _("Đặt phòng check-in phải trước ngày check-out."),
                'check_out': _("Đặt phòng check-out phải sau ngày check-in."),
            })

    def calculate_total_price(self):
        duration = (self.check_out - self.check_in).days
        if duration <= 0:
            duration = 1
        self.total_price = self.room.price * duration
        self.save()

    def get_total_price(self):
        return self.total_price

    @staticmethod
    def check_availability(room, check_in, check_out):
        bookings = Booking.objects.filter(room=room)
        for booking in bookings:
            if booking.check_in < check_out and booking.check_out > check_in:
                return False
        return True

class ServiceBooking(BaseBooking):
    """Lớp biểu diễn cho đặt dịch vụ của khách hàng kế thừa từ lớp cha BaseBooking"""
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    time_call = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Service {self.user} - {self.service} - {self.quantity} - {self.time_call} - {self.total_price} VND"

    def calculate_total_price(self):
        if self.quantity <= 0:
            raise ValidationError('Số lượng phải lớn hơn 0')
        self.total_price = self.service.price * self.quantity
        self.save()

    def get_total_price(self):
        return self.total_price

    def get_service_name(self):
        return self.service.service_name

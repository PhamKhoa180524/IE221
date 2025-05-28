# Hệ thống Quản lý Khách sạn

## Tính năng

### Người dùng
- **Đặt Phòng**: Xem và đặt phòng theo ngày
- **Đặt Dịch vụ**: Đặt các dịch vụ như đồ ăn, đồ uống, spa
- **Giỏ hàng**: Quản lý đơn đặt phòng và dịch vụ
- **Bảng điều khiển**: Theo dõi lịch sử đặt phòng và dịch vụ
- **Thông tin cá nhân**: Cập nhật thông tin cá nhân
- **Điểm tích lũy**: Tích điểm khi đặt phòng và dịch vụ

### Quản trị viên
- **Quản lý Phòng**: Thêm, sửa, xóa thông tin phòng
- **Quản lý Dịch vụ**: Thêm, sửa, xóa thông tin dịch vụ
- **Quản lý Người dùng**: Quản lý tài khoản và thông tin người dùng

## Cài đặt

### Yêu cầu hệ thống
- Python 3.11 trở lên
- Django 5.2.1
- Môi trường ảo (khuyến nghị)

### Các bước cài đặt
1. Tải mã nguồn:
   ```bash
   git clone https://github.com/PhamKhoa180524/IE221.git
   cd IE221
   ```

2. Tạo và kích hoạt môi trường ảo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   ```

3. Cài đặt các gói phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

4. Thực hiện migrate cơ sở dữ liệu:
   ```bash
   python manage.py migrate
   ```

5. Tạo tài khoản quản trị viên:
   ```bash
   python manage.py createsuperuser
   ```

6. Khởi chạy máy chủ phát triển:
   ```bash
   python manage.py runserver
   ```

7. Truy cập ứng dụng trong trình duyệt:
   ```
   http://127.0.0.1:8000/
   ```

## Cấu trúc dự án


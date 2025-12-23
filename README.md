# **🏦 Tingee Payments for Home Assistant (HASS)**

Bộ tích hợp mã nguồn mở cho phép Home Assistant nhận thông báo biến động số dư ngân hàng theo thời gian thực từ Tingee thông qua Webhook. Tự động phát loa thông báo (TTS), hiển thị số tiền và nội dung giao dịch ngay trên Dashboard của bạn.

## **🌟 Tính năng chính**

Xác thực bảo mật: Sử dụng thuật toán HMAC SHA512 để kiểm tra chữ ký từ Tingee, đảm bảo dữ liệu không bị giả mạo.

Tích hợp sẵn TTS: Tự động gọi dịch vụ tts.speak (tối ưu cho Edge TTS) để đọc số tiền và nội dung khi có tiền về.

Sensor giao dịch: Tạo ra thực thể sensor.tingee_last_transaction lưu trữ thông tin: Số tiền, Nội dung, Ngân hàng, Mã giao dịch.

Giao diện UI chuyên nghiệp: Cấu hình hoàn toàn qua giao diện Home Assistant, hỗ trợ nút "Cấu hình lại" (Configure).

Thông báo thông minh: Tự động gửi URL Webhook vào mục thông báo hệ thống để bạn dễ dàng sao chép.

## **🚀 Hướng dẫn cài đặt  **

Bước 1: Chuẩn bị phía Tingee

Truy cập [app.tingee.vn](https://app.tingee.vn/account/register-an-account?referral=0846087165) và đăng ký tài khoản.

Liên kết tài khoản ngân hàng của bạn vào hệ thống Tingee.

Nhấp vào Ảnh đại diện (Avatar) -> chọn Developers.

Sao chép dòng Secret Token (Đây là chìa khóa để HASS xác thực dữ liệu).

Bước 2: Cài đặt vào Home Assistant

Truy cập vào thư mục cấu hình của HASS (thường là /config).

Tìm (hoặc tạo mới) thư mục custom_components.

Tải bộ mã nguồn này về và copy thư mục tingee vào đó.

Cấu trúc đúng: /config/custom_components/tingee/__init__.py, v.v.

Khởi động lại Home Assistant (Bắt buộc để hệ thống nạp linh kiện mới).

Bước 3: Cấu hình trên giao diện HASS

Vào Settings (Cài đặt) -> Devices & Services (Thiết bị & Dịch vụ).

Nhấn nút Add Integration (Thêm tích hợp) ở góc dưới bên phải.

Tìm kiếm từ khóa Tingee và chọn nó.

Điền các thông số trong bảng hiện ra:

Secret Key: Dán mã Token lấy ở Bước 1.

Webhook ID: Đặt tên bất kỳ (ví dụ: shop_thanh_toan). Lưu ý: Không dùng dấu cách hoặc ký tự đặc biệt.

Media Player: Chọn loa bạn muốn phát thông báo (Ví dụ: media_player.google_home).

TTS Entity: Chọn bộ đọc giọng nói (Ví dụ: tts.edge_tts_2).

Nhấn Submit.

Bước 4: Lấy URL và dán vào Tingee

Sau khi cài xong, nhìn vào biểu tượng Cái chuông (Notifications) ở góc trái màn hình HASS.

Bạn sẽ thấy một thông báo chứa đường dẫn Webhook (Dạng: https://your-domain.duckdns.org/api/webhook/shop_thanh_toan).

Sao chép URL này.

Quay lại trang Tingee (Developers) -> Nhấn Thêm URL -> Dán URL vào và nhấn Lưu.

📊 Hiển thị lên Dashboard

Để xem thông tin giao dịch trên màn hình chính:

Nhấn Edit Dashboard -> Add Card.

Chọn thẻ Entities.

Tìm thực thể sensor.tingee_last_transaction.

(Tùy chọn) Sử dụng thuộc tính (Attributes) để hiện thêm Nội dung hoặc Ngân hàng bằng cách sử dụng attribute trong card.

🤖 Tự động hóa nâng cao (Automation)

Bộ tích hợp tự động bắn một sự kiện (Event) có tên tingee_new_transaction. Bạn có thể dùng nó để làm các việc khác như nháy đèn:

alias: "Nháy đèn khi có tiền về"
trigger:
  - platform: event
    event_type: "tingee_new_transaction"
action:
  - service: light.turn_on
    target:
      entity_id: light.phong_khach
    data:
      flash: short
      color_name: green


❓ Xử lý sự cố (Troubleshooting)

Lỗi "Handler is đã tồn tại": Xóa tích hợp cũ, khởi động lại HASS rồi cài lại với Webhook ID khác.

Không nhận được Webhook: - Đảm bảo HASS của bạn có thể truy cập từ internet (Sử dụng HTTPS, Nabu Casa hoặc Cloudflare).

Kiểm tra xem bạn đã dán đúng URL vào trang Tingee chưa.

Loa không đọc: Kiểm tra xem thực thể tts bạn chọn có đang hoạt động hay không bằng cách vào mục Developer Tools -> Services để thử gọi tts.speak.

🛡️ Bảo mật

Mọi dữ liệu thanh toán được xử lý nội bộ trong Home Assistant của bạn. Chữ ký được kiểm tra cục bộ bằng Secret Token, đảm bảo chỉ có dữ liệu từ Tingee mới được chấp nhận.

Phát triển bởi Cộng đồng Home Assistant Việt Nam.

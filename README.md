# **🏦 Tingee Payments for Home Assistant (HASS)**

Bộ tích hợp mã nguồn mở cho phép Home Assistant nhận thông báo biến động số dư ngân hàng theo thời gian thực từ Tingee thông qua Webhook. Tự động phát loa thông báo (TTS), hiển thị số tiền và nội dung giao dịch ngay trên Dashboard của bạn.

## **🌟 Tính năng chính**

Xác thực bảo mật: Sử dụng thuật toán HMAC SHA512 để kiểm tra chữ ký từ Tingee, đảm bảo dữ liệu không bị giả mạo.

Tích hợp sẵn TTS: Tự động gọi dịch vụ tts.speak (tối ưu cho Edge TTS) để đọc số tiền và nội dung khi có tiền về.

Sensor giao dịch: Tạo ra thực thể sensor.tingee_last_transaction lưu trữ thông tin: Số tiền, Nội dung, Ngân hàng, Mã giao dịch.

Giao diện UI chuyên nghiệp: Cấu hình hoàn toàn qua giao diện Home Assistant, hỗ trợ nút "Cấu hình lại" (Configure).

Thông báo thông minh: Tự động gửi URL Webhook vào mục thông báo hệ thống để bạn dễ dàng sao chép.

## **🚀 Hướng dẫn cài đặt  **

## ** Bước 1: Chuẩn bị phía Tingee 

Truy cập [app.tingee.vn](https://app.tingee.vn/account/register-an-account?referral=0846087165) và đăng ký tài khoản.

Liên kết tài khoản ngân hàng của bạn vào hệ thống Tingee.

Nhấp vào Ảnh đại diện (Avatar) -> chọn Developers.

Sao chép dòng Secret Token (Đây là chìa khóa để HASS xác thực dữ liệu).

### **Bước 2: Cài qua Hacs

Điền link vào kho lưu trữ tùy chỉnh https://github.com/trankhanhduy2929-beep/tingee

## ** Bước 3: Cấu hình trên giao diện HASS

Vào Settings (Cài đặt) -> Devices & Services (Thiết bị & Dịch vụ).

Nhấn nút Add Integration (Thêm tích hợp) ở góc dưới bên phải.

Tìm kiếm từ khóa Tingee và chọn nó.

Điền các thông số trong bảng hiện ra:

Secret Key: Dán mã Token lấy ở Bước 1.

Webhook ID: Đặt tên bất kỳ (ví dụ: shop_thanh_toan). Lưu ý: Không dùng dấu cách hoặc ký tự đặc biệt.

Media Player: Chọn loa bạn muốn phát thông báo (Ví dụ: media_player.google_home).

TTS Entity: Chọn bộ đọc giọng nói (Ví dụ: tts.edge_tts_2).

Nhấn Submit.

## ** Bước 4: Lấy URL và dán vào Tingee

Sau khi cài xong, nhìn vào biểu tượng Cái chuông (Notifications) ở góc trái màn hình HASS.

Bạn sẽ thấy một thông báo chứa đường dẫn Webhook (Dạng: https://your-domain.duckdns.org/api/webhook/shop_thanh_toan).

Sao chép URL này.

Quay lại trang Tingee (Developers) -> Nhấn Thêm URL -> Dán URL vào và nhấn Lưu.

## ** 📊 Hiển thị lên Dashboard
```yaml
type: grid
cards:
  - type: heading
    heading: tingee
    heading_style: title
  - type: vertical-stack
    cards:
      - type: custom:mushroom-title-card
        title: Biến động số dư
        subtitle: Hệ thống giám sát Tingee
      - type: grid
        columns: 2
        square: false
        cards:
          - type: custom:mushroom-entity-card
            entity: sensor.tingee_tong_hom_nay
            name: Hôm nay
            icon: mdi:wallet-outline
            icon_color: green
            primary_info: state
            secondary_info: name
          - type: custom:mushroom-entity-card
            entity: sensor.tingee_tong_thang_nay
            name: Tháng này
            icon: mdi:bank-transfer-in
            icon_color: blue
            primary_info: state
            secondary_info: name
      - type: custom:mushroom-template-card
        primary: "{{ states('sensor.tingee_so_tien') | float | format_number }} VNĐ"
        secondary: "{{ states('sensor.tingee_noi_dung') }}"
        icon: mdi:cash-plus
        icon_color: orange
        layout: horizontal
        multiline_secondary: true
        tap_action:
          action: more-info
        entity: sensor.tingee_so_tien
      - type: custom:mushroom-chips-card
        chips:
          - type: template
            content: "Ngân hàng: {{ states('sensor.tingee_ngan_hang') }}"
            icon: mdi:bank
            icon_color: grey
          - type: template
            content: >-
              {% set t = states('sensor.tingee_thoi_gian') %} {{ t[8:10] }}:{{
              t[10:12] }} - {{ t[6:8] }}/{{ t[4:6] }}/{{ t[0:4] }}
            icon: mdi:clock-outline
            icon_color: grey
        alignment: start
  - type: logbook
    entities:
      - sensor.tingee_so_tien
      - sensor.tingee_noi_dung
    title: Lịch sử tiền về
    hours_to_show: 48
```


## ** ❓ Xử lý sự cố (Troubleshooting)

Lỗi "Handler is đã tồn tại": Xóa tích hợp cũ, khởi động lại HASS rồi cài lại với Webhook ID khác.

Không nhận được Webhook: - Đảm bảo HASS của bạn có thể truy cập từ internet (Sử dụng HTTPS, Nabu Casa hoặc Cloudflare).

Kiểm tra xem bạn đã dán đúng URL vào trang Tingee chưa.

Loa không đọc: Kiểm tra xem thực thể tts bạn chọn có đang hoạt động hay không bằng cách vào mục Developer Tools -> Services để thử gọi tts.speak.

## ** 🛡️ Bảo mật

Mọi dữ liệu thanh toán được xử lý nội bộ trong Home Assistant của bạn. Chữ ký được kiểm tra cục bộ bằng Secret Token, đảm bảo chỉ có dữ liệu từ Tingee mới được chấp nhận.


Tingee Payments for Home Assistant
Bộ tích hợp (Custom Component) cho phép Home Assistant nhận thông báo biến động số dư ngân hàng theo thời gian thực từ Tingee thông qua Webhook.

✨ Tính năng chính
Webhook bảo mật: Xác thực tính toàn vẹn dữ liệu bằng giải thuật HMAC SHA512 và Secret Token.

Thông báo giọng nói (TTS): Tự động phát thông báo qua loa (Google Home, Alexa, v.v.) bằng Edge TTS khi có tiền về.

Cảm biến (Sensor): Hiển thị số tiền, nội dung, ngân hàng và thời gian giao dịch gần nhất lên Dashboard.

Giao diện trực quan: Cấu hình hoàn toàn qua UI (Config Flow), không cần sửa file configuration.yaml.

Thông báo URL: Tự động tạo thông báo trong Home Assistant để bạn copy đường dẫn Webhook nhanh chóng.

🛠 Cài đặt
Cách 1: Cài đặt thủ công
Tải thư mục tingee từ Repository này.

Copy thư mục tingee vào thư mục custom_components trong bộ cài Home Assistant của bạn.

Cấu trúc thư mục: /config/custom_components/tingee/

Khởi động lại Home Assistant.

Cách 2: Cài đặt qua HACS (Đang cập nhật)
Mở HACS -> Integrations.

Chọn dấu 3 chấm ở góc trên bên phải -> Custom repositories.

Dán URL của Repository này vào và chọn Category là Integration.

Nhấn Install.

⚙️ Cấu hình
Bước 1: Chuẩn bị trên Tingee
Đăng ký tài khoản tại app.tingee.vn.

Thêm cửa hàng và liên kết tài khoản ngân hàng của bạn.

Vào mục Avatar -> Developers để lấy Secret Token.

Bước 2: Thêm tích hợp vào Home Assistant
Vào Settings -> Devices & Services -> Add Integration.

Tìm kiếm Tingee Payments.

Nhập các thông số:

Secret Key: Token lấy từ mục Developers của Tingee.

Webhook ID: Tên đường dẫn bạn muốn (ví dụ: my_shop_payment).

Media Player: Chọn loa muốn phát thông báo.

TTS Entity: Chọn thực thể Edge TTS (ví dụ: tts.edge_tts_2).

Bước 3: Liên kết Webhook
Ngay sau khi nhấn Submit, một thông báo (Persistent Notification) sẽ hiện lên ở biểu tượng hình chuông trong Home Assistant.

Copy đường dẫn Webhook có dạng: https://domain-cua-ban.duckdns.org/api/webhook/webhook_id.

Truy cập trang quản trị Tingee -> Developers -> Thêm Url và dán đường dẫn vừa copy vào.

📊 Thông tin dữ liệu nhận được
Mỗi khi có giao dịch, Tingee sẽ gửi các thông tin sau về Home Assistant: | Trường thông tin | Mô tả | | :--- | :--- | | amount | Số tiền giao dịch | | content | Nội dung chuyển khoản | | bank | Tên ngân hàng nhận | | transactionCode | Mã giao dịch | | transactionDate | Thời gian giao dịch (yyyyMMddHHmmss) |

🔔 Tự động hóa mẫu
Ngoài tính năng TTS tự động có sẵn, bạn có thể dùng Event tingee_new_transaction để tạo các kịch bản riêng:

YAML

automation:
  - alias: "Nháy đèn xanh khi nhận tiền"
    trigger:
      - platform: event
        event_type: "tingee_new_transaction"
    action:
      - service: light.turn_on
        target:
          entity_id: light.quay_thu_ngan
        data:
          color_name: green
          brightness_pct: 100
⚠️ Lưu ý bảo mật
HTTPS: Bạn phải cấu hình Home Assistant chạy dưới giao thức HTTPS (qua DuckDNS, Nabu Casa hoặc Cloudflare) để Tingee có thể gửi Webhook về.

Xác thực: Bộ tích hợp này đã cài đặt sẵn quy tắc kiểm tra tính toàn vẹn dữ liệu: HMAC_SHA512({timestamp}:{body}, SecretKey) theo đúng yêu cầu của Tingee.

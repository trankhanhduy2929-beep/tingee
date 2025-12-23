import logging
import hmac
import hashlib
from datetime import datetime
from aiohttp import web
from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

_LOGGER = logging.getLogger(__name__)
DOMAIN = "tingee"
SIG_RECV = "tingee_data_update"

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    config = {**entry.data, **entry.options}
    webhook_id = config.get("webhook_id")
    hass.data[DOMAIN][entry.entry_id] = webhook_id

    async def handle_webhook(hass, webhook_id, request):
        try:
            # Tingee gửi header x-signature và x-request-timestamp để xác thực
            signature = request.headers.get("x-signature")
            timestamp = request.headers.get("x-request-timestamp")
            
            body_bytes = await request.read()
            body_str = body_bytes.decode("utf-8")
            data = await request.json()
            
            current_config = {**entry.data, **entry.options}
            secret_token = current_config.get("secret_token")

            # 1. Kiểm tra tính toàn vẹn (Signature) nếu có Token
            if secret_token:
                # Chuỗi cần hash: {timestamp}:{body}
                check_str = f"{timestamp}:{body_str}"
                mac = hmac.new(
                    secret_token.encode("utf-8"),
                    msg=check_str.encode("utf-8"),
                    digestmod=hashlib.sha512
                )
                expected_signature = mac.hexdigest()
                
                if not hmac.compare_digest(signature or "", expected_signature):
                    _LOGGER.error("Tingee: Chữ ký không hợp lệ!")
                    return web.json_response({"code": "09", "message": "Invalid signature"})

            # Gửi dữ liệu cho sensor
            async_dispatcher_send(hass, SIG_RECV, data)

            amount = data.get("amount", 0)
            content = data.get("content", "").lower()
            
            # 2. Xử lý TTS (Phát loa)
            if amount > 0:
                keyword = current_config.get("keyword_filter", "").lower()
                if keyword and keyword not in content:
                    _LOGGER.info("Tingee: Bỏ qua vì không khớp từ khóa")
                else:
                    # Kiểm tra giờ yên tĩnh
                    now = datetime.now().hour
                    start_q = current_config.get("quiet_start", 23)
                    end_q = current_config.get("quiet_end", 6)
                    
                    is_quiet = False
                    if start_q > end_q:
                        if now >= start_q or now < end_q: is_quiet = True
                    else:
                        if start_q <= now < end_q: is_quiet = True

                    if not is_quiet:
                        amount_str = "{:,}".format(int(amount)).replace(",", ".")
                        message = f"Bạn vừa nhận được {amount_str} đồng."
                        
                        await hass.services.async_call(
                            "tts", "speak",
                            {
                                "media_player_entity_id": [current_config.get("media_player")],
                                "message": message,
                                "language": current_config.get("language", "vi-VN"),
                                "cache": True,
                                "options": {
                                    "voice": current_config.get("voice", "vi-VN-HoaiMyNeural"),
                                    "rate": current_config.get("rate", "+0%"),
                                    "volume": current_config.get("volume", "+10%"),
                                }
                            },
                            target={"entity_id": current_config.get("tts_entity", "tts.edge_tts")}
                        )

            # Trả về thành công cho Tingee
            return web.json_response({"code": "00", "message": "success"})

        except Exception as e:
            _LOGGER.error("Lỗi Tingee Webhook: %s", str(e))
            return web.json_response({"code": "99", "message": str(e)})

    webhook.async_register(hass, DOMAIN, "Tingee Webhook", webhook_id, handle_webhook)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    webhook_id = hass.data[DOMAIN].pop(entry.entry_id, None)
    if webhook_id:
        try:
            webhook.async_unregister(hass, webhook_id)
        except:
            pass
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
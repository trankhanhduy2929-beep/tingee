from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

DOMAIN = "tingee"
SIG_RECV = "tingee_data_update"

async def async_setup_entry(hass, entry, async_add_entities):
    sensors = [
        TingeeSensor(entry, "Số tiền", "amount", "VND", "mdi:cash-multiple"),
        TingeeSensor(entry, "Nội dung", "content", None, "mdi:text-short"),
        TingeeSensor(entry, "Số tài khoản", "accountNumber", None, "mdi:account-card-details"),
        TingeeSensor(entry, "Mã giao dịch", "transactionCode", None, "mdi:identifier"),
        TingeeSensor(entry, "Thời gian", "transactionDate", None, "mdi:clock-outline"),
        TingeeSensor(entry, "Ngân hàng", "bank", None, "mdi:bank"),
        TingeeTotalSensor(entry, "Tổng hôm nay", "daily"),
        TingeeTotalSensor(entry, "Tổng tháng này", "monthly"),
    ]
    async_add_entities(sensors)

class TingeeSensor(SensorEntity, RestoreEntity):
    def __init__(self, entry, name, key, unit, icon):
        self._entry = entry
        self._key = key
        self._attr_name = f"Tingee: {name}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_native_value = 0 if unit == "VND" else "Chưa có dữ liệu"

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._entry.entry_id)}, "name": "Tingee Notifier", "manufacturer": "Tingee.vn"}

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in ["unknown", "unavailable"]:
            self._attr_native_value = last_state.state

        async def update_data(data):
            val = data.get(self._key)
            if val is not None:
                self._attr_native_value = val
                self.async_write_ha_state()
        self.async_on_remove(async_dispatcher_connect(self.hass, SIG_RECV, update_data))

class TingeeTotalSensor(SensorEntity, RestoreEntity):
    def __init__(self, entry, name, period):
        self._entry = entry
        self._period = period
        self._attr_name = f"Tingee: {name}"
        self._attr_unique_id = f"{entry.entry_id}_total_{period}"
        self._attr_native_unit_of_measurement = "VND"
        self._attr_icon = "mdi:chart-line"
        self._attr_native_value = 0
        self._last_reset = datetime.now()

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._entry.entry_id)}, "name": "Tingee Notifier"}

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state and last_state.state not in ["unknown", "unavailable"]:
            try: self._attr_native_value = float(last_state.state)
            except: self._attr_native_value = 0

        async def update_total(data):
            now = datetime.now()
            if self._period == "daily" and now.day != self._last_reset.day:
                self._attr_native_value = 0
            elif self._period == "monthly" and now.month != self._last_reset.month:
                self._attr_native_value = 0
            
            self._last_reset = now
            self._attr_native_value += float(data.get("amount", 0))
            self.async_write_ha_state()

        self.async_on_remove(async_dispatcher_connect(self.hass, SIG_RECV, update_total))
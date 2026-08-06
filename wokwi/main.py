import network
import time
from machine import Pin, ADC, I2C
from umqtt.simple import MQTTClient
import ujson
import os
import ssd1306

# 1. إعداد دبابيس المخرجات
relay = Pin(26, Pin.OUT)
buzzer = Pin(25, Pin.OUT)
green_led = Pin(27, Pin.OUT)

# 2. إعداد الشاشتين وتحديد العناوين لتجنب ETIMEDOUT
# الشاشة الأولى على HW I2C0
i2c1 = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
# الشاشة الثانية على HW I2C1
i2c2 = I2C(1, scl=Pin(16), sda=Pin(17), freq=400000)

try:
    oled1 = ssd1306.SSD1306_I2C(128, 64, i2c1, addr=0x3c)
    oled2 = ssd1306.SSD1306_I2C(128, 64, i2c2, addr=0x3c)
    print("OLED Displays Initialized Successfully!")
except Exception as e:
    print("OLED Init Warning:", e)

# 3. إعداد المدخلات التناظرية (ADC)
pot_current = ADC(Pin(34))
pot_voltage = ADC(Pin(35))
pot_current.atten(ADC.ATTN_11DB)
pot_voltage.atten(ADC.ATTN_11DB)
pot_current.width(ADC.WIDTH_12BIT)
pot_voltage.width(ADC.WIDTH_12BIT)

# 4. متغيرات ذاكرة Flash
FLASH_FILE = "energy_data.json"
TARIFF_PER_KWH = 1.5
CO2_FACTOR = 0.4

def load_flash_data():
    try:
        if FLASH_FILE in os.listdir():
            with open(FLASH_FILE, "r") as f:
                data = ujson.load(f)
                return data.get("total_kwh", 0.0), data.get("peak_power", 0.0)
    except Exception:
        pass
    return 0.0, 0.0

def save_flash_data(kwh, peak):
    try:
        with open(FLASH_FILE, "w") as f:
            ujson.dump({"total_kwh": kwh, "peak_power": peak}, f)
    except Exception:
        pass

total_kwh, peak_power_w = load_flash_data()
total_cost = total_kwh * TARIFF_PER_KWH
total_co2_kg = total_kwh * CO2_FACTOR

relay.value(1)
buzzer.value(0)
green_led.value(1)

manual_override = False

# 5. الاتصال بالـ Wi-Fi
print("Connecting to WiFi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Wokwi-GUEST', '')

while not wlan.isconnected():
    time.sleep(0.5)
print("WiFi Connected!")

# 6. دالة استقبال أوامر MQTT
def mqtt_callback(topic, msg):
    global manual_override, total_kwh, total_cost, total_co2_kg, peak_power_w
    command = msg.decode('utf-8')
    print("📩 Received Command:", command)

    if command == "RELAY_ON":
        manual_override = False
        relay.value(1)
    elif command == "RELAY_OFF":
        manual_override = True
        relay.value(0)
    if command == "BUZZER_ON":
        buzzer.value(1)
    elif command == "BUZZER_OFF":
        buzzer.value(0)
    if command in ["RESET_METER", "RESET"]:
        total_kwh = 0.0
        total_cost = 0.0
        total_co2_kg = 0.0
        peak_power_w = 0.0
        save_flash_data(0.0, 0.0)
        print("🧹 Meter Reset!")

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC_PUB = "electric11"
TOPIC_SUB = "electric/control11"

client = MQTTClient("esp32_electric_smart_ctrl", MQTT_BROKER, port=MQTT_PORT)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(TOPIC_SUB)
print(f"Connected to Broker & Subscribed to '{TOPIC_SUB}'!")

last_time = time.time()
last_save_time = time.time()

while True:
    try:
        client.check_msg()
    except Exception:
        pass

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    raw_current = pot_current.read()
    raw_voltage = pot_voltage.read()

    voltage_val = (raw_voltage / 4095.0) * 250.0
    current_amp = (raw_current / 4095.0) * 30.0

    load_ratio = raw_current / 4095.0
    power_factor = round(0.98 - (load_ratio * 0.23), 2)

    apparent_power = voltage_val * current_amp
    real_power = apparent_power * power_factor

    if real_power > peak_power_w:
        peak_power_w = real_power

    interval_kwh = (real_power / 1000.0) * (dt / 3600.0)
    total_kwh += interval_kwh
    total_cost = total_kwh * TARIFF_PER_KWH
    total_co2_kg = total_kwh * CO2_FACTOR

    status = "NORMAL"
    if raw_current > 2048:
        buzzer.value(1)
        green_led.value(0)
        relay.value(0)
        status = "OVERLOAD"
    else:
        buzzer.value(0)
        green_led.value(1)
        if not manual_override:
            relay.value(1)

    # تحديث الشاشات بحماية من الـ Crash
    try:
        oled1.fill(0)
        oled1.text("LIVE MONITOR", 15, 0)
        oled1.text(f"Volt: {voltage_val:.1f} V", 0, 18)
        oled1.text(f"Curr: {current_amp:.2f} A", 0, 33)
        oled1.text(f"Power:{real_power:.1f} W", 0, 48)
        oled1.show()

        oled2.fill(0)
        oled2.text("ENERGY METER", 15, 0)
        oled2.text(f"kWh : {total_kwh:.4f}", 0, 18)
        oled2.text(f"Cost: {total_cost:.2f} EGP", 0, 33)
        oled2.text(f"STAT: {status}", 0, 48)
        oled2.show()
    except Exception as e:
        pass

    if current_time - last_save_time >= 30:
        save_flash_data(total_kwh, peak_power_w)
        last_save_time = current_time

    payload = {
        "voltage": round(voltage_val, 2),
        "current": round(current_amp, 2),
        "power_w": round(real_power, 2),
        "power_factor": power_factor,
        "peak_power_w": round(peak_power_w, 2),
        "total_kwh": round(total_kwh, 4),
        "total_cost_egp": round(total_cost, 2),
        "co2_kg": round(total_co2_kg, 4),
        "relay_state": relay.value(),
        "status": status
    }

    client.publish(TOPIC_PUB, ujson.dumps(payload))
    time.sleep(1)   

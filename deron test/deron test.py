from machine import I2C, Pin, PWM
import mpu6050
import time
import math
from neopixel import NeoPixel

time.sleep(5)



# ========== کلاس PID ==========
class PID:
    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.last_error = 0
        self.integral = 0
        self.last_time = time.ticks_ms()

    def compute(self, current_value):
        now = time.ticks_ms()
        dt = time.ticks_diff(now, self.last_time) / 1000
        if dt <= 0: dt = 0.01

        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.last_error) / dt

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.last_error = error
        self.last_time = now
        return output

# ========== فیلتر IIR زاویه ==========
class IIRFilter:
    def __init__(self, alpha=0.9):
        self.alpha = alpha
        self.filtered = 0

    def update(self, new_value):
        self.filtered = self.alpha * self.filtered + (1 - self.alpha) * new_value
        return self.filtered

# ========== تنظیمات اولیه ==========
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
mpu = mpu6050.accel(i2c)

motor_pins = [Pin(n, Pin.OUT) for n in [4, 5, 16, 17]]
motors = [PWM(p, freq=20000) for p in motor_pins]

BASE_DUTY = 700
MAX_DUTY = 1023
MIN_DUTY = 0
PWM_LIMIT = 300  # حداکثر تغییر نسبت به بیس

# ========== PID محورها ==========
pid_roll = PID(3.0, 0.1, 1.0)
pid_pitch = PID(3.0, 0.1, 1.0)
pid_yaw = PID(1.5, 0.05, 0.5)

# ========== فیلتر Complementary ==========
def complementary_filter(acc_angle, gyro_rate, prev_angle, dt, alpha=0.96):
    gyro_angle = prev_angle + gyro_rate * dt
    return alpha * gyro_angle + (1 - alpha) * acc_angle

# ========== تابع محدودسازی خروجی PID ==========
def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)

# ========== تابع محدودسازی PWM نرم ==========
def soft_clamp(val, center=BASE_DUTY, limit=PWM_LIMIT):
    return int(max(MIN_DUTY, min(MAX_DUTY, center + max(-limit, min(limit, val - center)))))

# ========== زاویه قبلی ==========
roll_angle = 0
pitch_angle = 0
yaw_angle = 0

# ========== فیلترهای IIR برای زاویه ==========
iir_roll = IIRFilter(alpha=0.9)
iir_pitch = IIRFilter(alpha=0.9)
iir_yaw = IIRFilter(alpha=0.9)

# ========== حلقه اصلی ==========
while True:
    start_time = time.ticks_ms()

    data = mpu.get_values()
    acc_x = data['AcX'] / 16384
    acc_y = data['AcY'] / 16384
    acc_z = data['AcZ'] / 16384

    gyro_x = data['GyX'] / 131.0
    gyro_y = data['GyY'] / 131.0
    gyro_z = data['GyZ'] / 131.0

    acc_pitch = math.degrees(math.atan2(acc_x, acc_z))
    acc_roll = math.degrees(math.atan2(acc_y, acc_z))
    
    dt = time.ticks_diff(time.ticks_ms(), start_time) / 1000
    if dt <= 0: dt = 0.01

    pitch_angle = complementary_filter(acc_pitch, gyro_y, pitch_angle, dt)
    roll_angle = complementary_filter(acc_roll, gyro_x, roll_angle, dt)
    yaw_angle += gyro_z * dt  # فقط ژیروسکوپ

    # فیلتر نرم (IIR) روی زاویه‌ها
    filtered_roll = iir_roll.update(roll_angle)
    filtered_pitch = iir_pitch.update(pitch_angle)
    filtered_yaw = iir_yaw.update(yaw_angle)

    # خروجی PID
    roll_output = clamp(pid_roll.compute(filtered_roll), -PWM_LIMIT, PWM_LIMIT)
    pitch_output = clamp(pid_pitch.compute(filtered_pitch), -PWM_LIMIT, PWM_LIMIT)
    yaw_output = clamp(pid_yaw.compute(filtered_yaw), -PWM_LIMIT, PWM_LIMIT)

    # محاسبه PWM نهایی
    m0 = soft_clamp(BASE_DUTY + roll_output + pitch_output - yaw_output)
    m1 = soft_clamp(BASE_DUTY - roll_output + pitch_output + yaw_output)
    m2 = soft_clamp(BASE_DUTY - roll_output - pitch_output - yaw_output)
    m3 = soft_clamp(BASE_DUTY + roll_output - pitch_output + yaw_output)

    # اعمال به موتورها
    motors[0].duty(m0)  # موتور جلو چپ
    motors[1].duty(m1)  # جلو راست
    motors[2].duty(m2)  # عقب راست
    motors[3].duty(m3)  # عقب چپ

    # دیباگ
    print("Roll: {:.1f} Pitch: {:.1f} Yaw: {:.1f} | PWM: {}, {}, {}, {}".format(
        filtered_roll, filtered_pitch, filtered_yaw, m0, m1, m2, m3))

    # تاخیر برای رسیدن به حدود 100Hz
    while time.ticks_diff(time.ticks_ms(), start_time) < 10:
        pass

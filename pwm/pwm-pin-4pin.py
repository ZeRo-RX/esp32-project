from pwm_module_all_pin import PWMManager

pins = [2, 4, 18, 19]  # یا هر پین دلخواهی که دوست دارید
pwm_manager = PWMManager(pins)

try:
    while True:
        pwm_manager.increase_pwm_duty()
        pwm_manager.decrease_pwm_duty()

except KeyboardInterrupt:
    pwm_manager.cleanup()

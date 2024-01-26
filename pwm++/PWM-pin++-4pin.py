from pwm_module_pin_pin import PWMManager

pins = [2, 4, 18, 19]  # یا هر پین دلخواهی که دوست دارید
pwm_manager = PWMManager(pins)

try:
    pwm_manager.run_pwm_sequence()

except KeyboardInterrupt:
    pwm_manager.cleanup()

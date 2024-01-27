from pwm_module_all_pin import PWMManager

pins = [2, 4, 16, 17, 5, 18, 19, 21]  # Or any pin you like
pwm_manager = PWMManager(pins)

try:
    while True:
        pwm_manager.increase_pwm_duty()
        pwm_manager.decrease_pwm_duty()

except KeyboardInterrupt as exception:
    pwm_manager.cleanup()
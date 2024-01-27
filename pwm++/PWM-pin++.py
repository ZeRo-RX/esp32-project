from pwm_module_pin_pin import PWMManager

pins = [2, 4, 16, 17, 5, 18, 19, 21]  # Or any pin you like
pwm_manager = PWMManager(pins)

try:
    pwm_manager.run_pwm_sequence()

except KeyboardInterrupt as exception:
    pwm_manager.cleanup()

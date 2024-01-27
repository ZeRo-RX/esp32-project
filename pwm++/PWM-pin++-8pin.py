from pwm_module_pin_pin import PWMManager
from utils.logging import Logger

logger = Logger()

pins = [2, 4, 16, 17, 5, 18, 19, 21]  # یا هر پین دلخواهی که دوست دارید
pwm_manager = PWMManager(pins)

try:
    pwm_manager.run_pwm_sequence()

except KeyboardInterrupt as exception:
    logger.log_action(exception)
    pwm_manager.cleanup()

from pwm_module_all_pin import PWMManager
from utils.logging import Logger

logger = Logger()

pins = [2, 4, 18, 19]  # یا هر پین دلخواهی که دوست دارید
pwm_manager = PWMManager(pins)

try:
    while True:
        pwm_manager.increase_pwm_duty()
        pwm_manager.decrease_pwm_duty()

except KeyboardInterrupt as exception:
    logger.log_error(exception)
    pwm_manager.cleanup()

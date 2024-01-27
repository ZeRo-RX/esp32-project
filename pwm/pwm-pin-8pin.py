from pwm_module_all_pin import PWMManager
from utils.logging import Logger

logger = Logger()

pins = [2, 4, 16, 17, 5, 18, 19, 21]  # یا هر پین دلخواهی که دوست دارید
pwm_manager = PWMManager(pins)

try:
    while True:
        pwm_manager.increase_pwm_duty()
        pwm_manager.decrease_pwm_duty()

except KeyboardInterrupt as exception:
    logger.log_action(exception)
    pwm_manager.cleanup()
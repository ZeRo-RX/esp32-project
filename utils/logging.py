import os
from datetime import datetime


class Logger:
    def __init__(self, log_path: str = "logs/"):
        self.log_path = log_path
        self.today = datetime.today().strftime("%Y-%m-%d")

    def update_today_date(self):
        self.today = datetime.today().strftime("%Y-%m-%d")

    def create_folder_if_not_exists(self):
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

    def append_log(self, log_text, indicator: str):
        self.update_today_date()
        self.create_folder_if_not_exists()
        # self.create_file_with_todays_date_if_not_exists()
        current_time = datetime.now().time()
        with open(f"{self.log_path}/{self.today}.log", "a") as file:
            file.write(f"\n[{indicator}] [{current_time}] {log_text}")

    def log_error(self, err):
        self.append_log(err, "Error")

    def log_action(self, action):
        self.append_log(action, "Action")


if __name__ == "__main__":
    logger = Logger()
    logger.log_action("test action")
    logger.log_error("test error")

import tkinter as tk
from tkinter import ttk
import threading
import speech_recognition as sr
import requests

class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Recognition App")

        # آدرس IP ESP32
        self.esp32_ip_var = tk.StringVar()
        self.esp32_ip_var.set("192.168.1.100")

        # ایجاد ویجت‌ها
        self.ip_label = ttk.Label(root, text="آدرس IP ESP32:")
        self.ip_label.pack(pady=5)

        self.ip_entry = ttk.Entry(root, textvariable=self.esp32_ip_var)
        self.ip_entry.pack(pady=5)

        self.status_label = ttk.Label(root, text="لطفاً صحبت کنید...")
        self.status_label.pack(pady=10)

        self.start_button = ttk.Button(root, text="شروع تشخیص صدا", command=self.start_listening)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="توقف تشخیص صدا", command=self.stop_listening)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.refresh_button = ttk.Button(root, text="رفرش", command=self.refresh_status)
        self.refresh_button.pack(pady=10)
        self.refresh_button.config(state=tk.DISABLED)

        # تنظیمات تشخیص صدا
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # متغیر برای نگه‌داری وضعیت تشخیص صدا
        self.is_listening = False

    def start_listening(self):
        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.refresh_button.config(state=tk.DISABLED)

        # شروع یک thread جداگانه برای تشخیص صدا
        listening_thread = threading.Thread(target=self.listen_thread)
        listening_thread.start()

    def listen_thread(self):
        while self.is_listening:
            with self.microphone as source:
                try:
                    audio = self.recognizer.listen(source, timeout=3)
                    text = self.recognizer.recognize_google(audio, language="fa-IR")
                    self.update_status(f"متن شناسایی شده: {text}")
                    translated_text = self.translate_numbers(text)
                    self.update_status(f"ترجمه اعداد: {translated_text}")

                    # اعمال دستورات
                    self.process_commands(translated_text)

                except sr.UnknownValueError:
                    self.update_status("هیچ گفتاری شناخته نشد.")
                except sr.RequestError as e:
                    self.update_status(f"بروز خطا در ارتباط با سرویس گوگل: {e}")

    def stop_listening(self):
        self.is_listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.refresh_button.config(state=tk.NORMAL)

    def refresh_status(self):
        self.update_status("وضعیت به‌روزرسانی شد.")

    def update_status(self, message):
        self.status_label.config(text=message)

    def translate_numbers(self, text):
        translation_dict = {
            '0': '۰',
            '1': '۱',
            '2': '۲',
            '3': '۳',
            '4': '۴',
            '5': '۵',
            '6': '۶',
            '7': '۷',
            '8': '۸',
            '9': '۹'
        }
        translated_text = ''.join([translation_dict[char] if char in translation_dict else char for char in text])
        return translated_text

    def process_commands(self, command):
        if "پین روشن" in command:
            self.send_request_to_all("on")
        elif "پین خاموش" in command:
            self.send_request_to_all("off")
        elif "پین ۲ روشن" in command:
            self.send_request(2, "on")
        elif "پین ۲ خاموش" in command:
            self.send_request(2, "off")
        elif "پین ۴ روشن" in command:
            self.send_request(4, "on")
        elif "پین ۴ خاموش" in command:
            self.send_request(4, "off")
        elif "پین ۱۸ روشن" in command:
            self.send_request(18, "on")
        elif "پین ۱۸ خاموش" in command:
            self.send_request(18, "off")
        elif "پین ۱۹ روشن" in command:
            self.send_request(19, "on")
        elif "پین ۱۹ خاموش" in command:
            self.send_request(19, "off")
        elif "پین ۵ روشن" in command:
            self.send_request(5, "on")
        elif "پین ۵ خاموش" in command:
            self.send_request(5, "off")
        elif "پین ۱۶ روشن" in command:
            self.send_request(16, "on")
        elif "پین ۱۶ خاموش" in command:
            self.send_request(16, "off")
        elif "پین ۱۷ روشن" in command:
            self.send_request(17, "on")
        elif "پین ۱۷ خاموش" in command:
            self.send_request(17, "off")
        elif "پین ۳ روشن" in command:
            self.send_request(3, "on")
        elif "پین ۳ خاموش" in command:
            self.send_request(3, "off")
        elif "بستن کد" in command:
            self.root.quit()

    def send_request(self, pin, action):
        esp32_ip = self.esp32_ip_var.get()
        url = f"http://{esp32_ip}/pin{pin}/{action}"
        try:
            response = requests.get(url)
            self.update_status(f"وضعیت درخواست برای پین {pin}: {response.status_code}")
        except requests.RequestException as e:
            self.update_status(f"بروز خطا در ارسال درخواست برای پین {pin}: {e}")

    def send_request_to_all(self, action):
        for pin in [2, 4, 18, 19, 16, 17, 5, 3]:
            self.send_request(pin, action)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechRecognitionApp(root)
    root.mainloop()

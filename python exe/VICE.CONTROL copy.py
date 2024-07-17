import chaqupy.android.tkinter as tk
from chaqupy.android.ttk import ttk
import chaqupy.android.threading
import chaqupy.android.speech.SpeechRecognizer
import chaqupy.android.http.Request

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

        # تنظیمات تشخیص صدا
        self.recognizer = chaqupy.android.speech.SpeechRecognizer()
        self.microphone = chaqupy.android.speech.Microphone()

        # متغیر برای نگه‌داری وضعیت تشخیص صدا
        self.is_listening = False

    def start_listening(self):
        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # شروع یک thread جداگانه برای تشخیص صدا
        listening_thread = chaqupy.android.threading.Thread(target=self.listen_thread)
        listening_thread.start()

    def listen_thread(self):
        while self.is_listening:
            with self.microphone as source:
                try:
                    audio = self.recognizer.record(source, timeout=3)
                    text = self.recognizer.recognize()
                    self.update_status(f"متن شناسایی شده: {text}")
                    translated_text = self.translate_numbers(text)
                    self.update_status(f"ترجمه اعداد: {translated_text}")

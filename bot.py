# bot.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import threading
import tkinter as tk
from tkinter import messagebox

class StudyGuardBot:
    def __init__(self):
        self.driver = None

    def start_driver(self):
        if self.driver is None:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()

    def search_video(self, query):
        self.start_driver()
        self.driver.get("https://www.youtube.com/")
        time.sleep(3)

        # Search video
        search_box = self.driver.find_element(By.NAME, "search_query")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        # Click first video
        video = self.driver.find_element(By.ID, "video-title")
        title = video.get_attribute("title")
        url = video.get_attribute("href")
        video.click()
        time.sleep(5)

        # Start threads: skip ads & focus timer
        threading.Thread(target=self.skip_ads_continuous, daemon=True).start()
        threading.Thread(target=self.focus_timer_pop_up, daemon=True).start()

        return url, title

    def skip_ads_continuous(self):
        try:
            while True:
                time.sleep(1)
                try:
                    skip_btn = self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button")
                    if skip_btn.is_displayed():
                        skip_btn.click()
                except:
                    pass
        except:
            pass

    def focus_timer_pop_up(self, duration=60):
        # Wait for focus duration
        time.sleep(duration)

        # Tkinter popup for focus break
        root = tk.Tk()
        root.title("🎯 Focus Break")
        root.geometry("400x250")
        root.configure(bg="#0B3D91")  # navy background

        tk.Label(root, text="🎯", font=("Segoe Script", 60, "bold"),
                 fg="#FFB400", bg="#0B3D91").pack(pady=10)
        tk.Label(root, text="Focus session complete!\nTake a 1 minute break.",
                 font=("Georgia", 14, "bold"), fg="white",
                 bg="#0B3D91", justify="center").pack(pady=10)
        tk.Button(root, text="✔ Close", font=("Georgia", 12, "bold"),
                  bg="#FFB400", fg="#0B3D91", relief="flat",
                  command=root.destroy).pack(pady=15)
        root.mainloop()

    def generate_daily_plan(self):
        return {
            "Learning": "Python tutorial for beginners",
            "Career": "Career motivation for students",
            "Entertainment": "Tarak Mehta ka ulta Chasmah(5 min)"
        }

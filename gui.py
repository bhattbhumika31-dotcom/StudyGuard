# gui.py
import tkinter as tk
from bot import StudyGuardBot
from PIL import Image, ImageTk

# Ocean Gold Theme
THEME = {
    "bg": "#0B3D91",        # Deep navy
    "panel": "#FCEBB6",     # Soft gold
    "accent": "#FFB400",    # Golden buttons
    "text": "#FFFFFF"
}

def start_gui():
    bot = StudyGuardBot()
    root = tk.Tk()
    root.title("StudyGuard Dashboard")
    root.geometry("780x700")
    root.config(bg=THEME["bg"])

    # Title Frame
    title_frame = tk.Frame(root, bg=THEME["bg"])
    title_frame.pack(pady=15)

    # YouTube Icon
    try:
        icon_image = Image.open("youtube_icon.png")
        icon_image = icon_image.resize((40, 40), Image.ANTIALIAS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        tk.Label(title_frame, image=icon_photo, bg=THEME["bg"]).pack(side="left", padx=5)
    except:
        pass

    tk.Label(title_frame, text="StudyGuard", font=("Segoe Script", 36, "bold"),
             fg=THEME["accent"], bg=THEME["bg"]).pack(side="left")

    # Fun welcome line
    tk.Label(root, text="🚀 Focus Today, Shine Tomorrow! 🌟",
             font=("Georgia", 14, "italic"),
             fg=THEME["accent"], bg=THEME["bg"]).pack(pady=5)

    # Panel
    panel = tk.Frame(root, bg=THEME["panel"], padx=25, pady=25)
    panel.pack(pady=20, fill="both", expand=True)

    # Search
    tk.Label(panel, text="Search Topic:", font=("Georgia", 14, "bold"),
             fg=THEME["bg"], bg=THEME["panel"]).pack(anchor="w")
    search_entry = tk.Entry(panel, width=60, font=("Georgia", 12),
                            relief="flat", bg="#FFF9E3", fg=THEME["bg"])
    search_entry.pack(pady=10)

    # Suggested Video Box
    suggestion_box = tk.Text(panel, height=8, width=65, font=("Georgia", 12),
                             bg="#FFF9E3", fg=THEME["bg"], relief="flat")
    suggestion_box.pack(pady=10)
    suggestion_box.insert("end", "🎥 Your suggested videos will appear here...\n")
    suggestion_box.config(state="disabled")

    # Functions
    def search_video():
        query = search_entry.get()
        if not query:
            return
        url, title = bot.search_video(query)
        suggestion_box.config(state="normal")
        suggestion_box.delete("1.0", tk.END)
        suggestion_box.insert("end",
            f"✨ Top Suggested Video:\n\n📌 Title: {title}\n🔗 URL: {url}\n\nAds skip automatically & focus timer started!")
        suggestion_box.config(state="disabled")

    def show_daily_plan():
        plan = bot.generate_daily_plan()
        plan_window = tk.Toplevel()
        plan_window.title("📅 Daily Watch Plan")
        plan_window.geometry("480x300")
        plan_window.config(bg=THEME["bg"])

        tk.Label(plan_window, text="📅 Daily Watch Plan", font=("Segoe Script", 20, "bold"),
                 fg=THEME["accent"], bg=THEME["bg"]).pack(pady=10)

        panel_plan = tk.Frame(plan_window, bg=THEME["panel"], padx=20, pady=20)
        panel_plan.pack(pady=10, fill="both", expand=True)

        tk.Label(panel_plan, text=f"📘 Learning -> {plan['Learning']}", font=("Georgia", 12, "bold"),
                 fg=THEME["bg"], bg=THEME["panel"], anchor="w", justify="left").pack(pady=5, fill="x")
        tk.Label(panel_plan, text=f"💼 Career -> {plan['Career']}", font=("Georgia", 12, "bold"),
                 fg=THEME["bg"], bg=THEME["panel"], anchor="w", justify="left").pack(pady=5, fill="x")
        tk.Label(panel_plan, text=f"🎭 Entertainment -> {plan['Entertainment']}", font=("Georgia", 12, "bold"),
                 fg=THEME["bg"], bg=THEME["panel"], anchor="w", justify="left").pack(pady=5, fill="x")

        tk.Button(plan_window, text="Close", bg=THEME["accent"], fg="white",
                  font=("Georgia", 12, "bold"), relief="flat", command=plan_window.destroy).pack(pady=10)

    # Buttons
    button_style = {"font": ("Georgia", 12, "bold"), "bg": THEME["accent"],
                    "fg": "white", "relief": "flat", "width": 35, "pady": 6}

    tk.Button(panel, text="📅 Daily Watch Plan", command=show_daily_plan, **button_style).pack(pady=8)
    tk.Button(panel, text="🔍 Search Video", command=search_video, **button_style).pack(pady=8)

    root.mainloop()

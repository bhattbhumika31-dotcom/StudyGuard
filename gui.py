
"""StudyGuard GUI - User interface for the StudyGuard learning assistant."""

import logging
import tkinter as tk
from typing import Optional

from PIL import Image, ImageTk

from bot import StudyGuardBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ocean Gold Theme
THEME = {
    "bg": "#0B3D91",        # Deep navy
    "panel": "#FCEBB6",     # Soft gold
    "accent": "#FFB400",    # Golden buttons
    "text": "#FFFFFF"
}

# UI Constants
WINDOW_WIDTH = 780
WINDOW_HEIGHT = 700
ICON_SIZE = (40, 40)
SEARCH_ENTRY_WIDTH = 60
SUGGESTION_BOX_HEIGHT = 8
SUGGESTION_BOX_WIDTH = 65
PLAN_WINDOW_WIDTH = 480
PLAN_WINDOW_HEIGHT = 300


def load_icon(icon_path: str) -> Optional[ImageTk.PhotoImage]:
    """
    Load and resize an icon image.

    Args:
        icon_path: Path to the icon file

    Returns:
        PhotoImage object or None if loading fails
    """
    try:
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize(ICON_SIZE, Image.LANCZOS)
        return ImageTk.PhotoImage(icon_image)
    except FileNotFoundError:
        logger.warning(f"Icon file not found: {icon_path}")
        return None
    except Exception as e:
        logger.error(f"Failed to load icon {icon_path}: {e}")
        return None


def start_gui() -> None:
    """Initialize and start the StudyGuard GUI application."""
    try:
        bot = StudyGuardBot()
        root = tk.Tk()
        root.title("StudyGuard Dashboard")
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        root.config(bg=THEME["bg"])
        logger.info("GUI initialized")

        # Title Frame
        title_frame = tk.Frame(root, bg=THEME["bg"])
        title_frame.pack(pady=15)

        # YouTube Icon
        icon_photo = load_icon("youtube_icon.png")
        if icon_photo:
            tk.Label(title_frame, image=icon_photo, bg=THEME["bg"]).pack(side="left", padx=5)

        tk.Label(
            title_frame, text="StudyGuard", font=("Segoe Script", 36, "bold"),
            fg=THEME["accent"], bg=THEME["bg"]
        ).pack(side="left")

        # Fun welcome line
        tk.Label(
            root, text="🚀 Focus Today, Shine Tomorrow! 🌟",
            font=("Georgia", 14, "italic"),
            fg=THEME["accent"], bg=THEME["bg"]
        ).pack(pady=5)

        # Panel
        panel = tk.Frame(root, bg=THEME["panel"], padx=25, pady=25)
        panel.pack(pady=20, fill="both", expand=True)

        # Search
        tk.Label(
            panel, text="Search Topic:", font=("Georgia", 14, "bold"),
            fg=THEME["bg"], bg=THEME["panel"]
        ).pack(anchor="w")

        search_entry = tk.Entry(
            panel, width=SEARCH_ENTRY_WIDTH, font=("Georgia", 12),
            relief="flat", bg="#FFF9E3", fg=THEME["bg"]
        )
        search_entry.pack(pady=10)

        # Suggested Video Box
        suggestion_box = tk.Text(
            panel, height=SUGGESTION_BOX_HEIGHT, width=SUGGESTION_BOX_WIDTH,
            font=("Georgia", 12), bg="#FFF9E3", fg=THEME["bg"], relief="flat"
        )
        suggestion_box.pack(pady=10)
        suggestion_box.insert("end", "🎥 Your suggested videos will appear here...\n")
        suggestion_box.config(state="disabled")

        # Functions
        def search_video() -> None:
            """Handle video search button click."""
            query = search_entry.get().strip()
            if not query:
                logger.warning("Empty search query provided")
                return

            try:
                url, title = bot.search_video(query)
                if url and title:
                    suggestion_box.config(state="normal")
                    suggestion_box.delete("1.0", tk.END)
                    suggestion_box.insert(
                        "end",
                        f"✨ Top Suggested Video:\n\n📌 Title: {title}\n🔗 URL: {url}\n\n"
                        "Ads skip automatically & focus timer started!"
                    )
                    suggestion_box.config(state="disabled")
                    logger.info(f"Video search completed: {title}")
                else:
                    logger.error("Failed to retrieve video information")
            except Exception as e:
                logger.error(f"Error during video search: {e}")

        def show_daily_plan() -> None:
            """Display the daily watch plan in a new window."""
            try:
                plan = bot.generate_daily_plan()
                plan_window = tk.Toplevel()
                plan_window.title("📅 Daily Watch Plan")
                plan_window.geometry(f"{PLAN_WINDOW_WIDTH}x{PLAN_WINDOW_HEIGHT}")
                plan_window.config(bg=THEME["bg"])

                tk.Label(
                    plan_window, text="📅 Daily Watch Plan",
                    font=("Segoe Script", 20, "bold"),
                    fg=THEME["accent"], bg=THEME["bg"]
                ).pack(pady=10)

                panel_plan = tk.Frame(plan_window, bg=THEME["panel"], padx=20, pady=20)
                panel_plan.pack(pady=10, fill="both", expand=True)

                tk.Label(
                    panel_plan, text=f"📘 Learning -> {plan['Learning']}",
                    font=("Georgia", 12, "bold"),
                    fg=THEME["bg"], bg=THEME["panel"], anchor="w", justify="left"
                ).pack(pady=5, fill="x")

                tk.Label(
                    panel_plan, text=f"💼 Career -> {plan['Career']}",
                    font=("Georgia", 12, "bold"),
                    fg=THEME["bg"], bg=THEME["panel"], anchor="w", justify="left"
                ).pack(pady=5, fill="x")

                tk.Label(
                    panel_plan, text=f"🎭 Entertainment -> {plan['Entertainment']}",
                    font=("Georgia", 12, "bold"),
                    fg=THEME["bg"], bg=THEME["panel"], anchor="w", justify="left"
                ).pack(pady=5, fill="x")

                tk.Button(
                    plan_window, text="Close", bg=THEME["accent"], fg="white",
                    font=("Georgia", 12, "bold"), relief="flat",
                    command=plan_window.destroy
                ).pack(pady=10)

                logger.info("Daily plan window opened")
            except Exception as e:
                logger.error(f"Error displaying daily plan: {e}")

        # Buttons
        button_style = {
            "font": ("Georgia", 12, "bold"),
            "bg": THEME["accent"],
            "fg": "white",
            "relief": "flat",
            "width": 35,
            "pady": 6
        }

        tk.Button(panel, text="📅 Daily Watch Plan", command=show_daily_plan, **button_style).pack(pady=8)
        tk.Button(panel, text="🔍 Search Video", command=search_video, **button_style).pack(pady=8)

        root.mainloop()
        logger.info("GUI closed")

    except Exception as e:
        logger.error(f"Fatal error in GUI: {e}")
        raise

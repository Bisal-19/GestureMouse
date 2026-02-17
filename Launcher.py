import customtkinter as ctk
import main
import threading
import time
from PIL import Image
import os
import sys


# --- EXE RESOURCE PATH FIX ---
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --- THEME SETTINGS ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("Gesture Control System")

        # Define window size
        window_width = 900
        window_height = 600

        # --- CENTERING LOGIC ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.resizable(False, False)

        # --- FONTS ---
        self.font_header = ctk.CTkFont(family="Roboto", size=28, weight="bold")
        self.font_subheader = ctk.CTkFont(family="Roboto", size=16)
        self.font_button = ctk.CTkFont(family="Roboto", size=18, weight="bold")
        self.font_small = ctk.CTkFont(family="Roboto", size=12)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================================
        # SIDEBAR (Left)
        # ==========================================================
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="AI GESTURE\nCONTROLLER",
            font=self.font_header,
            text_color="#3B8ED0",
        )
        self.logo.grid(row=0, column=0, padx=20, pady=(40, 20))

        self.btn_help = ctk.CTkButton(
            self.sidebar,
            text="📖 User Manual",
            command=self.show_help,
            fg_color="transparent",
            border_width=2,
            border_color="#555",
            text_color=("gray10", "#DCE4EE"),
            font=self.font_subheader,
            height=40,
        )
        self.btn_help.grid(row=1, column=0, padx=20, pady=20)

        self.label_mode = ctk.CTkLabel(
            self.sidebar, text="Appearance:", anchor="w", font=self.font_small
        )
        self.label_mode.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.option_mode = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light"],
            command=self.change_theme,
            font=self.font_small,
        )
        self.option_mode.grid(row=6, column=0, padx=20, pady=(5, 30))

        # ==========================================================
        # MAIN AREA (Right)
        # ==========================================================
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 0))

        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text="Welcome Back, User",
            font=ctk.CTkFont(family="Roboto", size=32, weight="bold"),
        )
        self.welcome_label.pack(anchor="w")

        self.date_label = ctk.CTkLabel(
            self.header_frame,
            text="System Ready • v1.0.0",
            font=self.font_small,
            text_color="gray",
        )
        self.date_label.pack(anchor="w")

        # Control Panel Card
        self.card_frame = ctk.CTkFrame(
            self.main_area, corner_radius=20, fg_color=("gray85", "gray17")
        )
        self.card_frame.grid(row=1, column=0, sticky="nsew", pady=30)

        self.card_frame.grid_columnconfigure(0, weight=1)
        self.card_frame.grid_rowconfigure(0, weight=1)
        self.card_frame.grid_rowconfigure(4, weight=1)

        self.lbl_action = ctk.CTkLabel(
            self.card_frame,
            text="CHOOSE MODE",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            text_color="gray",
        )
        self.lbl_action.grid(row=0, column=0, pady=(30, 10))

        # Mouse Button
        self.btn_mouse = ctk.CTkButton(
            self.card_frame,
            text="🖱️  Start Mouse Control",
            command=lambda: self.start_initialization("MOUSE"),
            width=320,
            height=65,
            font=self.font_button,
            fg_color="#3B8ED0",
            hover_color="#36719F",
            corner_radius=12,
        )
        self.btn_mouse.grid(row=1, column=0, pady=15)

        self.lbl_mouse_desc = ctk.CTkLabel(
            self.card_frame,
            text="Control cursor, click & scroll with hands",
            font=self.font_small,
            text_color="gray",
        )
        self.lbl_mouse_desc.grid(row=2, column=0, pady=(0, 15))

        # Sign Button
        self.btn_sign = ctk.CTkButton(
            self.card_frame,
            text="✋  Start Sign Translator (Beta)",
            command=lambda: self.start_initialization("TRANSLATE"),
            width=320,
            height=65,
            font=self.font_button,
            fg_color="#E04F5F",
            hover_color="#C03948",
            corner_radius=12,
        )
        self.btn_sign.grid(row=3, column=0, pady=15)

        self.lbl_sign_desc = ctk.CTkLabel(
            self.card_frame,
            text="Experimental gesture-to-text translation",
            font=self.font_small,
            text_color="gray",
        )
        self.lbl_sign_desc.grid(row=4, column=0, pady=(0, 30))

        # Loading Bar
        self.status_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.status_frame.grid(row=2, column=0, sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.status_frame, text="", font=self.font_small
        )
        self.status_label.pack()

        self.progress = ctk.CTkProgressBar(
            self.status_frame, width=400, mode="indeterminate"
        )

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)

    def show_help(self):
        # Create Window
        window = ctk.CTkToplevel(self)
        window.geometry("700x650")
        window.title("User Manual")
        window.configure(fg_color=("white", "#1a1a1a"))

        # Center this window too
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (700 / 2))
        y = int((screen_height / 2) - (650 / 2))
        window.geometry(f"700x650+{x}+{y}")

        window.lift()
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))
        window.focus_force()

        # Tabs
        self.tab_view = ctk.CTkTabview(window, text_color=("black", "white"))
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        tab_mouse = self.tab_view.add("🖱️ Mouse Controller")
        tab_sign = self.tab_view.add("✋ Sign Translator")

        # Instruction Helper
        def add_instruction(parent, image_name, title, desc):
            row = ctk.CTkFrame(parent, fg_color=("#F0F0F0", "#2b2b2b"))
            row.pack(fill="x", pady=10, padx=10)

            # Use resource_path to find images in EXE
            image_path = resource_path(image_name)

            if os.path.exists(image_path):
                try:
                    pil_img = Image.open(image_path)
                    img = ctk.CTkImage(
                        light_image=pil_img, dark_image=pil_img, size=(60, 60)
                    )
                    ctk.CTkLabel(row, image=img, text="").pack(
                        side="left", padx=10, pady=10
                    )
                except:
                    ctk.CTkLabel(row, text="[IMG]", width=60).pack(side="left", padx=10)
            else:
                ctk.CTkFrame(
                    row, width=60, height=60, fg_color=("gray80", "gray40")
                ).pack(side="left", padx=10, pady=10)

            text_frame = ctk.CTkFrame(row, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(
                text_frame,
                text=title,
                font=("Roboto", 16, "bold"),
                text_color=("black", "white"),
                anchor="w",
            ).pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(
                text_frame,
                text=desc,
                font=("Roboto", 12),
                text_color=("gray20", "gray80"),
                anchor="w",
                wraplength=450,
                justify="left",
            ).pack(fill="x", pady=(0, 10))

        # Mouse Tab
        scroll_mouse = ctk.CTkScrollableFrame(tab_mouse, fg_color=("white", "#2b2b2b"))
        scroll_mouse.pack(fill="both", expand=True)
        ctk.CTkLabel(
            scroll_mouse,
            text="Virtual Mouse Gestures",
            font=("Roboto", 20, "bold"),
            text_color=("black", "white"),
        ).pack(pady=10)

        add_instruction(
            scroll_mouse,
            "move.png",
            "Move Cursor",
            "Point your INDEX finger up. Keep other fingers down.",
        )
        add_instruction(
            scroll_mouse,
            "click.png",
            "Left Click",
            "Pinch your INDEX and MIDDLE fingers together.",
        )
        add_instruction(
            scroll_mouse,
            "click.png",
            "Drag & Drop",
            "Pinch Index + Middle fingers together and MOVE hand to drag items.",
        )
        add_instruction(
            scroll_mouse,
            "rightclick.png",
            "Right Click",
            "Pinch your THUMB and INDEX fingers together.",
        )
        add_instruction(
            scroll_mouse,
            "scroll.png",
            "Scroll Page",
            "Raise your PINKY finger. Move hand Up/Down to scroll.",
        )
        add_instruction(
            scroll_mouse,
            "key_q.png",
            "Exit Camera",
            "Press the 'q' key on your keyboard to close the camera.",
        )

        # Sign Tab
        scroll_sign = ctk.CTkScrollableFrame(tab_sign, fg_color=("white", "#2b2b2b"))
        scroll_sign.pack(fill="both", expand=True)
        ctk.CTkLabel(
            scroll_sign,
            text="Translator Gestures (Beta)",
            font=("Roboto", 20, "bold"),
            text_color=("black", "white"),
        ).pack(pady=10)
        ctk.CTkLabel(
            scroll_sign,
            text="Note: This is an experimental feature.",
            text_color="orange",
            font=("Roboto", 12),
        ).pack(pady=(0, 20))

        add_instruction(
            scroll_sign,
            "stop.png",
            "Stop / No",
            "Show a CLOSED FIST to stop or indicate 'No'.",
        )
        add_instruction(
            scroll_sign,
            "hello.png",
            "Hello",
            "Show an OPEN PALM (5 fingers) to say Hello.",
        )
        add_instruction(
            scroll_sign,
            "victory.png",
            "Victory",
            "Show a 'V' sign (Index + Middle) for Victory.",
        )
        add_instruction(scroll_sign, "like.png", "Like", "Show a THUMBS UP gesture.")
        add_instruction(
            scroll_sign,
            "key_q.png",
            "Exit Camera",
            "Press the 'q' key on your keyboard to close the camera.",
        )

        # Back Button
        btn_close = ctk.CTkButton(
            window,
            text="Back to Menu",
            command=window.destroy,
            fg_color="transparent",
            border_width=2,
            border_color=("gray50", "gray70"),
            text_color=("black", "white"),
            width=200,
        )
        btn_close.pack(pady=20)

    # --- UPDATED INITIALIZATION LOGIC ---
    def start_initialization(self, mode):
        # 1. Disable buttons to prevent double-opening
        self.btn_mouse.configure(state="disabled")
        self.btn_sign.configure(state="disabled")

        # 2. Show loading status
        self.status_label.configure(text=f"Launching {mode} Mode...")
        self.progress.pack(pady=10)
        self.progress.start()

        # 3. Start Camera in a separate thread so UI stays active
        threading.Thread(
            target=self.run_camera_process, args=(mode,), daemon=True
        ).start()

    def run_camera_process(self, mode):
        # This function runs in the background
        main.initialize_camera()

        # Tell the main thread to stop the loading bar
        self.after(0, self.stop_loading_animation)

        # Start the app loop (This blocks this thread until 'q' is pressed)
        main.start_app(start_mode=mode)

        # When 'q' is pressed, the line above finishes.
        # Now tell the main thread to reset the buttons.
        self.after(0, self.reset_launcher_ui)

    def stop_loading_animation(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.configure(text="Camera Active (Press 'q' to exit)")

    def reset_launcher_ui(self):
        self.status_label.configure(text="")
        self.btn_mouse.configure(state="normal")
        self.btn_sign.configure(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()

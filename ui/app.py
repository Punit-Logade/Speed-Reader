import tkinter as tk
from tkinter import ttk, filedialog


class SpeedReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.COLORS = {
            "bg": "#121212",
            "surface": "#1e1e1e",
            "accent": "#00adb5",
            "orp": "#ff4d4d",
            "text": "#eeeeee",
        }

        self.title("Speed Reader Pro")
        self._center_window(900, 600)  # Professional centering
        self.configure(bg=self.COLORS["bg"])

        # State
        self.words = []
        self.current_index = 0
        self.wpm = 300  # Words per minute
        self.is_running = False

        self._setup_styles()
        self._create_widgets()

    def _center_window(self, width, height):
        """Calculates the screen center and sets geometry."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(expand=True, fill="both")

        ttk.Label(self.main_frame, text="SPEED READER PRO", style="Header.TLabel").pack(
            pady=(0, 20)
        )

        # Input Area
        self.text_field = tk.Text(
            self.main_frame,
            height=4,
            bg=self.COLORS["surface"],
            fg=self.COLORS["text"],
            insertbackground=self.COLORS["accent"],
            font=("Consolas", 12),
            padx=10,
            pady=10,
            relief="flat",
        )
        self.text_field.pack(fill="x", pady=10)

        # --- THE FIX: SHARED GRID SYSTEM ---
        self.display_container = ttk.Frame(self.main_frame)
        self.display_container.pack(expand=True, fill="x")

        # Force column 0 and 2 to be identical in size (weight=1)
        self.display_container.columnconfigure(0, weight=1)
        self.display_container.columnconfigure(1, weight=0)  # Middle stays tight
        self.display_container.columnconfigure(2, weight=1)

        self.left_part = ttk.Label(
            self.display_container,
            text="",
            style="ORP.TLabel",
            foreground=self.COLORS["text"],
            anchor="e",
        )
        self.mid_part = ttk.Label(
            self.display_container,
            text="",
            style="ORP.TLabel",
            foreground=self.COLORS["orp"],
            anchor="center",
        )
        self.right_part = ttk.Label(
            self.display_container,
            text="",
            style="ORP.TLabel",
            foreground=self.COLORS["text"],
            anchor="w",
        )

        # Place them in the grid
        self.left_part.grid(row=0, column=0, sticky="ew")
        self.mid_part.grid(row=0, column=1)
        self.right_part.grid(row=0, column=2, sticky="ew")
        # ----------------------------------

        # Controls
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.pack(fill="x", pady=20)

        self.start_btn = ttk.Button(
            self.btn_frame, text="START", command=self.toggle_reading
        )
        self.start_btn.pack(side="left", expand=True, fill="x", padx=5)

        self.browse_btn = ttk.Button(
            self.btn_frame, text="OPEN FILE", command=self.browse_file
        )
        self.browse_btn.pack(side="left", expand=True, fill="x", padx=5)

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.COLORS["bg"])
        style.configure(
            "Header.TLabel",
            background=self.COLORS["bg"],
            foreground=self.COLORS["accent"],
            font=("Helvetica", 18, "bold"),
        )
        style.configure(
            "ORP.TLabel", background=self.COLORS["bg"], font=("Consolas", 64, "bold")
        )

    def flash_word(self):
        if self.is_running and self.current_index < len(self.words):
            word = self.words[self.current_index]

            # ORP Calculation: Middle of the word
            if (len(word) <= 2):
                mid = 0
            else:
                mid = len(word) // 2
                self.left_part.configure(text=word[:mid])
                self.mid_part.configure(text=word[mid])
                self.right_part.configure(text=word[mid + 1:])

            self.current_index += 1
            self.after(int(60000 / self.wpm), self.flash_word)
        elif self.current_index >= len(self.words):
            self.is_running = False
            self.start_btn.configure(text="RESTART")
            self.current_index = 0

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.text_field.delete("1.0", "end")
                self.text_field.insert("1.0", f.read())

    def toggle_reading(self):
        if not self.is_running:
            raw_text = self.text_field.get("1.0", "end-1c").strip()
            if raw_text:
                self.words = raw_text.split()
                self.is_running = True
                self.start_btn.configure(text="PAUSE")
                self.flash_word()
        else:
            self.is_running = False
            self.start_btn.configure(text="RESUME")

    def run(self):
        self.mainloop()

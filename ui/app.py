import tkinter as tk
from tkinter import filedialog
from reader.engine import SpeedReaderEngine


class SpeedReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.bind("<space>", lambda e: self.toggle_reading())
        self.bind("<Up>", lambda e: self.increase_speed())
        self.bind("<Down>", lambda e: self.decrease_speed())
        self.bind("<Control-o>", lambda e: self.browse_file())
        self.bind("<Left>", lambda e: self.rewind())

        self.engine = SpeedReaderEngine()

        self.wpm = 300
        self.target_wpm = 300
        self.is_running = False

        self._setup_ui()

    def _setup_ui(self):
        self.title("Speed Reader Pro")
        self.geometry("900x600")

        self.text_field = tk.Text(self, height=4)
        self.text_field.pack(fill="x")

        self.wpm_label = tk.Label(self, text=f"WPM: {self.wpm}")
        self.wpm_label.pack()

        self.display = tk.Label(self, text="", font=("Consolas", 40))
        self.display.pack(expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack()

        tk.Button(btn_frame, text="START", command=self.toggle_reading).pack(
            side="left"
        )
        tk.Button(btn_frame, text="OPEN", command=self.browse_file).pack(side="left")
        tk.Button(btn_frame, text="REWIND", command=self.rewind).pack(side="left")
        tk.Button(btn_frame, text="CLEAR", command=self.clear_text).pack(side="left")

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.text_field.delete("1.0", "end")
                self.text_field.insert("1.0", f.read())

    def toggle_reading(self):
        if not self.engine.has_words():
            text = self.text_field.get("1.0", "end").strip()
            if not text:
                return
            self.engine.load_text(text)

        self.is_running = not self.is_running

        if self.is_running:
            self.flash_word()

    def flash_word(self):
        if not self.is_running:
            return

        if self.engine.is_finished():
            self.is_running = False
            self.engine.reset()
            return

        word = self.engine.get_next_word()

        # ORP logic
        if len(word) <= 2:
            mid = 0
        else:
            mid = len(word) // 2

        display_word = word[:mid] + "|" + word[mid] + "|" + word[mid + 1 :]
        self.display.config(text=display_word)

        # speed ramp
        if self.wpm < self.target_wpm:
            self.wpm += 5
        elif self.wpm > self.target_wpm:
            self.wpm -= 5

        self.wpm_label.config(text=f"WPM: {self.wpm}")

        delay = self.engine.calculate_delay(word, self.wpm)
        self.after(delay, self.flash_word)

    def increase_speed(self):
        self.target_wpm = min(1000, self.target_wpm + 50)

    def decrease_speed(self):
        self.target_wpm = max(50, self.target_wpm - 50)

    def rewind(self):
        self.engine.rewind()

    def clear_text(self):
        self.text_field.delete("1.0", "end")
        self.engine.reset()
        self.display.config(text="")

    def run(self):
        self.mainloop()

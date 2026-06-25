import re


class SpeedReaderEngine:
    def __init__(self):
        self.words = []
        self.index = 0

    def load_text(self, text):
        self.words = re.findall(r"\S+", text)
        self.index = 0

    def has_words(self):
        return len(self.words) > 0

    def get_next_word(self):
        if self.index < len(self.words):
            word = self.words[self.index]
            self.index += 1
            return word
        return None

    def rewind(self, steps=20):
        self.index = max(0, self.index - steps)

    def reset(self):
        self.index = 0

    def is_finished(self):
        return self.index >= len(self.words)

    def get_progress(self):
        return self.index, len(self.words)

    def calculate_delay(self, word, wpm):
        delay = int(60000 / wpm)

        if word.endswith(","):
            delay += 100
        elif word.endswith((".", "!", "?")):
            delay += 200

        if len(word) > 7:
            delay += 50
        if len(word) > 10:
            delay += 100

        return delay

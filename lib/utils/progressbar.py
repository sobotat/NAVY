

class ProgressBar:
    def __init__(self, max_value, message='Progress', length=20):
        self.value = 0
        self.max_value = max_value
        self.message = message
        self.length = length

        self.finished = False
        self.last_percent = -1
        self.draw("")

    def update(self, value, message_behind=""):
        if self.finished:
            return
        
        if value == self.max_value:
            self.finished = True

        self.value = value
        self.draw(message_behind)

    def draw(self, message_behind):
        percent = round((self.value / self.max_value) * 100, 1)

        if self.last_percent == percent and not self.finished:
            return
        
        self.last_percent = percent

        filled_length = int(self.length * self.value // self.max_value)
        bar = "\033[1;32m" + "—" * filled_length + "\033[0m" + "—" * (self.length - filled_length)

        print(f"\r{self.message} {bar} [{percent}%] {message_behind}", flush=True, end="")

        if self.finished:
            print()
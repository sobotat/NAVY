import readchar
import enum

class Color(enum.Enum):
    Gray = 30
    RED = 31
    GREEN = 32
    ORANGE = 33
    BLUE = 34
    PURPLE = 35
    CYEN = 36
    WHITE = 38 

class Menu:
    def __init__(self, heading, options:list[str], headingColor=Color.BLUE, selectedColor=Color.BLUE):
        self.options = options
        self.heading = heading

        self.headingColor = headingColor
        self.selectedColor = selectedColor

    def select(self, spaceBeforeHeading=True) -> str | None:
        def printOption(option, selected):
            prefix = f"\033[1;{self.selectedColor.value}m[*] " if selected else "\033[0;30m[ ] "
            print(f"{prefix}{option}\033[0m\033[K")

        def draw(index):
            print(f"\r\033[1;{self.headingColor.value}m{self.heading}: \033[0m\033[K")
            for i, option in enumerate(self.options):
                printOption(option, i == index)

        index = 0
        if spaceBeforeHeading:
            print()
        draw(index)
        
        while True:
            print(f"\033[{(len(self.options) + 1)}F\r", end="")
            draw(index)

            try:
                key = readchar.readkey()
            except KeyboardInterrupt:
                return None
            
            if key == readchar.key.UP:
                index = (index - 1) % len(self.options)
            elif key == readchar.key.DOWN:
                index = (index + 1) % len(self.options)
            elif key == readchar.key.ENTER:
                print(f"\033[K\033[J", end="")
                return self.options[index].lower().replace(" ", "-")



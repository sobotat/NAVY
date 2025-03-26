import tkinter
from tkinter import Button, PhotoImage, Canvas, OptionMenu, StringVar
from enum import Enum
from lib.exercises.cv04.map import Map, TileType

class Mode(Enum):
    Add = 0
    Remove = 1

class QLearningApp:

    def __init__(self):
        self.mode = None
        self.add_option = TileType.Wall
        
        self.map = Map(10, 10)

    def run(self):
        self.root = tkinter.Tk()
        root = self.root

        root.title("QLearning")
        icon = PhotoImage(file="res\icons\school_icon.png")
        root.iconphoto(True, icon)
        self.set_window_size(root, 30 * self.map.size_x + 95, 30 * self.map.size_y + 4)
        
        root.grid_columnconfigure(1, minsize=75)
        run_button = Button(root, text="Run", command=self.on_clicked_run)
        run_button.grid(row=0, column=1, sticky="ew")

        add_button = Button(root, text="Add Mode", command=self.on_click_add)
        add_button.grid(row=1, column=1, sticky="ew")

        add_options = [ 
            TileType.Wall.name, 
            TileType.Tresure.name, 
            TileType.Trap.name,
            TileType.Player.name
        ] 
        selected_add_option = StringVar(value=self.add_option.name) 
        add_options_menu = OptionMenu(root , selected_add_option, *add_options, command=self.on_selected_add_option)
        add_options_menu.grid(row=2, column=1, sticky="ew")

        remove_button = Button(root, text="Remove Mode", command=self.on_click_remove)
        remove_button.grid(row=3, column=1, sticky="ew")
        
        self.canvas = Canvas(root, width=30 * self.map.size_x, height=30 * self.map.size_y, background="#0e1c56")
        self.canvas.bind("<Button-1>", self.on_click_canvas)
        self.canvas.grid(row=0, column=0, rowspan=20)
        self.draw_canvas()

        root.mainloop()

    def set_window_size(self, root, window_width, window_height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.resizable(False, False)

    def draw_canvas(self):
        self.images = []

        tiles_res = {
            TileType.Empty:   "res/images/wall_point_dark.png",
            TileType.Wall:    "res/images/wall_point.png",
            TileType.Trap:    "res/images/kill.png",
            TileType.Player:  "res/images/player.png",
            TileType.Tresure: "res/images/doors.png"
        }

        for x in range(self.map.size_x):
            for y in range(self.map.size_y):
                tile = self.map.get_tile(x, y)
                
                bg_image = PhotoImage(file=tiles_res[TileType.Empty])
                self.images.append(bg_image)
                self.canvas.create_image(x * 30, y * 30, image=bg_image, anchor="nw")

                if tile != TileType.Empty:
                    tile_image = PhotoImage(file=tiles_res[tile])
                    self.images.append(tile_image)

                    offset_x = (30 - tile_image.width()) // 2
                    offset_y = (30 - tile_image.height()) // 2

                    self.canvas.create_image(x * 30 + offset_x, y * 30 + offset_y, image=tile_image, anchor="nw")


    def on_clicked_run(self):
        pass

    def on_click_add(self):
        self.mode = Mode.Add

    def on_selected_add_option(self, option:str):
        self.add_option = TileType[option]

    def on_click_remove(self):
        self.mode = Mode.Remove

    def on_click_canvas(self, event):
        x = event.x // 30
        y = event.y // 30
        
        match(self.mode):
            case Mode.Add:
                print(f"Adding on {x} {y} {self.add_option.name}")
                self.map.set_tile(x, y, self.add_option)
            case Mode.Remove:
                print(f"Removing on {x} {y}")
                self.map.set_tile(x, y, TileType.Empty)

        self.draw_canvas()

if __name__ == "__main__":
    QLearningApp().run()
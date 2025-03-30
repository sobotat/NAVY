import tkinter
from tkinter import Button, PhotoImage, Canvas, OptionMenu, StringVar
from enum import Enum
from lib.exercises.cv04.map import Map, TileType
from lib.exercises.cv04.qlearning_player import QLearningPlayer
from lib.exercises.cv04.q_table import QTable

class Mode(Enum):
    Add = 0
    Remove = 1

class QLearningApp:

    def __init__(self):
        self.mode = Mode.Add
        self.add_option = TileType.Wall
        
        self.map = Map(10, 10)
        self.player = None
        self.table = QTable(0.7, 5)
        self.running = False

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

        run_without_ui_button = Button(root, text="Run Without UI", command=self.on_clicked_run_without_ui)
        run_without_ui_button.grid(row=1, column=1, sticky="ew")

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

        low_epsilon_button = Button(root, text="Low Epsilon", command=lambda: self.set_epsilon(0.1))
        low_epsilon_button.grid(row=4, column=1, sticky="ew")

        high_epsilon_button = Button(root, text="High Epsilon", command=lambda: self.set_epsilon(0.7))
        high_epsilon_button.grid(row=5, column=1, sticky="ew")
        
        self.canvas = Canvas(root, width=30 * self.map.size_x, height=30 * self.map.size_y, background="#0e1c56")
        self.canvas.bind("<Button-1>", self.on_click_canvas)
        self.canvas.grid(row=0, column=0, rowspan=20)
        self.draw_canvas()

        root.mainloop()

    def run_qlearning(self, with_ui=True):
        if self.running == True:
            self.running = False
            return
        
        if self.player is None:
            print("Add Player to Map")
            return
        
        self.player.spawn_x = self.player.x
        self.player.spawn_y = self.player.y
        
        self.running = True
        while self.map.contains_tile(TileType.Tresure) and self.running:
            self.player.update()
            if with_ui:
                self.draw_canvas()
            self.root.update()

        self.player.update()
        self.draw_canvas()
        print(f"Finished Running")
        self.running = False

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

                if self.player is not None and (self.player.x == x and self.player.y == y):
                    tile_image = PhotoImage(file=tiles_res[TileType.Player])
                    self.images.append(tile_image)

                    offset_x = (30 - tile_image.width()) // 2
                    offset_y = (30 - tile_image.height()) // 2

                    self.canvas.create_image(x * 30 + offset_x, y * 30 + offset_y, image=tile_image, anchor="nw")
        self.canvas.update()
                    
    def set_epsilon(self, value):
        self.table.epsilon = value

    def on_clicked_run(self):
        self.run_qlearning()

    def on_clicked_run_without_ui(self):
        self.run_qlearning(with_ui=False)

    def on_selected_add_option(self, option:str):
        self.mode = Mode.Add
        self.add_option = TileType[option]

    def on_click_remove(self):
        self.mode = Mode.Remove

    def on_click_canvas(self, event):
        x = event.x // 30
        y = event.y // 30
        
        match(self.mode):
            case Mode.Add:
                print(f"Adding on {x} {y} {self.add_option.name}")                
                if self.add_option == TileType.Player:
                    self.player = QLearningPlayer(x, y, self.table, self.map)
                else:
                    self.map.set_tile(x, y, self.add_option)
            case Mode.Remove:
                print(f"Removing on {x} {y}")
                if self.player is not None and (self.player.x == x and self.player.y == y):
                    self.player = None
                else:
                    self.map.set_tile(x, y, TileType.Empty)

        self.draw_canvas()

if __name__ == "__main__":
    QLearningApp().run()
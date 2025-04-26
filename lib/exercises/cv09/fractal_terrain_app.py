import tkinter as tk
from tkinter import ttk, colorchooser
from lib.exercises.cv09.terrain_generator import TerrainGenerator

class FractalTerrainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fractal Terrain")
        
        self.bg_color = "#121212"
        self.fg_color = "#E0E0E0"
        self.button_bg = "#2A2A2A"
        self.button_fg = "#E0E0E0"
        self.highlight_color = "#5A5A5A"
        self.current_color = "#228B22"

        self.root.configure(bg=self.bg_color)               
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)        
        
        self.width = 800
        self.height = 500
        self.canvas = tk.Canvas(self.main_frame, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        self.create_control_elements()
        
        self.terrain_generator = TerrainGenerator(self.canvas, self.width, self.height)
        
        self.start_x_var.set(0)
        self.start_y_var.set(200)
        self.end_x_var.set(800)
        self.end_y_var.set(200)
        self.iterations_var.set(5)
        
        self.apply_style()

        self.root.mainloop()
    
    def apply_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.bg_color)
        style.configure('TButton', 
                        background=self.button_bg, 
                        foreground=self.button_fg, 
                        borderwidth=0, 
                        focusthickness=3, 
                        focuscolor=self.highlight_color)
        style.configure('TLabel', 
                        background=self.bg_color, 
                        foreground=self.fg_color)
        style.configure('TSpinbox', 
                        background=self.button_bg, 
                        foreground=self.fg_color, 
                        fieldbackground=self.button_bg)
        
        style.map('TButton',
                  background=[('active', self.highlight_color)],
                  foreground=[('active', '#FFFFFF')])
    
    def create_control_elements(self):
        self.start_x_var = tk.IntVar()
        self.start_y_var = tk.IntVar()
        self.end_x_var = tk.IntVar()
        self.end_y_var = tk.IntVar()
        self.iterations_var = tk.IntVar()
        
        controls_row1 = ttk.Frame(self.control_frame)
        controls_row1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(controls_row1, text="Start Point:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(controls_row1, text="X:").pack(side=tk.LEFT)
        ttk.Spinbox(controls_row1, from_=0, to=self.width, width=5, textvariable=self.start_x_var).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(controls_row1, text="Y:").pack(side=tk.LEFT)
        ttk.Spinbox(controls_row1, from_=0, to=self.height, width=5, textvariable=self.start_y_var).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(controls_row1, text="End Point:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(controls_row1, text="X:").pack(side=tk.LEFT)
        ttk.Spinbox(controls_row1, from_=0, to=self.width, width=5, textvariable=self.end_x_var).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(controls_row1, text="Y:").pack(side=tk.LEFT)
        ttk.Spinbox(controls_row1, from_=0, to=self.height, width=5, textvariable=self.end_y_var).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(controls_row1, text="Iterations:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Spinbox(controls_row1, from_=1, to=10, width=5, textvariable=self.iterations_var).pack(side=tk.LEFT)
        
        controls_row2 = ttk.Frame(self.control_frame)
        controls_row2.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(controls_row2, text="Color:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.color_button = tk.Button(
            controls_row2, 
            bg=self.current_color, 
            width=3, 
            relief=tk.RAISED,
            command=self.choose_color
        )
        self.color_button.pack(side=tk.LEFT, padx=(0, 5))
        
        add_layer_btn = ttk.Button(
            controls_row2, 
            text="Add Layer", 
            command=self.add_terrain_layer
        )
        add_layer_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        remove_layer_btn = ttk.Button(
            controls_row2, 
            text="Clear Last Layer", 
            command=self.remove_last_layer
        )
        remove_layer_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_all_btn = ttk.Button(
            controls_row2, 
            text="Clear", 
            command=self.clear_all
        )
        clear_all_btn.pack(side=tk.LEFT, padx=(0, 5))
    
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.current_color, title="Color Picker")
        if color[1]:
            self.current_color = color[1]
            self.color_button.configure(bg=color[1])
    
    def add_terrain_layer(self):
        start_x = self.start_x_var.get()
        start_y = self.start_y_var.get()
        end_x = self.end_x_var.get()
        end_y = self.end_y_var.get()
        iterations = self.iterations_var.get()
        
        self.terrain_generator.generate_layer(start_x, start_y, end_x, end_y, iterations, self.current_color)
    
    def remove_last_layer(self):
        self.terrain_generator.remove_last_layer()
    
    def clear_all(self):
        self.terrain_generator.clear_all()
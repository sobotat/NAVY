import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from lib.exercises.cv12.forest_fire_model import ForestFireModel

class ForestFireApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Forest Fire Cellular Automaton")
        
        self.bg_color = "#121212"
        self.fg_color = "#E0E0E0"
        self.button_bg = "#2A2A2A"
        self.button_fg = "#E0E0E0"
        self.highlight_color = "#5A5A5A"
        
        self.root.configure(bg=self.bg_color)
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.figure = plt.Figure(figsize=(8, 5), dpi=100, facecolor=self.bg_color)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        self.create_control_elements()
        
        self.apply_style()
        
        self.grid_size = (100, 200)
        self.model = ForestFireModel(self.grid_size, self.p_var.get(), self.f_var.get(), self.density_var.get())
        
        colors = ['#8B4513', '#228B22', '#FFA500', '#000000']
        cmap = mcolors.ListedColormap(colors)
        self.img = self.ax.imshow(self.model.grid, cmap=cmap, interpolation='nearest', vmin=0, vmax=3)
        self.ax.set_title('Forest Fire Simulation', color=self.fg_color)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.figure.tight_layout()
        
        self.animation_running = False
        self.anim = None
        
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
        self.p_var = tk.DoubleVar(value=0.05)  # Probability of a new tree
        self.f_var = tk.DoubleVar(value=0.001)  # Probability of spontaneous fire
        self.density_var = tk.DoubleVar(value=0.5)  # Initial forest density
        self.neighborhood_var = tk.StringVar(value="Von Neumann")  # Neighborhood type
        
        controls_row1 = ttk.Frame(self.control_frame)
        controls_row1.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(controls_row1, text="P (New Tree):").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Spinbox(controls_row1, from_=0.0, to=1.0, increment=0.01, width=5, textvariable=self.p_var).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(controls_row1, text="F (Fire Probability):").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Spinbox(controls_row1, from_=0.0, to=1.0, increment=0.001, width=5, textvariable=self.f_var).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(controls_row1, text="Initial Density:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Spinbox(controls_row1, from_=0.0, to=1.0, increment=0.1, width=5, textvariable=self.density_var).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(controls_row1, text="Neighborhood:").pack(side=tk.LEFT, padx=(0, 5))
        neighborhood_combobox = ttk.Combobox(controls_row1, textvariable=self.neighborhood_var, values=["Von Neumann", "Moore"], state="readonly", width=10)
        neighborhood_combobox.pack(side=tk.LEFT)
        
        controls_row2 = ttk.Frame(self.control_frame)
        controls_row2.pack(fill=tk.X, pady=(0, 5))
        
        self.start_btn = ttk.Button(controls_row2, text="Start", command=self.start_animation)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_btn = ttk.Button(controls_row2, text="Stop", command=self.stop_animation)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.reset_btn = ttk.Button(controls_row2, text="Reset", command=self.reset_simulation)
        self.reset_btn.pack(side=tk.LEFT, padx=(0, 5))

    def update_model_params(self):
        if self.model is None:
            return
        
        model = self.model
        model.p = self.p_var.get()
        model.f = self.f_var.get()
        model.density = self.density_var.get()
        model.neighborhood = "von_neumann" if self.neighborhood_var.get() == "Von Neumann" else "moore"
    
    def update_frame(self, frame):        
        self.update_model_params()
        self.model.update()
        self.img.set_array(self.model.grid)
        return [self.img]
    
    def start_animation(self):
        if not self.animation_running:
            self.update_model_params()
            
            self.anim = animation.FuncAnimation(
                self.figure, self.update_frame, interval=100, blit=True, cache_frame_data=False
            )
            self.canvas.draw()
            self.animation_running = True
    
    def stop_animation(self):
        if self.animation_running and self.anim is not None:
            self.anim.event_source.stop()
            self.animation_running = False
    
    def reset_simulation(self):
        self.stop_animation()
        
        self.model = ForestFireModel(
            self.grid_size, 
            self.p_var.get(), 
            self.f_var.get(), 
            self.density_var.get(),
            "von_neumann" if self.neighborhood_var.get() == "Von Neumann" else "moore"
        )
        
        self.img.set_array(self.model.grid)
        self.canvas.draw()
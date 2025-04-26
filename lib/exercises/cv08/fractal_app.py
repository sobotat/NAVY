import tkinter as tk
from lib.exercises.cv08.fractal.mandelbrot import MandelbrotSet
from lib.exercises.cv08.fractal.julia import JuliaSet
from tkinter import ttk

class FractalApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TEA")
        self.width = 800
        self.height = 600
        
        self.bg_color = "#121212"
        self.fg_color = "#E0E0E0"
        self.button_bg = "#2A2A2A"
        self.button_fg = "#E0E0E0"
        self.highlight_color = "#5A5A5A"
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TButton', 
                             background=self.button_bg, 
                             foreground=self.button_fg, 
                             borderwidth=0, 
                             focusthickness=3, 
                             focuscolor=self.highlight_color)
        self.style.configure('TLabel', 
                             background=self.bg_color, 
                             foreground=self.fg_color)
        self.style.configure('TSpinbox', 
                             background=self.button_bg, 
                             foreground=self.fg_color, 
                             fieldbackground=self.button_bg)
        
        self.style.map('TButton',
                       background=[('active', self.highlight_color)],
                       foreground=[('active', '#FFFFFF')])
        
        self.root.configure(bg=self.bg_color)
        
        self.frame = ttk.Frame(self.root, style='TFrame')
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height, bg='black', highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.control_frame = ttk.Frame(self.frame, style='TFrame')
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        self.mandelbrot_btn = self.create_button(self.control_frame, "Mandelbrot", self.show_mandelbrot)
        self.mandelbrot_btn.pack(side=tk.LEFT, padx=(0, 5), pady=5)
        
        self.julia_btn = self.create_button(self.control_frame, "Julia", self.show_julia)
        self.julia_btn.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(self.control_frame, text="Iterace:", style='TLabel').pack(side=tk.LEFT, padx=(10, 5))
        
        self.iterations = tk.IntVar(value=100)
        self.iterations_spinbox = ttk.Spinbox(
            self.control_frame, from_=10, to=1000, increment=10,
            textvariable=self.iterations, width=5,
            command=self.change_iter,
            style='TSpinbox'
        )
        self.iterations_spinbox.pack(side=tk.LEFT)
        
        self.reset_btn = self.create_button(self.control_frame, "Reset", self.reset_view)
        self.reset_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.info_label = ttk.Label(self.control_frame, text="LMB Zoom+ | RMB Zoom-", style='TLabel')
        self.info_label.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.show_mandelbrot()
        
        self.canvas.bind("<Button-1>", self.zoom_in)
        self.canvas.bind("<Button-3>", self.zoom_out)
        self.iterations_spinbox.bind('<Return>', lambda event: self.change_iter())
        self.iterations_spinbox.bind('<FocusOut>', lambda event: self.change_iter())

        self.root.mainloop()
    
    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command,
                           bg=self.button_bg, fg=self.button_fg,
                           activebackground=self.highlight_color, activeforeground="#FFFFFF",
                           relief=tk.FLAT, bd=0, padx=10, pady=5, highlightthickness=0)
        
        button.bind("<Enter>", lambda e, b=button: b.configure(bg=self.highlight_color))
        button.bind("<Leave>", lambda e, b=button: b.configure(bg=self.button_bg))
        
        return button
    
    def update_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.fractal.get_image())
    
    def show_mandelbrot(self):
        self.current_fractal = "mandelbrot"
        self.fractal = MandelbrotSet(self.width, self.height, max_iter=self.iterations.get())
        self.update_canvas()
    
    def show_julia(self):
        self.current_fractal = "julia"
        self.fractal = JuliaSet(self.width, self.height, max_iter=self.iterations.get())
        self.update_canvas()

    def change_iter(self):
        self.fractal.max_iter = self.iterations.get()
        self.fractal.compute()
        self.update_canvas()
    
    def reset_view(self):
        if self.current_fractal == "mandelbrot":
            self.show_mandelbrot()
        else:
            self.show_julia()
    
    def zoom_in(self, event):
        self.fractal.zoom(event.x, event.y, 0.5)
        self.update_canvas()
    
    def zoom_out(self, event):
        self.fractal.zoom(event.x, event.y, 2.0)
        self.update_canvas()
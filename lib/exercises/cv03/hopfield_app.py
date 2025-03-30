import tkinter
from tkinter import messagebox, Canvas, Button, PhotoImage, Frame
import numpy as np
from lib.exercises.cv03.hopfield_network import HopfieldNetwork

class HopfieldApp:

    def __init__(self, grid_size=5):
        self.grid_size = grid_size
        self.cell_size = 40
        self.network = HopfieldNetwork(self.grid_size * self.grid_size)

    def run(self):    
        self.root = tkinter.Tk()
        root = self.root

        root.title("Hopfield Network")
        icon = PhotoImage(file="res\icons\school_icon.png")
        root.iconphoto(True, icon)
        
        self.patterns = []
        self.grid_data = -np.ones((self.grid_size, self.grid_size))
        
        self.canvas = Canvas(root, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=1)
        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.frame = Frame(root)
        self.frame.grid(row=0, column=1)
        root.grid_columnconfigure(1, minsize=100)
        Button(self.frame, text="Save Pattern", command=self.save_pattern).grid(row=0, column=0, pady=1, sticky="ew")        
        Button(self.frame, text="Recover Pattern", command=self.recover_pattern).grid(row=1, column=0, pady=1, sticky="ew")
        Button(self.frame, text="Recover Pattern\nAsync", command=self.recover_pattern_async).grid(row=2, column=0, pady=1, sticky="ew")
        Button(self.frame, text="Clear", command=self.clear_grid).grid(row=3, column=0, pady=1, sticky="ew")
        Button(self.frame, text="Show Patterns", command=self.show_patterns).grid(row=4, column=0, pady=1, sticky="ew")
        Button(self.frame, text="Clear Patterns", command=self.clear_patterns).grid(row=5, column=0, pady=1, sticky="ew")
        
        self.draw_grid()
        root.mainloop()
    
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = "black" if self.grid_data[i, j] == 1 else "white"
                self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size, (j + 1) * self.cell_size, (i + 1) * self.cell_size, 
                    fill=color, outline="gray"
                )
    
    def toggle_cell(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.grid_data[y, x] *= -1
        self.draw_grid()
    
    def save_pattern(self):
        self.patterns.append(self.grid_data.copy())
        self.network.train(self.patterns)
        messagebox.showinfo("Info", "Pattern saved!")
    
    def recover_pattern(self):
        if not self.patterns:
            messagebox.showwarning("Warning", "No patterns saved!")
            return

        recovered_flat = self.network.recover(self.grid_data.flatten())
        self.grid_data = recovered_flat.reshape(self.grid_size, self.grid_size)
        self.draw_grid()

    def recover_pattern_async(self):
        if not self.patterns:
            messagebox.showwarning("Warning", "No patterns saved!")
            return
        
        recovered_flat = self.network.recover(self.grid_data.flatten(), async_method=True)
        self.grid_data = recovered_flat.reshape(self.grid_size, self.grid_size)
        self.draw_grid()
    
    def clear_grid(self):
        self.grid_data = -np.ones((self.grid_size, self.grid_size))
        self.draw_grid()

    def clear_patterns(self):
        self.patterns.clear()
        self.network.train(self.patterns)
        messagebox.showinfo("Info", "Patterns cleared")

    def show_patterns(self):
        if not self.patterns:
            messagebox.showwarning("Warning", "No patterns saved!")
            return
        
        def show_pattern_matrix(idx):
            weights_window = tkinter.Toplevel(self.root)
            weights_window.title(f"Matrix of Pattern {idx + 1}")
            weights_window.geometry("400x300")

            text = tkinter.Text(weights_window, wrap="none")
            text.pack(fill="both", expand=True)

            pattern_matrix = self.patterns[idx]
            for row in pattern_matrix:
                text.insert("end", " ".join(f"{val:.2f}" for val in row) + "\n")

        def show_pattern_weights(idx):
            weights_window = tkinter.Toplevel(self.root)
            weights_window.title(f"Weights of Pattern {idx + 1}")
            weights_window.geometry("400x300")

            text = tkinter.Text(weights_window, wrap="none")
            text.pack(fill="both", expand=True)

            weights = self.network.pattern_weights[idx]
            for row in weights:
                text.insert("end", " ".join(f"{val:.2f}" for val in row) + "\n")

        def show_pattern_vector(idx):
            vector_window = tkinter.Toplevel(self.root)
            vector_window.title(f"Vector of Pattern {idx + 1}")
            vector_window.geometry("400x300")

            text = tkinter.Text(vector_window, wrap="none")
            text.pack(fill="both", expand=True)

            pattern_vector = self.patterns[idx].flatten()
            text.insert("end", " ".join(f"{val:.2f}" for val in pattern_vector))

        for idx, pattern in enumerate(self.patterns):
            pattern_window = tkinter.Toplevel(self.root)
            pattern_window.title(f"Pattern {idx + 1}")
            pattern_window.geometry(f"{self.grid_size * self.cell_size + 100}x{self.grid_size * self.cell_size}")

            canvas = Canvas(pattern_window, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="white")
            canvas.grid(row=0, column=0)

            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    color = "black" if pattern[i, j] == 1 else "white"
                    canvas.create_rectangle(
                        j * self.cell_size, i * self.cell_size, (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                        fill=color, outline="gray"
                    )

            frame = Frame(pattern_window)
            frame.grid(row=0, column=1)            
            
            Button(frame, text="Pattern Matrix", command=lambda idx=idx: show_pattern_matrix(idx)).grid(row=0, column=0, pady=5, sticky="ew")
            Button(frame, text="Pattern Weights", command=lambda idx=idx: show_pattern_weights(idx)).grid(row=1, column=0, pady=5, sticky="ew")
            Button(frame, text="Pattern Vector", command=lambda idx=idx: show_pattern_vector(idx)).grid(row=2, column=0, pady=5, sticky="ew")
            Button(frame, text="Close", command=pattern_window.destroy).grid(row=3, column=0, pady=5, sticky="ew")

import tkinter
import math
from tkinter import Canvas, Frame, Label, Scale, Entry, Button
import tkinter.messagebox
from collections import deque
import time

# F+F+F+F     F+F-F-FF+F+F-F          90
# F++F++F     F+F--F+F                60
# F           F[+F]F[-F]F             pi/7
# F           FF+[+F-F-F]-[-F+F+F]    pi/8

class LSystemApp:

    def __init__(self, start_angle = 0):
        self.start_angle = start_angle

    def run(self):
        self.root = tkinter.Tk()
        self.root.title("L-Systems")
        self.root.geometry("800x700")

        self.frame_controls = Frame(self.root)
        self.frame_controls.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=5)

        Label(self.frame_controls, text="Axiom:").grid(row=0, column=0, padx=5)
        self.entry_axiom = Entry(self.frame_controls, textvariable=tkinter.StringVar(value='F+F+F+F'))
        self.entry_axiom.grid(row=1, column=0, padx=5)

        Label(self.frame_controls, text="Rule:").grid(row=0, column=1, padx=5)
        self.entry_rules = Entry(self.frame_controls, textvariable=tkinter.StringVar(value='F+F-F-FF+F+F-F'))
        self.entry_rules.grid(row=1, column=1, padx=5)

        Label(self.frame_controls, text="Angle:").grid(row=0, column=2, padx=5)
        self.entry_angle = Entry(self.frame_controls, textvariable=tkinter.StringVar(value='90'))
        self.entry_angle.grid(row=1, column=2, padx=5)

        Label(self.frame_controls, text="Iterace:").grid(row=0, column=3, padx=5)
        self.frame_scale = Frame(self.frame_controls)
        self.iteration_var = tkinter.IntVar(value=1)
        self.iteration_slider = Scale(self.frame_scale, from_=1, to=7, orient=tkinter.HORIZONTAL, showvalue=False, variable=self.iteration_var)
        self.iteration_slider.grid(row=0, column=0, padx=2)
        self.value_label = Label(self.frame_scale, width=3, textvariable=self.iteration_var)
        self.value_label.grid(row=0, column=1, padx=2, sticky="w")
        self.frame_scale.grid(row=1, column=3, padx=5)

        self.button_draw = Button(self.frame_controls, text="Draw", width=10, command=self.draw)
        self.button_draw.grid(row=0, column=4, rowspan=2, sticky="nsew")

        self.canvas = Canvas(self.root, bg="white")
        self.canvas.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.root.mainloop()

    def draw(self):
        if self.button_draw["state"] == tkinter.DISABLED:
            return
        
        self.button_draw.config(state=tkinter.DISABLED)

        axiom = self.entry_axiom.get()
        rule = self.entry_rules.get()
        angle = self.entry_angle.get()
        iterations = self.iteration_var.get()
        print(axiom, rule, angle)

        if(not axiom or not rule or not angle or not iterations):
            tkinter.messagebox.showinfo(title="Info", message="Fill please all inputs")
            return
        
        angle = eval(angle, {'pi': 180})
        iterations = int(iterations)

        system = self.generate_l_system(axiom, rule, iterations)
        print("System generated")
        # print(system)

        self.canvas.delete("all")
        self.draw_l_system(system, angle)

        self.button_draw.config(state=tkinter.NORMAL)

    def draw_l_system(self, system, angle):
        # Výpočet hranic kreslení pro správné škálování
        min_x, min_y, max_x, max_y = self.calculate_boundaries(system, angle)
        
        # Výpočet měřítka
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()        
        width = max_x - min_x
        height = max_y - min_y        
        scale = min(canvas_width / width * 0.9, canvas_height / height * 0.9)
        
        # Start
        start_x = canvas_width / 2 - (min_x + max_x) / 2 * scale
        start_y = canvas_height / 2 - (min_y + max_y) / 2 * scale
        
        # Vykreslení systému
        x, y = start_x, start_y
        current_angle = self.start_angle
        stack = deque()
        
        last_update_time = time.time()
        for i, cmd in enumerate(system):
            if time.time() - last_update_time >= 0.02:
                self.root.update()
                last_update_time = time.time()

            if cmd == 'F':
                new_x = x + scale * math.cos(math.radians(current_angle))
                new_y = y + scale * math.sin(math.radians(current_angle))
                self.canvas.create_line(x, y, new_x, new_y, fill="black", width=1)
                x, y = new_x, new_y
            elif cmd == 'b':
                x = x + scale * math.cos(math.radians(current_angle))
                y = y + scale * math.sin(math.radians(current_angle))
            elif cmd == '+':
                current_angle += angle
            elif cmd == '-':
                current_angle -= angle
            elif cmd == '[':
                stack.append((x, y, current_angle))
            elif cmd == ']':
                if stack:
                    x, y, current_angle = stack.pop()

    def calculate_boundaries(self, system, angle):
        x, y = 0, 0
        current_angle = self.start_angle
        
        min_x, min_y = 0, 0
        max_x, max_y = 0, 0
        
        stack = deque()
        
        last_update_time = time.time()
        for cmd in system:
            if time.time() - last_update_time >= 0.02:
                self.root.update()
                last_update_time = time.time()

            if cmd == 'F':
                x += math.cos(math.radians(current_angle))
                y += math.sin(math.radians(current_angle))
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            elif cmd == 'b':
                x += math.cos(math.radians(current_angle))
                y += math.sin(math.radians(current_angle))
            elif cmd == '+':
                current_angle += angle
            elif cmd == '-':
                current_angle -= angle
            elif cmd == '[':
                stack.append((x, y, current_angle))
            elif cmd == ']':
                if stack:
                    x, y, current_angle = stack.pop()
            
        return min_x, min_y, max_x, max_y

    def generate_l_system(self, axiom, rule, iterations):
        current = axiom
        for iteration in range(1, iterations + 1):
            print(f"Generation {iteration} Iteration")
            next_gen = []
            for char in current:
                self.root.update()

                if char == 'F':
                    next_gen.append(f' {rule} ')
                else:
                    next_gen.append(char)
            current = "".join(next_gen)
        return current
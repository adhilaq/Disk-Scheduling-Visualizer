import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import time


class LineGraph(tk.Frame):
    def __init__(self, master, n, **kw):
        super().__init__(master, **kw)
        self.root = master
        self.n = n
        self.fig = Figure(dpi=100, facecolor="yellow")
        ax = self.fig.add_subplot(111)
        ax.grid()
        ax.plot([0])
        plt.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.

        self.canvas.draw()
        self.canvas_obj = self.canvas.get_tk_widget()
        self.canvas_obj.pack(expand=True, fill="both", pady=10, padx=10)

    def animate(self, p, l, time, mark_on):
        if p == len(l) + 1:
            return
        self.fig.clf()
        ax = self.fig.add_subplot(111, title="Head Movement", xlabel="no of movements", ylabel="cylinder addresses",
                                  ylim=(0, self.n), xlim=(0, len(l)))
        ax.grid()
        ax.plot(l[:p + 1], "-gD", markevery=mark_on[:p + 1], color="red")
        self.canvas.draw()
        self.after(time, self.animate, p + 1, l, time, mark_on)


if __name__ == "__main__":
    root = tk.Tk()
    seq = [10, 3, 8, 1, 5, 9, 2]
    plot = LineGraph(root, 10,  bg="red", height=500, width=500)
    plot.pack(expand=True, fill="both")

    plot.animate(1, seq, 1, [True]*len(seq))

    root.mainloop()

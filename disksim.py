import tkinter as tk
import random
import time


def rand_col(n, var):
    r = 100  # random.randint(0, 255)
    g = 255
    b = 0
    for i in range(n):
        yield '#%02X%02X%02X' % (r, g, b)
        b = (b + var) % 255


class DiskSim(tk.Canvas):
    def __init__(self, root, n, **kw):
        super().__init__(root, **kw)
        self.root = root
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.bind("<Configure>", self.on_resize)
        self.circles = []
        self.circle_cols = []
        self.var = 20
        self.n = n
        self.draw_disks()
        self.in_motion = False

    def update_dim(self):
        self.height = self.winfo_height()
        self.width = self.winfo_width()

    def draw_disks(self):
        col = rand_col(self.n, self.var)
        self.update_dim()
        cr = self.height / 2
        cc = self.width / 2
        r = min(self.height, self.width) / 2
        for i in range(self.n, 0, -1):
            col_i = next(col)
            ri = i * r / self.n
            o = self.create_oval((cc - ri, cr - ri, cc + ri, cr + ri), fill=col_i)
            self.circles.append(o)
            self.circle_cols.append(col_i)

    def update_disks(self):
        self.update_dim()
        cr = self.height / 2
        cc = self.width / 2
        r = min(self.height, self.width) / 2
        i = self.n
        for o in self.circles:
            ri = i * r / self.n
            self.coords(o, (cc - ri, cr - ri, cc + ri, cr + ri))
            i -= 1

    def on_resize(self, event):
        '''wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        if event.width<event.height:
            hscale = wscale
        elif event.height<event.width:
            wscale = hscale'''
        self.width = event.width
        self.height = event.height
        self.update_disks()
        self.root.update()
        # self.scale("all", 0, 0, wscale, hscale)

    def delay(self, t):
        now = time.time()
        while time.time() - now < t / 1000:
            self.update()

    def hold_light(self, index):
        self.itemconfig(self.circles[self.n - index], fill="red")

    def high_light(self, index):
        self.itemconfig(self.circles[self.n - index], fill="purple")

    def release_light(self, index):
        self.itemconfig(self.circles[self.n - index], fill=self.circle_cols[self.n - index])

    def clear(self):
        for i in range(1,len(self.circles)+1):
            self.release_light(i)

    def strobe(self, index, time):
        self.hold_light(index)
        self.after(time, self.release_light, index)

    def animate_seq(self, p, l, time):
        self.in_motion = True
        if p == len(l):
            self.hold_light(l[p - 1])
            self.in_motion = False
            return
        self.strobe(l[p], time)
        self.after(time, self.animate_seq, p + 1, l, time)


if __name__ == "__main__":
    root = tk.Tk()
    d = DiskSim(root, 10, bg="orange", height=450, width=400)
    d.grid(row=0, column=0, sticky="nsew", columnspan=1)

    seq = [10, 3, 8, 1, 5, 9, 2]

    d.animate_seq(0, seq, 100)
    root.mainloop()

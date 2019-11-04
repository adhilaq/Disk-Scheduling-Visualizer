from disksim import *
from linegraph import *
from algorithms import *
import time


def get_full(sequence):
    complete_seq = []
    marker_array = []
    for i in range(len(sequence)):
        if i == len(sequence) - 1:
            complete_seq.append(sequence[i])
            marker_array.append(True)
            break
        if sequence[i] == sequence[i + 1]:
            complete_seq.append(sequence[i])
            marker_array.append(True)
            continue
        sign = -int(abs(sequence[i] - sequence[i + 1]) / (sequence[i] - sequence[i + 1]))
        complete_seq += list(range(sequence[i], sequence[i + 1], sign))
        marker_array += [True] + [False] * (abs(sequence[i + 1] - sequence[i]) - 1)
    return complete_seq, marker_array


def animate_seq(disk_obj, lg_obj, full_seq, mark_on, time_delay, p):
    global zero, pause_zero
    disk_obj.in_motion = True
    if 0 < p < len(full_seq):
        disk_obj.release_light(full_seq[p - 1])
    if p == len(full_seq):
        disk_obj.in_motion = False
        start_button.config(state='normal')
        pause_button.config(state='disabled')
        stop_button.config(state='disabled')
        lb.config(text="DONE")
        return
    if stopped:
        disk_obj.clear()
        lg_obj.fig.clf()
        ax = lg_obj.fig.add_subplot(111, title="Head Movement", xlabel="no of movements", ylabel="cylinder addresses")
        ax.grid()
        lg_obj.canvas.draw()
        return
    if paused:
        disk_obj.hold_light(full_seq[p])
        pause_zero = time.time()
    while paused:
        if stopped:
            disk_obj.clear()
            lg_obj.fig.clf()
            ax = lg_obj.fig.add_subplot(111, title="Head Movement", xlabel="no of movements",
                                        ylabel="cylinder addresses")
            ax.grid()
            lg_obj.canvas.draw()
            return
        root.update()
        if not paused:
            zero += time.time() - pause_zero
    disk_obj.hold_light(full_seq[p])

    lg_obj.fig.clf()
    ax = lg_obj.fig.add_subplot(111, title="Head Movement", xlabel="no of movements", ylabel="cylinder addresses",
                                ylim=(0, lg_obj.n), xlim=(0, len(full_seq)))
    ax.grid()
    ax.plot(full_seq[:p + 2], "-gD", markevery=mark_on[:p + 2], color="red")
    lg_obj.canvas.draw()
    lbl.config(text='Head movements: %d' % (p))
    lbr.config(text='Total Time: %f' % (time.time() - zero))
    root.after(time_delay, animate_seq, disk_obj, lg_obj, full_seq, mark_on, time_delay, p + 1)


def stop():
    global stopped, paused
    stopped = True
    lb.config(text="STOPPED")
    lbl.config(text='Head movements: %d' % (0))
    lbr.config(text='Total Time: %f' % (0))
    pause_button.config(text="PAUSE", state="disabled")
    start_button.config(state="normal")
    stop_button.config(state="disabled")


def pause():
    global paused, stopped
    if paused:
        paused = False
        lb.config(text="PLAYING")
        pause_button.config(text="PAUSED")
    else:
        paused = True
        lb.config(text="PAUSED")
        pause_button.config(text="CONTINUE")


def start(disk_obj):
    global stopped, paused, zero, dic
    dic = {
        "LOOK": look,
        "SCAN": scan,
        "C-LOOK": c_look,
        "C-SCAN": c_scan,
        "SSTF": sstf,
        "FCFS": fcfs,
        "OPTIMAL": optimal
    }
    stop_button.config(state="normal")
    lb.config(text="PLAYING")
    stopped = False
    paused = False
    disk_obj.clear()
    seq = [slider3.get()]+eval(tb.get())
    s = dic[choice.get()](seq)
    fi, m = get_full(s)
    start_button.config(state=tk.DISABLED)
    pause_button.config(state="normal")
    zero = time.time()
    animate_seq(disk, plot, fi, m, 0, 0)


def fill_entry():
    tb.delete(0,tk.END)
    l = []
    req_size = random.randint(8, 30)
    i = 0
    while i < req_size:
        r = random.randint(1, slider2.get())
        if r not in l:
            l.append(r)
            i+=1
    tb.insert(0,str(l))


stopped = False
paused = False
zero = 0.0
pause_zero = 0.0
sorts = ["LOOK", "SCAN", "C-LOOK", "C-SCAN", "SSTF", "FCFS", "OPTIMAL"]


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("DISK ALGORITHM SIMULATION")

    size = 40
    req_size = 12

    # REQUESTS ROW3
    row3 = tk.Frame(root, bg='red', bd=5, relief='groove')
    tk.Label(row3, text='REQUESTS:', fg='yellow', bg='green', font=('courier', 20, 'bold')).pack(side="left")
    tb = tk.Entry(row3, bd=5, fg='black', bg='gold', font=('courier', 12, 'bold'), highlightbackground='orange')
    tb.insert(0,'[15, 21, 4, 11, 1, 5, 22, 6, 35, 26]')
    tb.pack(side="left", expand=True, fill='both')
    rand_button = tk.Button(row3, text='RANDOMIZE', fg='green', bg='light blue', font=('courier', 20, 'bold'),
                            relief='groove', command=fill_entry, bd=10)
    rand_button.pack(side="right")

    def resize_consequence(event):
        slider3.config(to=slider2.get())
        tb.delete(0, tk.END)

    # SIZE ROW1
    row1 = tk.Frame(root, bg='red', bd=5, relief='groove')
    tk.Label(row1, text='SIZE OF DISK:', fg='yellow', bg='green', font=('courier', 20, 'bold')).pack(side="left")
    slider2 = tk.Scale(row1, from_=40, to=100, orient='horizontal', fg='white', bg='green',
                       font=('courier', 20, 'bold'), command=resize_consequence,
                       troughcolor='orange', activebackground='yellow', highlightbackground='orange')
    slider2.set(0)
    slider2.pack(side="right", fill='x', expand=True)

    def show_head(event):
        if slider3.get()>1:
            disk.release_light(slider3.get()-1)
        if slider3.get()<slider2.get():
            disk.release_light(slider3.get()+1)
        disk.high_light(slider3.get())


    # HEAD ROW2
    row2 = tk.Frame(root, bg='red', bd=5, relief='groove')
    tk.Label(row2, text='HEAD POSITION:', fg='yellow', bg='green', font=('courier', 20, 'bold')).pack(side="left")
    slider3 = tk.Scale(row2, from_=1, to=slider2.get(), orient='horizontal', fg='white', bg='green',
                       font=('courier', 20, 'bold'), command=show_head,
                       troughcolor='orange', activebackground='yellow', highlightbackground='orange')
    slider3.set(14)
    slider3.pack(side="right", fill='x', expand=True)

    # CHOICE ROW4
    row4 = tk.Frame(root, bg='red', bd=5, relief='groove')
    tk.Label(row4, text='DISC SCHEDULING ALGORITHM:', font=('courier', 20, 'bold'), fg='yellow', bg='green').pack(
        side="left",
        fill='x',
        expand=True)
    choice = tk.StringVar(row4)
    menu = tk.OptionMenu(row4, choice, *sorts)
    menu.config(fg='white', bg='green', font=('courier', 20, 'bold'), highlightbackground='orange',
                activebackground='yellow')
    choice.set("FCFS")
    menu.pack(side="right", fill='x', expand=True)

    # STATS ROW5
    row5 = tk.Frame(root, bd=5, relief='sunken')
    lbl = tk.Label(row5, text='Head movements: %d' % (0), fg='light blue', font=('courier', 20, 'italic'), bd=5,
                   bg='#c776b9',
                   relief='raised')
    lb = tk.Label(row5, text='START', fg='light blue', font=('courier', 20, 'italic'), bd=5, bg='#c776b9',
                  relief='raised')
    lbr = tk.Label(row5, text='Total Time: %f' % 0, fg='light blue', font=('courier', 20, 'italic'), bd=5, bg='#c776b9',
                   relief='raised')

    # SIMULATION ROW6
    f = tk.Frame()
    disk = DiskSim(f, size, bg="blue", height=500, width=400)
    plot = LineGraph(f, size, bg="red", height=500, width=400)
    disk.pack(side="right", fill="both", expand=True, padx=4, pady=4)
    plot.pack(side="left", fill="both", expand=True)


    def start_util():
        global disk, f, slider2
        disk.destroy()
        new_size = slider2.get()
        disk = DiskSim(f, new_size, bg="blue", height=500, width=400)
        plot.n = new_size
        disk.pack(side="right", fill="both", expand=True, padx=4, pady=4)
        start(disk)


    # BUTTONS
    buttons = tk.Frame(root, bg='red', bd=5, relief='groove')
    start_button = tk.Button(buttons, text='GO', fg='yellow', bg='orange', font=('courier', 20, 'bold'),
                             relief='groove', command=start_util,
                             bd=10)
    pause_button = tk.Button(buttons, text='PAUSE', fg='yellow', bg='orange',
                             font=('courier', 20, 'bold'),
                             relief='groove', command=pause, state='disabled',
                             bd=10)
    stop_button = tk.Button(buttons, text='STOP', fg='yellow', bg='orange', font=('courier', 20, 'bold'),
                            relief='groove', command=stop, state='disabled',
                            bd=10)
    # PACKING
    row1.pack(fill='x')
    row2.pack(fill='x')
    row3.pack(fill='x')
    row4.pack(fill='x')

    start_button.pack(side='left', fill='x', expand=True)
    pause_button.pack(side='left', fill='x', expand=True)
    stop_button.pack(side='right', fill='x', expand=True)
    buttons.pack(fill='x')

    lbl.pack(side="left", fill='x', expand=True)
    lb.pack(side="left", fill='x', expand=True)
    lbr.pack(side="right", fill='x', expand=True)
    row5.pack(fill='x')

    f.pack()

    root.mainloop()
'''
    seq = [10, 3, 8, 1, 5, 9, 2, 6, 8, 4, 19, 15, 12, 13]
    f, m = get_full(seq)
    animate_seq(disk, plot, f, m, 1, 0)
'''

import tkinter as tk


window = tk.Tk()


for i in range(3):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)

    for j in range(3):
        frame = tk.Frame(
            master=window,
            borderwidth=1,
            relief=tk.RAISED
        )
        frame.grid(
            row=i,
            column=j,
            padx=5,
            pady=5,
        )

        label = tk.Label(
            text="Row: {0} Column: {1}".format(i, j),
            master=frame
        )
        label.pack(padx=5, pady=5)


window.mainloop()

import tkinter as tk


labels = [
    "First Name:",
    "Last Name:",
    "Address Line 1:",
    "Address Line 2:",
    "City:",
    "State/Province:",
    "Postal Code:",
    "Country:",
]

window = tk.Tk()
window.title("Adress Form")

frm_form = tk.Frame(
    borderwidth=3,
    relief=tk.SUNKEN
)

frm_form.pack(fill=tk.X)

for idx, text in enumerate(labels):

    label = tk.Label(text=text, master=frm_form)

    entry = tk.Entry(width=50, master=frm_form)

    label.grid(row=idx, column=0, sticky="e")
    entry.grid(row=idx, column=1)

frm_btn = tk.Frame()

frm_btn.pack(fill=tk.X, ipadx=5, ipady=5)

submit_btn = tk.Button(master=frm_btn, text="Submit")

clear_btn = tk.Button(master=frm_btn, text="Clear")

submit_btn.pack(ipadx=10, padx=10,  side=tk.RIGHT)

clear_btn.pack(ipadx=10, side=tk.RIGHT)


window.mainloop()

import tkinter as tk

from .cli import methods, run


window = tk.Tk()
window.title("Cyber City Test GUI")

label_ip = tk.Label(window, text="IP Address")
entry_ip = tk.Entry(window)
entry_ip.insert(0, "127.0.0.1")
label_ip.pack()
entry_ip.pack()

label_methods = tk.Label(window, text="Modbus Method")
method = tk.StringVar()
method.set(methods[0])
option_methods = tk.OptionMenu(window, method, *methods)
label_methods.pack()
option_methods.pack()

label_start_addr = tk.Label(window, text="Start Address")
entry_start_addr = tk.Entry(window)
entry_start_addr.insert(0, "0")
label_start_addr.pack()
entry_start_addr.pack()

label_end_addr = tk.Label(window, text="End Address")
entry_end_addr = tk.Entry(window)
entry_end_addr.insert(0, "0")
label_end_addr.pack()
entry_end_addr.pack()

value = tk.IntVar()
checkbox_value = tk.Checkbutton(window, text="Value", variable=value)
checkbox_value.pack()


def send():
    ip = entry_ip.get()
    start_addr = int(entry_start_addr.get())
    end_addr = int(entry_end_addr.get())

    run(ip, method.get(), start_addr, end_addr, value.get())


button_send = tk.Button(window, text="Send", command=send)
button_send.pack()

window.mainloop()

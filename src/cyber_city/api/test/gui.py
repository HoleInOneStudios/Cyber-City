import tkinter as tk

from .cli import methods, run


window = tk.Tk()
window.title("Cyber City Test GUI")

frame_input = tk.Frame(window)
frame_input.grid(row=0, column=0)

label_ip = tk.Label(frame_input, text="IP Address")
entry_ip = tk.Entry(frame_input)
entry_ip.insert(0, "192.168.1.98")
entry_ip.grid(row=0, column=1)
label_ip.grid(row=0, column=0)

label_methods = tk.Label(frame_input, text="Modbus Method")
method = tk.StringVar()
method.set(methods[0])
option_methods = tk.OptionMenu(frame_input, method, *methods)
option_methods.grid(row=1, column=1)
label_methods.grid(row=1, column=0)

label_start_addr = tk.Label(frame_input, text="Start Address")
entry_start_addr = tk.Entry(frame_input)
entry_start_addr.insert(0, "0")
entry_start_addr.grid(row=2, column=1)
label_start_addr.grid(row=2, column=0)

label_end_addr = tk.Label(frame_input, text="End Address")
entry_end_addr = tk.Entry(frame_input)
entry_end_addr.insert(0, "0")
entry_end_addr.grid(row=3, column=1)
label_end_addr.grid(row=3, column=0)

value = tk.IntVar()
checkbox_value = tk.Checkbutton(frame_input, text="Value", variable=value)
checkbox_value.grid(row=5, column=0)

frame_output = tk.Frame(window)
frame_output.grid(row=0, column=1)


output_text = tk.Text(frame_output)
output_scroll = tk.Scrollbar(
    frame_output, orient=tk.VERTICAL, command=output_text.xview
)

output_text.config(xscrollcommand=output_scroll.set)
output_text.grid(row=0, column=0)
output_scroll.grid(row=0, column=1, sticky=tk.N + tk.S)


def send():
    ip = entry_ip.get()
    start_addr = int(entry_start_addr.get())
    end_addr = int(entry_end_addr.get())

    result = run(ip, method.get(), start_addr, end_addr, value.get())

    output_text.delete("1.0", tk.END)
    temp_start = start_addr
    if result:
        for i in result:
            output_text.insert(tk.END, f"{temp_start}: {i}\n")
            temp_start += 1


button_send = tk.Button(window, text="Send", command=send)
button_send.grid(row=1, column=0)

window.mainloop()

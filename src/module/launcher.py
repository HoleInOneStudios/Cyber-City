import tkinter as tk


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Launcher")
        self.geometry("300x200")

        self.add_widgets()

        self.mainloop()

    def add_widgets(self):
        # connection settings
        self.connection_settings = tk.LabelFrame(self, text="Connection Settings")
        self.connection_settings.pack(fill="both", expand="no", padx=20, pady=10)

        # host entry with label
        self.host_frame = tk.Frame(self.connection_settings)
        self.host_frame.pack(fill="x", expand="yes")
        self.host_label = tk.Label(self.host_frame, text="Host:")
        self.host_label.pack(side="left")
        self.host_entry = tk.Entry(self.host_frame)
        self.host_entry.pack(side="right")

        # port entry with label
        self.port_frame = tk.Frame(self.connection_settings)
        self.port_frame.pack(fill="x", expand="yes")
        self.port_label = tk.Label(self.port_frame, text="Port:")
        self.port_label.pack(side="left")
        self.port_entry = tk.Entry(self.port_frame)
        self.port_entry.pack(side="right")

        # launch button options
        self.launch_button_options = tk.LabelFrame(self, text="Launch")
        self.launch_button_options.pack(fill="both", expand="yes", padx=20, pady=10)

        # launch dashboard button
        self.launch_dashboard_button = tk.Button(
            self.launch_button_options,
            text="Launch Dashboard",
            command=self.launch_dashboard,
        )
        self.launch_dashboard_button.pack(expan="yes", fill="x")
        # launch offensive player button
        self.launch_offensive_player_button = tk.Button(
            self.launch_button_options,
            text="Launch Offensive Player",
            command=self.launch_offensive_player,
        )
        self.launch_offensive_player_button.pack(expand="yes", fill="x")

        # launch defensive player button
        self.launch_defensive_player_button = tk.Button(
            self.launch_button_options,
            text="Launch Defensive Player",
            command=self.launch_defensive_player,
        )
        self.launch_defensive_player_button.pack(expand="yes", fill="x")

    def launch_dashboard(self):
        host, port = self.get_host_port()
        print(f"Launching dashboard with host: {host} and port: {port}")

    def launch_offensive_player(self):
        host, port = self.get_host_port()
        print(f"Launching dashboard with host: {host} and port: {port}")

    def launch_defensive_player(self):
        host, port = self.get_host_port()
        print(f"Launching dashboard with host: {host} and port: {port}")

    def get_host_port(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        return host, port


if __name__ == "__main__":
    Launcher()

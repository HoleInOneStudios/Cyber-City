"""
Modbus test web server dashboard

requirements:
- pymodbus
- flask

to run the server:
- `flask --app ./cyber_city/api/server/main.py run'
"""

from flask import Flask, render_template, request
from pymodbus.client import ModbusTcpClient as ModbusClient

app = Flask(__name__)


@app.route("/")
@app.route("/<max_coils>")
@app.route("/<max_coils>/<ip>")
def main(ip_address="127.0.0.1", max_coils=50) -> str:
    """
    the main dashboard route for the web server

    Args:
        ip (str, optional): _description_. Defaults to "127.0.0.1".
        max_coils (int, optional): _description_. Defaults to 50.

    Returns:
        (str): html result
    """
    coils = {}
    max_coils = int(max_coils)
    for i in range(0, max_coils + 1):
        coils[i] = False
    return render_template("dashboard.html", ip=ip_address, coils=coils)


@app.route("/coil", methods=["POST", "GET"])
def coil() -> str:
    """
    the api side of the dashboard web server

    Returns:
        (str): method type
    """
    ip_address = request.headers["ip"]
    current_coil = request.headers["coil"]
    if request.method == "POST":
        value = request.get_json()["value"]
        client = ModbusClient(ip_address)
        if client.connect():
            client.write_coil(int(current_coil), value)
            client.close()
        return "POST"
    if request.method == "GET":
        client = ModbusClient(ip_address)
        if client.connect():
            result = client.read_coils(int(current_coil), 1).bits[0]
            client.close()
            return {
                "coil": int(current_coil),
                "value": result,
            }
        return "GET"

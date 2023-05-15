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
@app.route("/<input_coils>/")
@app.route("/<input_coils>/<ip_address>")
def main(input_coils=50, ip_address="127.0.0.1") -> str:
    print(ip_address, input_coils)
    coils = {}
    input_coils = int(input_coils)
    for i in range(0, int(input_coils) + 1):
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

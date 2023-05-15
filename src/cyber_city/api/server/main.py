from flask import Flask, render_template, request
from pymodbus.client import ModbusTcpClient as ModbusClient
import json

app = Flask(__name__)


coils = {}

max = 25
for i in range(0, max - 1):
    coils[i] = False


@app.route("/")
@app.route("/<ip>")
def main(ip="127.0.0.1"):
    return render_template("dashboard.html", coils=coils, ip=ip)


@app.route("/coil", methods=["POST", "GET"])
def coil():
    ip = request.headers["ip"]
    coil = request.headers["coil"]
    if request.method == "POST":
        value = request.get_json()["value"]
        client = ModbusClient(ip)
        if client.connect():
            client.write_coil(int(coil), value)
            client.close()
        return "POST"
    if request.method == "GET":
        client = ModbusClient(ip)
        if client.connect():
            result = client.read_coils(int(coil), 1).bits[0]
            client.close()
            return {
                "coil": int(coil),
                "value": result,
            }
        return "GET"

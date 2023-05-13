from pymodbus.client import ModbusTcpClient as ModbusClient
from time import sleep

client = ModbusClient("192.168.1.98")
client.connect()

depth = 50

client.write_coil(24, False)

# for i in range(16, 100, 8):
#    client.write_coil(i, True)
#    print(client.read_coils(i, 1).bits[0])

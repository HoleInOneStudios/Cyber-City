"""
This runs in a terminal and is used to test the Modbus connection.

- Reads and Writes to the Modbus server.
- Used for finding the correct Modbus addresses.
- Used for testing the Modbus server.
"""
from ipaddress import ip_address
from pymodbus.client import ModbusTcpClient as ModbusClient

IP: str
CLIENT: ModbusClient
ACTIVE: bool = True
OPTIONS: list = ["Read Coil", "Write Coil", "Exit"]

if __name__ == "__main__":
    # Get IP address from user
    IP: str = str(input("Enter the IP address of the Modbus server: "))

    # Check if the IP address is valid if not use the default IP address
    try:
        ip_address(IP)
        print("Valid IP address")
    except ValueError:
        IP = "127.0.0.1"
        print("Invalid IP address, using default IP address")

    # Create Modbus client
    CLIENT = ModbusClient(IP)

    # Tries to connect to the Modbus server
    if CLIENT.connect():
        print("Connected to Modbus server")
    else:
        CLIENT.close()
        print("Failed to connect to Modbus server")
        exit()

    while ACTIVE:
        print("What do you want to do?")
        for i in enumerate(OPTIONS):
            print(f"{i[0] + 1}. {i[1]}")

        option = int(input("Enter option: "))

        if OPTIONS[option - 1] == "Exit":
            CLIENT.close()
            exit()
        elif OPTIONS[option - 1] == "Read Coil":
            address = int(input("Enter address: "))
            print("=====================================")
            print(f"Coil {address} is {CLIENT.read_coils(address, 1).bits[0]}")
            print("=====================================")

        elif OPTIONS[option - 1] == "Write Coil":
            address = int(input("Enter address: "))
            value = max(0, min(int(input("Enter value: ")), 1))

            print("=====================================")
            print(f"Writing {value} to address {address}")
            print("=====================================")

            CLIENT.write_coil(address, value == 1)

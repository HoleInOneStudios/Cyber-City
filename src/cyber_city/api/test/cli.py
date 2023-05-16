"""
This file is used to test the connection to the modbus server and read/write to the modbus addresses.

Requirements:
- pymodus
- argparse

Features:
- Read and write to modbus registers
- Read and write to modbus coils
- Read modbus input registers
- Read modbus discrete inputs
"""

import argparse
from pymodbus.client import ModbusTcpClient as ModbusClient


def read_coils(client: ModbusClient, start_addr: int, end_addr: int) -> list:
    """
    Read the values of the coils from the modbus server.

    Parameters:
    - client: Modbus client
    - start_addr: Starting address of the coils
    - end_addr: Ending address of the coils
    - num_coils: Number of coils to read

    Returns:
    - List of values of the coils
    """
    response = client.read_coils(start_addr, end_addr - start_addr + 1)
    return response.bits[: end_addr - start_addr + 1]


def write_coils(
    client: ModbusClient, start_addr: int, end_addr: int, value: int
) -> None:
    """
    Write the value to the coils.

    Parameters:
    - client: Modbus client
    - start_addr: Starting address of the coils
    - end_addr: Ending address of the coils
    - value: Value to write to the coils
    """

    client.write_coils(start_addr, [value] * (end_addr - start_addr + 1))
    return None


def read_discrete_inputs(client: ModbusClient, start_addr: int, end_addr: int) -> list:
    """
    Read the values of the discrete inputs from the modbus server.

    Parameters:
    - client: Modbus client
    - start_addr: Starting address of the discrete inputs
    - end_addr: Ending address of the discrete inputs
    - num_coils: Number of discrete inputs to read

    Returns:
    - List of values of the discrete inputs
    """
    response = client.read_discrete_inputs(start_addr, end_addr - start_addr + 1)
    return response.bits[: end_addr - start_addr + 1]


def read_input_registers(client: ModbusClient, start_addr: int, end_addr: int) -> list:
    """
    Read the values of the input registers from the modbus server.

    Parameters:
    - client: Modbus client
    - start_addr: Starting address of the input registers
    - end_addr: Ending address of the input registers
    - num_coils: Number of input registers to read

    Returns:
    - List of values of the input registers
    """
    response = client.read_input_registers(start_addr, end_addr - start_addr + 1)
    return response.registers[: end_addr - start_addr + 1]


def read_holding_register(client: ModbusClient, start_addr: int, end_addr: int) -> list:
    """
    Read the values of the holding registers from the modbus server.

    Parameters:
    - client: Modbus client
    - start_addr: Starting address of the holding registers
    - end_addr: Ending address of the holding registers
    - num_coils: Number of holding registers to read

    Returns:
    - List of values of the holding registers
    """
    response = client.read_holding_registers(start_addr, end_addr - start_addr + 1)
    return response.registers[: end_addr - start_addr + 1]


def write_holding_register(client: ModbusClient, start_addr: int, value: int) -> None:
    """
    Write the value to the holding registers.

    Parameters:
    - client: Modbus client
    - start_addr: Starting address of the holding registers
    - end_addr: Ending address of the holding registers
    - value: Value to write to the holding registers
    """

    client.write_register(start_addr, value)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test the connection to the modbus server and read/write to the modbus addresses.",
    )

    parser.add_argument(
        "-i",
        "--ip",
        dest="ip_address",
        type=str,
        help="IP address of the modbus server",
        default="127.0.0.1",
        required=True,
    )

    parser.add_argument(
        "-m",
        "--method",
        dest="modbus_method",
        type=str,
        help="Modbus method to use",
        default="read_coils",
        choices=[
            "read_coils",
            "write_coils",
            "read_discrete_inputs",
            "read_input_registers",
            "read_holding_register",
            "write_holding_register",
        ],
        required=True,
    )

    parser.add_argument(
        "-s",
        "--start",
        dest="start",
        type=int,
        help="Starting address of the modbus address",
        default=0,
        required=True,
    )

    parser.add_argument(
        "-e",
        "--end",
        dest="end",
        type=int,
        help="Ending address of the modbus address",
        default=0,
    )

    parser.add_argument(
        "-v",
        "--value",
        dest="value",
        type=int,
        help="Value to write to the modbus address",
        default=0,
    )

    args = parser.parse_args()

    client = ModbusClient(args.ip_address, port=502)

    if args.modbus_method == "read_coils":
        print(read_coils(client, args.start, args.end - args.start))
    elif args.modbus_method == "write_coils":
        write_coils(client, args.start, args.end, args.value)
    elif args.modbus_method == "read_discrete_inputs":
        print(read_discrete_inputs(client, args.start, args.end - args.start + 1))
    elif args.modbus_method == "read_input_registers":
        print(read_input_registers(client, args.start, args.end - args.start + 1))
    elif args.modbus_method == "read_holding_register":
        print(read_holding_register(client, args.start, args.end - args.start + 1))
    elif args.modbus_method == "write_holding_register":
        write_holding_register(client, args.start, args.value)
    else:
        print("Invalid modbus method")

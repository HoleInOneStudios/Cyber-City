from cyber_city.api import System, ModbusSystem, TrafficLight, Power, District, SpecialDistrict

# Lights
G_NS = ModbusSystem(0)
Y_NS = ModbusSystem(1)
R_NS = ModbusSystem(2)
G_EW = ModbusSystem(3)
Y_EW = ModbusSystem(4)
R_EW = ModbusSystem(5)

# Traffic Lights
NS = TrafficLight(R_NS, Y_NS, G_NS)
EW = TrafficLight(R_EW, Y_EW, G_EW)

TRAFFICLIGHTS = [NS, EW]

# Power Grid
POWER_GRID = System()

# Power Systems
BD = Power(0, POWER_GRID)
HP = Power(1, POWER_GRID)
PF = Power(2, POWER_GRID)
IN = Power(3, POWER_GRID)
UN = Power(4, POWER_GRID)
RE = Power(5, POWER_GRID)

grid = [BD, HP, PF, IN, UN, RE]

# Special Districts
H_P = ModbusSystem(0)
H_G = ModbusSystem(1)
HOSPITAL = SpecialDistrict("Hospital", HP, H_P, H_G)

PF_P = ModbusSystem(0)
PF_G = ModbusSystem(1)
POLICE_FIRE = SpecialDistrict("Police/Fire", PF, PF_P, PF_G)

# Districts
BUSINESS = District("Business", BD)
INDUSTRIAL = District("Industrial", IN)
UNIVERSITY = District("University", UN)
RESIDENTIAL = District("Residential", RE)

DISTRICTS = [
    BUSINESS, HOSPITAL, POLICE_FIRE, INDUSTRIAL, UNIVERSITY, RESIDENTIAL]

# Print Districts
for district in DISTRICTS:
    print(district)
    
# Print Traffic Lights
for light in TRAFFICLIGHTS:
    print(light)
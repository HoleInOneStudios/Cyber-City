import os

from monitoring import parse_st

def get_addresses(b):
    for debug_data in b:
        if (debug_data.location.find('IX')) > 0:
            #Reading Input Status
            mb_address = debug_data.location.split('%IX')[1].split('.')
            result = int(mb_address[0])*8 + int(mb_address[1])
            debug_data.value = f"InputStatus:{result}"
            
        elif (debug_data.location.find('QX')) > 0:
            #Reading Coils
            mb_address = debug_data.location.split('%QX')[1].split('.')
            result = int(mb_address[0])*8 + int(mb_address[1])
            debug_data.value = f"Coil:{result}"
            
        elif (debug_data.location.find('IW')) > 0:
            #Reading Input Registers
            mb_address = debug_data.location.split('%IW')[1]
            result = int(mb_address)
            debug_data.value = f"InputRegister:{result}"
            
        elif (debug_data.location.find('QW')) > 0:
            #Reading Holding Registers
            mb_address = debug_data.location.split('%QW')[1]
            result = int(mb_address)
            debug_data.value = f"HoldingRegister:{result}"
            
        elif (debug_data.location.find('MW')) > 0:
            #Reading Word Memory
            mb_address = debug_data.location.split('%MW')[1]
            result = int(mb_address) + 1021
            debug_data.value = f"WordMemory:{result}"
            
        elif (debug_data.location.find('MD')) > 0:
            #Reading Double Memory
            mb_address = debug_data.location.split('%MD')[1]
            result = (int(mb_address)*2) + 2042
            debug_data.value = f"DoubleMemory:{result}"
                
        elif (debug_data.location.find('ML')) > 0:
            #Reading Long Memory
            mb_address = debug_data.location.split('%ML')[1]
            result = int(mb_address)*4 + 4096
            debug_data.value = f"LongMemory:{result}"

sts = os.listdir('./st_files')
print(sts)

for a in sts:
    print(a)
    b = parse_st(a)
    get_addresses(b)
    for debugs in b:
        print('Name: ' + debugs.name)
        print('Location: ' + debugs.location)
        print('Type: ' + debugs.type)
        print('Value: ' + debugs.value)
        print('')
    print("====================================")
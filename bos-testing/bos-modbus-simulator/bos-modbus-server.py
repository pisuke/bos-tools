import random
import logging
import time, threading
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server.async_io import StartTcpServer


upDown = [1,1,1,1,1,1]
# Simulate6 6 values to go up and down between 15 and 25,
# Indexes 2 and 5 are digitals switching between 1 and 0
# Values change every 60 seconds
def simulate_values():
    values = holding_registers.getValues(1,6)
    print(values)
    for idx, val in enumerate(values):
        #digital values
        if idx == 2 or idx == 5:
            if values[idx] == 1:
                values[idx] = 0
            else:
                values[idx] = 1
        #analogue values
        else:
            if upDown[idx] == 1:
                val += 1
                values[idx] = val
                if val == 25:
                    upDown[idx] = 0
            else:
                val -= 1
                values[idx] = val
                if val == 15:
                    upDown[idx] = 1
    holding_registers.setValues(1,values)
    print(values)
    threading.Timer(60, simulate_values).start()

# Enable logging (makes it easier to debug if something goes wrong)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Define the Modbus registers
coils = ModbusSequentialDataBlock(1, [False] * 100)
discrete_inputs = ModbusSequentialDataBlock(1, [False] * 100)
holding_registers = ModbusSequentialDataBlock(1, [0] * 100)
input_registers = ModbusSequentialDataBlock(1, [0] * 100)

integer_values = [random.randint(16, 24) for _ in range(6)]
integer_values[2] = 1
integer_values[5] = 0
holding_registers.setValues(1, integer_values)
print("integer_values:", integer_values)

# Define the Modbus slave context
slave_context = ModbusSlaveContext(
    di=discrete_inputs,
    co=coils,
    hr=holding_registers,
    ir=input_registers
)

# Define the Modbus server context
server_context = ModbusServerContext(slaves=slave_context, single=True)

# set random values
simulate_values()

# Start the Modbus TCP server
StartTcpServer(context=server_context, address=("192.168.1.110", 502))

import time
import BAC0
import time, threading
from BAC0.core.devices.local.models import (
    analog_input,
    analog_output,
    analog_value,
    binary_input,
    binary_output,
    binary_value,
    character_string,
    date_value,
    datetime_value,
    humidity_input,
    humidity_value,
    make_state_text,
    multistate_input,
    multistate_output,
    multistate_value,
    temperature_input,
    temperature_value,
)
from BAC0.core.devices.local.object import ObjectFactory

#bacnet = BAC0.connect(ip='192.168.1.110/24')
# or specify the IP you want to use / bacnet = BAC0.connect(ip='192.168.1.10/24')
# by default, it will attempt an internet connection and use the network adapter
# connected to the internet.
# Specifying the network mask will allow the usage of a local broadcast address
# like 192.168.1.255 instead of the global broadcast address 255.255.255.255
# which could be blocked in some cases.
# You can also use :
# bacnet = BAC0.lite() to force the script to load only minimum features.
# Please note that if Bokeh, Pandas or Flask are not installed, using connect()
# will in fact call the lite version.

#bacnet = BAC0.lite()

myValues = {"test_analogue_sensor": 1, "test_multistate_sensor": 1, "test_digital_sensor": 1, "test_analogue_setpoint": 1, "test_multistate_setpoint": 1, "test_digital_setpoint": 1}

def update_value(myObjectName):
    if myObjectName == "test_digital_setpoint" or myObjectName == "test_digital_sensor":
        if test_controller[myObjectName].presentValue == 1:
            test_controller[myObjectName].presentValue = 0
        else:
            test_controller[myObjectName].presentValue = 1
    else:
        if myValues[myObjectName] == 1:
            test_controller[myObjectName].presentValue += 1
            if test_controller[myObjectName].presentValue == 25:
                myValues[myObjectName] = 0
        else:
            test_controller[myObjectName].presentValue -= 1
            if test_controller[myObjectName].presentValue == 15:
                myValues[myObjectName] = 1
    print(str(myObjectName) + ": " + str(test_controller[myObjectName].presentValue))
    #threading.Timer(10, update_value(myObjectName)).start()

def add_points(device):
    # Start from fresh
    ObjectFactory.clear_objects()

    _new_objects = analog_input(
        name="test_analogue_sensor",
        properties={"units": "degreesCelsius"},
        description="Test Analogue Sensor",
        is_commandable=False,
        presentValue=17,
    )

    states = make_state_text(["Open", "Closed", "Ignored"])
    _new_objects = multistate_input(
        description="Test Multistate Sensor",
        properties={"stateText": states},
        name="test_multistate_sensor",
        is_commandable=False,
        presentValue=19,
    )

    _new_objects = binary_input(
        name="test_digital_sensor",
        properties={},
        description="Test Digital Sensor",
        presentValue=True,
    )

    _new_objects = analog_value(
        name="test_analogue_setpoint",
        properties={"units": "degreesCelsius"},
        description="Test Analogue Setpoint",
        is_commandable=True,
        presentValue=21,
    )

    states = make_state_text(["Open", "Closed", "Ignored"])
    _new_objects = multistate_value(
        description="Test Multistate Setpoint",
        properties={"stateText": states},
        name="test_multistate_setpoint",
        is_commandable=True,
        presentValue=23,
    )

    _new_objects = binary_value(
        name="test_digital_setpoint",
        properties={},
        description="Test Digital Setpoint",
        is_commandable=True,
        presentValue=False,
    )

    _new_objects.add_objects_to_application(device)


# Query and display the list of devices seen on the network
#bacnet.whois()
#print(bacnet.devices)

# Define a controller (this one is on MSTP #3, MAC addr 4, device ID 999)
#test_controller = BAC0.device('3:4', 5504, bacnet)
#test_controller = BAC0.device(port=47808, deviceId=999, bacnet)
test_controller = BAC0.lite(port=47808, deviceId=999)

print(dir(test_controller))

# Get the list of "registered" devices
#print(bacnet.registered_devices)

# Add points
add_points(test_controller)

ip = test_controller.localIPAddr.addrTuple[0]
boid = test_controller.Boid

print(ip, boid)

while True:
    time.sleep(60.00)
    update_value('test_analogue_sensor')
    update_value('test_multistate_sensor')
    update_value('test_digital_sensor')
    update_value('test_analogue_setpoint')
    update_value('test_multistate_setpoint')
    update_value('test_digital_setpoint')

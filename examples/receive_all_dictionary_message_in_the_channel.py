# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with CircuitPython.
# Receiving string from all address by setting BROADCAST ADDRESS
#
# Note: This code was written and tested using CircuitPython on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

import busio
import board

import time

from lora_e220 import LoRaE220, Configuration, BROADCAST_ADDRESS
from lora_e220_operation_constant import ResponseStatusCode

from lora_e220_constants import FixedTransmission, RssiEnableByte

# Create a UART object to communicate with the LoRa module with ESP32
uart2 = busio.UART(board.TX2, board.RX2, baudrate=9600)
# Create a LoRaE220 object, passing the UART object and pin configurations
lora = LoRaE220('400T22D', uart2, aux_pin=board.D15, m0_pin=board.D21, m1_pin=board.D19)

# Create a UART object to communicate with the LoRa module with Raspberry Pi Pico
# uart2 = busio.UART(board.TX1, board.RX1, baudrate=9600)
# Use the Serial1 pins of Arduino env on the Raspberry Pi Pico
# uart2 = busio.UART(board.D9, board.D8, baudrate=9600)
# lora = LoRaE220('433T20D', uart2, aux_pin=board.D2, m0_pin=board.D10, m1_pin=board.D11)
# STM32F411CEU6 Shield
# uart2 = busio.UART(board.TX2, board.RX2, baudrate=9600)
# lora = LoRaE220('400T22D', uart2, aux_pin=board.PA0, m0_pin=board.PB0, m1_pin=board.PB2)

code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration('400T22D')
# Comment this section if you want test transparent trasmission
configuration_to_set.ADDH = BROADCAST_ADDRESS # Address of this receive no sender
configuration_to_set.ADDL = BROADCAST_ADDRESS # Address of this receive no sender
configuration_to_set.CHAN = 23 # Address of this receive no sender
configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
# To enable RSSI, you must also enable RSSI on sender
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(configuration_to_set)
print("Set configuration: {}", ResponseStatusCode.get_description(code))

print("Waiting for messages...")
while True:
    if lora.available() > 0:
        # If the sender not set RSSI
        # code, value = lora.receive_dict()
        # If the sender set RSSI
        code, value, rssi = lora.receive_dict(rssi=True)
        print('RSSI: ', rssi)

        print(ResponseStatusCode.get_description(code))

        print(value)
        print(value['key1'])
        time.sleep(2)

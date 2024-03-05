import time
from .staticVariable.commlon_enum import *
from .staticVariable.controller_event_enum import *
from .staticVariable.ui_event_enum import * 
import logging
from typing import List
import serial

class Stage4Msg():
    """
    This class represent the Stage4 Messager, it only been use to communicate to the controller

    
    Stage4 message data structure:
    - Structure:         [did] [cmd]  [carry] [data] [end]                                         [read_byte]          
    - Size(byte):          1     1       1      4      1        x*2(x depend on the cmd and the number of bytes you expect the message to return)

    NOTE:
    end byte will alway be 0xC0

    NOTE:
    carry byte will be different depend on the data and cmd -> e.g address you want to read
    We only consider about the block read (cmd 0xB9) in this case
    carry will have three different value:
    - 0x00
    - 0x0A
    - 0x08
    Which depend on the address third bytes -> as address is make up with 4 bytes -> 0x018C -> 8 will be the third byte
    - If third byte in range of [0x0:0x7] -> then carry is 0x00 - case 1
    - elif third byte in range of [0x8:0xF] -> then carry is 0x0A - case 2
    - special case will be reading a range of memory and the starting address third byte in the case 1 and the ending address byte in the case 2 -> then carry is 0x08 - case 3
    
    NOTE:
    address data third byte will also changed - refer to this table
    ori val     : 0 1 2 3 4 5 6 7 8 9 A B C D E F
    changed val : 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7

    Example:
    Read address from 0x0171 to 0x0172
    then 
    Stage4 package will be 0x91 0xB9 0x00 0x01 0x71 0x01 0x72 0xC0 0xE0 0xE0 0xE0 0xE0

    Read address from 0x01F1 to 0x01F2
    then 
    Stage4 package will be 0x91 0xB9 0x0A 0x01 0x71 0x01 0x72 0xC0 0xE0 0xE0 0xE0 0xE0

    Read address from 0x017F to 0x0180
    then 
    Stage4 package will be 0x91 0xB9 0x08 0x01 0x7F 0x01 0x00 0xC0 0xE0 0xE0 0xE0 0xE0

    Detail documentation about stage4: 
    https://app.noteable.io/published/756f8436-4d4c-4e13-af74-363c91bcae65/Stage4_Message_Structure_and_Operations_v2

    To use this class an example:
    from commsHandler.stage4Msg import Stage4Msg
    stage4 = Stage4Msg("/dev/commlon0")
    stage4.clearAllEEPROM()

    """
    def __init__(self, usbPort="/dev/commlon1", baud=1200, destId=0x91):
        self._serialComms = serial.Serial(port=usbPort, baudrate=baud, timeout=0.1)
        self.logger = logging.getLogger(__class__.__name__)
        if not self._serialComms.isOpen():
            self._serialComms.open()
            self.logger.info(f'Opened serial commLonMsg')
    
    def _int_to_hex_string(self, int_val):
        return f'0x{int_val:04x}'

    def clearAllEEPROM(self):
        """
        This method will send clear all eeprom command to controller board through stage4 protocol
        FPSendMsg("0 0 false $91 $B7 $90 0 $9B $FF")
        """
        CLEAR_EEPROM_CMD: List[int] = [0x91, 0xB7, 0x0D, 0x10, 0x00, 0x1B, 0x7F, 0xC0]
        RETRY_COUNT: int = 10
        DELAY_BETWEEN_WRITE_AND_READ: float = 0.1
        success_flag = False  # Initialize a flag to track successful completion

        for retry in range(RETRY_COUNT):
            got_fail_byte = False
            for idx, byte in enumerate(CLEAR_EEPROM_CMD):
                self._serialComms.flushInput()
                self._serialComms.flushOutput()
                # Write and read
                self._serialComms.write(bytearray([byte]))
                time.sleep(DELAY_BETWEEN_WRITE_AND_READ)
                # Read two bytes
                read_back_bytes = self._serialComms.read(2)
                self.logger.info(f"\nSend {self._int_to_hex_string(byte)}, Need to received two bytes: [{self._int_to_hex_string(byte)},{self._int_to_hex_string(byte)}] \nThis is actual bytes we received [{' '.join([self._int_to_hex_string(b) for b in list(read_back_bytes)])}]")
                
                if [byte, byte] != list(read_back_bytes):
                    self.logger.warning(f'Clear EEPROM: Byte {idx}-{self._int_to_hex_string(byte)} not sent correctly. Retrying...')
                    got_fail_byte = True
            else:
                if not got_fail_byte:
                    self.logger.info(f'Successfully sent clear EEPROM command to controller')
                    success_flag = True  # Set the flag to True on successful completion
                    break  # Exit the loop
                
        # Check if the command was successfully sent, if not, raise an error
        if not success_flag:
            raise RuntimeError('Failed to send clear EEPROM command after maximum retries.')

    def close_stage4(self):
        self._serialComms.close()
        self.logger.info(f'Stage4 serial port closed')
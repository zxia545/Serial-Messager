from serial.serialutil import SerialException
from .singletonMeta import SingletonMeta
# from .commLonMsg import CommLonMsg
from .EnhancedCommLonMsg import CommLonMsg
from .staticVariable.commlon_enum import *
from .staticVariable.tempSensorCovert import *
from .staticVariable.controller_event_enum import *
from .staticVariable.ui_event_enum import *
import threading 
import time
import logging

# NOTE: This is a map from heater id to the commdef address which is related to heater_map dict in steps.py
heater_id_to_address_dict = {
    0: Integrated60CommDef.upper_compartment_heater,
    1: Integrated60CommDef.lower_compartment_heater,
    2: Integrated60CommDef.ice_maker_heater,
    3: Integrated60CommDef.upper_drain_heater,
    4: Integrated60CommDef.upper_throat_heater,
    5: Integrated60CommDef.middle_compartment_heater,
    6: Integrated60CommDef.lower_throat_heater,
    7: Integrated60CommDef.middle_throat_heater,
    8: Integrated60CommDef.defrost_heater,
    9: Integrated60CommDef.defrost_heater,
    10: Integrated60CommDef.defrost_heater
}

defrost_heater_mask_dict = {
    8: 0b00000001,
    9: 0b00000010,
    9: 0b00000100
}

# TODO: NEED TO UPDATE THIS DICT when add new personality
valve_manual_personality_covert_dict = {
    Personality60.TZ_FREEZER_60_PERSONALITY: {
        0 : 6,
        12: 5,
        24: 4,
        36: 7,
        48: 3,
    },
    Personality60.TZ_FRIDGE_60_PERSONALITY: {
        0 : 6,
        12: 3,
        24: 5,
        36: 7,
        48: 4,
    },
    Personality60.DZ_FRIDGE_60_PERSONALITY: {
        0 : 6,
        12: 4,
        24: 5,
        36: 7,
        48: 3,
    },
    Personality60.DZ_FREEZER_60_PERSONALITY: {
        0 : 6,
        12: 4,
        24: 5,
        36: 7,
        48: 3,
    },
    Personality60.DZ_B_MODEL_60_PERSONALITY: {
        0 : 6,
        12: 4,
        24: 5,
        36: 7,
        48: 3,
    },
    Personality60.B_MODEL_36_INCH_PERSONALITY: {
        0 : 6,
        12: 5,
        24: 4,
        36: 7,
        48: 3,
    },
    Personality60.WINE_60_UC_DZ_PERSONALITY: {
        0 : 6,
        12: 4,
        24: 5,
        36: 7,
        48: 3,
    },
    Personality60.BEV_60_UC_PERSONALITY: {
        0 : 6,
        12: 4,
        24: 5,
        36: 7,
        48: 3,
    }
}


valve_position_to_internal_position ={
    36: 0,
    12: 1,
    48: 3,
    24: 4,
    0: 6, 
}



class MockDisplay(CommLonMsg, metaclass=SingletonMeta):
    """
    This class contain the specific commlon cmd and msg we sent to controller and it works like a mock display
    It implemented the singleton design pattern such that will only have an instance of the class

    Args:
        CommLonMsg (_type_): CommLonMsg class that represent the commlon serial 
        metaclass (_type_, optional): Implementation of singleton design pattern. Defaults to SingletonMeta.
    """
    def __init__(self, usbPort="/dev/commlon0", baud=19200, destId=0x91):
        super().__init__(usbPort, baud, destId)
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info("MockDisplay be created")

    def validate_tx_event(self, txEvent, isControllerTxEvent, platform):
        if platform == "Integrated60":
            if isControllerTxEvent:
                packet_cmd = integrated60ControllerTxEventAckOrNotAckDict.get(txEvent)
            else:
                packet_cmd = integrated60UITxUEventAckOrNotAckDict.get(txEvent)
        elif platform == "column":
            if isControllerTxEvent:
                packet_cmd = ColumnControllerTxEventAckOrNotAckDict.get(txEvent)
            else:
                packet_cmd = ColumnUITxUEventAckOrNotAckDict.get(txEvent)

        if packet_cmd is None:
            self.logger.error(f'Provided TX Event: {txEvent} not supported')
            raise ValueError(f'Provided TX Event: {txEvent} not supported')
        return packet_cmd

    def send_packet_and_check_ack(self, packet_cmd, msg, txEvent, i, isControllerTxEvent, ignore_echo_block):
        return_value = self._send_packet(packet_cmd, msg, send_from_ctrl=isControllerTxEvent, ignore_echo_block=ignore_echo_block)
        if packet_cmd == CommLonCmds.Acked and return_value != [0]:
            self.logger.warning(f'Current TX event {txEvent} does not have a valid ACK value back, start retrying - {i}')
            return False
        
        self.logger.warning(f'Send and check ack work: {packet_cmd == CommLonCmds.Acked} ACK?  - return value {return_value}')
        return True

    def sentAndCheckTxEvent(self, maxRetry, txEvent, customizedMsg=None, isControllerTxEvent=False, platform="Integrated60", ignore_echo_block=False):
        """Schedules the sending of a display Tx event to the task queue and waits for completion."""
        event = threading.Event()
        task = lambda m_r, t_e, c_m, i_c_t, p, ignore: self._perform_sentAndCheckTxEvent(m_r, t_e, c_m, i_c_t, p, ignore)
        self.task_queue.put((task, event, (maxRetry, txEvent, customizedMsg, isControllerTxEvent, platform, ignore_echo_block)))
        event.wait()  # Wait for the task to complete
        
        if hasattr(task, 'exception'):
            raise task.exception
        return task.result

    def _perform_sentAndCheckTxEvent(self, maxRetry, txEvent, customizedMsg=None, isControllerTxEvent=False, platform="Integrated60", ignore_echo_block=False):
        """Executes the sending of a display Tx event and checks if it has been set."""
        
        # Validate the transaction event
        packet_cmd = self.validate_tx_event(txEvent, isControllerTxEvent, platform)
        
        # Prepare the message
        msg = customizedMsg if customizedMsg else self._TEventSuper(txEvent, sendFromCtrl=isControllerTxEvent, platform=platform)
        
        if platform == "Integrated60":
            event_name = Integrated60EventFromController(txEvent).name if isControllerTxEvent else Integrated60EventFromDisplay(txEvent).name
        elif platform == "column":
            event_name = ColumnEventFromController(txEvent).name if isControllerTxEvent else ColumnEventFromDisplay(txEvent).name
        
        for i in range(maxRetry):
            # Send packet and check acknowledgment
            if not self.send_packet_and_check_ack(packet_cmd, msg, txEvent, i, isControllerTxEvent, ignore_echo_block):
                time.sleep(0.5)
                continue
            
            self.logger.info(f'{"Controller" if isControllerTxEvent else "Display"} {event_name} has been set, Message set is {self._bytes_to_hex_string(msg)}')
            return True
        
        # If this point is reached, all retries have failed
        self.logger.error(f'Unable to set {"Controller" if isControllerTxEvent else "Display"} event: {event_name}')
        return False
        
        
    
    # =========== The methods below are used to read controller  =============
    def readFridgeState(self):
        return super().memRead(Integrated60CommDef.RAM_controlState)
    
    def readDefrostState(self):
        return super().memRead(Integrated60CommDef.RAM_defrost_state)
    
    def readFridgePersonality(self):
        """
        This methods used to read the fridge personality bytes

        Returns:
            int: personality byte in integer
        """
        return super().memRead(Integrated60CommDef.RAM_controllerPersonality)

    def readDispPersonality(self):
        return super().memRead(Integrated60CommDef.RAM_dispPersonality_RI60)
    
    def readIcemakerStatus(self):
        """This method is used to check if icemaker status

        Returns:
            bool: True if turn on and vice versa
        """
        # icemaker flag be save at address 0x000F -> right most bit
        return super().memRead(Integrated60CommDef.RAM_configGblCtrlFlag) & 0x01

    def readWaterDispenseLockStatus(self):
        """This method is used to check if dispense lock enable

        Returns:
            bool: True if turn on and vice versa
        """
        # water dispense lock save at address 0x000F -> number 4 bit count from the right
        return super().memRead(Integrated60CommDef.RAM_configGblCtrlFlag) & 0x08 == 0x08

    def readTempUnit(self):
        """This method is used to check temp unit

        Returns:
            str: string of tempeature Unit, "C" -> Celsius, "F" -> Fahrenheit 
        """
        # tempUnitBit is 0 mean temperature unit is C, F when it is 1
        tempUnitBit = super().memRead(Integrated60CommDef.RAM_configGblCtrlFlag) & 0x02 == 0x02
        self.logger.info(f'Current temp unit bit is {tempUnitBit}')
        return "F" if tempUnitBit else "C"
    
    def readCompartmentTempInK(self, compartmentNumber:int):
        temp_covert = {
            0: "Fridge",
            1: "Pantry",
            2: "Chill",
            3: "Freezer",
            4: "Soft Freezer",
            5: "Deep Freezer",
            7: "Invalid"
        }

        if compartmentNumber == 0:
            self.logger.warning(f'Upper mode: {super().memRead(0x01D4)} - {temp_covert[super().memRead(0x01D4)]}')
            return super().memRead(Integrated60CommDef.upper_temp, 2)
        elif compartmentNumber == 1:
            self.logger.warning(f'Lower mode: {super().memRead(0x01D5)} - {temp_covert[super().memRead(0x01D5)]}')
            return super().memRead(Integrated60CommDef.lower_temp, 2)
        elif compartmentNumber == 2:
            self.logger.warning(f'Middle mode: {super().memRead(0x02DD)} - {temp_covert[super().memRead(0x02DD)]}')
            return super().memRead(Integrated60CommDef.middle_temp, 2)
        else:
            self.logger.error(f'Compartement number {compartmentNumber} no valid')
            raise ValueError(f'Compartement number {compartmentNumber} no valid')
    
    def readIceTrayState(self):
        return super().memRead(Integrated60CommDef.RAM_iceTrayState)
    
    def readIceForceFlip(self)-> bool: 
        """
        This method is used to read the ice force flip bit 
        It is be saved at 5 bit from right to left -> 000x 0000

        Returns:
            bool: True if ice force flip be enable, and vice versa
        """
        return super().memRead(Integrated60CommDef.RAM_icemakerFlag3) & 0x10 == 0x10

    def readIcemakerHeaterEnable(self)-> bool:
        """
        This method is used to read the ice force flip bit 
        It is be saved at 2 bit from right to left -> 0000 00x0

        Returns:
            bool: True if ice force flip be enable, and vice versa
        """
        return super().memRead(Integrated60CommDef.RAM_icemakerFlag3) & 0x02 == 0x02

    def readTempSensorInKelvin(self, sensorId: int)-> float:
        """This method is used to read the real temp sensor value as Kelvin

        Args:
            sensorId (int): id of temp sensor from 0 - 7, more detail please check tempSensorCovert.py

        Returns:
            float: _description_
        """
        if sensorId > 7 or sensorId < 0:
            raise ValueError(f'Temp Sensor id is not valid -> please reference to tempSensorCovert.py')
        return super().memRead(temp_sensor_id_to_ram_address_dict[sensorId],2)/32
        


    def readTempSensorInCelsius(self, sensorId: int)-> float:
        tempInK = self.readTempSensorInKelvin(sensorId)
        return tempInK - 273


    def readTempSensorInFahrenheit(self, sensorId: int)-> float:
        tempInC = self.readTempSensorInCelsius(sensorId)
        return (tempInC * 9/5) + 32
    
    def readShabbathStatus(self):
        # Shabbath mode status bit is save in Commdef address 0x0002 -> 5 bit(In total 8 bits) -> 0b000x 0000 -> please refer to controller repo
        return ((self.memRead(Integrated60CommDef.RAM_ctrlCnfgFlag) & 0x10) == 0x10)

    def read_heater_pwm(self, heater_id):
        heater_ram_address = heater_id_to_address_dict[heater_id]
        # use defrost heater method to read defrost heater
        if heater_ram_address == Integrated60CommDef.defrost_heater:
            return self.read_defrost_heater(heater_id)
        return self.memRead(heater_ram_address)
    
    def read_defrost_heater(self, heater_id):
        defrost_heater_byte = self.memRead(Integrated60CommDef.defrost_heater)
        defrost_heater_mask = defrost_heater_mask_dict[heater_id]
        return (defrost_heater_byte & defrost_heater_mask) == defrost_heater_mask
    
    def read_icemaker_heater_enable_flag(self):
        return (super().memRead(Integrated60CommDef.RAM_icemakerFlag3) & 0b00000010) ==  0b00000010

    def read_controller_software_version(self):
        major_id = super().memRead(0x0063)
        minor_id = super().memRead(0x0064)
        development_id = super().memRead(0x0065)
        return [major_id, minor_id, development_id]

    def read_ui_software_version(self):
        major_id = super().memRead(0x0013, readController=False)
        minor_id = super().memRead(0x0014, readController=False)
        development_id = super().memRead(0x0015, readController=False)
        return [major_id, minor_id, development_id]

    def read_controller_crc(self):
        return super().memRead(Integrated60CommDef.Controller_Crc, 2)
    
    def read_ui_crc(self):
        return super().memRead(0x0010, 2, False)
    
    def read_eeprom_software_version(self):
        current_controller_software_version = self.read_controller_software_version()
        # The threshold version for determining EEPROM compatibility
        self.logger.info(f"Current controller software version is {[f'{int_val:02x}' for int_val in current_controller_software_version]}")
        eeprom_software_version_threshold = Integrated60EEPROM.eeprom_software_version_threhold.value
        # Compare the current software version with the threshold
        if current_controller_software_version >= eeprom_software_version_threshold:
            return 'v2'
        else:
            return 'v1'

    # =========== The methods below are used to set controller  =============
    def clearAllEEPROM(self):
        super().clearEEPROMBlock_v2([0x9000, 0x9BFF])

    def setIcemakerHeaterEnableFlag(self, isReset:bool=False):
        super().setResMemBit(Integrated60CommDef.RAM_icemakerFlag3, 1, isReset)
    
    def setIcemakerHeaterTimerExpired(self):
        super().setResMemBit(Integrated60CommDef.RAM_icemakerFlag3, 0)

    def setManualStateOff(self):
        super().setResMemBit(Integrated60CommDef.RAM_controlFlag0, 1, True)
        if self.readFridgeState() == FridgeState60.MANUAL_MODE:
            self.logger.error(f'Fridge State is in MANUAL_MODE state')
            raise SerialException(f'Fridge State is in MANUAL_MODE state')
        else:
            self.logger.info(f"Fridge State is set to Normal")

    def setManualState(self):
        super().setResMemBit(Integrated60CommDef.RAM_controlFlag0, 1)
        if self.readFridgeState() != FridgeState60.MANUAL_MODE:
            self.logger.error(f'Fridge State is not in Manual state')
            raise SerialException(f'Fridge State is not in Manual state')
        else:
            self.logger.info("Fridge State is set to Manual State")

    def setDefrostState(self):
        super().setResMemBit(Integrated60CommDef.RAM_ctrlCnfgFlag, 0)
        if self.readFridgeState() != FridgeState60.DEFROST_STATE:
            self.logger.error(f'Fridge State is not in Defrost State')
            raise SerialException(f'Fridge State is not in Defrost State')
        else:
            self.logger.info("Fridge State is set to Defrost State")
    
    def setFridgeCtrlAndDispPersonality(self, personality: int, ui_personality: int, software_version='v1'):
        """
        This method is used to set fridge (controller and display) personality

        Args:
            personality (int): personality want to set
        """
        self.logger.info(f'Current software version for eeprom is {software_version}')
        eeprom_key = f"EEPROM_personality_{software_version}"
        # clear EEPROM
        super().clearEEPROMBlock(Integrated60EEPROM[eeprom_key].value)
        # set controller personality
        self.setControllerPersonality(personality)
        # set controller to manual mode
        self.setManualState()
        time.sleep(0.5)
        # set display personality
        self.setDisplayPersonality(personality, ui_personality)
    
    def setControllerPersonality(self, personality: int, software_version='v1'):
        """This method is to set controller personality

        Args:
            personality (int): personality want to set
        """
        # set controller personality
        eeprom_key = f"EEPROM_personality_{software_version}"
        super().blockWrite(Integrated60EEPROM[eeprom_key].value, [personality, 255 - personality])
        super().memWrite(Integrated60CommDef.RAM_controllerPersonality, personality)
        self.logger.info(f'Controller personality have change to {personality}')
    
    def attempt_to_set_display_personality(self, personality: int, ui_personality: int) -> bool:
        """Attempt to set the display personality.

        Args:
            personality (int): The personality to set.

        """
        super().memWrite(Integrated60CommDef.RAM_dispPersonality_RI60, personality)
        # wait for 0.5 second to wait for commlon traffic
        time.sleep(0.5)
        # directly send the TX event to display
        self.set_display_personality_tx_event(personality)
        # wait for 0.5 second to wait for commlon traffic
        time.sleep(0.5)
        # Write to the display commdef - where personality byte at 0x0012
        self.logger.info(f'Writing ui personality to UI commdef')
        super().memWrite(0x0012, ui_personality, 1, False)

    def setDisplayPersonality(self, personality: int, ui_personality: int, maxRetry: int = 3):
        """Set the display personality, ensuring the fridge is in manual mode beforehand.

        Args:
            personality (int): The personality to set.
            maxRetry (int, optional): Maximum number of retries. Defaults to 3.
        """
        for retry in range(maxRetry):
            currentState = self.readFridgeState()
            
            if currentState != FridgeState60.MANUAL_MODE:
                self.logger.warning(f'Try {retry + 1} failed. Fridge is not in manual mode. Retrying...')
                self.setManualState()
                time.sleep(0.5)
                continue
            self.attempt_to_set_display_personality(personality, ui_personality)

            # if personality is column then we need to write the width as well
            # default to be 24 inch
            if personality < Personality60.DZ_FRIDGE_60_PERSONALITY:
                self.set_column_product_width(width=1)
            return

        self.logger.error(f'Unable to set display personality after {maxRetry} tries.')
        raise RuntimeError(f'Fridge state is not in manual mode and current state is {FridgeState60(currentState).name}, unable to change display personality')

    def set_display_personality_tx_event(self, personality: int, maxRetry: int=3):
        eventToSent = Integrated60EventFromController.EVT_DISP_PERSONALITY_WRITE
        msgToSent = self._TEventSuper(Integrated60EventFromController.EVT_DISP_PERSONALITY_WRITE, sendFromCtrl=True) + bytearray([personality])

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, customizedMsg=msgToSent, isControllerTxEvent=True)
    
    def set_column_product_width(self, width: int=1, maxRetry: int=3):
        eventToSent = Integrated60EventFromController.EVT_DISP_WIDTH_WRITE
        msgToSent = self._TEventSuper(Integrated60EventFromController.EVT_DISP_WIDTH_WRITE, sendFromCtrl=True) + bytearray([width])

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, customizedMsg=msgToSent, isControllerTxEvent=True)
    

    def setShabbath(self, isTurnOn:bool, maxRetry=3):
        """This method used to set shabbath mode on or off

        Args:
            isTurnOn (bool): If Ture mean turn on shabbath mode and vice versa
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_SABBATH_MODE_ON if isTurnOn else Integrated60EventFromDisplay.EVT_SIG_SABBATH_MODE_OFF

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)

    def setColumnShabbath(self, isTurnOn:bool, maxRetry=3):
        """This method used to set shabbath mode on or off

        Args:
            isTurnOn (bool): If Ture mean turn on shabbath mode and vice versa
        """
        eventToSent = ColumnEventFromDisplay.EVT_SHABBATH_MODE_ON if isTurnOn else ColumnEventFromDisplay.EVT_SHABBATH_MODE_OFF

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, platform="column")


    def setShowroomMode(self, isTurnOn:bool, maxRetry=3):
        """This method used to set showroom mode on or off

        Args:
            isTurnOn (bool): If Ture mean turn on showroom mode and vice versa
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_SHOWROOM_MODE_ON if isTurnOn else Integrated60EventFromDisplay.EVT_SIG_SHOWROOM_MODE_OFF

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)

    def setColumnShowroomMode(self, isTurnOn:bool, maxRetry=3):
        """This method used to set showroom mode on or off

        Args:
            isTurnOn (bool): If Ture mean turn on showroom mode and vice versa
        """
        eventToSent = ColumnEventFromDisplay.EVT_SHOWROOM_MODE_ON if isTurnOn else ColumnEventFromDisplay.EVT_SHOWROOM_MODE_OFF

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, platform="column")
    
    def setDoorAlarm(self, isMute:bool, maxRetry=3):
        """This method used to set door alarm

        Args:
            isMute (bool): If True mean mute door alarm and vice versa
            maxRetry (int, optional): _description_. Defaults to 3.
        """
        """
        NOTE: This is the covertion dict for door state
        doors_state_dict = {
            0: "DOORS_AO_INITIAL",
            1: "DOORS_AO_DOOR",
            2: "DOORS_AO_STARTUP",
            3: "DOORS_AO_CLOSED",
            4: "DOORS_AO_OPEN",
            5: "DOORS_AO_MANUAL",
            6: "DOORS_AO_DOOR_ALARM_ACTIVE",    
            7: "DOORS_AO_DOOR_ALARM_MUTE",
            8: "DOORS_AO_NO_OF_STATES"
        }
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_DOOR_ALARM_MUTE if isMute else Integrated60EventFromDisplay.EVT_SIG_DOOR_ALARM_UNMUTE
        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)

    def setColumnDoorAlarm(self, isMute:bool, maxRetry=3):
        """This method used to set door alarm

        Args:
            isMute (bool): If True mean mute door alarm and vice versa
            maxRetry (int, optional): _description_. Defaults to 3.
        """
        eventToSent = ColumnEventFromDisplay.EVT_DOOR_ALARM_MUTE if isMute else ColumnEventFromDisplay.EVT_DOOR_ALARM_UNMUTE
        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, platform="column")

    def setDisplaySound(self, isTurnOn: bool, maxRetry=3):
        """This method used to set display sound mute or unmute

        Args:
            isTurnOn (bool): If True mean enable display sound (unmute) and vice versa
            maxRetry (int, optional): _description_. Defaults to 3.
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_DISP_KEY_AUDIO_UNMUTE if isTurnOn else Integrated60EventFromDisplay.EVT_SIG_DISP_KEY_AUDIO_MUTE

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)
    
    def setDisplayLock(self, isTurnOn: bool, maxRetry=3):
        """This method used to set display lock or unlock
        NOTE: This method design for real display connect to controller -> 
                Such that we sent EVT_SIG_CTRL_KEYLOCK from control to disp and let disp response to it
                In this way, the real display will show display be locked

        Args:
            isTurnOn (bool): If True mean enable display key lock and vice verse 
            maxRetry (int, optional): _description_. Defaults to 3.
        """
        eventToSent = Integrated60EventFromController.EVT_CTRL_KEYLOCK
        msgToSent = self._TEventSuper(Integrated60EventFromDisplay.EVT_CTRL_KEYLOCK, sendFromCtrl=True) + bytearray([0x01]) if isTurnOn else self._TEventSuper(Integrated60EventFromDisplay.EVT_CTRL_KEYLOCK, sendFromCtrl=True) + bytearray([0x00])
        
        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, customizedMsg=msgToSent, sendFromCtrl=True)

    def playShortBeep(self, maxRetry=3):
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_DISP_PLAY_BEEP         

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)

    def playRaspBeep(self, maxRetry=3):
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_DISP_PLAY_RASP         

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)


    # Note column and integated have the same EVT number for icemaker so can just use it
    def setIcemaker(self, isTurnOn: bool, maxRetry=3):
        """
        Sets the icemaker to either on or off.

        Args:
            isTurnOn (bool): If True, turns on the icemaker. If False, turns it off.
            maxRetry (int, optional): The maximum number of attempts to send the event. Defaults to 3.

        Notes:
            - The icemaker message includes the compartment (2 bits) and enable (1 bit), represented by TFreezerConfig:
                - To enable the icemaker, set the compartment to Lower_cmpt (1) and the enable bit to 1: 0b0000 0101 -> 0x05.
                - To disable the icemaker, set the compartment to Lower_cmpt (1) and the enable bit to 0: 0b0000 0001 -> 0x01.

        Returns:
            None
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_ICE_ON
        msgToSent = self._TEventSuper(Integrated60EventFromDisplay.EVT_SIG_ICE_ON) + bytearray([0b00000101]) if isTurnOn else self._TEventSuper(Integrated60EventFromDisplay.EVT_SIG_ICE_ON) + bytearray([0b00000001])
        
        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, customizedMsg=msgToSent)
        
    def setWaterDispenseLock(self, isTurnOn: bool, maxRetry=3):
        """This method is used to set water dispenser lock

        Args:
            isTurnOn (bool): If Ture mean turn on water dispenser lock and vice versa
            maxRetry (int, optional): _description_. Defaults to 3.
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_DISP_WATER_DISPENSE_LOCK if isTurnOn else Integrated60EventFromDisplay.EVT_SIG_DISP_WATER_DISPENSE_UNLOCK

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)

        
    def setForceIceFlip(self, maxRetry=3):
        """
        Sets the force ice flip and sends an event to the display.

        Args:
            maxRetry (int, optional): The maximum number of attempts to send the event. Defaults to 3.

        Notes:
            - If the mock display has just been created, you must wait at least 0.5 seconds for the function to work properly.

        Returns:
            None
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_FORCE_ICE_FLIP

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)



    def setTempUnit(self, tempUnit:str, maxRetry=3):
        """This method used to set temp unit

        Args:
            tempUnit (str): only allow "C" or "F"

        Raises:
            ValueError: When target temp unit niether "C" nor "F"
        """
        # check tempUnit want to set
        if tempUnit not in ("C", "F"):
            self.logger.error(f'Given temp unit {tempUnit} is invalid')
            raise ValueError(f'Given temp unit is invalid')
        # check current tempUnit, only change temperature unit when target unit and current unit does no match
        if self.readTempUnit() != tempUnit:
            eventToSent = Integrated60EventFromDisplay.EVT_SIG_DISP_CHANGE_TEMP_UNITS
            self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent)

    # Note column used the same EVT number for update setpoint
    def setCompartmentTemp(self, compartmentNumber:int, temp:int, maxRetry=3):
        """This method will set temp with the given compartment number

        Args:
            compartmentNumber (int): For dz should be in 0-1 (UPR_CMPT is 0, LWR_CMPT is 1), For tz should be in 0-2 (UPR_CMPT is 0, LWR_CMPT is 1, MID_CMPT is 2)
            temp (int): temp in controller K format

        Raises:
            ValueError: provided compartment number not valid
        """
        if compartmentNumber < 0 or compartmentNumber > 3:
            self.logger.error(f'Compartment Number {compartmentNumber} is not valid')
            raise ValueError(f'Compartment Number {compartmentNumber} is not valid')

        eventToSent = Integrated60EventFromDisplay.EVT_SIG_UPDATE_SETPOINT
        tempMsb = (temp >> 8) & 0xFF
        tempLsb = temp & 0xFF
        msgToSent = self._TEventSuper(Integrated60EventFromDisplay.EVT_SIG_UPDATE_SETPOINT) + bytearray([compartmentNumber, tempLsb, tempMsb])

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, customizedMsg=msgToSent)
    
    def setCompartmentTempMemWrite(self, compartmentNumber, temp):
        tempMsb = (temp >> 8) & 0xFF
        tempLsb = temp & 0xFF
        temp_to_compartmentNumber_dict = {
            0: Integrated60CommDef.upper_temp, 
            1: Integrated60CommDef.lower_temp, 
            2: Integrated60CommDef.middle_temp,
        }
        for i in range(3):
            self.memWrite(temp_to_compartmentNumber_dict[compartmentNumber], tempMsb)
            self.memWrite(temp_to_compartmentNumber_dict[compartmentNumber] + 1, tempLsb)
            time.sleep(1)

            ramTempMsb = self.memRead(temp_to_compartmentNumber_dict[compartmentNumber])
            ramTempLsb = self.memRead(temp_to_compartmentNumber_dict[compartmentNumber] + 1)

            if ramTempMsb == tempMsb and ramTempLsb == tempLsb:
                break
            else:
                self.logger.error(f'Retry setting compartment temperature - {i}')
    
    def setInternalUIHumidityWithTemperature(self, humidity, ambient_temp_count):
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_HSUI_UPDATE
        msgToSent = self._TEventSuper(Integrated60EventFromDisplay.EVT_SIG_HSUI_UPDATE) + bytearray([ambient_temp_count, humidity])
        self.sentAndCheckTxEvent(maxRetry=3, txEvent=eventToSent, customizedMsg=msgToSent, isControllerTxEvent=False)
    

    def setExternalUIHumidityWithTemperature(self, humidity, ambient_temp_count):
        data = [ambient_temp_count, humidity, 0, 1]
        super().blockWrite([0x01C0, 0x01C3], data)
        self.logger.info(f'Set external ui humidity: {data}')

    def setRegionUItoController(self, region):
        def checkRegionByte():
            return self.memRead(Integrated60CommDef.REGION_BYTE) == region
        
        if region not in Region60:
            self.logger.error(f'Given region: {region} not support')
            raise ValueError(f'Given region: {region} not support')
        
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_DISP_SET_REGION
        msgToSent = self._TEventSuper(Integrated60EventFromDisplay.EVT_SIG_DISP_SET_REGION) + bytearray([region])
        self.sentAndCheckTxEvent(maxRetry=3, txEvent=eventToSent, customizedMsg=msgToSent, isControllerTxEvent=False)
    
    def setFoodModel(self, compartmentNumber:int, foodmode: int):
        food_mode_covert = {
            0: "Fridge",                  # DEFAULT_PC_MODE
            1: "Pantry",                  # PANTRY_MODE
            2: "Chill",                   # CHILL_MODE
            3: "Freezer",                 # DEFAULT_FC_MODE
            4: "Soft Freezer",            # SOFT_FREEZE_MODE
            5: "Deep Freezer",            # DEEP_FREEZE_MODE
            6: "Cellar Wine",             # DEFAULT_CELLAR_WINE_MODE
            7: "Red Wine",                # RED_WINE_MODE
            8: "White Wine",              # WHITE_WINE_MODE
            9: "Sparkling Wine",          # SPARK_WINE_MODE
            10: "Beverage",               # BEVERAGE_MODE
            11: "Max Number of Modes",    # MAX_NUM_MODES
            12: "Invalid"                 # INVALID_MODE
        }

        if compartmentNumber == 0:
            self.logger.warning(f'Previous set Upper mode: {super().memRead(0x01D4)} - {food_mode_covert[super().memRead(0x01D4)]}')
            super().memWrite(0x01D4, foodmode)
            self.logger.warning(f'After set Upper mode: {super().memRead(0x01D4)} - {food_mode_covert[super().memRead(0x01D4)]}')
        elif compartmentNumber == 1:
            self.logger.warning(f'Previous set Lower mode: {super().memRead(0x01D5)} - {food_mode_covert[super().memRead(0x01D5)]}')
            super().memWrite(0x01D5, foodmode)
            self.logger.warning(f'After set Lower mode: {super().memRead(0x01D5)} - {food_mode_covert[super().memRead(0x01D5)]}')
        elif compartmentNumber == 2:
            self.logger.warning(f'Previous set Middle mode: {super().memRead(0x02DD)} - {food_mode_covert[super().memRead(0x02DD)]}')
            super().memWrite(0x02DD, foodmode)
            self.logger.warning(f'After set Middle mode: {super().memRead(0x02DD)} - {food_mode_covert[super().memRead(0x02DD)]}')


    def setControllerRegion(self, region):
        if region not in Region60:
            self.logger.error(f'Given region: {region} not support')
            raise ValueError(f'Given region: {region} not support')
        self.memWrite(Integrated60CommDef.REGION_BYTE, region)
        self.logger.info(f'Controller region have set to {Region60(region).name}')
    
    def setWaterFilterExpire(self):
        self.memWrite(0x0074, 0x50, 1, False)

        
    def setDefrostMaxDuration(self, duration:int):
        """
        This method will write the max duration of deforst
        NOTE: Even you set it to duration to 1 min it will still take around 6-7 minutes to exit defrost
        Args:
            duration (int): _description_
        """
        self.memWrite(Integrated60CommDef.DEFROST_MAX_DURATION, duration)
    
    def setIceWaterSolenoid_Maunal(self, isTurnOn):
        if isTurnOn:
            self.setResMemBytes(0x01D6, 0x30)
            self.setResMemBytes(0x01D7,0x30)
        else:
            self.setResMemBytes(0x01D6, 0xDF, True)
            self.setResMemBytes(0x01D7,0x20)

    def setACWaterSolenoid_Manual(self, isTurnOn):
        if isTurnOn:
            self.setResMemBytes(0x0119, 0x80)
            self.setResMemBytes(0x011A,0x80)
        else:
            self.setResMemBytes(0x0119, 0x80)
            self.setResMemBytes(0x011A, 0x7F, True)

    def setStepperValvePosition(self, pos_num:int):
        personality = self.readFridgePersonality()
        if personality not in valve_manual_personality_covert_dict:
            self.logger.error(f'Personality: {personality} no support')
            raise ValueError(f'Personality: {personality} no support')
        
        pos_covert_dict = valve_manual_personality_covert_dict[personality]
        
        if pos_num not in pos_covert_dict:
            self.logger.error(f'Position Number {pos_num} not supported')
            raise ValueError(f'Position Number {pos_num} not supported')
        self.memWrite(Integrated60CommDef.Stepper_Valve_Control, pos_covert_dict.get(pos_num))

    def getStepperValvePosition(self):   
        pos_num = self.memRead(0x0072)
        if pos_num not in valve_position_to_internal_position:
            # sleep for 5 seconds as it may moving
            time.sleep(5)
            pos_num = self.memRead(0x0072)
            if pos_num not in valve_position_to_internal_position:
                self.logger.error(f'Position Number {pos_num} not supported')
                raise ValueError(f'Position Number {pos_num} not supported')
        return valve_position_to_internal_position.get(pos_num)

    def setIcemakerPowerBoost(self, isTurnOn: bool):
        isReset = not isTurnOn
        self.setResMemBit(Integrated60CommDef.ICEMAKER_AO_FLAGS_BY2,0,isReset)


    def setColumnIcemakerPowerBoost(self, isTurnOn: bool):
        isReset = not isTurnOn
        self.setResMemBit(ColumnCommDef.ICEMAKER_AO_FLAGS_BY2,1,isReset)


    def setColumnDisplaySound(self, isTurnOn: bool, maxRetry=3):
        """This method used to set display sound mute or unmute

        Args:
            isTurnOn (bool): If True mean enable display sound (unmute) and vice versa
            maxRetry (int, optional): _description_. Defaults to 3.
        """
        eventToSent = ColumnEventFromDisplay.EVT_DISP_KEY_AUDIO_UNMUTE if isTurnOn else ColumnEventFromDisplay.EVT_DISP_KEY_AUDIO_MUTE

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, platform="column")

    def setColumnWaterDispenseLock(self, isTurnOn: bool, maxRetry=3):
        """This method is used to set water dispenser lock

        Args:
            isTurnOn (bool): If Ture mean turn on water dispenser lock and vice versa
            maxRetry (int, optional): _description_. Defaults to 3.
        """
        eventToSent = ColumnEventFromDisplay.EVT_DISP_WATER_DISPENSE_LOCK if isTurnOn else ColumnEventFromDisplay.EVT_DISP_WATER_DISPENSE_UNLOCK

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, platform="column")


    def setColumnForceIceFlip(self, maxRetry=3):
        """
        Sets the force ice flip and sends an event to the display.

        Args:
            maxRetry (int, optional): The maximum number of attempts to send the event. Defaults to 3.

        Notes:
            - If the mock display has just been created, you must wait at least 0.5 seconds for the function to work properly.

        Returns:
            None
        """
        eventToSent = ColumnEventFromDisplay.EVT_FORCE_ICE_FLIP

        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, platform="column")

    def setColumnIcemaker(self, isTurnOn: bool, maxRetry=3):
        """
        Sets the icemaker to either on or off.

        Args:
            isTurnOn (bool): If True, turns on the icemaker. If False, turns it off.
            maxRetry (int, optional): The maximum number of attempts to send the event. Defaults to 3.

        Notes:
            - The icemaker message includes the compartment (2 bits) and enable (1 bit), represented by TFreezerConfig:
                - To enable the icemaker, set the compartment to Lower_cmpt (1) and the enable bit to 1: 0b0000 0101 -> 0x05.
                - To disable the icemaker, set the compartment to Lower_cmpt (1) and the enable bit to 0: 0b0000 0001 -> 0x01.

        Returns:
            None
        """
        eventToSent = ColumnEventFromDisplay.EVT_ICE_ON
        msgToSent = self._TEventSuper(ColumnEventFromDisplay.EVT_ICE_ON, platform="column") + bytearray([0b00000101]) if isTurnOn else self._TEventSuper(ColumnEventFromDisplay.EVT_ICE_ON, platform="column") + bytearray([0b00000001])
        
        self.sentAndCheckTxEvent(maxRetry=maxRetry, txEvent=eventToSent, customizedMsg=msgToSent, platform="column")


    def setColumnFoodModel(self, compartmentNumber:int, foodmode: int):
        temp_covert = {
            0: "Fridge",
            1: "Pantry",
            2: "Chill",
            3: "Freezer",
            4: "Soft Freezer",
            5: "Deep Freezer",
            7: "Invalid"
        }

        if compartmentNumber == 0:
            self.logger.warning(f'Previous set Upper mode: {super().memRead(0x01D4)} - {temp_covert[super().memRead(0x01D4)]}')
            super().memWrite(0x01D4, foodmode)
            self.logger.warning(f'After set Upper mode: {super().memRead(0x01D4)} - {temp_covert[super().memRead(0x01D4)]}')
        elif compartmentNumber == 1:
            self.logger.warning(f'Previous set Lower mode: {super().memRead(0x01D5)} - {temp_covert[super().memRead(0x01D5)]}')
            super().memWrite(0x01D5, foodmode)
            self.logger.warning(f'After set Lower mode: {super().memRead(0x01D4)} - {temp_covert[super().memRead(0x01D4)]}')
    
    def setFaceliftStepperValvePosition(self, position:int):
        """
        Position map:
        SMVC_AUTO = 0,
        SMVC_MANUAL_HOME_POS_RQ=1,
        SMVC_MANUAL_B_CLOSE_C_CLOSE_RQ=2,
        SMVC_MANUAL_B_CLOSE_C_OPEN_RQ=3,
        SMVC_MANUAL_B_OPEN_C_OPEN_RQ=4,
        SMVC_MANUAL_B_OPEN_C_CLOSE_RQ=5,
        SMVC_MANUAL_HOME_POS_INIT_RQ=6,
        SMVC_MANUAL_WAIT_IN_POS=7,
        SMVC_MANUAL_HOME_POS_IN_POS=8,
        SMVC_MANUAL_B_CLOSE_C_CLOSE_IN_POS=9,
        SMVC_MANUAL_B_CLOSE_C_OPEN_IN_POS=10,
        SMVC_MANUAL_B_OPEN_C_OPEN_IN_POS=11,
        SMVC_MANUAL_B_OPEN_C_CLOSE_IN_POS=12,

        Actual position map: 
        SMVC_MANUAL_HOME_POS_RQ=1 -> current, request, target = 216, 0, 216
        SMVC_MANUAL_B_CLOSE_C_CLOSE_RQ=2 -> current, request, target = x, 34, x
        SMVC_MANUAL_B_CLOSE_C_OPEN_RQ=3 -> current, request, target = x, 100, x
        SMVC_MANUAL_B_OPEN_C_OPEN_RQ=4 -> current, request, target = x, 154, x
        SMVC_MANUAL_B_OPEN_C_CLOSE_RQ=5 -> current, request, target = x, 195, x
        SMVC_MANUAL_HOME_POS_INIT_RQ=6 -> current, request, target = 216, 0, 216
        """
        if position < 7 and position > 0:
            self.memWrite(0x0070, position)
            # eventToSent = Integrated60EventFromDisplay.EVT_SIG_MANUAL_VALVE_CTRL
            # msgToSent = self._TEventSuper(Integrated60EventFromDisplay.EVT_SIG_MANUAL_VALVE_CTRL) + bytearray([position])
            
            # self.sentAndCheckTxEvent(maxRetry=3, txEvent=eventToSent, customizedMsg=msgToSent)

    def setColumnStepperValvePosition(self, position:int):
        """
        Position map:
            VALVE_AUTO = 0,
            VALVE_HOME, 1
            VALVE_B_CLOSE_C_CLOSE, 2
            VALVE_B_CLOSE_C_OPEN, 3
            VALVE_B_OPEN_C_OPEN, 4
            VALVE_B_OPEN_C_CLOSE, 5
            VALVE_HOME_POS_INIT, 6 
            MAX_VALVE_CMD,

        Actual position map: 

            /* SMVC_B_CLOSE_C_CLOSE_POS */  0, SMVC_B_CLOSE_C_CLOSE_POS_VAL, -> 34
            /* SMVC_B_CLOSE_C_OPEN_POS */   1, SMVC_B_CLOSE_C_OPEN_POS_VAL, -> 100
            /* SMVC_B_OPEN_C_OPEN_POS */    2, SMVC_B_OPEN_C_OPEN_POS_VAL, -> 154
            /* SMVC_B_OPEN_C_CLOSE_POS */   3, SMVC_B_OPEN_C_CLOSE_POS_VAL, -> 195
            /* SMVC_LAST_POS */             4, SMVC_VALVE_POS_INVALID -> 255
        """   
        if position < 8 and position > -1:
            eventToSent = ColumnEventFromDisplay.EVT_MANUAL_VALVE_CTRL
            msgToSent = self._TEventSuper(ColumnEventFromDisplay.EVT_MANUAL_VALVE_CTRL, platform="column") + bytearray([position])
            
            self.sentAndCheckTxEvent(maxRetry=3, txEvent=eventToSent, customizedMsg=msgToSent, platform="column")
                
    def setFactoryReset(self):
        """
        This method will simulate the TX factory reset event that UI send to controller
        """
        eventToSent = Integrated60EventFromDisplay.EVT_SIG_FACTORY_RST

        self.sentAndCheckTxEvent(maxRetry=3, txEvent=eventToSent, platform="Integrated60")



    #------------------------------------------------------------------------Manual Control Screen----------------------------------------------------------------
    def setFakeButtonClick(self, button:int):
        eventToSent = Integrated60EventFromController.EVT_SIG_VIEW_KEY_INPUT
        msgToSent = self._TEventSuper(Integrated60EventFromController.EVT_SIG_VIEW_KEY_INPUT) + bytearray([button])
        self.sentAndCheckTxEvent(maxRetry=3, txEvent=eventToSent, customizedMsg=msgToSent, isControllerTxEvent=True, ignore_echo_block=True)
    
    def setMenuShortClick(self):
        self.setFakeButtonClick(0)
        time.sleep(0.5)
    
    def setUpShortClick(self):
        self.setFakeButtonClick(1)
        time.sleep(0.5)

    def setDownShortClick(self):
        self.setFakeButtonClick(2)
        time.sleep(0.5)

    def setReturnShortClick(self):
        self.setFakeButtonClick(3)
        time.sleep(0.5)

    def setSelectShortClick(self):
        self.setFakeButtonClick(4)
        time.sleep(0.5)
    
    def setMenuLongClick(self):
        self.setFakeButtonClick(6)
        time.sleep(0.5)

    def setDiagModeClick(self):
        self.setFakeButtonClick(12)
        time.sleep(0.5)
    
    def setShowRoomClick(self):
        self.setFakeButtonClick(13)
        time.sleep(0.5)
    
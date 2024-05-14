from enum import IntEnum, Enum

# ============ COMMON Constants ===================
class State(IntEnum):
    OFF = 0
    ON = 1


class Cmpt(IntEnum):
    UPPER = 0
    LOWER = 1

class Personality60(IntEnum):
    INVALID_PERSONALITY_1 = 0
    COLUMN_FRIDGE_PERSONALITY = 1
    COLUMN_FREEZER_PERSONALITY = 2
    COLUMN_B_MODEL_PERSONALITY = 3
    COLUMN_WINE_PERSONALITY = 4
    DZ_FRIDGE_60_PERSONALITY = 5
    DZ_FREEZER_60_PERSONALITY = 6
    DZ_B_MODEL_60_PERSONALITY = 7
    TZ_FRIDGE_60_PERSONALITY = 8
    TZ_FREEZER_60_PERSONALITY = 9
    B_MODEL_36_INCH_PERSONALITY = 10
    WINE_60_UC_DZ_PERSONALITY = 11
    BEV_60_UC_PERSONALITY = 12
    MAX_PERSONALITY = 13
    INVALID_PERSONALITY_2 = 0xFF

class UIPersonality60(IntEnum):
    COLUMN_FREEZER_PERSONALITY = 0
    COLUMN_FRIDGE_PERSONALITY = 1
    COLUMN_B_MODEL_PERSONALITY = 2
    COLUMN_WINE_PERSONALITY = 3
    DZ_FRIDGE_60_PERSONALITY = 4
    DZ_FREEZER_60_PERSONALITY = 5
    DZ_B_MODEL_60_PERSONALITY = 6
    TZ_FRIDGE_60_PERSONALITY = 7
    TZ_FREEZER_60_PERSONALITY = 8
    B_MODEL_36_INCH_PERSONALITY = 9
    WINE_60_UC_DZ_PERSONALITY = 10
    BEV_60_UC_PERSONALITY = 11
    MAX_PERSONALITY = 12
    INVALID_PERSONALITY_2 = 0xFF

class IcemakerTrayState(IntEnum):
    INITIAL_STATE          = 0 
    ACTIVE_STATE           = 1 
    START_STATE            = 2 
    INIT_REV_HOME_STATE    = 3 
    INIT_FWD_ALIGN_STATE   = 4 
    INIT_REV_ALIGN_STATE   = 5 
    WAIT_FREEZE_STATE      = 6 
    TWIST_FWD_STATE        = 7 
    TWIST_FWD_STOP_STATE   = 8 
    TWIST_REV_STATE        = 9 
    TWIST_REV_RESUME_STATE = 10 
    HTR_DELAY_STATE        = 11 
    FILL_TRAY_STATE        = 12 
    BIN_FULL_REV_STATE     = 13 
    BIN_FULL_WAIT_STATE    = 14 
    FAULT_TIMEOUT_STATE    = 15 
    FAULT_REV_STATE        = 16 
    PAUSE_STATE            = 17 
    MANUAL_STATE           = 18 
    NO_OF_STATES           = 19

class Region60(IntEnum):
    AUSTRALIA_NZ = 0
    USA_CANADA = 1
    EUROPE = 2
    CHINA = 3
    ROW = 4
    ROW_NC = 5
    BI = 6
    MAX_REGION = 7
    INV_REGION = 0xFF

class FridgeState60(IntEnum):
    """
    Enum class that represent Columns and 60cm Fridge States
    """
    COOLING_COMP_ON = 0
    COOLING_COMP_OFF = 1
    CROWBAR_STATE = 2
    NORMAL_CONTROL = 3
    DEFROST_STATE = 4
    POWER_ON_DELAY = 5
    MANUAL_MODE = 6
    SHOW_ROOM_MODE = 7
    INSTALLER_CONTROL = 8
    COOLING_COMP_ON_FPRD = 9
    COOLING_COMP_ON_GPRD = 10
    MAX_NUM_CTRL_STATES = 11

class CommLonCmds(IntEnum):
    NonAcked = 0x20
    Acked = 0x39
    MemReadWrite = 0xB8
    BlockRead = 0xB9
    BlockWrite = 0xA9
    EchoBlock = 0xFA
    BitStr_Mask = 0xA1
    ClearE2 = 0xB6
class Integrated60CommDef(IntEnum):
    RAM_controlFlag0 = 0x0001
    RAM_ctrlCnfgFlag = 0x0002  # columnsConfigGbl.ctrlBts

    RAM_configGblCtrlFlag = 0x000F # columnsConfigGbl.configBts
    RAM_controlState = 0x0019

    # RAM read heater pwm addresses
    upper_compartment_heater = 0x0159
    lower_compartment_heater = 0x011E
    ice_maker_heater = 0x011C
    upper_drain_heater = 0x01D3
    upper_throat_heater = 0x01D2
    middle_compartment_heater = 0x030B
    lower_throat_heater = 0x0354
    middle_throat_heater = 0x0355    
    defrost_heater = 0x0028

    # RAM fan addresses for the new RX130 controller
    upper_FanOutPwm = 0x0026
    upper_FanManConPwm= 0x01FE

    middle_FanOutPwm = 0x0176
    middle_FanManConPwm = 0x01F2

    lower_FanOutPwm = 0x0025
    lower_FanManConPwm = 0x01FD

    condenser_FanOutPwm = 0x01AE
    condenser_FanManConPwm = 0x01FC

    # RAM light addresses for the new RX130 controller
    RAM_upperCeilLightOutPwm = 0x015C
    RAM_upperCeilLightManConPwm = 0x01FB

    RAM_upperDisplayLightOutPwm = 0x0151
    RAM_upperDisplayLightManConPwm = 0x010E

    RAM_upperSideLightOutPwm = 0x015A
    RAM_upperSideLightManConPwm = 0x01F3

    RAM_lowerCompLightOutPwm = 0x0024
    RAM_lowerCompLightManConPwm = 0x01FA

    RAM_dispPersonality_RI60 = 0x002B
    RAM_controllerPersonality = 0x0062

    # RAM address for personality coefficient
    RAM_upperAlpha = 0x01D8     # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_upperBeta = 0x01DC      # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_upperGamma = 0x01E0     # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_lowerAlpha = 0x01E4     # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_lowerBeta = 0x01E8      # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_lowerGamma = 0x01EC     # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_middleAlpha = 0x033C    # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_middleBeta = 0x0340     # Only MSB at this location, use special memRead method to read full value (4-bytes)
    RAM_middleGamma = 0x0344    # Only MSB at this location, use special memRead method to read full value (4-bytes)

    # RAM address for upper and lower temp setpoint
    upper_temp = 0x0214         # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    lower_temp = 0x0216         # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    upper_set_point = 0x0214    # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    lower_set_point = 0x0216    # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    middle_temp = 0x02DE        # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    middle_set_point = 0x02DE   # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read

    # RAM address for reading real temp sensor value
    upper_cmpt_temp_sensor = 0x0088
    lower_cmpt_temp_sensor = 0x008C
    middle_cmpt_temp_sensor = 0x008A
    upper_evap_temp_sensor = 0x008E
    lower_evap_temp_sensor = 0x0098
    middle_evap_temp_sensor = 0x009C
    plinth_temp_sensor = 0x009A
    ice_maker_temp_sensor = 0x009E

    # RAM address for fault
    RAM_faultMainService = 0x00FC
    RAM_faultMainUser = 0x00FD

    # RAM address for brownout DVP
    compressor_average_count = 0x00E2
    compressor_average_speed = 0x01AF
    time_since_last_defrost = 0x01BD    # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    valve_switch_count = 0x001A         # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read

    # RAM address for defrost state
    RAM_defrost_state= 0x01BC

    #RAM address for ice tray state
    RAM_iceTrayState = 0x0129

    # RAM address for icemaker flap
    RAM_icemakerFlag3 = 0x0369

    # RAM address for door state
    RAM_door_state = 0x000D

    # RAM address for defrost data recover DVP
    FROST_BUILD_COMPARTMENT_SELECTION = 0x0180  # set to 0 mean upper, 1 mean lower
    Maximum_Rate_Mass_Deposit = 0x0198          # Only MSB at this location, use special memRead method to read full value (4-bytes)
    Maximum_Rate_Mass_Ingress = 0x0194          # Only MSB at this location, use special memRead method to read full value (4-bytes)
    Average_Rate_Mass_Ingress = 0x01A0          # Only MSB at this location, use special memRead method to read full value (4-bytes)
    Defrost_Interval = 0x01BA                   # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    Interval_Limit = 0x01B8                     # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read
    Frost_Build_Total_Door_Open_Time = 0x00AD   # Only MSB at this location, use special memRead method to read 2 bytes instead of single byte-read

    # RAM address for deforst max duration
    DEFROST_MAX_DURATION = 0x00C0

    DEFROST_HEATERLESS_MAX_DURATION = 0x0460

    # stepper valve control
    Stepper_Valve_Control = 0x0156

    Stepper_Valve_State = 0x0075
    Stepper_Valve_Target_Position = 0x0071

    Stepper_Valve_Time_Since_Homed = 0x007A
    Stepper_Valve_Switch_Cnt_Since_Homed = 0x007C # Need set byte to write or read to 2

    Stepper_Valve_Manual = 0x0070

    manual_compressor_speed = 0x01FF
    compressor_output_speed = 0x0090

    icemaker_manual_state = 0x0128

    DOOR_CLARITY_CFG = 0x03A2
    
    # humidity sensor simulation - external
    HUMIDITY_HEARTBEAT = 0x01C3
    HUMIDITY_AMBIENT_TEMP_CNT = 0x01C0
    HUMIDITY_HS_TEMP_OFFSET = 0x01BF
    HUMIDITY_RH_CNT = 0x01C1
    HUMIDITY_AMBIENT_TEMP_MSB = 0x01CD # Need set byte to write or read to 2

    # humidity sensor simulation - internal ui
    DISP_HUMSNR_TEMPERATURE = 0x00B4
    DISP_HUMSNR_HUMIDITY = 0x00B5


    THROAT_0_TRACK = 0x03DE

    # CRC - Checksum
    Controller_Crc = 0x0010 # Need set byte to write or read to 2
    Disp_Crc = 0x0055 # Need set byte to write or read to 2
    Humidity_Crc = 0x01CB # Need set byte to write or read to 2

    REGION_BYTE = 0x03A1


class ColumnCommDef(IntEnum):
    ICEMAKER_AO_FLAGS_BY2 = 0x00C5

class Integrated60EEPROM(Enum):
    #######################################################################
    # Any software version equal or above it will be version 2 
    eeprom_software_version_threhold = [0x64, 0x09, 0x42]
    #######################################################################

    # version 1 - v1 before the brownout eeprom shifting - controller software version < 0.64.09.38
    EEPROM_personality_v1 = [0x93E0, 0x93E1]
    EEPROM_brownout_v1 = [0x9000, 0x9015]
    EEPROM_all_v1 = [0x9000, 0x97FF]
    EEPROM_E2_all_v1 = [0x9000, 0x93FF]
    EEPROM_defrost_v1 = [0x93B9, 0x93C7]


    EEPROM_defrost_access_dataA_v1 =[0x9000 , 0x9015]
    EEPROM_defrost_access_dataB_v1 =[0x9000 , 0x9015]
    EEPROM_defrost_reset_dataA_v1 =[0x9000 , 0x97FF]
    EEPROM_defrost_reset_dataB_v1 =[0x9000 , 0x97FF]
    EEPROM_periodic_datasave_dataA1_v1 =[0x901B , 0x901C]
    EEPROM_periodic_datasave_dataA2_v1 =[0x93DB , 0x93DC]
    EEPROM_periodic_datasave_dataB1_1_v1 =[0x901B , 0x901B]
    EEPROM_periodic_datasave_dataB1_2_v1 =[0x93DB , 0x93DB]
    EEPROM_periodic_datasave_dataB2_1_v1 =[0x901C , 0x901C]
    EEPROM_periodic_datasave_dataB2_2_v1 =[0x93DC , 0x93DC]
    EEPROM_cycleLogPtr_v1 =[0x901E, 0x901E]
    EEPROM_defrostLogPtr_v1 =[0x901F, 0x901F]

    EEPROM_cycleLog_dataA_1_v1 = [0x9020, 0x933F]
    EEPROM_cycleLog_dataA_2_v1 =[0x9544, 0x97FF]

    EEPROM_cycleLog_dataB_1_v1 = [0x9020, 0x9027]
    EEPROM_cycleLog_dataB_2_v1 = [0x9028, 0x933F]
    EEPROM_cycleLog_dataB_3_v1 = [0x9544, 0x954A]
    EEPROM_cycleLog_dataB_4_v1 = [0x954B, 0x97FF] 

    EEPROM_cycleLog_dataC_1_v1 = [0x90A8, 0x90AF]
    EEPROM_cycleLog_dataC_2_1_v1 = [0x9028, 0x90A7]
    EEPROM_cycleLog_dataC_2_2_v1 = [0x90B0, 0x933F]
    EEPROM_cycleLog_dataC_3_v1 = [0x95BB, 0x95C1] 
    EEPROM_cycleLog_dataC_4_1_v1 = [0x954B, 0x95BA] 
    EEPROM_cycleLog_dataC_4_2_v1 = [0x95C2, 0x97FF]

    # version 2 - v2 after the brownout eeprom shifting - controller software version >= 0.64.09.38

    EEPROM_personality_v2 = [0x93E0, 0x93E1]
    EEPROM_brownout_v2 = [0x9B40, 0x9B5E]
    EEPROM_all_v2 = [0x9000, 0x9B5E]
    EEPROM_E2_all_v2 = [0x9000, 0x93FF]
    EEPROM_defrost_v2= [0x93B9, 0x93C7]


    EEPROM_defrost_access_dataA_v2 =[0x9B40, 0x9B5E]
    EEPROM_defrost_access_dataB_v2 =[0x9B40, 0x9B5E]
    EEPROM_defrost_reset_dataA_v2 =[0x9000 , 0x97FF]
    EEPROM_defrost_reset_dataB_v2 =[0x9000 , 0x97FF]
    EEPROM_periodic_datasave_dataA1_v2 =[0x901B , 0x901C]
    EEPROM_periodic_datasave_dataA2_v2 =[0x93DB , 0x93DC]
    EEPROM_periodic_datasave_dataB1_1_v2 =[0x901B , 0x901B]
    EEPROM_periodic_datasave_dataB1_2_v2 =[0x93DB , 0x93DB]
    EEPROM_periodic_datasave_dataB2_1_v2 =[0x901C , 0x901C]
    EEPROM_periodic_datasave_dataB2_2_v2 =[0x93DC , 0x93DC]
    EEPROM_cycleLogPtr_v2 =[0x901E, 0x901E]
    EEPROM_defrostLogPtr_v2 =[0x901F, 0x901F]

    EEPROM_cycleLog_dataA_1_v2 = [0x9020, 0x933F]
    EEPROM_cycleLog_dataA_2_v2 =[0x9544, 0x97FF]

    EEPROM_cycleLog_dataB_1_v2 = [0x9020, 0x9027]
    EEPROM_cycleLog_dataB_2_v2 = [0x9028, 0x933F]
    EEPROM_cycleLog_dataB_3_v2 = [0x9544, 0x954A]
    EEPROM_cycleLog_dataB_4_v2 = [0x954B, 0x97FF] 

    EEPROM_cycleLog_dataC_1_v2 = [0x90A8, 0x90AF]
    EEPROM_cycleLog_dataC_2_1_v2 = [0x9028, 0x90A7]
    EEPROM_cycleLog_dataC_2_2_v2 = [0x90B0, 0x933F]
    EEPROM_cycleLog_dataC_3_v2 = [0x95BB, 0x95C1] 
    EEPROM_cycleLog_dataC_4_1_v2 = [0x954B, 0x95BA] 
    EEPROM_cycleLog_dataC_4_2_v2 = [0x95C2, 0x97FF]


    EEPROM_column_personality = [0x93E0, 0x93E1]
    EEPROM_column_brownout = [0x9000, 0x9015]

    EEPROM_column_defrost_access_dataA =[0x9000 , 0x9015]
    EEPROM_column_defrost_access_dataB =[0x9000 , 0x9015]
    EEPROM_column_defrost_reset_dataA =[0x9000 , 0x97FF]
    EEPROM_column_defrost_reset_dataB =[0x9000 , 0x97FF]
    EEPROM_column_periodic_datasave_dataA1 =[0x901B , 0x901C]
    EEPROM_column_periodic_datasave_dataA2 =[0x93DB , 0x93DC]
    EEPROM_column_periodic_datasave_dataB1_1 =[0x901B , 0x901B]
    EEPROM_column_periodic_datasave_dataB1_2 =[0x93DB , 0x93DB]
    EEPROM_column_periodic_datasave_dataB2_1 =[0x901C , 0x901C]
    EEPROM_column_periodic_datasave_dataB2_2 =[0x93DC , 0x93DC]
    EEPROM_column_cycleLogPtr =[0x901E, 0x901E]
    EEPROM_column_defrostLogPtr =[0x901F, 0x901F]

    EEPROM_column_cycleLog_dataA_1 = [0x9020, 0x933F]
    EEPROM_column_cycleLog_dataA_2 =[0x9544, 0x97FF]

    EEPROM_column_cycleLog_dataB_1 = [0x9020, 0x9027]
    EEPROM_column_cycleLog_dataB_2 = [0x9028, 0x933F]
    EEPROM_column_cycleLog_dataB_3 = [0x9544, 0x954A]
    EEPROM_column_cycleLog_dataB_4 = [0x954B, 0x97FF] 

    EEPROM_column_cycleLog_dataC_1 = [0x90A8, 0x90AF]
    EEPROM_column_cycleLog_dataC_2_1 = [0x9028, 0x90A7]
    EEPROM_column_cycleLog_dataC_2_2 = [0x90B0, 0x933F]
    EEPROM_column_cycleLog_dataC_3 = [0x95BB, 0x95C1] 
    EEPROM_column_cycleLog_dataC_4_1 = [0x954B, 0x95BA] 
    EEPROM_column_cycleLog_dataC_4_2 = [0x95C2, 0x97FF]
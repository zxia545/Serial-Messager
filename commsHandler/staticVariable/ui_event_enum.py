from enum import IntEnum
from ..staticVariable.commlon_enum import CommLonCmds


class ColumnEventFromDisplay(IntEnum):
    EVT_EMPTY = 0
    EVT_ENTRY = 1
    EVT_EXIT = 2
    EVT_INIT = 3

    # --------- Generic Timer Events -------------------------
    EVT_TIMER_MS = 4
    EVT_TIMER_SEC = 5
    EVT_TIMER_MIN = 6

    # --------- Personality Event --------------------------
    EVT_PERSONALITY_UPDATE = 7
    EVT_PERSONALITY_MISMATCH = 8
    EVT_SLAVE_JOIN = 9
    EVT_SLAVE_DONE = 10
    EVT_MASTER_JOIN_ACK = 11
    EVT_RETRY_TIMEOUT = 12

    # --------- Display Event --------------------------
    EVT_DISP_STARTUP_DATA = 13
    EVT_DISP_CURRENT_SETPOINTS = 14
    EVT_DISP_CURRENT_MODE = 15
    EVT_DISP_CURRENT_STATUS = 16
    EVT_DISP_CURRENT_WIFI = 17
    EVT_DISP_CURRENT_IO = 18

    EVT_DISP_GET_STARTUP = 19
    EVT_UPDATE_MODE = 20
    EVT_UPDATE_SETPOINT = 21
    EVT_DOOR_ALARM_MUTE = 22
    EVT_DOOR_ALARM_UNMUTE = 23
    EVT_DISP_PLAY_BEEP = 24
    EVT_DISP_PLAY_RASP = 25

    EVT_FORCED_DEFROST = 26
    EVT_SHABBATH_MODE_ON = 27
    EVT_SHABBATH_MODE_OFF = 28
    EVT_SHOWROOM_MODE_ON = 29
    EVT_SHOWROOM_MODE_OFF = 30
    EVT_FORCE_ICE_FLIP = 31
    EVT_BOTTLE_CHILL = 32
    EVT_FAST_FREEZE = 33
    EVT_ICE_ON = 34
    EVT_ICE_BOOST = 35
    EVT_DISP_CHANGE_TEMP_UNITS = 36
    EVT_DISP_KEY_AUDIO_MUTE = 37
    EVT_DISP_KEY_AUDIO_UNMUTE = 38

    EVT_OPT_DNL_CTRL_RESPONSE = 39
    EVT_OPT_DNL_REQUEST = 40

    EVT_DISP_CURRENT_TEMP = 41
    EVT_DISP_IO_DIAG_REQ = 42
    EVT_DISP_TEMP_DIAG_REQ = 43
    EVT_DISP_FAULT_DIAG_RESP = 44
    EVT_DISP_FAULT_DIAG_REQ = 45
    EVT_DISP_DOOR_STATUS = 46
    EVT_DISP_SET_CONTROL_BITS = 47

    EVT_KEY_TOUCH_TEST = 48
    EVT_DISP_FAULT = 49
    EVT_DISP_HEARTBEAT = 50
    EVT_DISP_CURRENT_FEATURES = 51
    EVT_DISP_CURRENT_ICEMAKER = 52
    EVT_DISP_BOTTLE_CHILL_DISABLE_ALARM = 53
    EVT_REQUEST_WIFI_ON = 54
    EVT_DISP_FORCE_KEY_AUDIO_MUTE = 55
    EVT_REQ_SW_VER_AND_CSUM = 56
    EVT_DISP_SW_VER_AND_CSUM = 57
    EVT_REQ_DISP_MAX_COOL = 58
    EVT_MAX_COOL_STATUS = 59
    EVT_MANUAL_VALVE_CTRL = 60
    EVT_MANUAL_VALVE_IN_POS = 61
    EVT_DISP_HEARTBEAT_RESP = 62
    EVT_PERSONALITY_RESET = 63
    EVT_WATER_FILTER_REPLACE = 64
    EVT_INSTALLER_MODE_OFF = 65
    EVT_WATER_FILTER = 66
    EVT_CTRL_KEY_AUDIO_MUTE = 67
    EVT_DISP_WATER_DISPENSE_LOCK = 68
    EVT_DISP_WATER_DISPENSE_UNLOCK = 69
    EVT_CTRL_FRDG_FREEZER_STATUS = 70
    EVT_DISP_WINE_OFF = 71
    EVT_DISP_WINE_LOW = 72
    EVT_DISP_WINE_HIGH = 73
    EVT_DISP_WINE_DISPLAY = 74
    EVT_DISP_WATER_DISPENSE_ON = 75
    EVT_DISP_WATER_DISPENSE_OFF = 76
    EVT_SEND_GEA_BOOTLOADER_DATA = 77

    EVT_VIEW_KEY_INPUT = 78
    EVT_RETRY_BUSY_COMMS_TIMER = 79

    EVT_HEARTBEAT_TIME = 80
    EVT_DISP_TIMEOUT = 81
    EVT_DISP_DIAG_TIMEOUT = 82
    EVT_RETRY_STARUP_TIMER = 83
    EVT_DOOR_DISP_TIMEOUT = 84
    EVT_FAULT_TIMEOUT = 85
    EVT_UPDATE_DISPLAY_PERSONALITY = 86
    EVT_PERSONALITY_RETRY_ERROR = 87
    EVT_REQ_MASTER_PERSONALITY = 88

    EVT_OPT_DNL_TO_ERR = 89
    EVT_OPT_DNL_START = 90
    EVT_OPT_DNL_END = 91
    EVT_OPT_DNL_DATA_TOPUP = 92
    EVT_OPT_DNL_RETRY_TO = 93
    EVT_DISP_SET_UPPER_SEG_LED_OUTPUTS = 94
    EVT_DISP_SET_LOWER_SEG_LED_OUTPUTS = 95
    EVT_DISP_SET_STATUS_LED_OUTPUTS = 96
    EVT_RETRY_ACK_COMMS_TIMER = 97
    EVT_SHOWROOM_BLOCK_TIME = 98

    NUM_OF_EVT_SIG_USED = 99

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__
    

# Define the dictionary based on the provided definition
ColumnUITxUEventAckOrNotAckDict = {
    ColumnEventFromDisplay.EVT_SLAVE_JOIN: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_SLAVE_DONE: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_DISP_GET_STARTUP: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_UPDATE_SETPOINT: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_UPDATE_MODE: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DOOR_ALARM_UNMUTE: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DOOR_ALARM_MUTE: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_PLAY_BEEP: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_PLAY_RASP: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_FORCED_DEFROST: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_SHOWROOM_MODE_OFF: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_SHOWROOM_MODE_ON: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_SHABBATH_MODE_OFF: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_SHABBATH_MODE_ON: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_FORCE_ICE_FLIP: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_BOTTLE_CHILL: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_FAST_FREEZE: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_ICE_ON: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_ICE_BOOST: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_CHANGE_TEMP_UNITS: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_KEY_AUDIO_MUTE: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_KEY_AUDIO_UNMUTE: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_OPT_DNL_REQUEST: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_DISP_IO_DIAG_REQ: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_DISP_TEMP_DIAG_REQ: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_DISP_FAULT_DIAG_REQ: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_KEY_TOUCH_TEST: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_DISP_BOTTLE_CHILL_DISABLE_ALARM: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_REQUEST_WIFI_ON: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_FORCE_KEY_AUDIO_MUTE: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_SW_VER_AND_CSUM: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_REQ_DISP_MAX_COOL: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_MANUAL_VALVE_CTRL: CommLonCmds.NonAcked,
    ColumnEventFromDisplay.EVT_DISP_HEARTBEAT_RESP: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_PERSONALITY_RESET: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_INSTALLER_MODE_OFF: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_WATER_FILTER: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_WATER_DISPENSE_LOCK: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_WATER_DISPENSE_UNLOCK: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_WINE_OFF: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_WINE_HIGH: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_WINE_LOW: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_DISP_WINE_DISPLAY: CommLonCmds.Acked,
    ColumnEventFromDisplay.EVT_SEND_GEA_BOOTLOADER_DATA: CommLonCmds.NonAcked
}



ColumnUIStaticEventSet = {
    # If need to update please refer to UI repo -> StaticEvt.c
    ColumnEventFromDisplay.EVT_DISP_IO_DIAG_REQ,
    ColumnEventFromDisplay.EVT_OPT_DNL_START,
    ColumnEventFromDisplay.EVT_OPT_DNL_END,
    ColumnEventFromDisplay.EVT_PERSONALITY_MISMATCH,
    ColumnEventFromDisplay.EVT_PERSONALITY_RETRY_ERROR,
    ColumnEventFromDisplay.EVT_OPT_DNL_TO_ERR,
    ColumnEventFromDisplay.EVT_DISP_PLAY_BEEP,
    ColumnEventFromDisplay.EVT_DISP_PLAY_RASP,
    ColumnEventFromDisplay.EVT_DOOR_ALARM_UNMUTE,
    ColumnEventFromDisplay.EVT_DOOR_ALARM_MUTE,
    ColumnEventFromDisplay.EVT_FORCED_DEFROST,
    ColumnEventFromDisplay.EVT_FORCE_ICE_FLIP,
    ColumnEventFromDisplay.EVT_DISP_CHANGE_TEMP_UNITS,
    ColumnEventFromDisplay.EVT_DISP_KEY_AUDIO_UNMUTE,
    ColumnEventFromDisplay.EVT_DISP_KEY_AUDIO_MUTE,
    ColumnEventFromDisplay.EVT_SHABBATH_MODE_OFF,
    ColumnEventFromDisplay.EVT_SHABBATH_MODE_ON,
    ColumnEventFromDisplay.EVT_SHOWROOM_MODE_OFF,
    ColumnEventFromDisplay.EVT_SHOWROOM_MODE_ON,
    ColumnEventFromDisplay.EVT_DISP_GET_STARTUP,
    ColumnEventFromDisplay.EVT_DISP_BOTTLE_CHILL_DISABLE_ALARM,
    ColumnEventFromDisplay.EVT_DISP_FORCE_KEY_AUDIO_MUTE,
    ColumnEventFromDisplay.EVT_DISP_HEARTBEAT_RESP,
    ColumnEventFromDisplay.EVT_PERSONALITY_RESET,
    ColumnEventFromDisplay.EVT_REQ_MASTER_PERSONALITY,
    ColumnEventFromDisplay.EVT_INSTALLER_MODE_OFF,
    ColumnEventFromDisplay.EVT_DISP_WATER_DISPENSE_LOCK,
    ColumnEventFromDisplay.EVT_DISP_WATER_DISPENSE_UNLOCK,
}

class Integrated60EventFromDisplay(IntEnum):
    """This class is used to store all EVENTs in UI -> UI Repo EdpCfg.h

    Args:
        IntEnum (_type_): _description_
    """
    # /* --------- Generic Timer Events ------------------------- */
    EVT_SIG_TIMER_MS = 4
    EVT_SIG_USER = 4
    EVT_SIG_TIMER_SEC = 5
    EVT_SIG_TIMER_MIN = 6
    # /* Start of Comm events */
    # /* --------- Personality Event -------------------------- */
    EVT_SIG_PERSONALITY_UPDATE = 7
    EVT_SIG_PERSONALITY_MISMATCH = 8
    EVT_SIG_SLAVE_JOIN = 9
    EVT_SIG_SLAVE_DONE = 10
    EVT_SIG_MASTER_JOIN_ACK = 11
    EVT_SIG_RETRY_TIMEOUT= 12
    # /* --------- Display Event -------------------------- */
    # /* sent */
    EVT_SIG_DISP_STARTUP_DATA = 13
    EVT_SIG_DISP_CURRENT_SETPOINTS = 14
    EVT_SIG_DISP_CURRENT_MODE = 15
    EVT_SIG_DISP_CURRENT_STATUS = 16
    EVT_SIG_DISP_CURRENT_WIFI = 17
    EVT_SIG_DISP_CURRENT_IO = 18
    EVT_SIG_DISP_GET_STARTUP = 19
    EVT_SIG_UPDATE_MODE = 20
    EVT_SIG_UPDATE_SETPOINT =21
    EVT_SIG_DOOR_ALARM_MUTE=22
    EVT_SIG_DOOR_ALARM_UNMUTE=23
    EVT_SIG_DISP_PLAY_BEEP=24
    EVT_SIG_DISP_PLAY_RASP=25
    EVT_SIG_FORCED_DEFROST=26
    EVT_SIG_SABBATH_MODE_ON=27
    EVT_SIG_SABBATH_MODE_OFF=28
    EVT_SIG_SHOWROOM_MODE_ON=29
    EVT_SIG_SHOWROOM_MODE_OFF=30
    EVT_SIG_FORCE_ICE_FLIP=31
    EVT_SIG_BOTTLE_CHILL=32
    EVT_SIG_FAST_FREEZE=33
    EVT_SIG_ICE_ON=34
    EVT_SIG_ICE_BOOST=35
    EVT_SIG_DISP_CHANGE_TEMP_UNITS=36
    EVT_SIG_DISP_KEY_AUDIO_MUTE=37
    EVT_SIG_DISP_KEY_AUDIO_UNMUTE=38
    # /*-----------Display-----*/
    EVT_SIG_DISP_CURRENT_TEMP=39
    EVT_SIG_DISP_IO_DIAG_REQ=40
    EVT_SIG_DISP_TEMP_DIAG_REQ=41
    EVT_SIG_DISP_FAULT_DIAG_RESP=42
    EVT_SIG_DISP_FAULT_DIAG_REQ=43
    EVT_SIG_DISP_DOOR_STATUS=44
    EVT_SIG_DISP_SET_CONTROL_BITS=45
    # /*--Key Touch test--------*/
    EVT_SIG_KEY_TOUCH_TEST=46
    EVT_SIG_DISP_FAULT=47
    EVT_SIG_DISP_HEARTBEAT=48
    EVT_SIG_DISP_CURRENT_FEATURES=49
    EVT_SIG_DISP_CURRENT_ICEMAKER=50
    EVT_SIG_DISP_BOTTLE_CHILL_DISABLE_ALARM=51
    EVT_SIG_REQUEST_WIFI_ON=52
    EVT_SIG_DISP_FORCE_KEY_AUDIO_MUTE=53
    EVT_SIG_REQ_SW_VER_AND_CSUM=54
    EVT_SIG_DISP_SW_VER_AND_CSUM=55
    EVT_SIG_REQ_DISP_MAX_COOL=56
    EVT_SIG_MAX_COOL_STATUS=57
    EVT_SIG_MANUAL_VALVE_CTRL=58
    EVT_SIG_MANUAL_VALVE_INPOS=59
    EVT_SIG_DISP_HEARTBEAT_RESP=60
    EVT_SIG_PERSONALITY_RESET=61
    EVT_SIG_WATER_FILTER_REPLACE=62
    EVT_SIG_INSTALLER_MODE_OFF=63
    EVT_SIG_WATER_FILTER=64
    EVT_SIG_CTRL_KEY_AUDIO_MUTE=65
    EVT_SIG_DISP_WATER_DISPENSE_LOCK=66
    EVT_SIG_DISP_WATER_DISPENSE_UNLOCK=67
    EVT_SIG_CTRL_FRDG_FREEZER_STATUS=68
    EVT_SIG_DISP_WATER_DISPENSE_ON=69                                                                         #/* used on b-model only */
    EVT_SIG_DISP_WATER_DISPENSE_OFF= 70                                                                       #/* used on b-model only */
    EVT_SIG_SEND_GEA_BOOTLOADER_DATA=  71                                                                     #/* used for interceptor code */
    EVT_SIG_SET_HS_UI_NORMAL_MODE=72                                                                          #/* set humidity sensor built in to UI to normal mode */
    EVT_SIG_HSUI_UPDATE=73                                                                                    #/* generated here and sent to controller */
    EVT_SIG_DISP_PERSONALITY_WRITE=74                                                                         #/* generated from the controller */
    EVT_SIG_DISP_DOOR_ALARM= 75                                                                               #/* TODO: Check if this event is necessary. Could use existing events that sends status. Received from Controller DoorAO */
    EVT_SIG_DISP_TZ_STARTUP_DATA=76
    EVT_SIG_DISP_TZ_GET_STARTUP=77
    EVT_SIG_DISP_GET_TEMP_SP_DATA=78                                                                          #/* Requested BY UI User food mode temp set points upper= lower limit and default value */
    EVT_SIG_DISP_TEMP_SP_DATA=79
    EVT_SIG_DISP_TZ_CURRENT_SETPOINTS=80
    EVT_SIG_DISP_TZ_CURRENT_MODE=81
    EVT_SIG_DISP_TZ_CURRENT_FEATURES=82
    EVT_SIG_FACTORY_RST=83
    EVT_SIG_FACTORY_RST_RESP=84
    EVT_SIG_60CM_MANUAL_VALVE_CTRL=85
    EVT_SIG_CNTRL_PERS_RST_RESP=86
    EVT_SIG_GET_SW_VER_REQ=87
    EVT_SIG_GET_SW_VER_RESP=88
    EVT_SIG_DISP_GET_FACTORY_NUM_REQ=89
    EVT_SIG_DISP_GET_FACTORY_NUM_RESP=90
    EVT_SIG_DISP_GET_PROD_SER_NUM_REQ=91
    EVT_SIG_DISP_GET_PROD_SER_NUM_RESP=92
    EVT_SIG_DISP_REQ_ALL_FAST_FREEZE=93
    EVT_SIG_DISP_REQ_ALL_BOTTLE_CHILL=94
    EVT_SIG_FORCE_ICE_FLIP_RESP=95
    EVT_SIG_DISP_REQ_SW_RST=96
    EVT_SIG_DISP_REQ_SW_RST_RESP=97
    EVT_UPDATE_FOODMODE_PRESET=98
    EVT_SIG_DISP_SET_REGION=99
    EVT_SIG_CNTR_REGION_RESP=100
    EVT_SIG_DISP_KEYLOCK=101
    EVT_SIG_CTRL_KEYLOCK=102
    EVT_SIG_CONN_REQ_BOTTLE_CHILL=103
    # /* End of Comm events */
    EVT_SERVICE_COMMS_TX_DEFER_QUEUE_TIMER=104
    EVT_RETRY_COMMS_BUS_ACCESS_TIMER=105
    # /*---- DispControlAO ----*/
    EVT_SIG_HEARTBEAT_TIME=106
    EVT_SIG_DISP_TIMEOUT=107
    EVT_SIG_DOOR_DISP_TIMEOUT=108
    EVT_SIG_PERSONALITY_RETRY_ERROR=109
    EVT_SIG_REQ_MASTER_PERSONALITY=110
    # /*---- WifiInterface ----*/
    EVT_SM_PCM_RECV_SMART_MSG=111
    EVT_SM_PCM_RECV_SMART_MSG_ACK_TIMEOUT=112
    EVT_SM_PCM_RECV_SMART_MSG_ACK=113
    EVT_SM_PCM_SEND_SMART_MSG_GEA_COMMON_CMD_PACKET=114   #/* Originates from WiFi module. */
    EVT_SM_PCM_SEND_SMART_MSG_ACK=115
    EVT_SM_JUMPTOBL_TIMEOUT=116
    EVT_SM_NEXT_STATE=117
    EVT_TIMEOUT=118
    # /*---- Connected AO ----*/
    EVT_SIG_CTRL_TO_UI_CONNECTED_CMD=119
    EVT_SIG_BUFFERED_CTRL_TO_UI_CONNECTED_CMD=120
    EVT_SIG_BUFFERED_UI_TO_CTRL_CONNECTED_CMD=121
    EVT_SIG_COMLON_BUSY_TIMEOUT=122
    EVT_SIG_COMLON_RECV_SMART_MSG_ACK_TIMEOUT=123
    EVT_SIG_CHECK_DEFER_QUEUE=124

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__


integrated60UITxUEventAckOrNotAckDict = {
    # If need to update please refer to UI repo -> CommsAOCfg.h 
    Integrated60EventFromDisplay.EVT_SIG_SLAVE_JOIN                        :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_SLAVE_DONE                        :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_DISP_GET_STARTUP                  :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_UPDATE_SETPOINT                   :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_UPDATE_MODE                       :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DOOR_ALARM_UNMUTE                 :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DOOR_ALARM_MUTE                   :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_PLAY_BEEP                    :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_PLAY_RASP                    :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_FORCED_DEFROST                    :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_SHOWROOM_MODE_OFF                 :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_SHOWROOM_MODE_ON                  :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_SABBATH_MODE_OFF                  :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_SABBATH_MODE_ON                   :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_FORCE_ICE_FLIP                    :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_BOTTLE_CHILL                      :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_FAST_FREEZE                       :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_ICE_ON                            :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_ICE_BOOST                         :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_CHANGE_TEMP_UNITS            :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_KEY_AUDIO_MUTE               :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_KEY_AUDIO_UNMUTE             :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_IO_DIAG_REQ                  :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_DISP_TEMP_DIAG_REQ                :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_DISP_FAULT_DIAG_REQ               :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_KEY_TOUCH_TEST                    :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_DISP_BOTTLE_CHILL_DISABLE_ALARM   :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_REQUEST_WIFI_ON                   :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_FORCE_KEY_AUDIO_MUTE         :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_SW_VER_AND_CSUM              :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_REQ_DISP_MAX_COOL                 :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_MANUAL_VALVE_CTRL                 :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_DISP_HEARTBEAT_RESP               :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_PERSONALITY_RESET                 :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_INSTALLER_MODE_OFF                :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_WATER_FILTER                      :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_WATER_DISPENSE_LOCK          :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_WATER_DISPENSE_UNLOCK        :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_SEND_GEA_BOOTLOADER_DATA          :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_HSUI_UPDATE                       :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_DISP_TZ_GET_STARTUP               :      CommLonCmds.NonAcked,      
    Integrated60EventFromDisplay.EVT_SIG_DISP_GET_TEMP_SP_DATA             :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_FACTORY_RST                       :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_60CM_MANUAL_VALVE_CTRL            :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_GET_SW_VER_REQ                    :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_GET_FACTORY_NUM_REQ          :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_GET_PROD_SER_NUM_REQ         :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_REQ_ALL_FAST_FREEZE          :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_REQ_ALL_BOTTLE_CHILL         :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_REQ_SW_RST                   :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_UPDATE_FOODMODE_PRESET                :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_SET_REGION                   :      CommLonCmds.Acked,          
    Integrated60EventFromDisplay.EVT_SIG_DISP_KEYLOCK                      :      CommLonCmds.Acked,        
    Integrated60EventFromDisplay.EVT_SIG_CTRL_KEYLOCK                      :      CommLonCmds.Acked, # This EVT_SIG_CTRL_KEYLOCK is from CommsAOCfg.h in control repo, we need it for enable display keylock
}


integrated60UIStaticEventSet = {
    # If need to update please refer to UI repo -> StaticEvt.c
    Integrated60EventFromDisplay.EVT_SIG_DISP_IO_DIAG_REQ,
    Integrated60EventFromDisplay.EVT_SIG_PERSONALITY_MISMATCH,
    Integrated60EventFromDisplay.EVT_SIG_PERSONALITY_RETRY_ERROR,
    Integrated60EventFromDisplay.EVT_SIG_REQ_MASTER_PERSONALITY,
    Integrated60EventFromDisplay.EVT_SIG_DISP_GET_STARTUP,
    Integrated60EventFromDisplay.EVT_SIG_DISP_TZ_GET_STARTUP,
    Integrated60EventFromDisplay.EVT_SIG_DISP_PLAY_BEEP,
    Integrated60EventFromDisplay.EVT_SIG_DISP_PLAY_RASP,
    Integrated60EventFromDisplay.EVT_SIG_DOOR_ALARM_UNMUTE,
    Integrated60EventFromDisplay.EVT_SIG_DOOR_ALARM_MUTE,
    Integrated60EventFromDisplay.EVT_SIG_DISP_HEARTBEAT_RESP,
    Integrated60EventFromDisplay.EVT_SIG_DISP_BOTTLE_CHILL_DISABLE_ALARM,
    Integrated60EventFromDisplay.EVT_SIG_DISP_WATER_DISPENSE_LOCK,
    Integrated60EventFromDisplay.EVT_SIG_DISP_WATER_DISPENSE_UNLOCK,
    Integrated60EventFromDisplay.EVT_SIG_SABBATH_MODE_ON,
    Integrated60EventFromDisplay.EVT_SIG_SABBATH_MODE_OFF,
    Integrated60EventFromDisplay.EVT_SIG_DISP_KEY_AUDIO_UNMUTE,
    Integrated60EventFromDisplay.EVT_SIG_DISP_KEY_AUDIO_MUTE,
    Integrated60EventFromDisplay.EVT_SIG_DISP_FORCE_KEY_AUDIO_MUTE,
    Integrated60EventFromDisplay.EVT_SIG_FACTORY_RST,
    Integrated60EventFromDisplay.EVT_SIG_INSTALLER_MODE_OFF,
    Integrated60EventFromDisplay.EVT_SIG_FORCE_ICE_FLIP,
    Integrated60EventFromDisplay.EVT_SIG_DISP_CHANGE_TEMP_UNITS,
    Integrated60EventFromDisplay.EVT_SIG_FORCED_DEFROST,
    Integrated60EventFromDisplay.EVT_SIG_GET_SW_VER_REQ,
    Integrated60EventFromDisplay.EVT_SIG_DISP_GET_FACTORY_NUM_REQ,
    Integrated60EventFromDisplay.EVT_SIG_DISP_GET_PROD_SER_NUM_REQ,
    Integrated60EventFromDisplay.EVT_SIG_DISP_REQ_SW_RST,
    Integrated60EventFromDisplay.EVT_SIG_SHOWROOM_MODE_ON,
    Integrated60EventFromDisplay.EVT_SIG_SHOWROOM_MODE_OFF
}
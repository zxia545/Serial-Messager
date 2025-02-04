from enum import IntEnum
from ..staticVariable.commlon_enum import CommLonCmds


class ColumnEventFromController(IntEnum):
    EVT_EMPTY = 0
    EVT_ENTRY = 1
    EVT_EXIT = 2
    EVT_INIT = 3
    EVT_TIMER_MS = 4
    EVT_TIMER_SEC = 5
    EVT_TIMER_MIN = 6
    EVT_PERSONALITY_UPDATE = 7
    EVT_PERSONALITY_MISMATCH = 8
    EVT_SLAVE_JOIN = 9
    EVT_SLAVE_DONE = 10
    EVT_MASTER_JOIN_ACK = 11
    EVT_RETRY_TIMEOUT = 12
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
    EVT_BOTTLE_CHILL_ALARM = 78
    EVT_BOTTLE_CHILL_TIMER = 79
    EVT_DISP_READY = 80
    EVT_RETRY_BUSY_COMMS_TIMER = 81
    EVT_HEARTBEAT_TIMER = 82
    EVT_CYCLE_TIMER = 83
    EVT_POWER_ON_DELAY = 84
    EVT_MANUAL_UPDATE = 85
    EVT_STATE_CHANGE = 86
    EVT_UPDATE_PROCESS_VARS = 87
    EVT_REQUIRE_ISENSE = 88
    EVT_ABORT_ISENSE = 89
    EVT_UPDATE_CONTROL = 90
    EVT_DEFROST_START = 91
    EVT_DEFROST_ABORT = 92
    EVT_DEICE_FINISHED = 93
    EVT_DEFROST_FINISH = 94
    EVT_DELAY_FINISHED = 95
    EVT_RESET_OR_BOOTLOAD_WAIT = 96
    EVT_FROST_INGRESS_HIGH = 97
    EVT_OFFCYCLE_DEFROST_START = 98
    EVT_OFFCYCLE_DEFROST_FINISH = 99
    EVT_DOOR_OPEN = 100
    EVT_DOOR_CLOSE = 101
    EVT_DOOR_ALARM = 102
    EVT_DOOR_ALARM_OVER = 103
    EVT_DOOR_TIMER_COUNT = 104
    EVT_SEND_DOOR_COUNT = 105
    EVT_RESET_DOOR_COUNT = 106
    EVT_DOORS_ALL_CLOSED = 107
    EVT_QUERY_DOOR_STATE = 108
    EVT_DOOR_OPEN_DURATION = 109
    EVT_HARNESS_DETECT = 110
    EVT_FAN_SPEED = 111
    EVT_FAN_TIMER_EXPIRED = 112
    EVT_FAN_FEEDBACK = 113
    EVT_ISENSE_REQUIRES_CONTROL = 114
    EVT_ISENSE_REQUIRES_ON = 115
    EVT_ISENSE_REQUIRES_OFF = 116
    EVT_ISENSE_DOESNT_REQUIRE_CONTROL = 117
    EVT_ISENSE_TIMER_EXPIRED = 118
    EVT_ISENSE_HAS_CONTROL = 119
    EVT_ISENSE_START = 120
    EVT_COMP_SPEED_CHANGE = 121
    EVT_OVERRIDE_COMP_SPEED = 122
    EVT_COMP_MIN_TIMER_EXPIRED = 123
    EVT_COMP_OFF = 124
    EVT_COMP_ON = 125
    EVT_RESET_AVERAGE = 126
    EVT_SEND_AVERAGE = 127
    EVT_REFRIGERANT_INITIALISED = 128
    EVT_HEATER_ON = 129
    EVT_HEATER_OFF = 130
    EVT_TEMPERATURE = 131
    EVT_HS_UPDATE = 132
    EVT_HS_HEART_BEAT = 133
    EVT_AUDIO_ON = 134
    EVT_AUDIO_OFF = 135
    EVT_AUDIO_ENABLE = 136
    EVT_AUDIO_DISABLE = 137
    EVT_AUDIO_DONE = 138
    EVT_AUDIO_MANUAL = 139
    EVT_SOL_ON = 140
    EVT_SOL_OFF = 141
    EVT_SOL_SWITCH_Q = 142
    EVT_SOL_TIMEOUT = 143
    EVT_GEARBOX_ON = 144
    EVT_GEARBOX_OFF = 145
    EVT_GEARBOX_TIMER_EXPIRED = 146
    EVT_GEARBOX_LMT_SW = 147
    EVT_GEARBOX_I_STBL_TIMER_EXPIRED = 148
    EVT_ICEMAKER = 149
    EVT_IM_TIMER_EXPIRED = 150
    EVT_ICE_TRAY_TEMP_FAULT_TIMER_EXPIRED = 151
    EVT_TRAY_FULL_ROTATION_TIMEOUT = 152
    EVT_POWERBOOST_TIMER_EXPIRED = 153
    EVT_LOW_TEMP_INTEGRAL_TIMER_EXPIRED = 154
    EVT_GEARBOX_I_HIGH = 155
    EVT_SOL_I_HI = 156
    EVT_ICEMAKER_NEXT_STATE = 157
    EVT_IM_MANUAL_STATE_VAR_CHANGED = 158
    EVT_ICEMAKER_DISPENSE = 159
    EVT_DISPENSE = 160
    EVT_WATER_DISPENSE_TIMEOUT = 161
    EVT_DOOR_OPEN_DELAY = 162
    EVT_WATER_DISPENSE_DOOR_CLOSE_DELAY = 163
    EVT_WATER_SOLENOID_TEMPERATURE_CHANGE_UPDATE = 164
    EVT_E2_DOOR_COUNT_SAVE = 165
    EVT_E2_PERSONALITY_SAVE = 166
    EVT_E2_DEFROST_DATA_SAVE = 167
    EVT_E2_FINISH_CONTROL_UPDATE = 168
    EVT_E2_BROWNOUT_DATA_SAVE = 169
    EVT_DEFROST_SAVE = 170
    EVT_CYCLE_SAVE = 171
    EVT_CYCLE_SAVE_SECONDARY = 172
    EVT_MANUAL_MODE_ON = 173
    EVT_MANUAL_MODE_OFF = 174
    EVT_I2C_WRITE_COMPLETE = 175
    EVT_I2C_WRITE_OP_TIMEOUT = 176
    EVT_I2C_READ_COMPLETE = 177
    EVT_I2C_READ_OP_TIMEOUT = 178
    EVT_I2C_PERIODIC_READ = 179
    EVT_I2C_RETRY_WRITE = 180
    EVT_I2C_SEQ_SWITCHING_READ_STATE = 181
    EVT_I2C_SAFE_SEQ_SWITCHING_TIMER_EXPIRED = 182
    EVT_I2C_SET_PIN_DATA = 183
    EVT_I2C_AC_VALVE_EVT_PAIR_WAIT_TIMER_EXPIRED = 184
    EVT_CONNECTED_CMD = 185
    EVT_CONNECTED_ACK_RECEIVED = 186
    EVT_CONNECTED_SEND_MSG = 187
    EVT_CONNECTED_CHANGE_TEMP_UNIT = 188
    EVT_CONNECTED_JUMP_TO_RESET = 189
    EVT_CONNECTED_JUMP_TO_BOOTLOADER = 190
    EVT_CONNECTED_ICE_ON = 191
    EVT_CONNECTED_ICE_BOOST = 192
    EVT_CONNECTED_SHABBATH_MODE_ON = 193
    EVT_CONNECTED_SHABBATH_MODE_OFF = 194
    EVT_WIFI_STATUS_UPDATE = 195
    EVT_REQUEST_WIFI_STATUS_UPDATE = 196
    EVT_SEND_START_UP_INFO = 197
    EVT_WIFI_SW_VER_RQ = 198
    EVT_COMM_BUSY_TIME_OUT = 199
    EVT_ERD_REF_MODEL_TIME_OUT = 200
    EVT_GEA_RAW_DATA = 201
    EVT_FAULT = 202
    EVT_RESCIND_FAULT = 203
    EVT_VALVE_IN_POS = 204
    EVT_SET_VALVE_POS = 205
    EVT_DISABLE = 206
    EVT_ENABLE = 207
    EVT_VALVE_PURGE_TIMEOUT = 208
    EVT_SHABBATH_MODE_STARTUP = 209
    EVT_MANUAL_VALVE_TIMEOUT = 210
    EVT_I_SENSE_1_HR = 211
    EVT_DOOR_ALARM_MUTE_DELAYED = 212
    EVT_RETRY_ACK_COMMS_TIMER = 213
    EVT_SUSPEND_PERIPH = 214
    EVT_STEPPER_DELAY_ON = 215
    EVT_STEPPER_DELAY_OFF = 216
    EVT_UPDATE_LIGHT_MODE = 217
    EVT_LIGHT_STANDBY = 218
    NUM_OF_EVT_USED = 219

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__

ColumnControllerTxEventAckOrNotAckDict = {
    ColumnEventFromController.EVT_MASTER_JOIN_ACK: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_DISP_STARTUP_DATA: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_DISP_CURRENT_SETPOINTS: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_CURRENT_MODE: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_CURRENT_STATUS: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_CURRENT_WIFI: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_CURRENT_IO: CommLonCmds.Acked,
    ColumnEventFromController.EVT_OPT_DNL_CTRL_RESPONSE: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_DISP_CURRENT_TEMP: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_FAULT_DIAG_RESP: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_DISP_SET_CONTROL_BITS: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_FAULT: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_DISP_HEARTBEAT: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_DISP_CURRENT_FEATURES: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_CURRENT_ICEMAKER: CommLonCmds.Acked,
    ColumnEventFromController.EVT_REQ_SW_VER_AND_CSUM: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_MAX_COOL_STATUS: CommLonCmds.Acked,
    ColumnEventFromController.EVT_MANUAL_VALVE_IN_POS: CommLonCmds.NonAcked,
    ColumnEventFromController.EVT_WATER_FILTER_REPLACE: CommLonCmds.Acked,
    ColumnEventFromController.EVT_CTRL_KEY_AUDIO_MUTE: CommLonCmds.Acked,
    ColumnEventFromController.EVT_CTRL_FRDG_FREEZER_STATUS: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_WATER_DISPENSE_ON: CommLonCmds.Acked,
    ColumnEventFromController.EVT_DISP_WATER_DISPENSE_OFF: CommLonCmds.Acked
}


ColumnControllerStaticEventSet = {
    # If need to update please refer to Controller repo -> StaticEvt.c 
    ColumnEventFromController.EVT_AUDIO_OFF,
    ColumnEventFromController.EVT_AUDIO_DONE,
    ColumnEventFromController.EVT_AUDIO_DISABLE,
    ColumnEventFromController.EVT_AUDIO_ENABLE,
    ColumnEventFromController.EVT_BOTTLE_CHILL_ALARM,
    ColumnEventFromController.EVT_COMP_ON,
    ColumnEventFromController.EVT_COMP_OFF,
    ColumnEventFromController.EVT_DOOR_ALARM,
    ColumnEventFromController.EVT_DOOR_ALARM_OVER,
    ColumnEventFromController.EVT_DOORS_ALL_CLOSED,
    ColumnEventFromController.EVT_DOOR_OPEN,
    ColumnEventFromController.EVT_DOOR_ALARM_MUTE,
    ColumnEventFromController.EVT_DOOR_ALARM_UNMUTE,
    ColumnEventFromController.EVT_FAN_FEEDBACK,
    ColumnEventFromController.EVT_GEARBOX_I_HIGH,
    ColumnEventFromController.EVT_GEARBOX_OFF,
    ColumnEventFromController.EVT_SOL_ON,
    ColumnEventFromController.EVT_SOL_OFF,
    ColumnEventFromController.EVT_ICEMAKER_NEXT_STATE,
    ColumnEventFromController.EVT_IM_MANUAL_STATE_VAR_CHANGED,
    ColumnEventFromController.EVT_ICEMAKER_DISPENSE,
    ColumnEventFromController.EVT_REQUIRE_ISENSE,
    ColumnEventFromController.EVT_ABORT_ISENSE,
    ColumnEventFromController.EVT_ISENSE_HAS_CONTROL,
    ColumnEventFromController.EVT_DEFROST_FINISH,
    ColumnEventFromController.EVT_RESET_AVERAGE,
    ColumnEventFromController.EVT_RESET_DOOR_COUNT,
    ColumnEventFromController.EVT_DEFROST_START,
    ColumnEventFromController.EVT_MANUAL_MODE_ON,
    ColumnEventFromController.EVT_MANUAL_MODE_OFF,
    ColumnEventFromController.EVT_SHOWROOM_MODE_ON,
    ColumnEventFromController.EVT_SHOWROOM_MODE_OFF,
    ColumnEventFromController.EVT_SHABBATH_MODE_OFF,
    ColumnEventFromController.EVT_SHABBATH_MODE_ON,
    ColumnEventFromController.EVT_SHABBATH_MODE_STARTUP,
    ColumnEventFromController.EVT_ICEMAKER_DISPENSE,
    ColumnEventFromController.EVT_REFRIGERANT_INITIALISED,
    ColumnEventFromController.EVT_HS_HEART_BEAT,
    ColumnEventFromController.EVT_ISENSE_TIMER_EXPIRED,
    ColumnEventFromController.EVT_COMP_MIN_TIMER_EXPIRED,
    ColumnEventFromController.EVT_FORCE_ICE_FLIP,
}

class Integrated60EventFromController(IntEnum):
    EVT_EMPTY   = EVT_SIG_EMPTY = 0,
    EVT_ENTRY   = EVT_SIG_ENTRY = 1,
    EVT_EXIT    = EVT_SIG_EXIT  = 2,
    EVT_INIT    = EVT_SIG_INIT  = 3,
    # /* --------- Generic Timer Events ------------------------- */
    EVT_TIMER_MS = EVT_SIG_USER =4,
    EVT_TIMER_SEC =5,
    EVT_TIMER_MIN =6,

    # /* --------- Personality Event -------------------------- */
    EVT_PERSONALITY_UPDATE = 7, #/* OBSOLETE - Kept to ensure display and controller event signals are in sync */
    EVT_PERSONALITY_MISMATCH = 8,
    EVT_SLAVE_JOIN = 9,
    EVT_SLAVE_DONE = 10,
    EVT_MASTER_JOIN_ACK = 11,
    EVT_RETRY_TIMEOUT = 12,

    # /* --------- Display Event -------------------------- */
    # /* sent */
    EVT_DISP_STARTUP_DATA = 13,
    EVT_DISP_CURRENT_SETPOINTS = 14,
    EVT_DISP_CURRENT_MODE = 15,
    EVT_DISP_CURRENT_STATUS = 16,
    EVT_DISP_CURRENT_WIFI = 17,
    EVT_DISP_CURRENT_IO = 18,
    # /* sent */
    EVT_DISP_GET_STARTUP = 19,
    EVT_UPDATE_MODE = 20,
    EVT_UPDATE_SETPOINT = 21,
    EVT_DOOR_ALARM_MUTE = 22,
    EVT_DOOR_ALARM_UNMUTE = 23,
    EVT_DISP_PLAY_BEEP = 24,
    EVT_DISP_PLAY_RASP = 25,

    EVT_FORCED_DEFROST = 26,
    EVT_SHABBATH_MODE_ON = 27,
    EVT_SHABBATH_MODE_OFF = 28,
    EVT_SHOWROOM_MODE_ON = 29,
    EVT_SHOWROOM_MODE_OFF = 30,
    EVT_FORCE_ICE_FLIP = 31,
    EVT_BOTTLE_CHILL = 32,
    EVT_FAST_FREEZE = 33,
    EVT_ICE_ON = 34,
    EVT_ICE_BOOST = 35,
    EVT_DISP_CHANGE_TEMP_UNITS = 36,
    EVT_DISP_KEY_AUDIO_MUTE = 37,
    EVT_DISP_KEY_AUDIO_UNMUTE = 38,
    EVT_DISP_CURRENT_TEMP = 39,
    EVT_DISP_IO_DIAG_REQ = 40,
    EVT_DISP_TEMP_DIAG_REQ = 41,
    EVT_DISP_FAULT_DIAG_RESP = 42,
    EVT_DISP_FAULT_DIAG_REQ = 43,
    # /* ----------Door Events ---------------------------------*/
    EVT_DISP_DOOR_STATUS = 44,
    EVT_DISP_SET_CONTROL_BITS = 45,
    # /*--Key Touch test--------*/
    EVT_KEY_TOUCH_TEST = 46,
    EVT_DISP_FAULT = 47,
    EVT_DISP_HEARTBEAT = 48,
    EVT_DISP_CURRENT_FEATURES = 49,
    EVT_DISP_CURRENT_ICEMAKER = 50,
    EVT_DISP_BOTTLE_CHILL_DISABLE_ALARM = 51,
    EVT_REQUEST_WIFI_ON = 52,
    EVT_DISP_FORCE_KEY_AUDIO_MUTE = 53,
    EVT_REQ_SW_VER_AND_CSUM = 54,
    EVT_DISP_SW_VER_AND_CSUM = 55,
    EVT_REQ_DISP_MAX_COOL = 56,
    EVT_MAX_COOL_STATUS = 57,
    EVT_MANUAL_VALVE_CTRL = 58,
    EVT_MANUAL_VALVE_IN_POS = 59,
    EVT_DISP_HEARTBEAT_RESP = 60,
    EVT_PERSONALITY_RESET = 61,
    EVT_WATER_FILTER_REPLACE = 62,
    EVT_INSTALLER_MODE_OFF = 63,
    EVT_WATER_FILTER = 64,
    EVT_CTRL_KEY_AUDIO_MUTE = 65,
    EVT_DISP_WATER_DISPENSE_LOCK = 66,
    EVT_DISP_WATER_DISPENSE_UNLOCK = 67,
    EVT_CTRL_FRDG_FREEZER_STATUS = 68,
    EVT_DISP_WATER_DISPENSE_ON = 69,                                                                          # /* used on b-model only */
    EVT_DISP_WATER_DISPENSE_OFF = 70,                                                                         # /* used on b-model only */
    EVT_SEND_GEA_BOOTLOADER_DATA = 71,                                                                        # /* used for interceptor board */
    EVT_SET_HS_UI_NORMAL_MODE = 72,                                                                           # /* set humidity sensor built in to UI to normal mode */
    EVT_SIG_HSUI_UPDATE = 73,                                                                                 # /* generated from the display and handled here */
    EVT_DISP_PERSONALITY_WRITE = 74,                                                                          # /* generated here and sent to display */
    EVT_DISP_DOOR_ALARM = 75,
    EVT_DISP_TZ_STARTUP_DATA = 76,
    EVT_DISP_TZ_GET_STARTUP = 77,
    EVT_DISP_GET_TEMP_SP_DATA = 78,                                                                           # /* Requested BY UI User food mode temp set points upper, lower limit and default value */
    EVT_DISP_TEMP_SP_DATA = 79,
    EVT_DISP_TZ_CURRENT_SETPOINTS = 80,
    EVT_DISP_TZ_CURRENT_MODE = 81,
    EVT_DISP_TZ_CURRENT_FEATURES = 82,
    EVT_DISP_FACTORY_RST = 83,
    EVT_DISP_FACTORY_RST_RESP = 84,
    EVT_DISP_MANUAL_VALVE_CTRL = 85,
    EVT_SIG_CNTRL_PERS_RST_RESP = 86,
    EVT_DISP_GET_SW_VER_REQ = 87,
    EVT_DISP_GET_SW_VER_RESP = 88,
    EVT_DISP_GET_FACTORY_NUM_REQ = 89,
    EVT_DISP_GET_FACTORY_NUM_RESP = 90,
    EVT_DISP_GET_PROD_SER_NUM_REQ = 91,
    EVT_DISP_GET_PROD_SER_NUM_RESP = 92,
    EVT_DISP_REQ_ALL_FAST_FREEZE = 93,
    EVT_DISP_REQ_ALL_BOTTLE_CHILL = 94,
    EVT_FORCE_ICE_FLIP_RESP = 95,
    EVT_DISP_REQ_SW_RST = 96,
    EVT_DISP_REQ_SW_RST_RESP = 97,
    EVT_UPDATE_FOODMODE_PRESET = 98,
    EVT_DISP_SET_REGION = 99,
    EVT_CNTR_REGION_RESP = 100,
    EVT_DISP_KEYLOCK = 101,
    EVT_CTRL_KEYLOCK = 102,
    EVT_CONN_REQ_BOTTLE_CHILL = 103,
    EVT_DISP_NUM_FOODMODE_PRESETS_CFG = 104,
    EVT_CONN_REQ_FOODMODE_PRESET = 105,
    EVT_SET_HS_UI_SLAVE_MODE=106,
    EVT_DISP_CMPT_LIGHT_MODE = 107,
    EVT_CNTR_CMPT_LIGHT_MODE_RESP = 108,
    EVT_SET_DISP_DOOR_CLARITY = 109,
    EVT_CNTR_DISP_DOOR_CLARITY_RESP = 110,
    EVT_STORE_BROWNOUT_DATA = 111,
    EVT_CNTR_STORE_BROWNOUT_DATA_RESP = 112,
    EVT_DISP_GET_FOOD_MODES = 113,
    EVT_DISP_FOOD_MODES = 114,
    EVT_DISP_WIDTH_WRITE = 115,
    # /* End of Comm events ***********************************************************************************************/
    EVT_BOTTLE_CHILL_ALARM = 116,
    EVT_BOTTLE_CHILL_TIMER = 117,
    EVT_DISP_READY = 118,
    EVT_SERVICE_COMMS_TX_DEFER_QUEUE_TIMER = 119,
    EVT_HEARTBEAT_TIMER = 120,
    # /* --------- Controller Events -------------------------------- */
    EVT_CYCLE_TIMER = 121,
    EVT_POWER_ON_DELAY = 122,
    EVT_MANUAL_UPDATE = 123,
    EVT_STATE_CHANGE = 124,
    EVT_UPDATE_PROCESS_VARS = 125,
    EVT_REQUIRE_ISENSE = 126,
    EVT_ABORT_ISENSE = 127,
    EVT_UPDATE_CONTROL = 128,
    # /** --------- Defrost Control Events ------------------------- **/
    EVT_DEFROST_START = 129,
    EVT_DEFROST_ABORT = 130,
    EVT_DEICE_FINISHED = 131,
    EVT_DEFROST_FINISH = 132,
    EVT_DELAY_FINISHED = 133,
    EVT_RESET_OR_BOOTLOAD_WAIT = 134,
    EVT_FROST_INGRESS_HIGH = 135,
    EVT_OFFCYCLE_DEFROST_START = 136,
    EVT_POST_DEFROST_MASS_DEDUCT = 137,
    # /** --------- Door Events ------------------------------------ **/
    EVT_DOOR_OPEN = 138,
    EVT_DOOR_CLOSE = 139,
    EVT_DOOR_ALARM = 140,
    EVT_DOOR_ALARM_OVER = 141,
    EVT_DOOR_TIMER_COUNT = 142,
    EVT_SEND_DOOR_COUNT = 143,
    EVT_RESET_DOOR_COUNT = 144,
    EVT_DOORS_ALL_CLOSED = 145,
    EVT_QUERY_DOOR_STATE = 146,
    EVT_DOOR_OPEN_DURATION = 147,
    EVENT_DOOR_OPEN_WARNING = 148,
    # /* --------- Fan Events -------------------------------- */
    EVT_FAN_SPEED = 149,
    EVT_FAN_TIMER_EXPIRED = 150,
    EVT_FAN_FEEDBACK = 151,
    # /* --------- Current Sense Events ---------------------- */
    EVT_ISENSE_REQUIRES_CONTROL = 152,
    EVT_ISENSE_REQUIRES_ON = 153,
    EVT_ISENSE_REQUIRES_OFF = 154,
    EVT_ISENSE_DOESNT_REQUIRE_CONTROL = 155,
    EVT_ISENSE_TIMER_EXPIRED = 156,
    EVT_ISENSE_HAS_CONTROL = 157,
    EVT_ISENSE_START = 158,
    # /* --------- Compressor Events ------------------------ */
    EVT_COMP_SPEED_CHANGE = 159,
    EVT_OVERRIDE_COMP_SPEED = 160,
    EVT_COMP_MIN_TIMER_EXPIRED = 161,
    EVT_COMP_OFF = 162,
    EVT_COMP_ON = 163,
    EVT_RESET_AVERAGE = 164,
    EVT_SEND_AVERAGE = 165,
    EVT_REFRIGERANT_INITIALISED = 166,
    # /* --------- Heater Events -------------------- */
    EVT_HEATER_ON = 167,
    EVT_HEATER_OFF = 168,
    EVT_AUXILIARY_HEATER_ON = 169,
    EVT_AUXILIARY_HEATER_OFF = 170,
    EVT_AUXILIARY_TIMER = 171,
    # /* --------- Temperature Sensor Events ------------------ */
    EVT_TEMPERATURE = 172,
    # /* --------- Humidity Sensor Events --------------------- */
    EVT_HS_UPDATE = 173,
    EVT_HS_HEART_BEAT = 174,
    # /* --------- Audio Events ------------------------------- */
    EVT_AUDIO_PLAY = 175,
    EVT_AUDIO_STATE = 176,
    EVT_AUDIO_DONE = 177,
    EVT_AUDIO_MANUAL = 178,
    # /* --------- Solenoid Events -------------------------------- */
    EVT_SOL_ON = 179,
    EVT_SOL_OFF = 180,
    EVT_SOL_TIMEOUT = 181,
    # /* --------- Gearbox Events -------------------------------- */
    EVT_GEARBOX_ON = 182,
    EVT_GEARBOX_OFF = 183,
    EVT_GEARBOX_TIMER_EXPIRED = 184,
    EVT_GEARBOX_LMT_SW = 185,
    EVT_GEARBOX_I_STBL_TIMER_EXPIRED = 186,
    # /* --------- Icemaker Events -------------------------------- */
    EVT_ICEMAKER = 187,
    EVT_IM_TIMER_EXPIRED = 188,
    EVT_IM_HTR_TIMER_EXPIRED = 189,
    EVT_ICE_TRAY_TEMP_FAULT_TIMER_EXPIRED = 190,
    EVT_TRAY_FULL_ROTATION_TIMEOUT = 191,
    EVT_POWER_BOOST_TIMER_EXPIRED = 192,
    EVT_LOW_TEMP_INTEGRAL_TIMER_EXPIRED = 193,
    EVT_GEARBOX_I_HIGH = 194,
    EVT_ICEMAKER_NEXT_STATE = 195,
    EVT_IM_MANUAL_STATE_VAR_CHANGED = 196,
    EVT_ICEMAKER_DISPENSE = 197,
    EVT_ICEMAKER_FILL_TRAY_CHECK = 198,
    # /* --------- Water Dispenser Events -------------------------------- */
    EVT_DISPENSE = 199,
    EVT_DOOR_OPEN_DELAY = 200,
    EVT_WATER_DISPENSE_DOOR_CLOSE_DELAY = 201,
    EVT_WATER_SOLENOID_TEMPERATURE_CHANGE_UPDATE = 202,
    # /* --------- EEPROM Events ------------------------------- */
    EVT_E2_BROWNOUT_DATA_SAVE = 203,
    EVT_E2_FACTORY_RESET_CHECKSUM = 204,
    # /* --------- Mode Events ------------------------------- */
    EVT_MANUAL_MODE_ON = 205,
    EVT_MANUAL_MODE_OFF = 206,
    # /* --------- I2c expander ao events---------------------- */
    EVT_I2C_WRITE_COMPLETE = 207,
    EVT_I2C_WRITE_OP_TIMEOUT = 208,
    EVT_I2C_READ_COMPLETE = 209,
    EVT_I2C_READ_OP_TIMEOUT = 210,
    EVT_I2C_PERIODIC_READ = 211,
    EVT_I2C_RETRY_WRITE = 212,
    EVT_I2C_SAFE_SEQ_SWITCHING_TIMER_EXPIRED = 213,
    EVT_I2C_SET_PIN_DATA = 214,
    EVT_I2C_AC_VALVE_EVT_PAIR_WAIT_TIMER_EXPIRED = 215,
    # /* --------- Connected Events --------------------------- */
    EVT_CONNECTED_CMD = 216,
    EVT_CONNECTED_ACK_RECEIVED = 217,
    EVT_CONNECTED_SEND_MSG = 218,
    EVT_CONNECTED_CHANGE_TEMP_UNIT = 219,
    EVT_CONNECTED_JUMP_TO_RESET = 220,
    EVT_CONNECTED_JUMP_TO_BOOTLOADER = 221,
    EVT_CONNECTED_ICE_ON = 222,
    EVT_CONNECTED_ICE_BOOST = 223,
    EVT_WIFI_STATUS_UPDATE = 224,
    EVT_CONNECTED_REFRESH_ERDS_AFTER_PERS_HANDSHAKE = 225,
    EVT_REQUEST_WIFI_STATUS_UPDATE = 226,
    EVT_DELAY_STARTING_PERIODIC_STATUS_ERD_REFRESH = 227,
    EVT_SEND_START_UP_INFO = 228,
    EVT_WIFI_SW_VER_RQ = 229,
    EVT_COMM_BUSY_TIME_OUT = 230,
    # /* --------- GEA raw data Events --------------------------- */
    EVT_GEA_RAW_DATA = 231,
    # /* --------- Misc Events -------------------------------- */
    EVT_FAULT = 232,
    EVT_RESCIND_FAULT = 233,
    EVT_VALVE_IN_POS = 234,
    EVT_SET_VALVE_POS = 235,
    EVT_DISABLE = 236,
    EVT_ENABLE = 237,
    EVT_VALVE_PURGE_TIMEOUT = 238,
    EVT_SHABBATH_MODE_STARTUP = 239,
    EVT_MANUAL_VALVE_TIMEOUT = 240,
    EVT_I_SENSE_1_HR = 241,
    EVT_RETRY_COMMS_BUS_ACCESS_TIMER = 242,
    EVT_SUSPEND_PERIPH = 243,
    EVT_STEPPER_DELAY_ON = 244,
    EVT_STEPPER_DELAY_OFF = 245,
    EVT_UPDATE_LIGHT_MODE = 246,
    EVT_LIGHT_STANDBY = 247,
    EVT_FORCE_ICE_FLIP_COMPLETE = 248,
    EVT_CONNECTED_DOOR_UNMUTE = 249,
    EVT_EXCL_PERIPH_ON = 250,
    NUM_OF_EVT_USED = 251

    EVT_SIG_VIEW_KEY_INPUT=116,


    @classmethod
    def has_key(cls, name):
        return name in cls.__members__
integrated60ControllerTxEventAckOrNotAckDict = {
    # If need to update please refer to controller repo -> CommsAOCfg.h 
    Integrated60EventFromController.EVT_MASTER_JOIN_ACK             :         CommLonCmds.NonAcked,
    Integrated60EventFromController.EVT_DISP_STARTUP_DATA           :         CommLonCmds.NonAcked,
    Integrated60EventFromController.EVT_DISP_CURRENT_SETPOINTS      :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_CURRENT_MODE           :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_CURRENT_STATUS         :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_CURRENT_WIFI           :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_CURRENT_IO             :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_CURRENT_TEMP           :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_FAULT_DIAG_RESP        :         CommLonCmds.NonAcked,
    Integrated60EventFromController.EVT_DISP_SET_CONTROL_BITS       :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_FAULT                  :         CommLonCmds.NonAcked,
    Integrated60EventFromController.EVT_DISP_HEARTBEAT              :         CommLonCmds.NonAcked,
    Integrated60EventFromController.EVT_DISP_CURRENT_FEATURES       :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_CURRENT_ICEMAKER       :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_REQ_SW_VER_AND_CSUM         :         CommLonCmds.NonAcked,
    Integrated60EventFromController.EVT_MAX_COOL_STATUS             :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_MANUAL_VALVE_IN_POS         :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_WATER_FILTER_REPLACE        :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_CTRL_KEY_AUDIO_MUTE         :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_CTRL_FRDG_FREEZER_STATUS    :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_WATER_DISPENSE_ON      :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_WATER_DISPENSE_OFF     :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_SET_HS_UI_NORMAL_MODE       :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_PERSONALITY_WRITE      :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_TZ_STARTUP_DATA        :         CommLonCmds.NonAcked,
    Integrated60EventFromController.EVT_DISP_TEMP_SP_DATA           :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_TZ_CURRENT_SETPOINTS   :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_TZ_CURRENT_MODE        :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_TZ_CURRENT_FEATURES    :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_DOOR_ALARM             :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_FACTORY_RST_RESP       :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_SIG_CNTRL_PERS_RST_RESP     :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_GET_SW_VER_RESP        :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_GET_FACTORY_NUM_RESP   :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_GET_PROD_SER_NUM_RESP  :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_FORCE_ICE_FLIP_RESP         :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_DISP_REQ_SW_RST_RESP        :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_CNTR_REGION_RESP            :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_CTRL_KEYLOCK                :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_CONN_REQ_BOTTLE_CHILL       :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_CONN_REQ_FOODMODE_PRESET    :         CommLonCmds.Acked,    
    Integrated60EventFromController.EVT_SIG_VIEW_KEY_INPUT          :         CommLonCmds.Acked,
    Integrated60EventFromController.EVT_DISP_WIDTH_WRITE            :         CommLonCmds.Acked,
}

integrated60ControllerStaticEventSet = {
    # If need to update please refer to Controller repo -> StaticEvt.c 
    Integrated60EventFromController.EVT_AUDIO_DONE,
    Integrated60EventFromController.EVT_BOTTLE_CHILL_ALARM,
    Integrated60EventFromController.EVT_COMP_ON,
    Integrated60EventFromController.EVT_COMP_OFF,
    Integrated60EventFromController.EVT_DOOR_ALARM,
    Integrated60EventFromController.EVT_DOOR_ALARM_OVER,
    Integrated60EventFromController.EVT_DOORS_ALL_CLOSED,
    Integrated60EventFromController.EVT_DOOR_OPEN,
    Integrated60EventFromController.EVT_DOOR_ALARM_MUTE,
    Integrated60EventFromController.EVT_DOOR_ALARM_UNMUTE,
    Integrated60EventFromController.EVT_CONNECTED_DOOR_UNMUTE,
    Integrated60EventFromController.EVENT_DOOR_OPEN_WARNING,
    Integrated60EventFromController.EVT_FAN_FEEDBACK,
    Integrated60EventFromController.EVT_GEARBOX_I_HIGH,
    Integrated60EventFromController.EVT_GEARBOX_OFF,
    Integrated60EventFromController.EVT_SOL_ON,
    Integrated60EventFromController.EVT_SOL_OFF,
    Integrated60EventFromController.EVT_ICEMAKER_NEXT_STATE,
    Integrated60EventFromController.EVT_IM_MANUAL_STATE_VAR_CHANGED,
    Integrated60EventFromController.EVT_ICEMAKER_DISPENSE,
    Integrated60EventFromController.EVT_REQUIRE_ISENSE,
    Integrated60EventFromController.EVT_ABORT_ISENSE,
    Integrated60EventFromController.EVT_ISENSE_HAS_CONTROL,
    Integrated60EventFromController.EVT_DEFROST_FINISH,
    Integrated60EventFromController.EVT_RESET_AVERAGE,
    Integrated60EventFromController.EVT_RESET_DOOR_COUNT,
    Integrated60EventFromController.EVT_DEFROST_START,
    Integrated60EventFromController.EVT_MANUAL_MODE_ON,
    Integrated60EventFromController.EVT_MANUAL_MODE_OFF,
    Integrated60EventFromController.EVT_SHOWROOM_MODE_ON,
    Integrated60EventFromController.EVT_SHOWROOM_MODE_OFF,
    Integrated60EventFromController.EVT_SHABBATH_MODE_OFF,
    Integrated60EventFromController.EVT_SHABBATH_MODE_ON,
    Integrated60EventFromController.EVT_SHABBATH_MODE_STARTUP,
    Integrated60EventFromController.EVT_REFRIGERANT_INITIALISED,
    Integrated60EventFromController.EVT_HS_HEART_BEAT,
    Integrated60EventFromController.EVT_ISENSE_TIMER_EXPIRED,
    Integrated60EventFromController.EVT_COMP_MIN_TIMER_EXPIRED,
    Integrated60EventFromController.EVT_FORCE_ICE_FLIP,
    Integrated60EventFromController.EVT_FORCE_ICE_FLIP_COMPLETE,
    Integrated60EventFromController.EVT_EXCL_PERIPH_ON,
    Integrated60EventFromController.EVT_GEARBOX_TIMER_EXPIRED,
}
import time
from .staticVariable.crc16_ansi_table import integrated_60cm_crc16_ansi_table
from .staticVariable.commlon_enum import *
from .staticVariable.controller_event_enum import *
from .staticVariable.ui_event_enum import * 
import serial
import sys
if sys.platform != 'win32':
    import terimos
import logging
import threading
import queue
import serial
from serial.serialutil import SerialException
from typing import Union

class CommLonMsg():
    """
    The `CommLonMsg` class serves as a communication interface between a controller and a display unit. 
    It encapsulates the logic for constructing, sending, and receiving CommLon messages following a specific data structure.

    ## CommLon Message Data Structure
    - **Structure**: [l2a header] [l2b header] [sid] [did] [seq no] [cmd] [data] [crc32]
    - **Size**:       1 byte       2 bytes      1     1     1        1     Variable    2 bytes

    ### Layer 2A Header (Most significant to least):
    - 6 bits: Delta backlog
    - 1 bit : Alternative path
    - 1 bit : Priority bit (least significant bit)

    ### Layer 2B Header (Most significant to least):
    - 4  bits: ID size (in number of bytes; most significant nibble)
    - 12 bits: Data size (in number of bytes)

    All other components are 1-byte each, except for `data`, whose size is dictated by the 12-bit field in the Layer 2B header, and `crc32`, which is 32 bits.

    ## Example Message Construction
    - **Layer 2A header**: `0x40`  
      Delta backlog is 1, i.e., one message expected as a result of this message. It is not a priority packet.
    - **Layer 2B header**: `0x1004`  
      ID size is 1 byte; Data size is 4 bytes.
    - **Source ID**: `0x02`  
      Module ID is 2.
    - **Destination ID**: `0x03`  
      Module ID is 3.
    - **Sequence number**: `0xA5`  
      Identification number of this message is 0xA5.
    - **Command**: `0xB9`  
      The command is block read.
    - **Data**: `0x00 0x10 0x00 0x10`  
      Read from address 0x10 to 0x10 (1 return byte expected).
    - **CRC32**: `0x?? 0x??`  
      Calculated 32-bit CRC value for the entire packet.

    """
    # static private variable for this class
    # NOTE: _max_num_of_sent_packet_retry * _echo_retry_delay_time * _max_echo_retries will tbe maximum blocking time
    _max_num_of_sent_packet_retry = 20
    _echo_retry_delay_time = 0.05
    _max_echo_retries = 5
    _maxNumOfTries = 10

    _slots_ = ('_pktSend', '_destId', '_srcId', '_seqNum', '_rxedData', '_rxedCmd', '_serialComms')

    def __init__ (self, usbPort="/dev/commlon0", baud=19200, destId=0x91):
        """
        Initializes the CommLonMsg instance with the given parameters.

        Args:
            usbPort (str, optional): _description_. Defaults to "/dev/commlon0".
            baud (int, optional): _description_. Defaults to 19200.
            destId (hexadecimal, optional): _description_. Defaults to 0x91.
        """
        try:
            self._logger = logging.getLogger(__class__.__name__)
            self._serialComms = serial.Serial(port=usbPort, baudrate=baud, timeout=0.1)
            self._pktSend = None
            self._srcId = 0x00
            self._destId = destId
            self._seqNum = 0x00
            self._crc = None
            self._rxedCmd = None
            self._rxedData = None
            self._retry_count = 0
            # start comms
            self._startComms()
            self._logger.info("CommLonMsg be created")

            self._lock = threading.Lock()
            self.task_queue = queue.Queue()
            self.worker_thread = threading.Thread(target=self._process_tasks)
            self.worker_thread.daemon = True
            self.worker_thread.start()


        except SerialException:
            self._logger.error(f'Cannot open USB port at {usbPort}, please check settings')
            raise SerialException(f'Cannot open USB port at {usbPort}, please check settings')
    
    def _process_tasks(self):
        """
        Processes tasks from the queue, handling exceptions and signaling task completion.
        """
        while True:
            task, event, args = self.task_queue.get()
            try:
                result = task(*args)
                task.result = result
            except Exception as e:
                task.exception = e
            finally:
                event.set()  # Signal completion of the task
                self.task_queue.task_done()

    def _startComms(self):
        """
        Starts the communication by opening the serial port if it is not already open.
        """
        if not self._serialComms.isOpen():
            self._serialComms.open()
            self._logger.info(f'Opened serial commLonMsg')
        return

    def _stopComms(self):
        """
        Stops the communication by closing the serial port if it is open.
        """
        self._serialComms.close()
        self._logger.info(f'Closed serial commLonMsg')
        return

    def _commsRead(self, num_of_bytes: int) -> bytes:
        """
        Reads the specified number of bytes from the serial communication port.

        Args:
            num_of_bytes (int): The number of bytes to read from the serial port.

        Returns:
            bytes: The bytes read from the serial port.
        """
        bytes_list = bytearray()

        # Continue reading until the specified number of bytes is obtained
        while num_of_bytes > 0:
            available_bytes = self._serialComms.inWaiting()

            if available_bytes:
                # Read the minimum of the remaining bytes or the available bytes
                to_read = min(num_of_bytes, available_bytes)
                
                new_bytes = self._serialComms.read(to_read)
                bytes_list.extend(new_bytes)
                
                num_of_bytes -= to_read

        return bytes(bytes_list)

    # =========== Low-level data sending/recieving FNs =============
    # NOTE: These methods below are private methods should only be accessed by internal class function

    def _crc16_byte(self, crc: bytes, data: bytes)-> bytearray:
        """
        Calculates the CRC16 for a single byte.

        Args:
            crc (bytes): The current CRC value.
            data (bytes): The data byte to include in the CRC calculation.

        Returns:
            bytearray: The updated CRC value.
        """
        return (crc >> 8) ^ integrated_60cm_crc16_ansi_table[((crc & 0xff) ^ data) & 0xff]

    def _crc16_ansi(self, crc, data):
        """
        Calculates the CRC16 for a data array.

        Args:
            crc (int): The initial CRC value.
            data (bytes): The data array for CRC calculation.

        Returns:
            int: The final CRC value.
        """
        for d in data:
            crc = self._crc16_byte(crc, d)
        return crc
    
    def _TEventSuper(self, sig, sendFromCtrl=False, platform="Integrated60"):
        """
        Creates the header bytes for Static and NonStatic TEvent.

        Args:
            sig: The signal for the event.
            sendFromCtrl (bool, optional): Whether the signal is from the controller. Defaults to False.
            platform (str, optional): The platform for the event. Defaults to "Integrated60".

        Returns:
            bytearray: The header bytes for the event.
        """
        if platform == "Integrated60":
            if sendFromCtrl:
                return bytearray([sig, 0, 0]) if sig in integrated60ControllerStaticEventSet else bytearray([sig, 1, 1])
            else:
                return bytearray([sig, 0, 0]) if sig in integrated60UIStaticEventSet else bytearray([sig, 1, 1])
        elif platform == "column":
            if sendFromCtrl:
                return bytearray([sig, 0, 0]) if sig in ColumnControllerStaticEventSet else bytearray([sig, 1, 1])
            else:
                return bytearray([sig, 0, 0]) if sig in ColumnUIStaticEventSet else bytearray([sig, 1, 1])

    def _int_to_hex_string(self, int_val):
        """
        Converts an integer to a hexadecimal string.

        Args:
            int_val (int): The integer to convert.

        Returns:
            str: The hexadecimal string representation of the integer.
        """
        return f'0x{int_val:04x}'

    def _bytes_to_hex_string(self, byte_array):
        """
        Converts a byte array to a hexadecimal string.

        Args:
            byte_array (bytes): The byte array to convert.

        Returns:
            str: The hexadecimal string representation of the byte array.
        """
        hex_list = [f'0x{b:04x}' for b in byte_array]
        hex_string = ', '.join(hex_list)
        return hex_string
        
    def _create_packet(self, cmd: bytes, msg, sendFromCtrl=False)-> bytearray:
        """
        Generates the full CommLon packet based on the given command and message.

        Args:
            cmd (bytes): The command to send.
            msg (int | list): The message to send.
            sendFromCtrl (bool, optional): Whether the packet is sent from the controller. Defaults to False.

        Returns:
            bytearray: The full CommLon packet.
        """

        if (cmd == CommLonCmds.Acked or cmd == CommLonCmds.NonAcked):
            if sendFromCtrl:
                # set src is controller and dest be display
                self._srcId = 0x91
                self._destId = 0x05
            else:
                # set src is display and dest be controller 
                self._srcId = 0x05
                self._destId = 0x91
        else:
            if sendFromCtrl:
                self._srcId = 0xAA
                self._destId = 0x05
            else:
                self._srcId = 0xAA
                self._destId = 0x91
        '''
        NOTE:
        HeaderData list explaination:
        index in the list: element in this index -> meaning of the element in CommLon
        
        0: 0x04 -> l2a header
        1: 0x10 -> l2b header MSB
        2: length of data bytes -> l2b header LSB
        3: 0x05 -> source id
        4: 0x91 -> destination id
        5: seq number -> identification number 
        6: cmd -> command
        7-x: data -> x depend on the number of data
        x+1-x+2: crc bytes
        '''
        headerData = bytearray([0x04, 0x10, len(msg), self._srcId, self._destId, self._seqNum, cmd])
        data = bytearray(msg)
        pkt = headerData + data
        crc = self._crc16_ansi(0xFFFF, pkt)
        fullPkt = bytearray(pkt) + bytearray([(crc >> 8), (crc & 0xFF)])
        return fullPkt
    
    def _read_packet(self):
        """
        Reads an ACK packet from the controller with a maximum waiting time of 10 seconds.
        Updates instance variables with received data if a valid packet is received.

        Returns:
            int or None: 1 if a valid packet is received; None otherwise.
        """
        read_result = self._read_and_verify_headers_and_data()
        if read_result is None:
            return None
        data, command = read_result
        self._process_received_packet(data, command)
        return 1

    def _read_and_verify_headers_and_data(self):
        """
        Reads and verifies the header and data from the communication channel. This method is responsible
        for reading various components of the packet sent over the communication channel, including headers, 
        sequence ID, command, data, and CRC checksum. It then verifies the integrity of the received packet 
        by comparing the generated and received CRC, checking the sequence number, and validating the source ID.
        
        HeaderData List Explanation:
            0: 0x04          -> l2a header: Indicates the beginning of the Layer 2 header
            1: 0x10          -> l2b header MSB: Most Significant Byte of the Layer 2 header
            2: length of data bytes -> l2b header LSB: Least Significant Byte indicating the length of the data segment
            3: 0x05          -> source id: Identifier for the source of the packet
            4: 0x91          -> destination id: Identifier for the destination of the packet
            5: seq number    -> identification number: Sequence number for ordering packets
            6: cmd           -> command: Command to be executed
            7-x: data        -> x depends on the number of data bytes: The actual payload data
            x+1-x+2: crc bytes -> CRC checksum for packet integrity

        Returns:
            tuple | None: A tuple containing the data and the command if the received packet is valid.
                Specifically, the first element is a list of data bytes and the second element is a list containing the command byte.
                An exception is raised if the packet is found to be invalid, facilitating robust error handling.
        """
        lHdrs = self._commsRead(3)
        header = self._commsRead(2)
        seqId = self._commsRead(1)
        command = self._commsRead(1)
        len_data_bytes = lHdrs[2]
        data = self._commsRead(len_data_bytes)
        crc = self._commsRead(2)  # Read CRC32 bytes

        # checking the received packet is correct
        rece_pkt = bytearray([*lHdrs, *header, *seqId, *command, *data])
        generate_crc = self._crc16_ansi(0xFFFF, rece_pkt)
        # checking crc and seqid and received packet destId with sent packet srcId
        if generate_crc != int.from_bytes(crc, 'big') or int.from_bytes(seqId, 'big') != self._seqNum or header[1] != self._srcId:
            return None
        return data, command

    def _process_received_packet(self, data, command):        
        """
        Processes the received packet, updates the state variables, and increments the sequence number.
        
        Parameters:
            data (list): The received data.
            command (list): The received command.
        
        Returns:
            None
        """
        self._pktSend = True
        self._rxedData = list(data)
        self._rxedCmd = command[0]
        self._seqNum = (self._seqNum + 1) % 256

    def _send_packet(self, command, message, ignore_echo_block=False, send_from_ctrl=False):
        """
        Sends a packet to the controller and returns the acknowledgment if expected.

        Args:
            command (bytes): The command to send.
            message (bytes): The message payload.
            ignore_echo_block (bool, optional): Whether to ignore echo block commands. Defaults to False.
            send_from_ctrl (bool, optional): Whether the packet is being sent from the controller. Defaults to False.

        Returns:
            list or None: ACK message if expected, None otherwise.
        """
        self._pktSend = False
        max_retries = self._maxNumOfTries

        for _ in range(max_retries + 1):
            full_packet = self._create_packet(command, message, send_from_ctrl)
            self._flush_serial_buffers()

            if self._send_and_validate_echo(full_packet):
                if command == CommLonCmds.NonAcked:
                    self._retry_count = 0
                    return None

                read_result = self._read_packet()
                if read_result is not None:
                    self._retry_count = 0
                    return self._rxedData

            self._handle_retry()

    def _send_and_validate_echo(self, packet):
        """
        Sends a packet and validates the echo from the hardware.

        Args:
            packet (bytes): The packet to send.

        Returns:
            bool: True if the echo is validated, False otherwise.
        """
        for i in range(self._max_echo_retries):
            self._serialComms.write(packet)
            if packet == self._commsRead(len(packet)):
                return True
            self._logger.debug(f'Retry for receiving hardware echo message - {i+1}')
            time.sleep(self._echo_retry_delay_time)
            self._flush_serial_buffers()
        return False

    def _handle_retry(self):
        """
        Handles retries for sending a packet.

        Raises:
            SerialException: If the maximum number of retries is exceeded.
        """
        self._logger.warn("Send packet retry")
        if self._retry_count > self._max_num_of_sent_packet_retry:
            self._logger.error("Couldn't get a valid reply back from controller")
            raise SerialException("Couldn't get a valid reply back from controller")
        self._retry_count += 1

    def _flush_serial_buffers(self):
        """
        Flushes the input and output buffers of the serial communication.

        Logs an error if there is a termios error.
        """
        try:
            self._serialComms.flushInput()
            self._serialComms.flushOutput()
        except Exception:
            self._logger.error("Got a termios.error when trying to reset input buffer")

    # =========== Read/Write Helper Functions =============

    def clearEEPROMBlock(self, eeprom_addresses):
        """
        Clears the specified EEPROM block.

        Args:
            eeprom_addresses (list): List containing the start and end addresses of the EEPROM block.

        Returns:
            bool: True if the EEPROM block is cleared successfully.
        """
        event = threading.Event()
        task = lambda addr_start, addr_end: self._perform_clearEEPROMBlock(addr_start, addr_end)
        self.task_queue.put((task, event, (eeprom_addresses[0], eeprom_addresses[1])))
        event.wait()  # Wait here until the task is processed
        if hasattr(task, 'exception'):
            raise task.exception
        return task.result

    def _perform_clearEEPROMBlock(self, start_address, end_address):
        """
        Clears the specified EEPROM block.

        Args:
            start_address (int): The start address of the EEPROM block.
            end_address (int): The end address of the EEPROM block.

        Returns:
            bool: True if the EEPROM block is cleared successfully.
        """
        with self._lock:    
            for current_address in range(start_address, end_address + 1):
                for _ in range(self._maxNumOfTries):
                    rx_data = self._clear_single_eeprom_address(current_address)
                    # current_val = self.blockRead([current_address,current_address])[0]
                    current_val = 0xFF
                    if rx_data == [0] and current_val == 0xFF:
                        self._logger.info(f'Current EEPROM address: {self._int_to_hex_string(current_address)} - value: {current_val}')
                        self._logger.info(f'Cleared EEPROM address: {self._int_to_hex_string(current_address)}')
                        break
                    else:
                        self._logger.warn(f'Clear operation for EEPROM address: {self._int_to_hex_string(current_address)} - Receive rx_data: {rx_data}, current eeprom value: {current_val}')
                        self._logger.warn(f'Retrying clear operation for EEPROM address: {self._int_to_hex_string(current_address)}')
                else:
                    self._logger.error(f'Failed to clear EEPROM address: {self._int_to_hex_string(current_address)} after {self._maxNumOfTries} retries.')
            return True

    def _clear_single_eeprom_address(self, address):
        """
        Clears a single EEPROM address.

        Args:
            address (int): The EEPROM address to clear.

        Returns:
            list: Received data from the _send_packet method.
        """
        sMSB = address >> 8
        sLSB = address & 0xFF
        msg = [sMSB, sLSB, 0xFF]
        return self._send_packet(CommLonCmds.BlockWrite, msg)
    
    def blockWrite(self, eeproaddress_list: list, values: Union[int, list]):
        """
        Writes values to a block of RAM or EEPROM memory, handling special address ranges and chunking large writes.

        Args:
            eeproaddress_list (list): List containing the start and end addresses.
            values (Union[int, list]): The values to write.

        Returns:
            bool: True if the block is written successfully.
        """
        event = threading.Event()
        task = lambda addr, values: self._perform_blockWrite(addr, values)
        self.task_queue.put((task, event, (eeproaddress_list, values)))
        event.wait()  # Wait here until the task is processed
        if hasattr(task, 'exception'):
            raise task.exception
        return task.result

    def _perform_blockWrite(self, address_list: list, values: Union[int, list]):
        """
        Writes values to a block of RAM or EEPROM memory, handling special address ranges and chunking large writes.

        Args:
            address_list (list): List containing the start and end addresses.
            values (Union[int, list]): The values to write.

        Returns:
            bool: True if the block is written successfully.
        """
        with self._lock:
            start_address, end_address = address_list

            # Convert single value to list for uniform processing
            if isinstance(values, int):
                values = [values] * (end_address - start_address + 1)

            if start_address == end_address:
                self._write_and_verify_single_address(start_address, values[0])
            elif len(values) != end_address - start_address + 1:
                self._log_error_and_raise("Length of values does not match address range.", ValueError)
            elif start_address >= 0x9000:
                self._write_and_verify_range_eeprom(start_address, end_address, values)
            else:
                self._write_and_verify_range(start_address, end_address, values)
            return True

    def _write_and_verify_single_address(self, address, value):
        """
        Writes and verifies a single value at a specific address.

        Args:
            address (int): The address to write to.
            value (int): The value to write.
        """
        self._write_single_address_and_retry(address, value)
        self._verify_written_value(address, [value])

    def _write_and_verify_range_eeprom(self, start_address, end_address, values):
        """
        Handles EEPROM range write and verification logic for addresses starting from 0x9000.

        Args:
            start_address (int): The start address of the range.
            end_address (int): The end address of the range.
            values (list): The values to write.
        """
        for index, current_address in enumerate(range(start_address, end_address + 1)):
            self._write_single_address_and_retry(current_address, values[index])
            self._verify_written_value(current_address, [values[index]])

    def _write_and_verify_range(self, start_address, end_address, values):
        """
        Writes and verifies a range of values, chunking the write operations.

        Args:
            start_address (int): The start address of the range.
            end_address (int): The end address of the range.
            values (list): The values to write.
        """
        max_chunk_size = 25
        for i in range(0, len(values), max_chunk_size):
            chunk = values[i:i + max_chunk_size]
            chunk_start_address = start_address + i
            self._write_chunk_and_retry(chunk_start_address, chunk)
            self._verify_written_value(chunk_start_address, chunk, len(chunk))

    def _write_single_address_and_retry(self, address, value):
        """
        Attempts to write a single value to an address, retrying up to _maxNumOfTries times.

        Args:
            address (int): The address to write to.
            value (int): The value to write.
        """
        for _ in range(self._maxNumOfTries):
            rx_data = self._write_single_address(address, value)
            if rx_data == [0]:
                self._logger.info(f"BlockWrite: Wrote value {value} to address: {self._int_to_hex_string(address)}")
                return
            else:
                self._logger.warn(f"Retrying write operation for address: {self._int_to_hex_string(address)}")
        self._logger.error(f"Failed to write to address: {self._int_to_hex_string(address)} after {self._maxNumOfTries} retries.")

    def _write_chunk_and_retry(self, start_address, chunk):
        """
        Writes a chunk of values starting from a specific address, retrying up to _maxNumOfTries times.

        Args:
            start_address (int): The starting address of the chunk.
            chunk (list): The chunk of values to write.
        """
        msg = [start_address >> 8, start_address & 0xFF] + chunk
        for _ in range(self._maxNumOfTries):
            rx_data = self._send_packet(CommLonCmds.BlockWrite, msg)
            if rx_data == [0]:
                self._logger.info(f"BlockWrite: Wrote value {chunk} to address: {self._int_to_hex_string(start_address)} - {self._int_to_hex_string(start_address+len(chunk)-1)}")
                break  # Exit the retry loop on success
        else:  # Executed only if the loop was not broken out of
            self._logger.error(f"Failed to write chunk starting at address: {self._int_to_hex_string(start_address)} after {self._maxNumOfTries} retries.")

    def _verify_written_value(self, start_address, expected_values, length=1):
        """
        Verifies that the expected values have been written starting from a specific address.

        Args:
            start_address (int): The starting address of the range.
            expected_values (list): The expected values.
            length (int, optional): The number of bytes to verify. Defaults to 1.
        """
        return

    def _write_single_address(self, address: int, value: Union[int, list]):
        """
        Writes a value to a single address.

        Args:
            address (int): The address to write to.
            value (Union[int, list]): The value to write.

        Returns:
            list: Received data from the _send_packet method.
        """
        if isinstance(value, list):
            value = int(value[0])  # Convert list to int, assuming list contains only one int

        msg = [address >> 8, address & 0xFF, value]
        return self._send_packet(CommLonCmds.BlockWrite, msg)

    def _log_error_and_raise(self, message, exception_type):
        """
        Logs an error message and raises a specified exception.

        Args:
            message (str): The error message to log.
            exception_type (Exception): The type of exception to raise.
        """
        self._logger.error(message)
        raise exception_type(message)


    def blockRead(self, address_list):
        """
        Reads a block of memory from EEPROM between the start and end addresses.

        Args:
            address_list (list): List containing the start and end addresses in EEPROM.

        Returns:
            list: List of integers representing the read values from EEPROM.
        """

        event = threading.Event()
        task = lambda addrStart, addrEnd: self._perform_blockRead(addrStart, addrEnd)
        self.task_queue.put((task, event, (address_list[0], address_list[1])))
        event.wait()  # Wait here until the task is processed
        if hasattr(task, 'exception'):
            raise task.exception
        return task.result
    
    def _perform_blockRead(self, start_address, end_address) -> list:
        """
        Reads a block of memory from EEPROM between the start and end addresses.

        Args:
            start_address (int): The starting address of the block.
            end_address (int): The ending address of the block.

        Returns:
            list: List of integers representing the read values from EEPROM.
        """
        with self._lock:
            total_data = []
            block_size = 0x1F

            for current_block_start in self._generate_block_addresses(start_address, end_address, block_size):
                block_end = min(current_block_start + block_size - 1, end_address)
                msg = self._format_block_message(current_block_start, block_end)

                read_values = self._send_packet(CommLonCmds.BlockRead, msg)
                if read_values:
                    total_data.extend(read_values)
                else:
                    self._logger.error(f"Failed to read block starting at {self._int_to_hex_string(current_block_start)}")
                    raise ValueError(f"Failed to read block starting at {self._int_to_hex_string(current_block_start)}")

            return total_data

    def _generate_block_addresses(self, start: int, end: int, block_size: int):
        """
        Generates the start addresses for each block to be read.

        Args:
            start (int): The start address.
            end (int): The end address.
            block_size (int): The size of each block.

        Yields:
            int: The start address of each block.
        """
        for address in range(start, end + 1, block_size):
            yield address

    def _format_block_message(self, start: int, end: int) -> list:
        """
        Formats the message to send for reading a block.

        Args:
            start (int): The start address of the block.
            end (int): The end address of the block.

        Returns:
            list: A list containing the formatted message.
        """
        sMSB, sLSB = divmod(start, 0x100)
        eMSB, eLSB = divmod(end, 0x100)
        return [sMSB, sLSB, eMSB, eLSB]



    def memRead(self, address: int, bytes_to_read: int = 1, readController=True):
        """
        Reads the COMMDEF table starting from the given address for the specified number of bytes.

        Args:
            address (int): The starting address in the COMMDEF table.
            bytes_to_read (int, optional): The number of bytes to read. Defaults to 1.
            readController (bool, optional): Whether to read from the controller. Defaults to True.

        Returns:
            int: The integer representation of the read bytes.
        """
        event = threading.Event()
        task = lambda addr,b_t_r, r_c : self._perform_memRead(addr, b_t_r, r_c)
        self.task_queue.put((task, event, (address, bytes_to_read, readController)))
        event.wait()  # Wait here until the task is processed
        if hasattr(task, 'exception'):
            raise task.exception
        return task.result


    def _perform_memRead(self, address: int, bytes_to_read: int = 1, readController=True) -> int:
        """
        Reads the COMMDEF table starting from the given address for the specified number of bytes.

        Args:
            address (int): The starting address in the COMMDEF table.
            bytes_to_read (int, optional): The number of bytes to read. Defaults to 1.
            readController (bool, optional): Whether to read from the controller. Defaults to True.

        Returns:
            int: The integer representation of the read bytes.
        """
        with self._lock:
            value = 0
            for offset in range(bytes_to_read):
                current_address = address + offset
                msg = self._format_memory_read_message(current_address)
                for i in range(self._maxNumOfTries):
                    read_byte = self._read_single_byte(msg, readController)
                    if read_byte is not None:
                        break
                    self._logger.warn(f'MemRead on address: {self._int_to_hex_string(current_address)} return None, retry to read it again - {i}')
                else:
                    self._logger.error(f'MemRead on address: {self._int_to_hex_string(current_address)} return None, retry to read it again - {i}')
                    raise ValueError(f'Read CommDef address: {self._int_to_hex_string(current_address)} failed after retry {self._maxNumOfTries} times')
                self._logger.info(f"Read CommDef address: {self._int_to_hex_string(current_address)}, value is {read_byte}")
                value = (value << 8) + read_byte
            return value

    def _format_memory_read_message(self, address: int) -> list:
        """
        Formats the message for reading memory.

        Args:
            address (int): The address to read from.

        Returns:
            list: A list containing the formatted message.
        """
        sMSB, sLSB = divmod(address, 0x100)
        return [sMSB, sLSB, 0x00, 0x00]

    def _read_single_byte(self, msg: list, readController: bool) -> Union[int, None]:
        """
        Reads a single byte from memory.

        Args:
            msg (list): The message to send for reading.
            readController (bool, optional): Whether to read from the controller. Defaults to True.

        Returns:
            int or None: The read byte as an integer, or None if the read operation failed.
        """
        send_from_ctrl = not readController
        response = self._send_packet(CommLonCmds.MemReadWrite, msg, send_from_ctrl=send_from_ctrl)
        if response:
            return response[0]
        else:
            return None

    def memWrite(self, address: int, value: int, bytes_to_read: int = 1, setController=True):
        """
        Writes the given value to the COMMDEF table starting from the specified address.

        Args:
            address (int): The starting address in the COMMDEF table.
            value (int): The value to write.
            bytes_to_read (int, optional): The number of bytes to write. Defaults to 1.
            setController (bool, optional): Whether to write to the controller. Defaults to True.

        Returns:
            bool: True if the value is written successfully.
        """
        event = threading.Event()
        task = lambda addr,v, b_t_r, s_c : self._perform_memWrite(addr, v, b_t_r, s_c)
        self.task_queue.put((task, event, (address, value, bytes_to_read, setController)))
        event.wait()  # Wait here until the task is processed
        if hasattr(task, 'exception'):
            raise task.exception
        return task.result


    def _perform_memWrite(self, address: int, value: int, bytes_to_write: int = 1, setController=True):
        """
        Writes the given value to the COMMDEF table starting from the specified address.

        Args:
            address (int): The starting address in the COMMDEF table.
            value (int): The value to write.
            bytes_to_write (int, optional): The number of bytes to write. Defaults to 1.

        Returns:
            bool: True if the value is written successfully.
        """
        with self._lock:
            current_address = address
            for i in reversed(range(bytes_to_write)):
                byte_value = (value >> (8 * i)) & 0xFF
                msg = self._format_memory_write_message(current_address, byte_value)
                
                for _ in range(self._maxNumOfTries):
                    rx_data = self._write_single_byte(msg, setController)
                    if rx_data == [0]:
                        self._logger.info(f"Wrote value {byte_value} to CommDef address: {self._int_to_hex_string(current_address)}")
                        break
                    else:
                        self._logger.warning(f"Retrying write operation for CommDef address: {self._int_to_hex_string(current_address)}")
                else:
                    self._logger.error(f"Failed to write to CommDef address: {self._int_to_hex_string(current_address)} after {self._maxNumOfTries} retries.")
                current_address += 1
            return True


    def _format_memory_write_message(self, address: int, byte_value: int) -> list:
        """
        Formats the message for writing memory.

        Args:
            address (int): The address to write to.
            byte_value (int): The byte value to write.

        Returns:
            list: A list containing the formatted message.
        """
        sMSB, sLSB = divmod(address, 0x100)
        return [sMSB, sLSB, 0x01, byte_value]

    def _write_single_byte(self, msg: list, setController) -> int:
        """
        Writes a single byte to memory.

        Args:
            msg (list): The message to send for writing.
            setController (bool, optional): Whether to write to the controller. Defaults to True.

        Returns:
            int: The data received from the _send_packet method.
        """
        send_from_ctrl = not setController
        return self._send_packet(CommLonCmds.MemReadWrite, msg, send_from_ctrl=send_from_ctrl)



    def setResMemBit(self, address: int, bit_position: int, reset: bool = False):
        """
        Sets or resets a specific bit in the COMMDEF memory table at a given address.

        Args:
            address (int): Address in the COMMDEF table.
            bit_position (int): Bit position (0-7) to set or reset.
            reset (bool, optional): Whether to reset the bit. Defaults to False (sets the bit).

        Returns:
            bool: True if the bit is set/reset successfully.
        """
        event = threading.Event()
        task = lambda addr, b_p, rst : self._perform_setResMemBit(addr, b_p, rst)
        self.task_queue.put((task, event, (address, bit_position, reset)))
        event.wait()  # Wait here until the task is processed
        if hasattr(task, 'exception'):
            raise task.exception
        return task.result

    def _perform_setResMemBit(self, address: int, bit_position: int, reset: bool = False):
        """
        Sets or resets a specific bit in the COMMDEF memory table at a given address.

        Args:
            address (int): Address in the COMMDEF table.
            bit_position (int): Bit position (0-7) to set or reset.
            reset (bool, optional): Whether to reset the bit. Defaults to False (sets the bit).

        Returns:
            bool: True if the bit is set/reset successfully.
        """
        with self._lock:
            if not 0 <= bit_position <= 7:
                self._logger.error(f'Bit poistion need to be in range of 0 - 7')
                raise ValueError(f'Bit poistion need to be in range of 0 - 7')
            
            msb, lsb = divmod(address, 0x100)
            # if reset arg is false, srBit is true i.e. set bit or vice versa (srBit stands for set/reset bit)
            srBit = reset == False
            mask = 1 << bit_position
            if srBit == False:
                mask = ~mask & 0xFF
            msg = [msb, lsb, srBit, mask]

            for _ in range(self._maxNumOfTries):
                rx_data = self._send_packet(CommLonCmds.BitStr_Mask, msg)
                if rx_data == [0]:
                    self._logger.info(f'Successfully set/reset bit at address {self._int_to_hex_string(address)}, bit position {bit_position}')
                    break
                else:
                    self._logger.warning(f'Failed to set/reset bit at address {self._int_to_hex_string(address)}, bit position {bit_position}. Retrying...')
            else:
                self._logger.error(f'Failed to set/reset bit at address {self._int_to_hex_string(address)}, bit position {bit_position} after {self._maxNumOfTries} retries.')
            return True

    def setResMemBytes(self, address: int, byte_value: int, reset: bool = False):
        """
        Sets or resets multiple bits in the COMMDEF memory table at a given address.

        Example 1
        "SEND MESSAGE 1 0 false $91 $A1 $01 $19 $00 $E3"
        -> "$A1" -> "Set memory bit"
        -> "$01 $19" -> "Address 0x0119"
        -> "$00 $E3" -> "00" mean reset, "E3" -> 1110 0011

        For reset, we only care about "0" in binary code, which in this case "1110 0011". However, setResMemBit function
        can only handle one "0" at each function call. To reset all the three bit of "0", we need to call this function
        three time with different bitPlace: "1111 1011" (bit place 2), "1111 0111" (bit place 3) and "1110 1111" (bit place 4)
        setResMemBit(0x0119, 2, True)
        setResMemBit(0x0119, 3, True)
        setResMemBit(0x0119, 4, True)

        Example 2
        "SEND MESSAGE 1 0 false $91 $A1 $01 $19 $01 $0C"
        -> "$A1" -> "Set memory bit"
        -> "$01 $19" -> "Address 0x0119"
        -> "$01 $0C" -> "01" mean set, "0C" -> 0000 1100

        For set, we only care about "1" in binary code, which in this case "0000 1100". However, setResMemBit function
        can only handle one "1" at each function call. To set all the two bit of "1", we need to call this function
        two time with different bitPlace: "0000 0100" (bit place is 2), "0000 1000" (bit place is 3)
        setResMemBit(0x0119, 2)
        setResMemBit(0x0119, 3)
        Args:
            address (int): Address in the COMMDEF table.
            byte_value (int): Byte value representing the bits to set or reset.
            reset (bool, optional): Whether to reset the bits. Defaults to False (sets the bits).
        """
        binary_string = format(byte_value, '08b')  # Convert to 8-bit binary string
        for i, bit in enumerate(reversed(binary_string)):
            if (bit == '1' and not reset) or (bit == '0' and reset):
                self.setResMemBit(address, i, reset)
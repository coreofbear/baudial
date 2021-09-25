# Baudial - minimalistic Python based UART console terminal

import serial
import signal
import argparse
import sys

DATA_SIZE_MAX = 255                     # Maximum data size
WAITING_TIMEOUT_S = 0.1                 # Reading timeout (in seconds)

PORT_DEFAULT = 'COM7'                   # Default UART port
BAUDRATE_DEFAULT = 115200               # Default baudrate
PARITY_DEFAULT = serial.PARITY_NONE
STOPBITS_DEFAULT = serial.STOPBITS_ONE
MSGLEN_DEFAULT = serial.EIGHTBITS

global_uart_dev = serial.Serial()

global_format = ''

# Message sending
def message(uart_dev, port):
    print(port, "->", sep='', end=' ')
    msg_str = input()

    msg_bytes = bytes()
    if 'utf-8' == global_format:
        # TODO: add \n adding argument
        # msg_str = msg_str + '\n'
        msg_bytes = str.encode(msg_str, 'utf-8')
    elif 'hex' == global_format:
        msg_bytes = bytes.fromhex(msg_str)

    uart_dev.write(msg_bytes)

# Transmission cycle
def cycle(uart_dev, port):
    while uart_dev.isOpen():
        message(uart_dev, port)

        msg_bytes = uart_dev.read(DATA_SIZE_MAX)
        msg_str = str()
        if 'utf-8' == global_format:
            msg_str = str(msg_bytes, 'utf-8')
        elif 'hex' == global_format:
            msg_str = msg_bytes.hex()

        if 0 != len(msg_str):
            print(msg_str)
        uart_dev.flush()

# SIGING handler
def sigint_handler(sig, frame):
    print('\n[baudial] You pressed Ctrl+C. Exit from script.')
    if global_uart_dev.isOpen():
            global_uart_dev.close()
    sys.exit(0)

# Program entry point
def main():
    signal.signal(signal.SIGINT, sigint_handler)
    
    parser = argparse.ArgumentParser(description='Program arguments')
    parser.add_argument('--port', 
                    dest = 'port', 
                    default = PORT_DEFAULT,
                    help = 'UART port (COM7 by default)')
    parser.add_argument('--rate', 
                    dest = 'rate', 
                    default = BAUDRATE_DEFAULT,
                    help = 'Baudrate (115200 by default)')
    parser.add_argument('--parity', 
                    dest = 'parity', 
                    default = PARITY_DEFAULT,
                    help = 'Parity (N by default)')
    parser.add_argument('--stopbits', 
                    dest = 'stopbits', 
                    default = STOPBITS_DEFAULT,
                    help = 'Stop bits (1 by default)')
    parser.add_argument('--msglen', 
                    dest = 'msglen', 
                    default = MSGLEN_DEFAULT,
                    help = 'UART message length in bits (8 by default)')
    parser.add_argument('--format', 
                    dest = 'format', 
                    default = 'hex',
                    help = 'Format type ("hex" by default))')
    args = parser.parse_args()

    global global_uart_dev
    global_uart_dev = serial.Serial(
        port = args.port,
        baudrate = args.rate,
        parity = args.parity,
        stopbits = args.stopbits,
        bytesize = args.msglen,
        timeout = WAITING_TIMEOUT_S
    )

    global global_format
    global_format = args.format

    if ('utf-8' != global_format) and ('hex' != global_format):
        print("[baudial] Invalid format type '", global_format, "'.", sep='')
        sys.exit(0)

    print("[baudial] Open ", args.port, 
          " port with baudrate - ", args.rate, 
          "; parity - ", args.parity, 
          "; stop bits - ", args.stopbits,
          "; message length - ", args.msglen, ".", sep='')
    cycle(global_uart_dev, args.port)
    print("[baudial] ", args.port, " port was closed.")
    sys.exit(0)
    
main()
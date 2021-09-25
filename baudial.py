# Baudial - minimalistic Python based UART console terminal

import serial
import signal
import argparse
import sys

DATA_SIZE_MAX = 255                     # Maximum data size
WAITING_TIMEOUT_S = 0.1                 # Reading timeout (in seconds)
PORT_DEFAULT = 'COM7'                   # Default UART port
BAUDRATE_DEFAULT = 115200               # Default baudrate

global_uart_dev = serial.Serial()

# Message sending
def message(uart_dev, port):
    print(port, "->", sep='', end=' ')
    msg_str = input()
    uart_dev.write(str.encode(msg_str))

# Transmission cycle
def cycle(uart_dev, port):
    while uart_dev.isOpen():
        message(uart_dev, port)
        msg_to_cli = uart_dev.read(DATA_SIZE_MAX)
        if 0 != len(msg_to_cli):
            print(msg_to_cli)
        uart_dev.flush()

# SIGING handler
def sigint_handler(sig, frame):
    print('\n[baudial] You pressed Ctrl+C. Exit from script')
    if global_uart_dev.isOpen():
            global_uart_dev.close()
    sys.exit(0)

# Program entry point
def main():
    signal.signal(signal.SIGINT, sigint_handler)
    print("[baudial] Script started")
    
    parser = argparse.ArgumentParser(description='Program arguments')
    parser.add_argument('--port', 
                    dest='port', 
                    default=PORT_DEFAULT,
                    help='UART port')
    # TODO: and baudrate, parity, stopbits and bytesize arguments
    args = parser.parse_args()

    global global_uart_dev
    global_uart_dev = serial.Serial(
        port = args.port,
        baudrate = BAUDRATE_DEFAULT,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = WAITING_TIMEOUT_S
    )

    print("[baudial] ", args.port, " port was opened")
    cycle(global_uart_dev, args.port)
    print("[baudial] ", args.port, " port was closed")
    sys.exit(0)
    
main()
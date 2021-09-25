# baudial
Baudial - minimalistic Python based UART console terminal

## Installing dependencies 
Execute ```pip install -r reqs.txt``` to install dependencies

### Usage

1. Define using UART port on your system. 

2. Run terminal with ```python baudial.py --port=COM7```. For example:

    List of possible arguments:
    - *--port* UART port (COM7 by default)
    - *--rate* Baudrate (115200 by default)
    - *--parity* Parity (N by default)
    - *--stopbits* Stop bits (1 by default)')
    - *--msglen* UART message length in bits (8 by default)')
    - *--format* Format type ("hex" by default))')

3. 
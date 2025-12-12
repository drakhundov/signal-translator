# Signal Translator

This project aims at implementing various **encoding/decoding** and
**modulation/demodulation** techniques used in computer communications.
I have implemented a basic user interface (CLI) and several schemes listed below.

## Algorithms implemented
| Input Data        | Output Signal           | Mode                 |
| ----------------- | ----------------------- |----------------------|
| Digital → Digital | Digital line coding     | NRZ, Manchester, AMI |
| Digital → Analog  | Modulation              | ASK, FSK, PSK        |
| Analog → Digital  | Sampling + quantization | PCM, Delta           |
| Analog → Analog   | Analog modulation       | AM, FM, PM           |

## Usage
```bash
  python3 main.py
  
 >> Select a transmission mode:
 >> ... # options
 >> 1 # digital to digital
 
 >> Select an encoding/modulation scheme:
 >> ... # options
 >> 2 # Manchester Code
 
 >>  Input source (Computer A): # text message or raw bit sequence
 >> 0 # text message
 
 >> Enter message to transmit: <user_input>
 
 >> Show the transmitted signal? (y/n) # shows the signal as a plot
 
 >> Received (Computer B): <decoded_message>
```


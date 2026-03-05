# Brookshear Machine Emulator
### Inspired by Glenn Brookshear's "Computer Science: An Overview" (11th Edition)

This project is a Python-based implementation of the virtual machine architecture 
described in Glenn Brookshear's seminal textbook. It simulates a CPU with 16 
registers and 256 bytes of RAM.

---
## The Instruction Set Architecture (ISA)

| Opcode | Instruction | Description |
| :--- | :--- | :--- |
| **1** | LOAD | Load register $R$ with the bit pattern found in memory cell $XY$. |
| **2** | LOAD | Load register $R$ with the bit pattern $XY$. |
| **3** | STORE | Store the bit pattern in register $R$ into memory cell $XY$. |
| **4** | MOVE | Copy the bit pattern in register $X$ to register $Y$. |
| **5** | ADD | Add bit patterns in registers $X$ and $Y$ (2's complement), result in $R$. |
| **7** | OR | Bitwise OR of registers $X$ and $Y$, result in $R$. |
| **8** | AND | Bitwise AND of registers $X$ and $Y$, result in $R$. |
| **9** | XOR | Bitwise XOR of registers $X$ and $Y$, result in $R$. |
| **A** | ROTATE | Rotate the bit pattern in register $R$ to the right $Y$ times. |
| **B** | JUMP | Jump to instruction at address $XY$ if Reg $R$ equals Reg 0. |
| **C** | HALT | Terminate the program execution. |

**Note:** The code expects a hexadecimal value in the format [ **Opcode** | **R** ] [ **X** | **Y** ]. (i.e 1A2B)

---
## Usage Guide

Here's a minimal version to run a code in the Brookshear machine simulator.

```python
from Machine_language_CORE import Machine

cpu = Machine()
cpu.load(CODE_STRING)
cpu.run()
```

The **CODE_STRING** must be a non-empty Python string in one of the following formats.

```python
CODE_STRING = "ORXYORXYORXY ..."

CODE_STRING = """
ORXY
ORXY
ORXY ...
"""

CODE_STRING = """
ORXY ; Comment No.1
ORXY ; Comment No.2

ORXY ; Comment No.3 ...
"""
```

Additionally you can customize the way the machine is run by changing the following properties.

```python
# Disable the printing logs of the CPU decode
cpu.debug = False

"""Configure the printing window"""
# Printing the last i rows
cpu.ROWS = i
# Starting at column j
cpu.COLS = j
```

Also the user is able to change the ISA as needed.

```python
# You can ignore inputs given by either (_) or (*args)
def _NEW_ISA_OPERATION(o1, o2, o3, next_byte, code):
    """ YOUR ISA LOGIC HERE """

# The empty opcodes are 0xD, 0xE, 0xF
cpu.ISA[0xD] = _NEW_ISA_OPERATION
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

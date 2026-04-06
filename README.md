# Brookshear Machine Emulator
### Inspired by Glenn Brookshear's "Computer Science: An Overview" (11th Edition)

This project is a Python-based implementation of the virtual machine architecture 
described in Glenn Brookshear's seminal textbook. It simulates a CPU with 16 
registers and 256 bytes of RAM.

**Also included:** A collection of programs that push the 256-byte limit - including 
a playable Snake game, Conway's Game of Life, and a sorting visualizer, all written 
in raw hexadecimal.

## Featured Programs

What can you actually build in 256 bytes of hand-written hex? More than you'd think.

| Project | Highlights |
|---------|------------|
| [🐍 **Snake**](./Snake/) | Real-time input, collision detection, random food with validation, win state |
| [🧬 **Conway's Life**](./Conways_Game_Of_Life/) | Toroidal grid, neighbor counting via bit rotation, double buffering |
| [📊 **Sorting Visualizer**](./Sort/) | Bit-by-bit comparison sort, progress bar, audio feedback |
| [🔢 **Seven-Segment Display**](./7_Segment_Display/) | Font rendering with bit-testing, cycles through 0-F |
| [🌊 **Wave Animation**](./Wave_Animation/) | Rotating pattern using self-modifying code |

**The Challenge:** No assembler. No debugger. No comparison operators. Just hex, 
bitwise logic, and manually calculated jump offsets. One wrong byte = hours of debugging.

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
def _NEW_ISA_OPERATION(o1, o2, o3, next_byte):
    """ YOUR ISA LOGIC HERE """

# The empty opcodes are 0xD, 0xE, 0xF
cpu.ISA[0xD] = _NEW_ISA_OPERATION
```

---
## Debug Tools

Two dump utilities are available for inspecting machine state after execution.
```python
# Dumps memory and registers to memory_dump.txt as hex grid
cpu.memory_dump()

# Dumps log_buffer to log_dump.txt (requires debug=True)
cpu.log_dump()
```

### memory_dump.txt layout
```
     0  1  2 ...  F  ← Registers (r0 -> rF)
    XX XX XX ... XX  ← register values hex

    0  1   2 ...  F  ← memory indices (0 -> F)
0   XX XX XX ... XX  ← 0x00 -> 0x0F
1   XX XX XX ... XX
...
F   XX XX XX ... XX  ← 0xF0 -> 0xFF
```

---

## What I Learned Building These

**Jump offset calculation is everything.** Adding a feature means inserting bytes, 
which shifts all subsequent addresses. Every jump that crosses the insertion point 
needs recalculating. Miss one? Infinite loop or crash.

**Build iteratively, not monolithically.** Snake started as simple movement (40 bytes), 
then grew: +collision, +food, +validation, +input blocking. Each addition was surgical. 
Writing 186 bytes at once would've been impossible to debug.

**Bit manipulation replaces entire algorithms.** No modulo? Use `AND 0x07`. 
No comparison operator? Scan bits MSB-first. Constraints force creativity.

**Self-modifying code is elegant under pressure.** When space is tight, storing 
computed addresses and loading from them beats any alternative.

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

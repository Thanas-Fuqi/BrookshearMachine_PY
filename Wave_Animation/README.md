# Brookshear "Wave" Display Demo

<p align="center">
  <img src="ML_Wave_Loop.gif" alt="Brookshear Wave Animation">
</p>

This project demonstrates the extensibility of the Brookshear Emulator by adding a custom "Display Driver" opcode (`0xF`) that renders bit patterns from memory as graphics in the terminal.

## New Opcode: 0xF (Display)
The emulator has been extended with a custom function `_display`. When the machine hits an instruction starting with `F` (e.g., `F000`), it triggers the following logic:
1. **Memory Mapping:** It reads from memory address `0xF6` onwards.
2. **Binary Visualization:** Each 8-bit pattern in RAM is converted into "pixels" (`██` for 1, spaces for 0).
3. **ANSI Positioning:** Uses escape codes to lock the graphics to the top-left of the terminal.

## Property Overrides
To accommodate the visualization, the machine configuration is modified:
* **cpu.ROWS** The number of rows is changed to create a scrollable terminal loging window with the same height as the screen added.
* **cpu.COLS** The columns are changed so the logs start with a padding from the left so the screen its not overwritenn by the logs.
* **Global Delay:** The script uses `time.perf_counter()` to ensure the animation runs at a consistent frame rate (i.e. ~10 FPS), compensating for the execution overhead.

## The Wave Program
The `Wave_Loop` assembly performs bitwise rotations (`AF01`) and incremental jumps to create a moving pattern in the memory range `0xF6` - `0xFF`. Because the `DISPLAY` opcode is inside the loop, the terminal updates in real-time.

## Usage
Run the script as follows to ensure the CORE code is correctly linked

```bash
python -m Wave_Animation.ML_Wave_Loop
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

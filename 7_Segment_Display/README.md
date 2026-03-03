# Brookshear 7-Segment Hex Counter

<p align="center">
  <img src="ML_Hexadecimal.gif" alt="Brookshear Hex Animation">
</p>

This project simulates a 7-segment LED display using the Brookshear Machine. It implements a logic gate system to translate 4-bit values into visual segments, mimicking the behavior of a hardware decoder/driver (like the 74LS47 IC).

## Custom ISA Extension: Opcode 0xF
The `Machine` core is extended with a "Video Output" function. 
1. **The Display Buffer:** The machine monitors memory addresses `0xF6` through `0xFF`.
2. **Hardware Refresh:** When the `F000` instruction is executed, the current buffer is rendered.
3. **Mapping to screen:** The `_display` function displays ANSI blocks (`██` for 1 and `  ` for 0 from the binary of a line).

## Changes to parameters
* **cpu.ROWS:** It limits the amount of printed lines to match the "DISPLAY" rows visually.
* **cpu.COLS:** Margin the left side by the number of the "DISPLAY" column to not overlap one another.
* **Refresh Rate:** The `delay` is set to `1/5` (~5 FPS) to make the updates slower so that it can visually appear better.

## The core Logic
* **Pre-cursor:** In a seven segment display the bars are encoded in a `abcdefg` fashion as explained in [*Wiki*](https://en.wikipedia.org/wiki/Seven-segment_display?utm_source=chatgpt.com#Characters).
* **Lookup Table:** Addresses `00` through `3E` store the bit-patterns for Hex characters `0-F` using the said encoding.
* **Segment Bars:** `BAR A` through `BAR G` in the code are the portions that "draw" each vertical or horizontal line in the "DISPLAY" buffer.
* **Dawing:** A line is drawn by **Or**ing with a value which binary representation matches 1 to a drawn pixels and 0 to the other bits.

## Usage
To run the 7-segment simulation, ensure you are in the root directory and execute:

```bash
python -m 7_Segment_Display.ML_Hexadecimal
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

# Brookshear Machine: Conway's Game of Life

<p align="center">
  <img src="Cellular_Automata_ML.gif" alt="Brookshear Automata Animation">
</p>

This project implements John Conway's "Game of Life" cellular automaton on a simulated 8-bit architecture. It demonstrates how complex, emergent behavior can be calculated and rendered using a minimalist 256-byte memory system.

## What is Conway's Game of Life?
The Game of Life is a "zero-player game" consisting of a grid of cells. Each cell is either **Alive** or **Dead**. The state of the grid evolves in discrete "generations" based on three mathematical rules:

1. **Survival:** A live cell with 2 or 3 neighbors stays alive.
2. **Death:** A live cell with fewer than 2 neighbors (solitude) or more than 3 (overpopulation) dies.
3. **Birth:** A dead cell with exactly 3 neighbors becomes a live cell.

## Custom ISA Extension: Opcode 0xF (Display)
The standard Brookshear instruction set has been extended with a custom "Display Driver" mapped to **Opcode 0xF**. This allows the machine to communicate with the terminal.

1. **Memory Mapping:** The machine displays a specific region of RAM (starting at `0xF8`) known as the **Frame Buffer**.
2. **Binary Visualization:** When the instruction `F000` is executed, the machine reads the bits in the Frame Buffer section.
3. **Pixel Rendering:** The `_display` function turns the binary representation of lines to visual chars .(`1` -> `██`, `0` -> `  `)

## Core Logic & Data Bits
In this simulation, every single bit in the 64-byte display represents a living or dead cell.

* **Bit-Packed:** The cells are received in 8-bit packs from memory as one bit of that same line is also a pixel in the display.
* **Moving Window:** The code sets a bit pointer at the far right side of the byte on top of the current cell. The byte is rotated to the right which moves the 2 other positions of adjacent cells to the pointer position. This is done for the byte on top, the byte where the cell is and the byte after it.
* **Death default:** By default the screen starts as a matrix of 0s each generation. The code only has to worry about what needs to be alive and skips the "Killing" side of logic.
* **Alive Cell:** If the cell is alive it subtracts 1 for the "self" count and then it checks if the count of the adjacent cells is 2 or 3 which would mean the cell has to be alive.
* **Dead cell:** If the cell is dead it checks whether the adjacent cell count is exactly 3 so it can be set alive.
* **Buffer/Screen:** Each update is done on the buffer using data from the current screen. After a full update every byte of the buffer is copied to the screen and then zeroed. After the copy-update cycle finishes the screen section is displayed.

## Usage
To ensure the internal library links are handled correctly, run this command from the root folder:

```bash
python -m Connways_Game_Of_Life.Cellular_Automata_ML
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

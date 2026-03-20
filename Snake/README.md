"""
# Brookshear Machine: Snake Game

<p align="center">
  <img src="Snake_ML.gif" alt="Snake Machine Language Animation">
</p>

This project implements the classic "Snake" arcade game on a simulated 8-bit architecture. It demonstrates how real-time input handling, collision logic, and dynamic memory allocation can be achieved within a minimalist 256-byte system.

## What is the Snake Game?
Snake is a sub-genre of action video games where the player maneuvers a growing line that becomes a primary obstacle to itself. The goal is to eat food while avoiding the walls and the snake's own tail.

1. **Growth:** Every time the snake eats a piece of food, its length increases (Score++).
2. **Movement:** The snake moves continuously in one of four directions until the player changes its course.
3. **Collision:** If the snake's head hits its body or the boundary, the simulation terminates (BREAK).

## Custom ISA Extensions: Opcode 0xF & 0xD
The standard Brookshear instruction set has been extended with two custom drivers to handle the game's high-level requirements:

1. **Opcode 0xF (Display Driver):** Maps the memory region starting at `0xF8` (Frame Buffer) to the terminal. It renders bits as `██` pixels and highlights the food position using ANSI colors.
2. **Opcode 0xD (Food Generator):** Provides a pseudo-random coordinate generator. It ensures new food is placed on an empty memory address not currently occupied by the snake's body.

## Core Logic & Memory Mapping
The game relies on efficient bit-packing and pointer arithmetic to manage the snake's state in a very tight memory space.

* **Coordinate Packing:** Both the food and the snake segments are stored as single bytes in the format `IIII JJJJ`. The high nibble represents the Row (I) and the low nibble represents the Column (J).
* **The Body Array:** The snake's body is stored as a contiguous array in RAM starting at `0xB8`. The register `0xB` acts as the index/length pointer.
* **Movement Logic:** When a move is made, the code calculates the new head position. If no food is eaten, it "shifts" the entire body array forward, effectively removing the tail and adding the new head.
* **Bit-Mapped Rendering:** The assembly logic iterates through the body array, translates the `IIII JJJJ` coordinates into bit-offsets within the `0xF8` display buffer, and flips the corresponding bits to `1` before the Display Driver draws the frame.

## Usage
To ensure the internal library links and machine instance are handled correctly, run this command from the root folder:

```bash
python -m Machine_Language_CORE.Snake_Game
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

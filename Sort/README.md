"""
# Brookshear Machine: Sorting Visualizer

<p align="center">
  <img src="Sort_ML.gif" alt="Brookshear Sorting Animation">
</p>

This project implements a **Sorting algorithm visualization** on a simulated 8-bit Brookshear architecture. It demonstrates how low-level machine instructions can be used not only to compute logic, but also to render dynamic, real-time graphical output using a constrained 256-byte memory system.

## What is this program?
This is a **Sorting visualizer** where each memory cell from **0xF0** to **0xFF**, holds a value. The system sorts these values while continuously displaying the process in the terminal.

Unlike high-level sorting implementations, this operates entirely through **bitwise comparison and rotation**, mimicking how a primitive CPU might process and compare values at the binary level.

## Custom ISA Extension: Opcode 0xF (Display)
The standard Brookshear instruction set has been extended with a custom **Display Driver** mapped to **Opcode 0xF**, allowing terminal-based visualization.

1. **Memory Mapping:** The display reads from a memory region starting at `0xF0`, where each byte is a horizontal bar.
2. **Rendering Logic:** Executing `FFF0` triggers the `_display` function.
3. **Visualization:**
   - Each value is rendered as a horizontal bar using `■`.
   - A progress bar shows how much of the array has been processed.
   - Color highlights distinguish sorted vs unsorted regions.

## Core Logic & Data Handling
The algorithm sorts values using **bitwise masking and rotation**, rather than direct comparison operators.

* **Row-Based Structure:** Each memory slot represents a row.
* **Dual Indexing:** Two pointers (`ROW_I` and `ROW_J`) traverse and compare elements.
* **Bit Mask Comparison:**  
  A mask (starting at MSB) is rotated right to compare numbers bit-by-bit.
* **Conditional Swapping:**  
  Values are swapped only when a higher-priority bit comparison determines ordering.
* **Looping Mechanism:**  
  The algorithm iterates until all rows are sorted or a termination condition is met.
* **Display Refresh:**  
  After each major step, the display updates to reflect the current state.

## Visual & Audio Feedback
* **Frame Rendering:** Smooth terminal updates simulate animation (~2 FPS).
* **Progress Indicator:** A dynamic bar shows sorting completion percentage.
* **Sound Cue:** A short beep (`winsound.Beep`) plays every frame for feedback.

## Usage
To ensure the internal library links are handled correctly, run this command from the root folder:

```bash
python -m Sort.Sort_ML
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

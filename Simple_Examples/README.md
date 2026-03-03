# Brookshear Diagnostic Runner

This script demonstrates how to you could run a minimal program with the machine. A feature of the code is that it sets the Program Counter (`cpu.PC`) to `0xA0` before loading the code. Which in terms of the RAM puts the program starting at `0xA0` instead of the default `0x00`.

## Usage
To run and to ensure the internal imports are handled correctly by the interpreter. Open CMD/PowerShell in the root folder and run. 

```bash
python -m Simple_Examples.Machine_language_BASIC
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

# Brookshear Diagnostic Runner

This script demonstrates how you could run a minimal program with the machine. A feature of the code is that it sets the Program Counter (`cpu.PC`) to `0xA0` before loading the code. In terms of RAM, it loads the program starting at `0xA0` instead of the default `0x00`.

## Usage
To ensure that internal imports are handled correctly by the interpreter, open CMD or PowerShell in the project’s root folder and run:

```bash
python -m Simple_Examples.Machine_language_BASIC
```

---
<p align="center"><sub>Inspired by Glenn Brookshear's CS: An Overview (11th Ed).<br>Copyright © Thanas Fuqi 2026</sub></p>

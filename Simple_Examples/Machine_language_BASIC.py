from Machine_language_CORE import Machine
cpu = Machine() # Import and init a machine

# Diagnostic program to run
check = """
2203 ; A0 LDA R2, 0x03     | R2 = 0x03
200A ; A2 LDA R0, 0x0A     | R0 = 0x0A
2105 ; A4 LDA R1, 0x05     | R1 = 0x05
5012 ; A6 R1 + R2 -> R0    | R0 = 0x05 + 0x03 = 0x08
7001 ; A8 R0 | R1 -> R0    | R0 = 0x08 | 0x05 = 0x0D
8012 ; AA R1 & R2 -> R0    | R0 = 0x05 & 0x03 = 0x01
9012 ; AC R1 ^ R2 -> R0    | R0 = 0x05 ^ 0x03 = 0x06
A002 ; AE ROT_R (R0, 2)    | R0 = 0x06 >> 2 = 0x81
4031 ; B0 R3 -> R1         | R1 = R3 = 0x00
3010 ; B2 STORE R0 -> 0x10 | MEM[0x10] = R0 = 0x81
1001 ; B4 LD R0, 0x01      | R0 = MEM[0x01] = 0x00
B0B8 ; B6 JMP 0xB8         | JMP MEM[0xB8]
C000 ; B8 BREAK            | -> BREAK
"""

# --- EXPECTED ---
# MEM[0x10] = 0x81
# R0 = 0x00
# R1 = 0x00
# R2 = 0x03

# OTHERS = 0x00

cpu.PC = int("A0", 16) # Update Program Counter
cpu.load(check) # Load the hexadecimal string
cpu.run() # Run the emulation with given state

from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
cpu.delay = 0.0001 # Delay prints to debug
cpu.ROWS, cpu.COLS = 12, 20 # Display x:y
start = time.perf_counter() # Global time

def _display(*args):
  global start # Use timer
  TOP = 0xF6 # Display Start
  print(f"\033[1;1H┌{'─'*(cpu.COLS-4)}┐")

  for i in range(cpu.ROWS-3):
    binary = f"{cpu.memory[TOP]:08b}" # 8 Bit
    row_str = ''.join('██' if bit == '1' else '  ' for bit in binary)
    print(f"\033[{i+2};1H│{row_str}│")
    TOP = (TOP + 1) & 0xFF

  print(f"\033[{cpu.ROWS-1};1H└{'─'*(cpu.COLS-4)}┘")

  elapsed = time.perf_counter() - start
  print(f"\033[{cpu.ROWS};1HTime: {round(elapsed, 6)} sec")
  start = time.perf_counter()

cpu.ISA[0xf] = _display

Wave_Loop = """
2FCC ; 00 11001100

10F6 ; 02
70F0 ; 04 ADD
30F6 ; 06

AF01 ; 08 EXCHANGE

1003 ; 0A CURRENT
2101 ; 0C +1
2200 ; 0E 0

5001 ; 10 INCREMENT
B21A ; 12
3003 ; 14
3007 ; 16
B002 ; 18

F000 ; 1A DISPLAY
AF01 ; 1C EXCHANGE

32F6 ; 1E

101F ; 20
5001 ; 22
B22A ; 24
301F ; 26
B01E ; 28

20F6 ; 2A
301F ; 2C
B014 ; 2E BACK UP
C000 ; 30 HALT
""" # PC = "00"

cpu.load(Wave_Loop)
print("""
┌────────────────────────────────┐
│ █    █  █▀▀▀▀█  ▀▄   ▄▀  █▀▀▀▀ │
│ █    █  █    █   █   █   █     │
│ █ ▌▐ █  █■■■■█   ▀▄ ▄▀   █■■■■ │
│ █ ▌▐ █  █    █    █ █    █     │
│ █▄▌▐▄█  █    █    ▀█▀    █▄▄▄▄ │
└────────────────────────────────┘
""")
input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
cpu.run() # Clear and run emulation

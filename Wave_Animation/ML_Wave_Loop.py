from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
cpu.ROWS, cpu.COLS = 13, 20 # Display x:y

delay = 1/10 # Delayed printing (~10 fps)
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
  time.sleep(max(0, delay - elapsed)) # 0 if negative
  print(f"\033[{cpu.ROWS};1HTime: {round(elapsed, 6)} sec")
  start = time.perf_counter()

cpu.ISA[0xf] = _display

Wave_Loop = """
2FCC ; 00 MASK 11001100
2101 ; 02 CONST 1
2200 ; 04 CONST 0

3FF6 ; 06 ADD MASK
AF01 ; 08 ROTATE MASK

1007 ; 0A CURRENT ROW_NAME
5001 ; 0C ROW_NAME += 1
B214 ; 0E IF ROW_NAME == 0: GOTO 14

3007 ; 10 LOAD NEXT_NAME
B006 ; 12 JMP0 06

F000 ; 14 DISPLAY
AF01 ; 16 ROTATE MASK

20F6 ; 18 LOAD BASE ROW_NAME
3007 ; 1A LOAD BASE ROW_NAME

B006 ; 1C JMP0 06
C000 ; 1E HALT
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

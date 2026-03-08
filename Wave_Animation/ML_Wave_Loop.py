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
32F6 ; 18 ADD 00 TO ROW_NAME

1019 ; 1A CURRENT ROW_NAME
5001 ; 1C ROW_NAME += 1
B224 ; 1E IF ROW_NAME == 0: GOTO 24

3019 ; 20 LOAD NEXT ROW
B018 ; 22 JMP0 18

20F6 ; 24 LOAD BASE ROW_NAME
3007 ; 26 LOAD BASE ROW_NAME
3019 ; 28 LOAD BASE ROW_NAME

B006 ; 2A JMP0 06
C000 ; 2C HALT
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

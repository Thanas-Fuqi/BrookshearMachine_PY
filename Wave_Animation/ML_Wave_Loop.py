from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
delay = 1/10 # Delayed printing (~10 fps)
time_start = time.perf_counter() # Global time

# ------------ DEBUG OPTIONS ------------
cpu.ROWS, cpu.COLS = 13, 20 # Terminal xy

def _display(n, _, __, display_top):
  global time_start # Use timer
  print("\033[1;1H", end="")
  output = []

  output.append("┌────────────────┐")

  for i in range(n):
    binary = f"{cpu.memory[display_top]:08b}" # 8 Bit
    row_str = ''.join('██' if bit == '1' else '  ' for bit in binary)
    output.append(f"\n│{row_str}│")
    display_top = (display_top + 1) & 0xFF

  output.append("\n└────────────────┘")
  print("".join(output), end="", flush=True)

  elapsed = time.perf_counter() - time_start
  print(f"\nTime: {elapsed:.6f} sec")

  time.sleep(max(0, delay - elapsed)) # 0 if negative
  time_start = time.perf_counter()

cpu.ISA[0xF] = _display
cpu.log_dispatcher[0xF] = lambda o1, _, __, nb, code: f"{cpu.PC-2:02X} : {code} : Displayed {o1} bytes from memory {nb:02X}"

Wave_Loop = """
2FCC ; 00 LOAD MASK (11001100)
2101 ; 02 CONSTANT 01

3FF6 ; 04 STORE MASK -> DISPLAY_ROW [STORE_ROW]
AF01 ; 06 ROTATE MASK RIGHT

1005 ; 08 LOAD DISPLAY_ROW (NAME)
5001 ; 0A DISPLAY_ROW += 01
B212 ; 0C IF DISPLAY_ROW == 00 :DISPLAY:

3005 ; 0E LOAD NEW DISPLAY_ROW (NAME)
B004 ; 10 JMP :STORE_ROW:

FAF6 ; 12 DISPLAY A BYTES FROM 0xF6 [DISPLAY]
AF01 ; 14 ROTATE MASK RIGHT

20F6 ; 16 LOAD DISPLAY_TOP (NAME)
3005 ; 18 LOAD DISPLAY_TOP (NAME)

B004 ; 1A JMP :STORE_ROW:
"""

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

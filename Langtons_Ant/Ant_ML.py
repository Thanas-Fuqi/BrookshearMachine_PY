from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
delay = 1/10 # Delayed printing (~10 fps)
count = 1 # Count how many Gen done total
time_start = time.perf_counter() # Global

# ------------ DEBUG OPTIONS ------------
cpu.debug = False # Disable debuging mode

def _display(n, _, __, display_top):
  global time_start, count # Globals
  ant_row = cpu.register[0xD] # RD = row address
  ant_col = cpu.register[0xE] # RE = column mask
  print("\033[1;1H", end="")
  print(f"Counted: {count:.3e}")
  count += 1
  
  output = ["┌────────────────┐"]
  for i in range(n):
    binary = f"{cpu.memory[display_top]:08b}"

    row = []
    for j, bit in enumerate(binary):
      if (display_top == ant_row) and (ant_col == (0x80 >> j)):
        row.append(f"\033[31m██\033[0m") # Red
      else:
        row.append("██" if bit == "1" else "  ")

    output.append(f"\n│{''.join(row)}│")
    display_top = (display_top + 1) & 0xFF

  output.append("\n└────────────────┘")
  print("".join(output), end="", flush=True)

  elapsed = time.perf_counter() - time_start
  print(f"\nTime: {elapsed:.15f}"[:15] + " sec")
  
  time.sleep(max(0, delay - elapsed)) # 0 if negative
  time_start = time.perf_counter()

cpu.ISA[0xF] = _display

Ant_ML = """
2E08 ; 00 COLUMN (MASK)
2DFB ; 02 ROW (NAME)
2C01 ; 04 HEADING (RIGHT)

3D09 ; 06 LOAD ROW (NAME) [TOP]
1000 ; 08 LOAD ROW (CONFIG)


710E ; 0A CHECK = ROW_CONFIG | MASK
B112 ; 0C IF CHECK == ROW_CONFIG :WAS_WHITE:
2B00 ; 0E COLOR (BLACK)
B014 ; 10 JMP :FLIP:
2BFF ; 12 COLOR (WHITE) [WAS_WHITE]


900E ; 14 FLIP BY XOR THE ANT POS [FLIP]

3D19 ; 16 LOAD ROW (NAME)
3000 ; 18 LOAD ROW (NEW_CONFIG)


2000 ; 1A LOAD COLOR (BLACK)
BB22 ; 1C IF COLOR == BLACK :BLACK:

2A40 ; 1E CLOCKWISE ADD
B024 ; 20 JMP :PROCED:
2AC0 ; 22 COUNTERCLOCKWISE ADD [BLACK]

5CCA ; 24 HEADING = HEADING + ADD [PROCED]


2001 ; 26 LOAD RIGHT
BC44 ; 28 IF HEADING == RIGHT :RIGHT:
2081 ; 2A LOAD LEFT
BC48 ; 2C IF HEADING == LEFT :LEFT:
2041 ; 2E LOAD DOWN
BC36 ; 30 IF HEADING == DOWN :DOWN:

2FFF ; 32 LOAD OFFSET -1
B038 ; 34 JMP :TOPOLOGY:
2F01 ; 36 LOAD OFFSET +1 [DOWN]

5DDF ; 38 ROW = ROW + OFFSET [TOPOLOGY]

2107 ; 3A LOAD CONSTANT 07
20F8 ; 3C CLAMP ROW_TOP
8DD1 ; 3E ROW_NAME = ROW_NAME & 07
7DD0 ; 40 ROW_NAME = ROW_NAME | ROW_TOP

B04E ; 42 JMP :DISPLAY:


2F01 ; 44 LOAD `RIGHT` [RIGHT]
B04A ; 46 JMP :ROR:
2F07 ; 48 LOAD `LEFT` [LEFT]

3F4D ; 4A LOAD SIDE (NAME) [ROR]
AE00 ; 4C ROR SIDE-WISE


F8F8 ; 4E DISPLAY 8 ROWS FROM F8 [DISPLAY]
B006 ; 50 JMP :TOP:
"""

cpu.load(Ant_ML)
cpu.run() # Run

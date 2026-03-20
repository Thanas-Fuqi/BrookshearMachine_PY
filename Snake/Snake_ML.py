from Machine_language_CORE import Machine
import threading, msvcrt, time, random

cpu = Machine() # Init a machine instance
cpu.ROWS, cpu.COLS = 11, 20 # Display x:y
cpu.debug = False # Disable debuging mode
start = time.perf_counter() # Global time

def _listener():
	while True:
		if msvcrt.kbhit():
			cpu.register[0xF] =  msvcrt.getch()[0]
		time.sleep(0.001)

threading.Thread(target=_listener, daemon=True).start()

def _display(N, _, __, START, ___):
  global start
  print("\033[1;1H", end="") 

  output = []
  output.append(f"┌{'─' * (N*2)}┐\n")
  grid = [["  " for _ in range(N)] for _ in range(N)]

  for k in range(N * N):
    byte = cpu.memory[START + k]
    if byte == 0xff: continue

    di, dj = (byte >> 4) & 0xF, byte & 0xF
    grid[di][dj] = "\033[91m██\033[0m" if k==0 else "██"

  for row in grid:
    output.append("│" + "".join(row) + "│\n")

  output.append(f"└{'─' * (N*2)}┘\n")

  score_text = "FINISH! RESPECT++" if cpu.register[0xC] == 63 else f"YOUR SCORE IS : {cpu.register[0xC]:02d}"
  output.append(score_text)

  print("".join(output), end="", flush=True)
  delay = 1 / (5 + min(cpu.register[0xC] // 4, 8))
  elapsed = time.perf_counter() - start
  time.sleep(max(0, delay - elapsed))
  start = time.perf_counter()

cpu.ISA[0xF] = _display

def _place_food(*args):
  top = cpu.register[0xE]
  dist = cpu.register[0xD]
  index = cpu.register[0xC]

  occupied = {
    cpu.memory[addr] for addr in range(top, top+index+1)
  }

  while True:
    i = random.randint(0, 7)
    j = random.randint(0, 7)

    food_ij = (i << 4) | j
    if food_ij not in occupied:
      break

  cpu.memory[dist] = food_ij

cpu.ISA[0xD] = _place_food


# --------------- PRELOAD ---------------
cpu.register[0xE] = 0xC0 # TOP_ARRAY
cpu.register[0xD] = 0xBF # FOOD_ROW
cpu.register[0xC] = 0x00 # INDEX
cpu.register[0xB] = 0x01 # CONSTANT
cpu.register[0xA] = 0x01 # DEFAULT DELTA

# --------------- PRELOAD ---------------
for i in range(64): # NULL VALUE
  cpu.memory[0xBF+i] = 0xFF

# --------------- PRELOAD ---------------
cpu.memory[0xC0] = 0x31 # I=3,J=3 # HEAD
cpu.memory[0xBF] = 0x00 # I=0,J=0 # FOOD


Snake_Game = """
2061 ; 00 LOAD b'a' [TOP]
BF06 ; 02 IF KEY == b'a'
B00A ; 04 JNZ :SKIP:
2A07 ; 06 LOAD 07 (I, J-1)
B026 ; 08 JNZ :CONTINUE:

2064 ; 0A LOAD b'd' [SKIP]
BF10 ; 0C IF KEY == b'd'
B014 ; 0E JNZ :SKIP:
2A01 ; 10 LOAD 01 (I, J+1)
B026 ; 12 JNZ :CONTINUE:

2077 ; 14 LOAD b'w' [SKIP]
BF1A ; 16 IF KEY == b'w'
B01E ; 18 JNZ :SKIP:
2AF0 ; 1A LOAD F0 (I-1, J)
B026 ; 1C JNZ :CONTINUE:

2073 ; 1E LOAD b's' [SKIP]
BF24 ; 20 IF KEY == b's'
B026 ; 22 JNZ :CONTINUE:
2A10 ; 24 LOAD 10 (I+1, J)


50EC ; 26 HEAD_ROW = TOP_ARRAY + INDEX [CONTINUE]
302B ; 28 LOAD HEAD_ROW (NAME)
1200 ; 2A LOAD HEAD_ROW (CONFIG)

522A ; 2C HEAD_ROW += DELTA
2077 ; 2E CONSTANT 77
8220 ; 30 CONSTRAIN TO 00-77


21FF ; 32 LOAD CONSTANT FF
511B ; 34 CONSTANT += 01 [NEXT]
4010 ; 36 LOAD CONSTANT
BC44 ; 38 IF CONSTANT == INDEX :FOOD:
53E0 ; 3A CHECK_ROW = TOP_ARRAY + CONSTANT
333F ; 3C LOAD CHECK_ROW (NAME)
1000 ; 3E LOAD CHECK_ROW (CONFIG)
B276 ; 40 IF NEW HEAD_ROW == CHECK_ROW :BREAK:
B034 ; 42 JNZ :NEXT:


3D47 ; 44 LOAD FOOD_ROW (NAME) [FOOD]
1000 ; 46 LOAD FOOD_ROW (CONFIG)
B24C ; 48 IF HEAD_XY == FOOD_XY
B056 ; 4A JNZ :REMOVE:
5CCB ; 4C INDEX = INDEX + 01
203F ; 4E LOAD 63 (MAX_INDEX)
BC76 ; 50 IF INDEX == 63 :BREAK:
D000 ; 52 CHANGE FOOD POS
B06C ; 54 JNZ :STAMP:


20FF ; 56 LOAD CONSTANT FF [REMOVE]

40E3 ; 58 ONE = TOP_ARRAY
543B ; 5A TWO = ONE + 01 [NEXT]

3363 ; 5C LOAD ONE (NAME)
3461 ; 5E LOAD TWO (NAME)
1500 ; 60 LOAD TWO (CONFIG)
3500 ; 62 STORE ONE (DIST)

500B ; 64 CONSTANT = CONSTANT + 01
BC6C ; 66 IF CONSTANT == INDEX -> :STAMP:
533B ; 68 ONE = ONE + 01
B05A ; 6A JNZ :NEXT:


50EC ; 6C HEAD_ROW = TOP_ARRAY + INDEX [STAMP]
3071 ; 6E LOAD HEAD_ROW (NAME)
3200 ; 70 STORE HEAD_ROW (CONFIG)


F8BF ; 72 DISPLAY
B000 ; 74 JNZ :TOP:
C000 ; 76 [BREAK]
"""

cpu.load(Snake_Game)
input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
cpu.run() # Clear and run emulation

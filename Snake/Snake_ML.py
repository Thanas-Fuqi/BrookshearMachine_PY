from Machine_language_CORE import Machine
import threading, msvcrt, time, random

cpu = Machine() # Init a machine instance
cpu.ROWS, cpu.COLS = 11, 20 # Terminal xy
cpu.debug = False # Disable debuging mode
start = time.perf_counter() # Global time

def _listener():
	while True:
		if msvcrt.kbhit():
			cpu.register[0xF] =  msvcrt.getch()[0]
		time.sleep(0.001)

threading.Thread(target=_listener, daemon=True).start()

def _random(R, _, __, mask, ___):
  cpu.register[R] = random.randint(0, 0xFF) & mask

cpu.ISA[0xD] = _random

def _display(n, _, __, top, ___):
  global start
  print("\033[1;1H", end="") 
  output = []

  score_text = "FINISH! RESPECT++" if cpu.register[0xC] == 63 else f"YOUR SCORE IS : {cpu.register[0xC]:02d}"
  output.append(score_text)

  output.append(f"\n┌{'─' * (n*2)}┐\n")
  grid = [["  " for _ in range(n)] for _ in range(n)]

  for k in range(n * n):
    byte = cpu.memory[top + k]
    if byte == 0xFF: continue

    i, j = (byte >> 4) & 0xF, byte & 0xF
    grid[i][j] = "\033[91m██\033[0m" if k==0 else "██"

  for row in grid:
    output.append("│" + "".join(row) + "│\n")

  output.append(f"└{'─' * (n*2)}┘\n")

  elapsed = time.perf_counter() - start
  output.append(f"Time: {round(elapsed, 6)} sec")

  print("".join(output), end="", flush=True)

  delay = 1 / (7 + min(cpu.register[0xC] // 5, 6))
  time.sleep(max(0, delay - elapsed))
  start = time.perf_counter()

cpu.ISA[0xF] = _display


# ---------------- PRELOAD ----------------
cpu.register[0xE] = 0xC0 # TOP_ARRAY
cpu.register[0xD] = 0xBF # FOOD_ROW
cpu.register[0xC] = 0x00 # INDEX
cpu.register[0xB] = 0x01 # CONSTANT
cpu.register[0xA] = 0x01 # GLOBAL DELTA

# ---------------- PRELOAD ----------------
for i in range(64): # FILL WITH NULL VALUE
  cpu.memory[cpu.register[0xD]+i] = 0xFF

# ---------------- PRELOAD ----------------
cpu.memory[cpu.register[0xE]] = 0x31 # HEAD
cpu.memory[cpu.register[0xD]] = 0x00 # FOOD


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
B28C ; 40 IF NEW HEAD_ROW == CHECK_ROW :BREAK:
B034 ; 42 JNZ :NEXT:


3D47 ; 44 LOAD FOOD_ROW (NAME) [FOOD]
1000 ; 46 LOAD FOOD_ROW (CONFIG)
B24C ; 48 IF HEAD_XY == FOOD_XY
B06C ; 4A JNZ :REMOVE:
5CCB ; 4C INDEX = INDEX + 01
203F ; 4E LOAD 63 (MAX_INDEX)
BC8C ; 50 IF INDEX == 63 :BREAK:


D477 ; 52 GET RANDOM_POS [RANDOM]
21FF ; 54 LOAD CONSTANT FF
53E1 ; 56 CHECK_ROW = TOP_ARRAY + CONSTANT [NEXT]
335B ; 58 LOAD CHECK_ROW (NAME)
1300 ; 5A LOAD CHECK_ROW (CONFIG)

4040 ; 5C LOAD RANDOM_POS
B352 ; 5E IF CHECK_ROW == RANDOM_POS :RANDOM:

4010 ; 60 LOAD CONSTANT
BC68 ; 62 IF INDEX == CONSTANT
511B ; 64 CONSTANT += 01
B056 ; 66 JNZ :NEXT:


34BF ; 68 LOAD NEW FOOD_POS
B082 ; 6A JNZ :STAMP:


20FF ; 6C LOAD CONSTANT FF [REMOVE]

40E3 ; 6E ONE = TOP_ARRAY
543B ; 70 TWO = ONE + 01 [NEXT]

3379 ; 72 LOAD ONE (NAME)
3477 ; 74 LOAD TWO (NAME)
1500 ; 76 LOAD TWO (CONFIG)
3500 ; 78 STORE ONE (DIST)

500B ; 7A CONSTANT = CONSTANT + 01
BC82 ; 7C IF CONSTANT == INDEX -> :STAMP:
533B ; 7E ONE = ONE + 01
B070 ; 80 JNZ :NEXT:


50EC ; 82 HEAD_ROW = TOP_ARRAY + INDEX [STAMP]
3087 ; 84 LOAD HEAD_ROW (NAME)
3200 ; 86 STORE HEAD_ROW (CONFIG)


F8BF ; 88 DISPLAY
B000 ; 8A JNZ :TOP:
C000 ; 8C [BREAK]
"""

cpu.load(Snake_Game)
input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
cpu.run() # Clear and run emulation

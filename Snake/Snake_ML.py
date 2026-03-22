from Machine_language_CORE import Machine
import threading, msvcrt, time, random

cpu = Machine() # Init a machine instance
time_start = time.perf_counter() # Global time

# ------------ DEBUG OPTIONS ------------
cpu.ROWS, cpu.COLS = 12, 20 # Terminal xy
cpu.debug = False # Disable debuging mode

def _listener():
	while True:
		if msvcrt.kbhit():
			cpu.register[0xF] =  msvcrt.getch()[0]
		time.sleep(0.001)

threading.Thread(target=_listener, daemon=True).start()

def _random(R, _, __, mask, ___):
  cpu.register[R] = random.randint(0, 0xFF) & mask

cpu.ISA[0xD] = _random

def _display(n, _, __, display_top, ___):
  global time_start
  print("\033[1;1H", end="") 
  output = []

  score_text = "FINISH! RESPECT++" if cpu.register[0xC] == 62 else f"SNAKE LENGTH -> {cpu.register[0xC]+1:02d}"
  output.append(score_text)

  output.append(f"\n┌{'─' * (n*2)}┐\n")
  grid = [["  " for _ in range(n)] for _ in range(n)]

  for k in range(n * n):
    byte = cpu.memory[display_top + k]
    if byte == 0xFF: continue

    i, j = (byte >> 4) & 0xF, byte & 0xF
    grid[i][j] = "\033[91m██\033[0m" if k==0 else "██"

  for row in grid:
    output.append("│" + "".join(row) + "│\n")

  output.append(f"└{'─' * (n*2)}┘\n")

  elapsed = time.perf_counter() - time_start
  output.append(f"Time: {elapsed:.6f} sec")

  print("".join(output), end="", flush=True)

  delay = 1 / (7 + min(cpu.register[0xC] // 5, 6))
  time.sleep(max(0, delay - elapsed))
  time_start = time.perf_counter()

cpu.ISA[0xF] = _display

Snake_Game = """
2EC1 ; 00 LOAD TOP_ARRAY
2DC0 ; 02 LOAD FOOD_ROW
2C02 ; 04 LOAD INDEX
2B01 ; 06 LOAD CONSTANT 01
2A01 ; 08 LOAD GLOBAL DELTA

20FF ; 0A LOAD NULL_VALUE
30C4 ; 0C STORE NULL_VALUE [NEXT_STORE]
110D ; 0E LOAD STORE_ROW (NAME)
B118 ; 10 IF STORE_ROW == FF :INIT:
511B ; 12 STORE_ROW += 01
310D ; 14 LOAD NEW STORE_ROW (NAME)
B00C ; 16 JMP :NEXT_STORE:

2033 ; 18 LOAD X=3, Y=3 [INIT]
30C0 ; 1A STORE FOOD XY


2061 ; 1C LOAD b'a' [TOP]
BF22 ; 1E IF KEY == b'a'
B026 ; 20 JMP :SKIP:
2A07 ; 22 LOAD 07 (I, J-1)
B042 ; 24 JMP :CONTINUE:

2064 ; 26 LOAD b'd' [SKIP]
BF2C ; 28 IF KEY == b'd'
B030 ; 2A JMP :SKIP:
2A01 ; 2C LOAD 01 (I, J+1)
B042 ; 2E JMP :CONTINUE:

2077 ; 30 LOAD b'w' [SKIP]
BF36 ; 32 IF KEY == b'w'
B03A ; 34 JMP :SKIP:
2AF0 ; 36 LOAD F0 (I-1, J)
B042 ; 38 JMP :CONTINUE:

2073 ; 3A LOAD b's' [SKIP]
BF40 ; 3C IF KEY == b's'
B042 ; 3E JMP :CONTINUE:
2A10 ; 40 LOAD 10 (I+1, J)


50EC ; 42 HEAD_ROW = TOP_ARRAY + INDEX [CONTINUE]
3047 ; 44 LOAD HEAD_ROW (NAME)
1200 ; 46 LOAD HEAD_ROW (CONFIG)

522A ; 48 HEAD_ROW += DELTA
2077 ; 4A CONSTANT 77
8220 ; 4C HEAD_ROW = HEAD_ROW & 77


2100 ; 4E LOAD CONSTANT 00
511B ; 50 CONSTANT += 01 [NEXT_HEAD]
4010 ; 52 LOAD CONSTANT
BC60 ; 54 IF CONSTANT == INDEX :FOOD:
53E0 ; 56 CHECK_ROW = TOP_ARRAY + CONSTANT
335B ; 58 LOAD CHECK_ROW (NAME)
1000 ; 5A LOAD CHECK_ROW (CONFIG)
B2A8 ; 5C IF NEW HEAD_ROW == CHECK_ROW :BREAK:
B050 ; 5E JMP :NEXT_HEAD:


3D63 ; 60 LOAD FOOD_ROW (NAME) [FOOD]
1000 ; 62 LOAD FOOD_ROW (CONFIG)
B268 ; 64 IF HEAD_XY == FOOD_XY :INDEX++:
B088 ; 66 JMP :REMOVE:
5CCB ; 68 INDEX = INDEX + 01 [INDEX++]
203E ; 6A LOAD 62 (MAX_INDEX)
BCA8 ; 6C IF INDEX == 62 :BREAK:


D477 ; 6E GET RANDOM_POS [RANDOM]
21FF ; 70 LOAD CONSTANT FF
53E1 ; 72 CHECK_ROW = TOP_ARRAY + CONSTANT [NEXT_RANDOM]
3377 ; 74 LOAD CHECK_ROW (NAME)
1300 ; 76 LOAD CHECK_ROW (CONFIG)

4040 ; 78 LOAD RANDOM_POS
B36E ; 7A IF CHECK_ROW == RANDOM_POS :RANDOM:

4010 ; 7C LOAD CONSTANT
BC84 ; 7E IF INDEX == CONSTANT :LOAD_FOOD:
511B ; 80 CONSTANT += 01
B072 ; 82 JMP :NEXT_RANDOM:


34C0 ; 84 LOAD NEW FOOD_POS [LOAD_FOOD]
B09E ; 86 JMP :STAMP:


20FF ; 88 LOAD CONSTANT FF [REMOVE]

40E3 ; 8A SNAKE[I] = TOP_ARRAY
543B ; 8C SNAKE[I+1] = SNAKE[I] + 01 [NEXT_SNAKE]

3395 ; 8E LOAD SNAKE[I] (NAME)
3493 ; 90 LOAD SNAKE[I+1] (NAME)
1500 ; 92 LOAD SNAKE[I+1] (CONFIG)
3500 ; 94 STORE SNAKE[I] (DIST)

500B ; 96 CONSTANT = CONSTANT + 01
BC9E ; 98 IF CONSTANT == INDEX :STAMP:
533B ; 9A SNAKE[I] = SNAKE[I] + 01
B08C ; 9C JMP :NEXT_SNAKE:


50EC ; 9E HEAD_ROW = TOP_ARRAY + INDEX [STAMP]
30A3 ; A0 LOAD HEAD_ROW (NAME)
3200 ; A2 STORE HEAD_ROW (CONFIG)


F8C0 ; A4 DISPLAY 8*8 BYTES FROM C0
B01C ; A6 JMP :TOP:
C000 ; A8 [BREAK]
"""

cpu.load(Snake_Game)
input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
cpu.run() # Clear and run emulation

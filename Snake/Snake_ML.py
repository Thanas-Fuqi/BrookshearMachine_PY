from Machine_language_CORE import Machine
import threading, msvcrt, time, random

cpu = Machine() # Init a machine instance
time_start = time.perf_counter() # Global time

# ------------ DEBUG OPTIONS ------------
cpu.debug = False # Disable debuging mode

def _listener():
	while True:
		if msvcrt.kbhit():
			cpu.register[0xF] =  msvcrt.getch()[0]
		time.sleep(0.001)

threading.Thread(target=_listener, daemon=True).start()

def _display(n, _, __, display_top):
  global time_start
  print("\033[1;1H", end="")

  output = ["FINISH! RESPECT++" if cpu.register[0xC] == 62 else f"SNAKE LENGTH -> {cpu.register[0xC]+1:02d}"]
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
  print("".join(output), end="", flush=True)

  elapsed = time.perf_counter() - time_start
  print(f"Time: {elapsed:.15f}"[:15] + " sec")

  delay = 1 / (7 + min(cpu.register[0xC] // 5, 6))
  time.sleep(max(0, delay - elapsed))
  time_start = time.perf_counter()

cpu.ISA[0xF] = _display
cpu.ISA[0xD] = lambda R, _, __, mask: cpu.register.__setitem__(R, random.randint(0, 0xFF) & mask)

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
BF22 ; 1E IF KEY == b'a' :OPPOSITE:
B02A ; 20 JMP :SKIP:
2001 ; 22 LOAD DELTA(RIGHT) [OPPOSITE]
BA2A ; 24 JMP :SKIP:
2A07 ; 26 LOAD DELTA(LEFT) (I, J-1)
B052 ; 28 JMP :CONTINUE:

2064 ; 2A LOAD b'd' [SKIP]
BF30 ; 2C IF KEY == b'd' :OPPOSITE:
B038 ; 2E JMP :SKIP:
2007 ; 30 LOAD DELTA(LEFT) [OPPOSITE]
BA38 ; 32 JMP SKIP:
2A01 ; 34 LOAD DELTA(RIGHT) (I, J+1)
B052 ; 36 JMP :CONTINUE:

2077 ; 38 LOAD b'w' [SKIP]
BF3E ; 3A IF KEY == b'w' :OPPOSITE:
B046 ; 3C JMP :SKIP:
2010 ; 3E LOAD DELTA(DOWN) [OPPOSITE]
BA46 ; 40 JMP :SKIP:
2AF0 ; 42 LOAD DELTA(UP) (I-1, J)
B052 ; 44 JMP :CONTINUE:

2073 ; 46 LOAD b's' [SKIP]
BF4C ; 48 IF KEY == b's' :OPPOSITE:
B052 ; 4A JMP :CONTINUE:
20F0 ; 4C LOAD DELTA(UP) [OPPOSITE]
BA52 ; 4E JMP :CONTINUE:
2A10 ; 50 LOAD 10 (I+1, J)


50EC ; 52 HEAD_ROW = TOP_ARRAY + INDEX [CONTINUE]
3057 ; 54 LOAD HEAD_ROW (NAME)
1200 ; 56 LOAD HEAD_ROW (CONFIG)

522A ; 58 HEAD_ROW += DELTA
2077 ; 5A CONSTANT 77
8220 ; 5C HEAD_ROW = HEAD_ROW & 77


2100 ; 5E LOAD CONSTANT 00
511B ; 60 CONSTANT += 01 [NEXT_HEAD]
4010 ; 62 LOAD CONSTANT
BC70 ; 64 IF CONSTANT == INDEX :FOOD:
53E0 ; 66 CHECK_ROW = TOP_ARRAY + CONSTANT
336B ; 68 LOAD CHECK_ROW (NAME)
1000 ; 6A LOAD CHECK_ROW (CONFIG)
B2B8 ; 6C IF NEW HEAD_ROW == CHECK_ROW :BREAK:
B060 ; 6E JMP :NEXT_HEAD:


3D73 ; 70 LOAD FOOD_ROW (NAME) [FOOD]
1000 ; 72 LOAD FOOD_ROW (CONFIG)
B278 ; 74 IF HEAD_XY == FOOD_XY :INDEX++:
B098 ; 76 JMP :REMOVE:
5CCB ; 78 INDEX = INDEX + 01 [INDEX++]
203E ; 7A LOAD 62 (MAX_INDEX)
BCB8 ; 7C IF INDEX == 62 :BREAK:


D477 ; 7E GET RANDOM_POS [RANDOM]
21FF ; 80 LOAD CONSTANT FF
53E1 ; 82 CHECK_ROW = TOP_ARRAY + CONSTANT [NEXT_RANDOM]
3387 ; 84 LOAD CHECK_ROW (NAME)
1300 ; 86 LOAD CHECK_ROW (CONFIG)

4040 ; 88 LOAD RANDOM_POS
B37E ; 8A IF CHECK_ROW == RANDOM_POS :RANDOM:

4010 ; 8C LOAD CONSTANT
BC94 ; 8E IF INDEX == CONSTANT :LOAD_FOOD:
511B ; 90 CONSTANT += 01
B082 ; 92 JMP :NEXT_RANDOM:


34C0 ; 94 LOAD NEW FOOD_POS [LOAD_FOOD]
B0AE ; 96 JMP :STAMP:


20FF ; 98 LOAD CONSTANT FF [REMOVE]

40E3 ; 9A SNAKE[I] = TOP_ARRAY
543B ; 9C SNAKE[I+1] = SNAKE[I] + 01 [NEXT_SNAKE]
33A5 ; 9E LOAD SNAKE[I] (NAME)
34A3 ; A0 LOAD SNAKE[I+1] (NAME)
1500 ; A2 LOAD SNAKE[I+1] (CONFIG)
3500 ; A4 STORE SNAKE[I] (DIST)

500B ; A6 CONSTANT = CONSTANT + 01
BCAE ; A8 IF CONSTANT == INDEX :STAMP:
533B ; AA SNAKE[I] = SNAKE[I] + 01
B09C ; AC JMP :NEXT_SNAKE:


50EC ; AE HEAD_ROW = TOP_ARRAY + INDEX [STAMP]
30B3 ; B0 LOAD HEAD_ROW (NAME)
3200 ; B2 STORE HEAD_ROW (CONFIG)


F8C0 ; B4 DISPLAY 8*8 BYTES FROM C0
B01C ; B6 JMP :TOP:
C000 ; B8 [BREAK]
"""

cpu.load(Snake_Game)
cpu.run() # Run Sim

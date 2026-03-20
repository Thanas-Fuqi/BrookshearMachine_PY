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


def _display(*args):
  global start
  TOP = 0xF8

  val = cpu.memory[0xB7]
  fi, fj = (val >> 4) & 0x0F, val & 0x0F

  print(f"\033[1;1H┌{'─'*(cpu.COLS-4)}┐")

  for i in range(cpu.ROWS - 3):
    binary = f"{cpu.memory[TOP]:08b}"

    row_str = ''.join(
      f"\033[91m██\033[0m" if i==fi and j==fj else ('██' if bit == '1' else '  ')
      for j, bit in enumerate(binary)
    )

    print(f"\033[{i+2};1H│{row_str}│")
    TOP = (TOP + 1) & 0xFF

  print(f"\033[{cpu.ROWS-1};1H└{'─'*(cpu.COLS-4)}┘")

  score_text = "FINISH! RESPECT++" if cpu.register[0xB]==63 else f"YOUR SCORE IS : {cpu.register[0xB]:02d}"
  print(f"\033[{cpu.ROWS};1H{score_text}")

  delay = 1 / (5 + min(cpu.register[0xB] // 4, 8))

  elapsed = time.perf_counter() - start
  time.sleep(max(0, delay - elapsed))
  start = time.perf_counter()

cpu.ISA[0xf] = _display


def _place_food(*args):
  occupied = {
    cpu.memory[addr] for addr in range(0xB8, 0xB8 + cpu.register[0xB] + 1)
  }

  while True:
    i = random.randint(0, 7)
    j = random.randint(0, 7)

    food_ij = (i << 4) | j
    if food_ij not in occupied:
      break

  cpu.memory[0xB7] = food_ij

cpu.ISA[0xd] = _place_food


# ----------- PRELOAD -----------
cpu.memory[0xB8] = 0x31 # I=3,J=3
cpu.memory[0xB7] = 0x00 # I=0,J=0

cpu.register[0xE] = 0xF8 # TOP_SCREEN
cpu.register[0xD] = 0xB8 # TOP_ARRAY
cpu.register[0xC] = 0xB7 # FOOD_ROW
cpu.register[0xB] = 0x00 # INDEX
cpu.register[0xA] = 0x01 # CONSTANT
cpu.register[0x9] = 0x01 # DEFAULT DELTA


Snake_Game = """
2061 ; 00 LOAD b'a' [TOP]
BF06 ; 02 IF KEY == b'a'
B00A ; 04 JNZ :SKIP:
2907 ; 06 LOAD 07 (I, J-1)
B026 ; 08 JNZ :CONTINUE:

2064 ; 0A LOAD b'd' [SKIP]
BF10 ; 0C IF KEY == b'd'
B014 ; 0E JNZ :SKIP:
2901 ; 10 LOAD 01 (I, J+1)
B026 ; 12 JNZ :CONTINUE:

2077 ; 14 LOAD b'w' [SKIP]
BF1A ; 16 IF KEY == b'w'
B01E ; 18 JNZ :SKIP:
29F0 ; 1A LOAD F0 (I-1, J)
B026 ; 1C JNZ :CONTINUE:

2073 ; 1E LOAD b's' [SKIP]
BF24 ; 20 IF KEY == b's'
B026 ; 22 JNZ :CONTINUE:
2910 ; 24 LOAD 10 (I+1, J)


50DB ; 26 HEAD_ROW = TOP_ARRAY + INDEX [CONTINUE]
302B ; 28 LOAD HEAD_ROW (NAME)
1200 ; 2A LOAD HEAD_ROW (CONFIG)

5229 ; 2C NEW HEAD_ROW
2077 ; 2E CONSTANT 77
8220 ; 30 CONSTRAIN TO 00-77


21FF ; 32 LOAD CONSTANT FF
511A ; 34 CONSTANT += 01 [NEXT]
4010 ; 36 LOAD CONSTANT
BB44 ; 38 IF CONSTANT == INDEX :FOOD:
53D0 ; 3A CHECK_ROW = TOP_ARRAY + CONSTANT
333F ; 3C LOAD CHECK_ROW (NAME)
1000 ; 3E LOAD CHECK_ROW (CONFIG)
B2B2 ; 40 IF NEW HEAD_ROW == CHECK_ROW :BREAK:
B034 ; 42 JNZ :NEXT:


3C47 ; 44 LOAD FOOD_ROW (NAME) [FOOD]
1000 ; 46 LOAD FOOD_ROW (CONFIG)
B24C ; 48 IF HEAD_XY == FOOD_XY
B056 ; 4A JNZ :REMOVE:
5BBA ; 4C INDEX = INDEX + 01

203F ; 4E LOAD 63 (MAX_INDEX)
BBB2 ; 50 IF INDEX == 63 :BREAK:

D000 ; 52 CHANGE FOOD POS
B06C ; 54 JNZ :STAMP:


20FF ; 56 LOAD CONSTANT FF [REMOVE]

40D3 ; 58 ONE = TOP_ARRAY
543A ; 5A TWO = ONE + 01 [NEXT]

3363 ; 5C LOAD ONE (NAME)
3461 ; 5E LOAD TWO (NAME)
1500 ; 60 LOAD TWO (CONFIG)
3500 ; 62 STORE ONE (DIST)

500A ; 64 CONSTANT = CONSTANT + 01
BB6C ; 66 IF CONSTANT == INDEX -> :STAMP:
533A ; 68 ONE = ONE + 01
B05A ; 6A JNZ :NEXT:


50DB ; 6C HEAD_ROW = TOP_ARRAY + INDEX [STAMP]
3071 ; 6E LOAD HEAD_ROW (NAME)
3200 ; 70 STORE HEAD_ROW (CONFIG)


20FE ; 72 LOAD CONSTANT FE
40C1 ; 74 ORIGIN = FOOD_ROW

3179 ; 76 LOAD ORIGIN (NAME) [DISPLAY]
1200 ; 78 LOAD ORIGIN (CONFIG)


23F0 ; 7A LOAD CONSTANT F0 (1111 0000)
8323 ; 7C ISO_I = ORIGIN AND CONSTANT (IIII 0000)
A304 ; 7E ISO_I = ISO_I ROT 4 (0000 IIII) [I]


53E3 ; 80 SCREEN_ROW = TOP_SCREEN + ISO_I
3387 ; 82 LOAD SCREEN_ROW  (NAME)
3395 ; 84 LOAD SCREEN_ROW  (NAME)
1400 ; 86 LOAD SCREEN_ROW  (CONFIG)


230F ; 88 LOAD CONSTANT 0F (0000 1111)
8323 ; 8A ISO_J = ORIGIN AND CONSTANT (0000 JJJJ) [J]
3391 ; 8C LOAD ISO_J (VALUE)
2580 ; 8E LOAD BASE_POINTER (1000 0000)
A500 ; 90 ROTATE BASE_POINTER J TIMES

7445 ; 92 SCREEN_ROW = SCREEN_ROW OR BASE_POINTER
3400 ; 94 STORE SCREEN_ROW (CONFIG)

500A ; 96 CONSTANT = CONSTANT + 01
BB9E ; 98 IF CONSTANT == INDEX
511A ; 9A ORIGIN = ORIGIN + 01
B076 ; 9C JNZ :DISPLAY:


F000 ; 9E DISPLAY
2000 ; A0 CLEAR VALUE


3EA5 ; A2 RESET TO F8
3000 ; A4 LOAD 00 [CLEAR]
11A5 ; A6 LOAD ROW (NAME)
511A ; A8 ROW = ROW + 01
B1B0 ; AA IF ROW == 00
31A5 ; AC LOAD ROW + 01
B0A4 ; AE JNZ :CLEAR:


B000 ; B0 JNZ :TOP:
C000 ; B2 [BREAK]
"""

cpu.load(Snake_Game)
input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
cpu.run() # Clear and run emulation

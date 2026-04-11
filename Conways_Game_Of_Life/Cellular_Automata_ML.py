from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
delay = 1/10 # Delayed printing (~10 fps)
time_start = time.perf_counter() # Global time

# ------------ DEBUG OPTIONS ------------
cpu.debug = False # Disable debuging mode

def _display(n, _, __, display_top):
  global time_start # Use timer
  print("\033[1;1H", end="")
  output = ["┌────────────────┐"]

  for i in range(n):
    binary = f"{cpu.memory[display_top]:08b}" # 8 Bit
    row_str = ''.join('██' if bit == '1' else '  ' for bit in binary)
    output.append(f"\n│{row_str}│")
    display_top = (display_top + 1) & 0xFF

  output.append("\n└────────────────┘")
  print("".join(output), end="", flush=True)

  elapsed = time.perf_counter() - time_start
  print(f"\nTime: {elapsed:.15f}"[:15] + " sec")

  time.sleep(max(0, delay - elapsed)) # 0 if negative
  time_start = time.perf_counter()

cpu.ISA[0xF] = _display

Cellular_Automata = """
2080 ; 00 + LOAD GLIDER NO.0
2160 ; 02 + LOAD GLIDER NO.1
22C0 ; 04 + LOAD GLIDER NO.2

30F8 ; 06 + ██--------------
31F9 ; 08 + --████----------
32FA ; 0A + ████------------

2DF8 ; 0C DISPLAY_TOP
2C01 ; 0E CONSTANT 01
2A03 ; 10 CONSTANT 03
2600 ; 12 G_I
2901 ; 14 G_J

2B00 ; 16 ALIVE_COUNT [NEXT]
2700 ; 18 DELTA_I

1FFF ; 1A ROW_CONFIG [GET_ROW]
1E1B ; 1C ROW_NAME

2801 ; 1E DELTA_J
2140 ; 20 ALIVE_POINTER

701F ; 22 CHECK = ALIVE_POINTER | ROW_CONFIG [CHECK]
BF30 ; 24 IF ROW_CONFIG == CHECK :COUNT++:
4080 ; 26 LOAD DELTA_J [LOAD_J]
BA34 ; 28 IF DELTA_J == 03 :ROW++:
AF01 ; 2A ROTATE ROW_CONFIG
588C ; 2C DELTA_J += 01
B022 ; 2E JMP :CHECK:
5BBC ; 30 ALIVE_COUNT += 01 [COUNT++]
B026 ; 32 JMP :LOAD_J:

5EEC ; 34 ROW_NAME += 01 [ROW++]
577C ; 36 DELTA_I += 01

2107 ; 38 LOAD CONSTANT 07
8EE1 ; 3A ROW_NAME = ROW_NAME & 07
7EED ; 3C ROW_NAME = ROW_NAME | 07
3E1B ; 3E LOAD NEW ROW_NAME

4070 ; 40 LOAD DELTA_I
BA46 ; 42 IF DELTA_I == 03 :CHECK_SELF:
B01A ; 44 JMP :GET_ROW:

2101 ; 46 LOAD POINTER 01 (0000 0001) [CHECK_SELF]
394B ; 48 LOAD G_J
A100 ; 4A ROTATE POINTER G_J TIMES

52D6 ; 4C NEW_ROW = DISPLAY_TOP + G_I
3251 ; 4E LOAD NEW_ROW (NAME)
1000 ; 50 LOAD NEW_ROW (CONFIG)

7310 ; 52 CHECK = POINTER | NEW_ROW (CONFIG)
B35C ; 54 IF CHECK == NEW_ROW (CONFIG) :COUNT--:

2003 ; 56 LOAD CONSTANT 03
BB6A ; 58 IF ALIVE_COUNT == 03 :DRAW_CELL:
B078 ; 5A JMP :ROT_POINTER:

20FF ; 5C LOAD CONSTANT FF (-1) [COUNT--]
5BB0 ; 5E ALIVE_COUNT += FF (-= 1)

2003 ; 60 LOAD CONSTANT 03
BB6A ; 62 IF ALIVE_COUNT == 03 :DRAW_CELL:
2002 ; 64 LOAD CONSTANT 02
BB6A ; 66 IF ALIVE_COUNT == 02 :DRAW_CELL:
B078 ; 68 JMP :ROT_POINTER:

20F0 ; 6A LOAD BUFFER_TOP [DRAW_CELL]
5006 ; 6C ROW = BUFFER_TOP + G_I
3073 ; 6E LOAD ROW (NAME)
3077 ; 70 LOAD ROW (NAME)
1000 ; 72 LOAD ROW (CONFIG)
7001 ; 74 NEW_ROW = ROW | POINTER (REVIVE)
3000 ; 76 STORE NEW_ROW -> BUFFER

1021 ; 78 LOAD ALIVE_POINTER [ROT_POINTER]
A001 ; 7A ROTATE ALIVE_POINTER
3021 ; 7C LOAD NEW ALIVE_POINTER

599C ; 7E G_J += 01
2009 ; 80 LOAD CONSTANT 09
B992 ; 82 IF G_J == 09 :G_I++:

20FF ; 84 LOAD ROW0 [NEXT_ROW]
5006 ; 86 ROW0 += G_I
2407 ; 88 LOAD CONSTANT 07
8004 ; 8A ROW0 = ROW0 & 07
700D ; 8C ROW0 = ROW0 | 07
301B ; 8E LOAD NEW ROW0
B016 ; 90 JMP :NEXT:

566C ; 92 G_I += 01 [G_I++]
2008 ; 94 LOAD CONSTANT 08
B69C ; 96 IF G_I == 08 :COPY_PASTE:

2901 ; 98 G_J = 01 [RESET_G_J]
B084 ; 9A JMP :NEXT_ROW:

21F0 ; 9C ORIGIN (NAME) [COPY_PASTE]
22F8 ; 9E TARGET (NAME)

31A3 ; A0 LOAD ORIGIN (NAME) [SWAP]
1300 ; A2 LOAD ORIGIN (CONFIG)
32A7 ; A4 LOAD TARGET (NAME)
3300 ; A6 STORE CONFIG (ORIGIN -> TARGET)

2000 ; A8 LOAD CONSTANT 00
31AD ; AA LOAD ORIGIN (NAME)
3000 ; AC STORE 00 TO ORIGIN

511C ; AE ORIGIN (NAME) += 01
522C ; B0 TARGET (NAME) += 01

B2B6 ; B2 IF TARGET == 00 :DISPLAY:
B0A0 ; B4 JMP :SWAP:

F8F8 ; B6 DISPLAY 8 BYTES FROM 0xF8 [DISPLAY]
2600 ; B8 G_I = 00 (RESET G_I)
B098 ; BA JMP :RESET_G_J:
"""

cpu.load(Cellular_Automata)
cpu.run() # Run

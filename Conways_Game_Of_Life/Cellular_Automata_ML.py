from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
cpu.ROWS, cpu.COLS = 11, 20 # Display x:y
cpu.debug = False # Disable debuging mode

delay = 1/10 # Delayed printing (~40 fps)
start = time.perf_counter() # Global time

def _display(*args):
  global start # Use timer
  TOP = 0xF8 # Display Start
  print("\033[30;47m", end="")
  print(f"\033[1;1H┌{'─'*(cpu.COLS-4)}┐")

  for i in range(cpu.ROWS-3):
    binary = f"{cpu.memory[TOP]:08b}" # 8 Bit
    row_str = ''.join('██' if bit == '1' else '  ' for bit in binary)
    print(f"\033[{i+2};1H│{row_str}│")
    TOP = (TOP + 1) & 0xFF

  print(f"\033[{cpu.ROWS-1};1H└{'─'*(cpu.COLS-4)}┘")
  print("\033[0m", end="")  # reset colors

  elapsed = time.perf_counter() - start
  time.sleep(max(0, delay - elapsed)) # 0 if negative
  print(f"\033[{cpu.ROWS};1HTime: {round(elapsed, 6)} sec")
  start = time.perf_counter()

cpu.ISA[0xf] = _display

Cellular_Automata = """
2080 ; 00 + LOAD GLIDER PROGRAM
30F8 ; 02 + -------------------
2060 ; 04 + -------------------
30F9 ; 06 + -------------------
20C0 ; 08 + -------------------
30FA ; 0A + -------------------

2DF8 ; 0C TOP ROW NAME
2C01 ; 0E 1 CONSTANT
2A03 ; 10 3 CONSTANT
2600 ; 12 GEN_I
2901 ; 14 GEN_J

2B00 ; 16 ALIVE_COUNT
2700 ; 18 CELL I

1FFF ; 1A ROW CONFIG
1E1B ; 1C ROW NAME

2801 ; 1E CELL J
2140 ; 20 ALIVE_MASK

701F ; 22
BF30 ; 24 IF ALIVE
4080 ; 26 LOAD CELL J
BA34 ; 28 IF CELL J == 3 => DONE
AF01 ; 2A SHIFT ROW CONFIG
588C ; 2C CELL J += 1
B022 ; 2E JMP0 TO 22
5BBC ; 30 ALIVE_COUNT += 1
B026 ; 32 JMP0 TO 26

5EEC ; 34 ROW NAME += 1
577C ; 36 CELL I += 1

2107 ; 38 LOAD ROWS - 1 (8-1)
8EE1 ; 3A AND WITH MASK
7EED ; 3C OR WITH MASK
3E1B ; 3E STORE NEXT ROW

4070 ; 40 LOAD CELL I
BA46 ; 42 IF CELL I == 3 FINISH
B01A ; 44 JMP0 TO 1A

2101 ; 46 POINTER BASE POS
394B ; 48 LOAD GEN_J
A100 ; 4A APPLY ROTATE TO POINTER

52D6 ; 4C NEW_ROW = TOP ROW + GEN_I
3251 ; 4E LOAD NEW_ROW
1000 ; 50 GET NEW_ROW CONFIG

7310 ; 52
B35C ; 54 IF ALIVE

2003 ; 56 LOAD 3
BB6A ; 58 IF ALIVE_COUNT == 3
B078 ; 5A JMP0 TO 78

20FF ; 5C LOAD -1
5BB0 ; 5E ALIVE_COUNT += -1

2003 ; 60 LOAD 3
BB6A ; 62 IF ALIVE_COUNT == 3
2002 ; 64 LOAD 2
BB6A ; 66 IF ALIVE_COUNT == 2
B078 ; 68 JMP0 TO 78

20F0 ; 6A LOAD TOP ROW (BUFFER)
5006 ; 6C TOP ROW + GEN_I (BUFFER)
3073 ; 6E LOAD NEW_ROW NAME (BUFFER)
3077 ; 70 LOAD NEW_ROW NAME (BUFFER)
1000 ; 72 GET NEW_ROW CONFIG (BUFFER)
7001 ; 74 REVIVE CELL WITH POINTER (BUFFER)
3000 ; 76 LOAD THE CHANGED ROW (BUFFER)

1021 ; 78 GET ALIVE_MASK
A001 ; 7A SHIFT ALIVE_MASK
3021 ; 7C LOAD THE CHANGED ALIVE_MASK

599C ; 7E GEN_J += 1
2009 ; 80 LOAD 9
B992 ; 82 IF GEN_J == 9 : FINISH

20FF ; 84 LOAD ROW0
5006 ; 86 ROW0 += GEN_I
2407 ; 88 LOAD ROWS - 1 (8-1)
8004 ; 8A AND WITH MASK
700D ; 8C OR WITH MASK
301B ; 8E LOAD MASKED ROW0
B016 ; 90 JMP0 TO 16

566C ; 92 GEN_I += 1
2008 ; 94 LOAD 8
B69C ; 96 IF GEN_I == 8 : FINISH

2901 ; 98 RESET GEN_J TO 1 
B084 ; 9A JMP0 TO 84

21F0 ; 9C LOAD NAME ORIGIN
22F8 ; 9E LOAD NAME TARGET

31A3 ; A0 LOAD NAME ORIGIN
1300 ; A2 GET CONFIG ORIGIN
32A7 ; A4 LOAD NAME TARGET
3300 ; A6 LOAD CONFIG (ORIGIN -> TARGET)

2000 ; A8 LOAD 0
31AD ; AA GET CURRENT NAME ORIGIN
3000 ; AC LOAD 0 TO ORIGIN

511C ; AE ORIGIN += 1
522C ; B0 TARGET += 1

B2B6 ; B2 IF TARGET == 00 : FINISH
B0A0 ; B4 JMP0 TO A0

F000 ; B6 DISPLAY CHANGES
2600 ; B8 RESET GEN_I TO 0
B098 ; BA JMP0 TO 98

C000 ; BC HALT
"""  # PC = 0

cpu.load(Cellular_Automata)
print("""
     CONWAY'S GAME OF ...
┌────────────────────────────┐
│ █      ▀▀█▀▀  █▀▀▀▀  █▀▀▀▀ │
│ █        █    █      █     │
│ █        █    █■■■■  █■■■■ │
│ █        █    █      █     │
│ █▄▄▄▄  ▄▄█▄▄  █      █▄▄▄▄ │
└────────────────────────────┘
""")
input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
cpu.run() # Clear and run emulation

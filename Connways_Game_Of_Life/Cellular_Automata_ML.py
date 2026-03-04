from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
cpu.ROWS, cpu.COLS = 11, 20 # Display x:y
cpu.debug = False # Disable debuging mode

delay = 1/10 # Delayed printing (~40 fps)
start = time.perf_counter() # Global time

# --- GLIDER ---
cpu.memory[0xF8] = 0x80
cpu.memory[0xF9] = 0x60
cpu.memory[0xFA] = 0xC0

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
2DF8 ; 00 TOP ROW NAME
2C01 ; 02 1 CONSTANT
2A03 ; 04 3 CONSTANT
2600 ; 06 GEN_I
2901 ; 08 GEN_J

2B00 ; 0A ALIVE_COUNT
2700 ; 0C CELL I

1FFF ; 0E ROW CONFIG
1E0F ; 10 ROW NAME

2801 ; 12 CELL J
2140 ; 14 ALIVE_MASK

701F ; 16
BF24 ; 18 IF ALIVE
4080 ; 1A LOAD CELL J
BA28 ; 1C IF CELL J == 3 => DONE
AF01 ; 1E SHIFT ROW CONFIG
588C ; 20 CELL J += 1
B016 ; 22 JMP0 TO 16
5BBC ; 24 ALIVE_COUNT += 1
B01A ; 26 JMP0 TO 1A

5EEC ; 28 ROW NAME += 1
577C ; 2A CELL I += 1

2107 ; 2C LOAD ROWS - 1 (8-1)
8EE1 ; 2E AND WITH MASK
7EED ; 30 OR WITH MASK
3E0F ; 32 STORE NEXT ROW

4070 ; 34 LOAD CELL I
BA3A ; 36 IF CELL I == 3 FINISH
B00E ; 38 JMP0 TO 0E

2101 ; 3A POINTER BASE POS
393F ; 3C LOAD GEN_J
A100 ; 3E APPLY ROTATE TO POINTER

52D6 ; 40 NEW_ROW = TOP ROW + GEN_I
3245 ; 42 LOAD NEW_ROW
1000 ; 44 GET NEW_ROW CONFIG

7310 ; 46
B350 ; 48 IF ALIVE

2003 ; 4A LOAD 3
BB5E ; 4C IF ALIVE_COUNT == 3
B06C ; 4E JMP0 TO 6C

20FF ; 50 LOAD -1
5BB0 ; 52 ALIVE_COUNT += -1

2003 ; 54 LOAD 3
BB5E ; 56 IF ALIVE_COUNT == 3
2002 ; 58 LOAD 2
BB5E ; 5A IF ALIVE_COUNT == 2
B06C ; 5C JMP0 TO 6C

20F0 ; 5E LOAD TOP ROW (BUFFER)
5006 ; 60 TOP ROW + GEN_I (BUFFER)
3067 ; 62 LOAD NEW_ROW NAME (BUFFER)
306B ; 64 LOAD NEW_ROW NAME (BUFFER)
1000 ; 66 GET NEW_ROW CONFIG (BUFFER)
7001 ; 68 REVIVE CELL WITH POINTER (BUFFER)
3000 ; 6A LOAD THE CHANGED ROW (BUFFER)

1015 ; 6C GET ALIVE_MASK
A001 ; 6E SHIFT ALIVE_MASK
3015 ; 70 LOAD THE CHANGED ALIVE_MASK

599C ; 72 GEN_J += 1
2009 ; 74 LOAD 9
B986 ; 76 IF GEN_J == 9 : FINISH

20FF ; 78 LOAD ROW0
5006 ; 7A ROW0 += GEN_I
2407 ; 7C LOAD ROWS - 1 (8-1)
8004 ; 7E AND WITH MASK
700D ; 80 OR WITH MASK
300F ; 82 LOAD MASKED ROW0
B00A ; 84 JMP0 TO 0A

566C ; 86 GEN_I += 1
2008 ; 88 LOAD 8
B690 ; 8A IF GEN_I == 8 : FINISH

2901 ; 8C RESET GEN_J TO 1 
B078 ; 8E JMP0 TO 78

21F0 ; 90 LOAD NAME ORIGIN
22F8 ; 92 LOAD NAME TARGET

3197 ; 94 LOAD NAME ORIGIN
1300 ; 96 GET CONFIG ORIGIN
329B ; 98 LOAD NAME TARGET
3300 ; 9A LOAD CONFIG (ORIGIN -> TARGET)

2000 ; 9C LOAD 0
31A1 ; 9E GET CURRENT NAME ORIGIN
3000 ; A0 LOAD 0 TO ORIGIN

511C ; A2 ORIGIN += 1
522C ; A4 TARGET += 1

B2AA ; A6 IF TARGET == 00 : FINISH
B094 ; A8 JMP0 TO 94

F000 ; AA DISPLAY CHANGES
2600 ; AC RESET GEN_I TO 0
B08C ; AE JMP0 TO 8C

C000 ; 70 HALT
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

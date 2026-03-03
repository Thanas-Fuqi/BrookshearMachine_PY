import os, sys, time

delay = 0 #Delay run
if "-f" in sys.argv:
  index = sys.argv.index("-f")
  delay = 1/int(sys.argv[index + 1])

os.system("") # enable ANSI
log_buffer = [] # buffer
ROWS, COLS = 11, 20

memory = [0] * 256
register = [0] * 16

# --- GLIDER ---
memory[0xF8] = 0x80
memory[0xF9] = 0x60
memory[0xFA] = 0xC0

def log(*args):
  if not "-d" in sys.argv:
    return # Skip if not debug
  msg = " ".join(map(str, args))
  log_buffer.append(msg)
  visible_logs = log_buffer[-ROWS:]

  for i, line in enumerate(visible_logs):
    print(f"\033[{i+1};{COLS}H\033[92m{line}\033[0m\033[K",end="")

  print("", end="", flush=True)

def run(PC):
  start = time.perf_counter()
  while True:
    current_byte = memory[PC]
    next_byte = memory[(PC + 1) & 0xFF]

    o0 = (current_byte >> 4) & 0xF
    o1 = current_byte & 0xF
    o2 = (next_byte >> 4) & 0xF
    o3 = next_byte & 0xF

    code = f"{((current_byte << 8) | next_byte):04X}"

    if o0 == 0x1:
      log("%02X"%PC, ":",code,": Loaded register",o1,"with bit pattern of Memory",next_byte)
      register[o1] = memory[next_byte]
    elif o0 == 0x2:
      log("%02X"%PC, ":",code,": Loaded register",o1,"with bit pattern",next_byte)
      register[o1] = next_byte
    elif o0 == 0x3:
      log("%02X"%PC, ":",code,": Loaded Memory",next_byte,"with bit pattern of register",o1)
      memory[next_byte] = register[o1]
    elif o0 == 0x4:
      log("%02X"%PC, ":",code,": Copied the bit pattern of register",o2,"to register",o3)
      register[o3] = register[o2]
    elif o0 == 0x5:
      log("%02X"%PC, ":",code,": Sum-ed registers",o2,"and",o3,"added the result to",o1)
      register[o1] = (register[o2] + register[o3]) & 0xFF
    # elif o0 == 0x6: # Addition in floating point numbers
    elif o0 == 0x7:
      log("%02X"%PC, ":",code,": OR-ed registers",o2,"and",o3,"added the result to",o1)
      register[o1] = register[o2] | register[o3]
    elif o0 == 0x8:
      log("%02X"%PC, ":",code,": AND-ed registers",o2,"and",o3,"added the result to",o1)
      register[o1] = register[o2] & register[o3]
    elif o0 == 0x9:
      log("%02X"%PC, ":",code,": XOR-ed registers",o2,"and",o3,"added the result to",o1)
      register[o1] = register[o2] ^ register[o3]
    elif o0 == 0xA:
      n, v = o3 % 8, register[o1]
      register[o1] = ((v >> n) | (v << (8 - n))) & 0xFF
    elif o0 == 0xB:
      if register[0] == register[o1]:
        PC = next_byte
        continue
      log("%02X"%PC, ":",code,": Failed to jump to Memory adress",next_byte)
    elif o0 == 0xC:
      log("%02X"%PC, ":",code,": Code halted without errors")
      break

    elif o0 == 0xF:
      TOP = 0xF8 # Display Start
      print("\033[30;47m", end="")
      print(f"\033[1;1H┌{'─'*(COLS-4)}┐")

      for i in range(ROWS-3):
        binary = f"{memory[TOP]:08b}" # 8 Bit
        row_str = ''.join('██' if bit == '1' else '  ' for bit in binary)
        print(f"\033[{i+2};1H│{row_str}│")
        TOP = (TOP + 1) & 0xFF

      print(f"\033[{ROWS-1};1H└{'─'*(COLS-4)}┘")

      elapsed = time.perf_counter() - start
      time.sleep(max(0, delay - elapsed)) # 0 if negative
      print(f"\033[{ROWS};1HTime: {round(elapsed, 6)} sec")
      start = time.perf_counter()

      print("\033[0m", end="")  # reset colors

    else:
      log("%02X"%PC, ":",code,": Code halted with errors !")
      break

    PC = (PC + 2) & 0xFF

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

data = Cellular_Automata
PC = 0

if "\n" in data:
  lines = data.splitlines()

  cleaned = []
  for line in lines: # remove ; AND space
    line = line.split(";")[0].strip()
    if line: # Skip empty lines
      cleaned.append(line)

  data = "".join(cleaned)

for i in range(0, len(data), 2):
  memory[PC] = int(data[i:i+2], 16)
  PC = (PC + 1) & 0xFF

input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
run(0)






























from Machine_language_CORE import Machine
import time # Calculate delay and overhead

cpu = Machine() # Init a machine instance
delay = 1 # Add a delay to debug printing
cpu.ROWS, cpu.COLS = 13, 20 # Display x:y
start = time.perf_counter() # Global time

def _display(*args):
  global start # Use timer
  TOP = 0xF6 # Display Start
  print(f"\033[1;1H┌{'─'*(cpu.COLS-4)}┐")

  for i in range(cpu.ROWS-3):
    binary = f"{cpu.memory[TOP]:08b}" # 8 Bit
    row_str = ''.join('██' if bit == '1' else '  ' for bit in binary)
    print(f"\033[{i+2};1H│{row_str}│")
    TOP = (TOP + 1) & 0xFF

  print(f"\033[{cpu.ROWS-1};1H└{'─'*(cpu.COLS-4)}┘")

  elapsed = time.perf_counter() - start
  time.sleep(max(0, delay - elapsed)) # 0 if negative
  print(f"\033[{cpu.ROWS};1HTime: {round(elapsed, 6)} sec")
  start = time.perf_counter()

cpu.ISA[0xf] = _display

Loop_7_Segments = """
20FC ; 00 NUM 0
30E6 ; 02
2060 ; 04 NUM 1
30E7 ; 06
20DA ; 08 NUM 2
30E8 ; 0A
20F2 ; 0C NUM 3
30E9 ; 0E
2066 ; 10 NUM 4
30EA ; 12
20B6 ; 14 NUM 5
30EB ; 16
20BE ; 18 NUM 6
30EC ; 1A
20E4 ; 1C NUM 7 
30ED ; 1E
20FE ; 20 NUM 8
30EE ; 22
20F6 ; 24 NUM 9
30EF ; 26
20EE ; 28 NUM A
30F0 ; 2A
203E ; 2C NUM B
30F1 ; 2E
209C ; 30 NUM C
30F2 ; 32
207A ; 34 NUM D
30F3 ; 36
209E ; 38 NUM E
30F4 ; 3A
208E ; 3C NUM F
30F5 ; 3E

1FE6 ; 40 CUREENT STATE

2080 ; 42 BAR A
70F0 ; 44
BF4A ; 46
B04E ; 48
2138 ; 4A
31F7 ; 4C

2040 ; 4E BAR B
70F0 ; 50
BF56 ; 52
B062 ; 54

2104 ; 56
10F8 ; 58
7001 ; 5A
30F8 ; 5C
30F9 ; 5E
30FA ; 60

2020 ; 62 BAR C
70F0 ; 64
BF6A ; 66
B076 ; 68

2104 ; 6A
10FC ; 6C
7001 ; 6E
30FC ; 70
30FD ; 72
30FE ; 74

2010 ; 76 BAR D
70F0 ; 78
BF7E ; 7A
B082 ; 7C
2138 ; 7E
31FF ; 80

2008 ; 82 BAR E
70F0 ; 84
BF8A ; 86
B096 ; 88

2140 ; 8A
10FC ; 8C
7001 ; 8E
30FC ; 90
30FD ; 92
30FE ; 94

2004 ; 96 BAR F
70F0 ; 98
BF9E ; 9A
B0AA ; 9C

2140 ; 9E
10F8 ; A0
7001 ; A2
30F8 ; A4
30F9 ; A6
30FA ; A8

2002 ; AA BAR G
70F0 ; AC
BFB2 ; AE
B0B6 ; B0
2138 ; B2
31FB ; B4

F000 ; B6 DISPLAY CHANGES

2000 ; B8 CLEAR
2101 ; BA INCREMENT

30F6 ; BC ADD 0
12BD ; BE
5212 ; C0
B2C8 ; C2
32BD ; C4
B0BC ; C6

1041 ; C8
22F6 ; CA
32BD ; CC RESTART CLEAR

5001 ; CE
B2D6 ; D0 ADD E6
3041 ; D2
B040 ; D4 BACK UP
20E6 ; D6
B0D2 ; D8

C000 ; DA HALT
"""  # PC = "00"

cpu.load(Loop_7_Segments)
print("""
┌────────────────────────┐
│ █    █  █▀▀▀▀  ▀▄   ▄▀ │
│ █    █  █       ▀▄ ▄▀  │
│ █■■■■█  █■■■■    ▄▀▄   │
│ █    █  █       ▄▀ ▀▄  │
│ █    █  █▄▄▄▄  ▄▀   ▀▄ │
└────────────────────────┘
""")
input("PRESS ANY KEY ... ")
print("\033[2J\033[1;1H", end="")
cpu.run() # Clear and run emulation

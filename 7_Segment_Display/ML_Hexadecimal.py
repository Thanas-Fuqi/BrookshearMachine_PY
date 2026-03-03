from Machine_language_CORE import Machine
import time # Used for timing delays

cpu = Machine() # Init a machine instance
cpu.ROWS, cpu.COLS = 13, 20 # Display x:y

delay = 1/5 # Delayed printing (~5 fps)
start = time.perf_counter() # Global Time

def _display(*args):
  global start # Use timer
  TOP = 0xF6 # Display Start
  print(f"\033[1;1H┌{'─'*(cpu.COLS-4)}┐")

  for i in range(cpu.ROWS-3):
    binary = f"{cpu.memory[TOP]:08b}" # 8 Bit
    row_str = "".join("██" if bit == "1" else "  " for bit in binary)
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

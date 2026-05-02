from Machine_language_CORE import Machine
import threading, msvcrt, time

cpu = Machine() # Init a machine instance
cpu.time_start = time.perf_counter()

# ------------ DEBUG OPTIONS ------------
cpu.debug = False # Disable debuging mode

def _listener():
	while True:
		if msvcrt.kbhit():
			cpu.register[0xF] = msvcrt.getch()[0]
		time.sleep(0.001)

threading.Thread(target=_listener, daemon=True).start()

def _display(n, _, __, display_top):
  print("\033[1;1H", end="")
  output = [f"┌{'─'*(n*2)}┐"]

  for i in range(7, -1, -1):
    row_str = ""
    dis = display_top
    for _ in range(n):
      bit = f"{cpu.memory[dis]:08b}"[i]

      if (dis == cpu.register[0x7]) and ((cpu.register[0x6] << i) & 0x80):
        row_str += "\033[96m██\033[0m"
      elif dis==display_top+(n//2) and i%2==1:
        row_str += "██"
      else:
        row_str += "██" if bit == "1" else "  "

      dis = (dis+1) & 0xFF
    output.append(f"\n│{row_str}│")

  output.append(f"\n└{'─'*(n-1)}\033[30;47m──\033[0m{'─'*(n-1)}┘\n")

  score_1 = cpu.register[0xB]
  score_2 = cpu.register[0xA]

  final_message = ""
  if score_1 == 11:
    final_message = f"{'Player 1 has WON':^{(n+1)*2}}"
  elif score_2 == 11:
    final_message = f"{'Player 2 has WON':^{(n+1)*2}}"
  else:
    txt_1 = f"{cpu.register[0xB]:02d}"
    txt_2 = f"{cpu.register[0xA]:02d}"
    final_message = f"{txt_1:^{n+1}}{txt_2:^{n+1}}"

  output.append(f"\033[91m{final_message}\033[0m\n")
  print("".join(output), end="", flush=True)

  elapsed = time.perf_counter() - cpu.time_start
  time.sleep(max(0, 1/3000 - elapsed))
  cpu.time_start = time.perf_counter()

cpu.ISA[0xF] = _display

Pong = """
2E00 ; 00 CYCLE_COUNT

2D0E ; 02 P1_PADDLE
2C70 ; 04 P2_PADDLE

2B00 ; 06 P1_SCORE
2A00 ; 08 P2_SCORE

2901 ; 0A BALL_Y_DELTA (ROTATION)
2801 ; 0C BALL_X_DELTA (ADDITION)

27F8 ; 0E BALL_ROW (X_POS)
2610 ; 10 BALL_POS (Y_POS)


3715 ; 12 LOAD BALL_ROW (NAME) [LOOP]
3600 ; 14 ADD BALL_POS TO BALL_ROW


2077 ; 16 LOAD b'W'
BF1C ; 18 IF KEY == b'W' :EDGE:
B024 ; 1A JMP :SKIP:
2007 ; 1C LOAD EDGE CASE [EDGE]
BD24 ; 1E IF P1_PADDLE == EDGE :SKIP:
AD01 ; 20 MOVE P1_PADDLE UP
2F00 ; 22 RESET KEY

2073 ; 24 LOAD b's' [SKIP]
BF2A ; 26 IF KEY == b's' :EDGE:
B032 ; 28 JMP :SKIP:
20E0 ; 2A LOAD EDGE CASE [EDGE]
BD32 ; 2C IF P1_PADDLE == EDGE :SKIP:
AD07 ; 2E MOVE P1_PADDLE DOWN
2F00 ; 30 RESET KEY

2069 ; 32 LOAD b'i' [SKIP]
BF38 ; 34 IF KEY == b'i' :EDGE:
B040 ; 36 JMP :SKIP:
2007 ; 38 LOAD EDGE CASE [EDGE]
BC40 ; 3A IF P2_PADDLE == EDGE :SKIP:
AC01 ; 3C MOVE P2_PADDLE UP
2F00 ; 3E RESET KEY

206B ; 40 LOAD b'k' [SKIP]
BF46 ; 42 IF KEY == b'k' :EDGE:
B04E ; 44 JMP :SKIP:
20E0 ; 46 LOAD EDGE CASE [EDGE]
BC4E ; 48 IF P2_PADDLE == EDGE :SKIP:
AC07 ; 4A MOVE P2_PADDLE DOWN
2F00 ; 4C RESET KEY

3DF1 ; 4E STORE NEW_P1 [SKIP]
3CFF ; 50 STORE NEW_P2


2501 ; 52 LOAD CONST 01

20C8 ; 54 LOAD CONST C8
BE5A ; 56 IF CYCLE_COUNT == C8 :MOVE_BALL:
B09C ; 58 JMP :SKIP:


2E00 ; 5A RESET CYCLE_COUNT [MOVE_BALL]
2000 ; 5C LOAD CONST 00
3761 ; 5E LOAD PREV_BALL_ROW (NAME)
3000 ; 60 STORE 00 TO PREV_BALL_ROW


20F2 ; 62 LOAD P1_SIDE
B76C ; 64 IF BALL_ROW == P1_SIDE :CHECK_P1:

20FE ; 66 LOAD P2_SIDE
B774 ; 68 IF BALL_ROW == P2_SIDE :CHECK_P2:

B086 ; 6A JMP :CHECK_Y:


70D6 ; 6C CHECK = P1_PADDLE | BALL_POS [CHECK_P1]
BD80 ; 6E IF CHECK == P1_PADDLE :REVERSE_LEFT:
5AA5 ; 70 P2_SCORE += 01
B07A ; 72 JMP :RESET:

70C6 ; 74 CHECK = P2_PADDLE | BALL_POS [CHECK_P2]
BC84 ; 76 IF CHECK == P2_PADDLE :REVERSE_RIGHT:
5BB5 ; 78 P1_SCORE += 01

27F8 ; 7A RESET BALL_ROW [RESET]
2610 ; 7C RESET BALL_POS
B086 ; 7E JMP :CHECK_Y:

2801 ; 80 TURN RIGHT [REVERSE_LEFT]
B086 ; 82 JMP :CHECK_Y:
28FF ; 84 TURN LEFT [REVERSE_RIGHT]


2080 ; 86 LOAD LOW_Y [CHECK_Y]
B690 ; 88 IF BALL_POS == LOW_Y :LOAD_UP:

2001 ; 8A LOAD HIGH_Y
B694 ; 8C IF BALL_POS == HIGH_Y :LOAD_DOWN:

B096 ; 8E JMP :APPLY_CHANGES:

2901 ; 90 LOAD UP_Y_DELTA [LOAD_UP]
B096 ; 92 JMP :APPLY_CHANGES:
2907 ; 94 LOAD DOWN_Y_DELTA [LOAD_DOWN]


3999 ; 96 LOAD BALL_Y_DELTA (NAME) [APPLY_CHANGES]
A600 ; 98 MOVE BALL_POS
5778 ; 9A BALL_ROW += BALL_X_DELTA


5EE5 ; 9C CYCLE_COUNT += 01 [SKIP]
FFF1 ; 9E DISPLAY F ROWS FROM F1

200B ; A0 LOAD WIN_SCORE (11)
BAA8 ; A2 IF P2_SCORE == WIN_SCORE :BREAK:
BBA8 ; A4 IF P1_SCORE == WIN_SCORE :BREAK:

B012 ; A6 JMP :LOOP:
C000 ; A8 HALT EXECUTION [BREAK]
"""
cpu.load(Pong)
cpu.run() # Run

from Machine_language_CORE import Machine
import time, random, winsound # Used Libs

cpu = Machine() # Init a machine instance
delay = 1/2 # Delayed to print ( ~2 fps )
time_start = time.perf_counter() # Global
span = 0x27 # The span of the array width

# ------------ DEBUG OPTIONS ------------
cpu.debug = False # Disable debuging mode

def _display(o1, _, __, nb):
  global time_start # Use timer
  print("\033[1;1H", end="")
  output = [f"┌{'─'*span}┐"]

  for i in range(o1):
    val = cpu.memory[nb + i]
    color = "\033[92m" if nb+i < cpu.register[0x2] else ""
    output.append(f"\n│{color}{'■'*val}{' '*(span-val)}\033[0m│")

  amount = 0xFF - cpu.register[0x2]
  output.append(
    f"\n└{'─'*span}┘"
    f"\n┌───────────────┐"
    f"\n│\033[96m{'█'*(o1-amount)}{' '*amount}\033[0m│ "
    f"{(o1-amount)*6.6666:5.1f}% Time: "
  )

  print("".join(output), end="", flush=True)
  elapsed = time.perf_counter() - time_start
  print(f"{elapsed:6.4f} sec\n└───────────────┘")

  winsound.Beep(2500, 30)
  time.sleep(max(0, delay - elapsed))
  time_start = time.perf_counter()

cpu.ISA[0xF] = _display

for i in range(0xF):
  cpu.memory[0xF0 + i] = random.randint(0, span)

Sort_ML = """
2101 ; 00 LOAD CONST 01
22F0 ; 02 LOAD ROW_I
5421 ; 04 ROW_J = ROW_I + 01 [TOP]

20FF ; 06 LOAD FF [CHECK_I]
B240 ; 08 IF ROW_I == FF :BREAK:
320D ; 0A LOAD ROW_I (NAME)
1300 ; 0C LAOD ROW_I (CONFIG) (NUM_1)

2000 ; 0E LOAD 00 [NEXT_CHECK]
B43A ; 10 IF ROW_J = 00 :ROW_I++:
3415 ; 12 LOAD ROW_J (NAME)
1500 ; 14 LAOD ROW_J (CONFIG) (NUM_2)

2680 ; 16 LOAD MASK (MSB)

4030 ; 18 LOAD NUM_1
B52C ; 1A NUM_1 == NUM_2 :ROW_J++:

7036 ; 1C CHECK = NUM_1 | MASK [COMPARE]
B328 ; 1E IF CHECK == NUM_1 :CHECK_2:
7056 ; 20 CHECK = NUM_2 | MASK
B530 ; 22 IF CHECK == NUM_2 :SWAP:
A601 ; 24 ROTATE MASK 1 RIGHT [NEXT_MASK]
B01C ; 26 JMP :COMPARE:
7056 ; 28 CHECK = NUM_2 | MASK [CHECK_2]
B524 ; 2A IF CHECK == NUM_2 :NEXT_MASK:

5441 ; 2C ROW_J += 01 [ROW_J++]
B006 ; 2E JMP :CHECK_I:

3237 ; 30 LOAD ROW_I (NAME) [SWAP]
3435 ; 32 LOAD ROW_J (NAME)
3300 ; 34 LOAD NUM_1 -> ROW_J
3500 ; 36 LOAD NUM_2 -> ROW_I
B02C ; 38 JMP :ROW_J++:

5221 ; 3A ROW_I += 01 [ROW_I++]
FFF0 ; 3C PRINT F ROWS FROM F0
B004 ; 3E JMP :TOP:

C000 ; 40 HALT [BREAK]
"""

cpu.load(Sort_ML)
cpu.run() # Run

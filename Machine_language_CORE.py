import os
os.system("") # enable ANSI

class Machine():
  def __init__(self):
    self.memory = [0] * 256 # RAM Memory
    self.register = [0] * 16 # CPU registers

    self.halted = False # Run until halt is True
    self.PC = 0 # Initial state of Program Counter

    self.debug = True # Enable Printing by default
    self.log_buffer = [] # Hold every printed line
    self.ROWS = 0 # Start with all rows printed
    self.COLS = 1 # Start from the first column

    self.ISA = { # OPCODE : ACTION
      0x1: self._load_mem,
      0x2: self._load_val,
      0x3: self._store,
      0x4: self._move,
      0x5: self._add,
      #0x6: self._add_float,
      0x7: self._or,
      0x8: self._and,
      0x9: self._xor,
      0xA: self._rotate,
      0xB: self._jump,
      0xC: self._halt,
    }

  # --- Printing Logic ---
  def log(self, *args):
    if not self.debug:
      return # Skip if not debug mode

    formatted = []
    for a in args:
      if isinstance(a, int): # If a number, format 2-digit hex
        formatted.append(f"{a:02X}")
      else:
        formatted.append(str(a))  # Leave strings as-is
    # The formatted string to print
    msg = " ".join(formatted)

    # If not constrained print all
    if self.ROWS == 0:
      print(msg) # Basic Printing
    # Otherwise print "ROWS" rows
    else:
      self.log_buffer.append(msg)
      visible_logs = self.log_buffer[-self.ROWS:]

      for i, line in enumerate(visible_logs):
        print(f"\033[{i+1};{self.COLS}H\033[92m{line}\033[0m\033[K",end="")

      print("", end="", flush=True)

  # operation(o1, o2, o3, next_byte, code)
  # --- Instruction Set Functions ---
  def _load_mem(self, o1, o2, o3, next_byte, code):
    self.log(self.PC-2,":",code,": Loaded register",o1,"with bit pattern of Memory",next_byte)
    self.register[o1] = self.memory[next_byte]

  def _load_val(self, o1, o2, o3, next_byte, code):
    self.log(self.PC-2,":",code,": Loaded register", o1, "with bit pattern", next_byte)
    self.register[o1] = next_byte

  def _store(self, o1, o2, o3, next_byte, code):
    self.log(self.PC-2,":",code,": Loaded Memory",next_byte,"with bit pattern of register",o1)
    self.memory[next_byte] = self.register[o1]

  def _move(self, _, o2, o3, __, code):
    self.log(self.PC-2,":",code,": Copied the bit pattern of register",o2,"to register",o3)
    self.register[o3] = self.register[o2]

  def _add(self, o1, o2, o3, _, code):
    self.log(self.PC-2,":",code,": Sum-ed registers",o2,"and",o3,"added the result to",o1)
    self.register[o1] = (self.register[o2] + self.register[o3]) & 0xFF

  #def _add_float(self, o1, o2, o3, next_byte, code):

  def _or(self, o1, o2, o3, _, code):
    self.log(self.PC-2,":",code,": OR-ed registers",o2,"and",o3,"added the result to",o1)
    self.register[o1] = self.register[o2] | self.register[o3]

  def _and(self, o1, o2, o3, _, code):
    self.log(self.PC-2,":",code,": AND-ed registers",o2,"and",o3,"added the result to",o1)
    self.register[o1] = self.register[o2] & self.register[o3]

  def _xor(self, o1, o2, o3, _, code):
    self.log(self.PC-2,":",code,": XOR-ed registers",o2,"and",o3,"added the result to",o1)
    self.register[o1] = self.register[o2] ^ self.register[o3]

  def _rotate(self, o1, _, o3, __, code):
    self.log(self.PC-2,":",code,": Rotated bits of register",o1,",",o3,"times to the right")
    n, v = o3 % 8, self.register[o1]
    self.register[o1] = ((v >> n) | (v << (8 - n))) & 0xFF

  def _jump(self, o1, o2, o3, next_byte, code):
    if self.register[0] == self.register[o1]:
      self.log(self.PC-2,":",code,": Jumped successfully to Memory adress",next_byte)
      self.PC = next_byte
    else:
      self.log(self.PC-2,":",code,": Failed to jump to Memory adress",next_byte)

  def _halt(self, _, __, ___, ____, code):
    self.log(self.PC-2,":",code,": Code halted without errors")
    self.halted = True

  # --- The main execution loop ---
  def run(self):    
    while not self.halted:
      # 1. Fetch
      current_byte = self.memory[self.PC]
      next_byte = self.memory[(self.PC + 1) & 0xFF]

      # 2. Decode
      o0 = (current_byte >> 4) & 0xF
      o1 = current_byte & 0xF
      o2 = (next_byte >> 4) & 0xF
      o3 = next_byte & 0xF

      code = f"{((current_byte << 8) | next_byte):04X}"
      
      # 3. Execute
      operation = self.ISA.get(o0)
      self.PC = (self.PC + 2) & 0xFF

      if operation:
        operation(o1, o2, o3, next_byte, code)
      else:
        self.log(self.PC-2,":",code,": Code halted with errors !")
        break

  def load(self, hex_string):
    # --- Cleans and loads a hex string into memory. ---
    # Remove comments and whitespace
    if "\n" in hex_string:
      lines = hex_string.splitlines()

      cleaned = []
      for line in lines: # remove ; AND space
        line = line.split(";")[0].strip()
        if line: # Skip empty lines
          cleaned.append(line)

      hex_string = "".join(cleaned)

    load_i = self.PC
    for i in range(0, len(hex_string), 2):
      self.memory[load_i] = int(hex_string[i:i+2], 16)
      load_i = (load_i + 1) & 0xFF

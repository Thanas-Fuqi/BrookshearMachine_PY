import os, re
os.system("") # enable ANSI

class Machine():
  def __init__(self):
    self.memory = [0] * 256 # RAM Memory
    self.register = [0] * 16 # CPU registers

    self.halted = False # Run until halt is True
    self.PC = 0 # Initial state of Program Counter

    self.debug = True # Enable Printing by default
    self.log_buffer = [] # Hold every printed line
    self.ROWS, self.COLS = 0, 1 # Start terminal xy

    self.color = {
      "D" : "\033[0m",                # [D]efault -> reset
      "R" : "\033[38;2;0;188;212m",   # [R]egister -> teal cyan
      "C" : "\033[38;2;105;255;71m",  # [C]ode -> neon green
      "M" : "\033[38;2;255;64;129m",  # [M]emory -> hot red
      "G" : "\033[38;2;107;114;128m", # [G]ray -> muted gray
    }

    self.ISA = { # OPCODE : lambda x: ACTION x
      0x1: lambda o1, _, __, nb: self.register.__setitem__(o1, self.memory[nb]),
      0x2: lambda o1, _, __, nb: self.register.__setitem__(o1, nb),
      0x3: lambda o1, _, __, nb: self.memory.__setitem__(nb, self.register[o1]),
      0x4: lambda _, o2, o3, __: self.register.__setitem__(o3, self.register[o2]),
      0x5: lambda o1, o2, o3, _: self.register.__setitem__(o1, (self.register[o2] + self.register[o3]) & 0xFF),
      0x7: lambda o1, o2, o3, _: self.register.__setitem__(o1, self.register[o2] | self.register[o3]),
      0x8: lambda o1, o2, o3, _: self.register.__setitem__(o1, self.register[o2] & self.register[o3]),
      0x9: lambda o1, o2, o3, _: self.register.__setitem__(o1, self.register[o2] ^ self.register[o3]),
      0xA: lambda o1, _, o3, __: self.register.__setitem__(o1, ((self.register[o1] >> (o3 % 8)) | (self.register[o1] << (8 - (o3 % 8)))) & 0xFF),
      0xB: lambda o1, _, __, nb: self.__setattr__("PC", nb) if self.register[0] == self.register[o1] else None,
      0xC: lambda *_: self.__setattr__("halted", True),
    }

    self.log_dispatcher = {
      0x1: lambda o1, _, __, nb, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : Loaded register [R]{o1:X}[G] with bit pattern of memory [M]{nb:02X}[D]",
      0x2: lambda o1, _, __, nb, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : Loaded register [R]{o1:X}[G] with bit pattern [M]{nb:02X}[D]",
      0x3: lambda o1, _, __, nb, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : Loaded memory [M]{nb:02X}[G] with bit pattern of register [R]{o1:X}[D]",
      0x4: lambda _, o2, o3, __, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : Copied the bit pattern of register [R]{o2:X}[G] to register [R]{o3:X}[D]",
      0x5: lambda o1, o2, o3, _, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : Sum-ed registers [R]{o2:X}[G] and [R]{o3:X}[G], place the result in [R]{o1:X}[D]",
      0x7: lambda o1, o2, o3, _, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : OR--ed registers [R]{o2:X}[G] and [R]{o3:X}[G], place the result in [R]{o1:X}[D]",
      0x8: lambda o1, o2, o3, _, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : AND-ed registers [R]{o2:X}[G] and [R]{o3:X}[G], place the result in [R]{o1:X}[D]",
      0x9: lambda o1, o2, o3, _, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : XOR-ed registers [R]{o2:X}[G] and [R]{o3:X}[G], place the result in [R]{o1:X}[D]",
      0xA: lambda o1, _, o3, __, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : ROR bits of register [R]{o1:X}[G] , [R]{o3:X}[G] times to the right[D]",
      0xB: lambda _, __, ___, nb, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : Attempted to jump to memory address [M]{nb:02X}[D]",
      0xC: lambda _, __, ___, ____, code: f"{self.PC-2:02X}[G] : [C]{code}[G] : Code halted without errors[D]",
    }

  # --- Printing Logic ---
  def log(self, args):
    apply_color = lambda m: self.color.get(m.group(1), "")
    msg = re.sub(r'\[(\w+)\]', apply_color, args)
    self.log_buffer.append(msg)

    if self.ROWS == 0:
      print(msg)
    else:
      for i, line in enumerate(self.log_buffer[-self.ROWS:]):
        print(f"\033[{i+1};{self.COLS}H{line}\033[K", end="")
      print("", end="", flush=True)

  # --- The main execution loop ---
  def run(self):
    _default_op = lambda *_: (self.log(f"Error : [M]Unknown[G] opcode ... [D]"), self.__setattr__("halted", True))
    _default_lo = lambda *_: f"{self.PC-2:02X}[G] : [M]No[G] logs where found ...[D]" # Default entry if no logs

    while not self.halted:
      # 1. Fetch
      current_byte = self.memory[self.PC]
      next_byte = self.memory[(self.PC + 1) & 0xFF]

      # 2. Decode
      o0 = (current_byte >> 4) & 0xF
      o1 = current_byte & 0xF
      o2 = (next_byte >> 4) & 0xF
      o3 = next_byte & 0xF

      # 3. Execute
      operation = self.ISA.get(o0, _default_op)
      self.PC = (self.PC + 2) & 0xFF

      if self.debug: # If debug mode print text
        code = f"{((current_byte << 8) | next_byte):04X}"
        thisLog = self.log_dispatcher.get(o0, _default_lo)
        self.log(thisLog(o1, o2, o3, next_byte, code))

      operation(o1, o2, o3, next_byte)

  def load(self, hex_string):
    hex_string = "".join( # Remove commented ";"
      line.split(";")[0].strip() # Remove new lines
      for line in hex_string.splitlines()
    )

    for i, byte in enumerate(bytes.fromhex(hex_string)):
      self.memory[(self.PC + i) & 0xFF] = byte

  # --- DEBUG TOOLS (DUMPS) ---
  # RUN in root python -i -m folder.file
  def memory_dump(self):
    cols = "   " + "  ".join(f"{c:2X}" for c in range(16))
    regs = "   " + "  ".join(f"{self.register[c]:02X}" for c in range(16))
    mem  = "\n".join(
      f"{r:X}  " + "  ".join(f"{self.memory[r*16+c]:02X}" for c in range(16)) for r in range(16)
    )

    with open("memory_dump.txt", "w") as f:
      f.write(f"{cols}\n{regs}\n\n{cols}\n{mem}")

  def log_dump(self):
    if self.debug: # Remove ansi codes
      clean = re.compile(r'\033\[[0-9;]*m') # Remove all ANSI
      with open("log_dump.txt", "w") as f:  # Export all logs
        f.writelines(clean.sub("", f"{line}\n") for line in self.log_buffer)
    else:
      print(f"{self.color['R']}log_dump(){self.color['G']} method requires {self.color['M']}debug = True{self.color['D']}")

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
    self.ROWS, self.COLS = 0, 1 # Start terminal xy

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
      0xB: lambda o1, _, __, nb: self.__setattr__('PC', nb) if self.register[0] == self.register[o1] else None,
      0xC: lambda _, __, ___, ____: self.__setattr__('halted', True),
    }

    self.log_dispatcher = {
      0x1: lambda o1, _, __, nb, code: f"{self.PC-2:02X} : {code} : Loaded register {o1:X} with bit pattern of memory {nb:02X}",
      0x2: lambda o1, _, __, nb, code: f"{self.PC-2:02X} : {code} : Loaded register {o1:X} with bit pattern {nb:02X}",
      0x3: lambda o1, _, __, nb, code: f"{self.PC-2:02X} : {code} : Loaded memory {nb:02X} with bit pattern of register {o1:X}",
      0x4: lambda _, o2, o3, __, code: f"{self.PC-2:02X} : {code} : Copied the bit pattern of register {o2:X} to register {o3:X}",
      0x5: lambda o1, o2, o3, _, code: f"{self.PC-2:02X} : {code} : Sum-ed registers {o2:X} and {o3:X}, added the result to {o1:X}",
      0x7: lambda o1, o2, o3, _, code: f"{self.PC-2:02X} : {code} : OR--ed registers {o2:X} and {o3:X}, added the result to {o1:X}",
      0x8: lambda o1, o2, o3, _, code: f"{self.PC-2:02X} : {code} : AND-ed registers {o2:X} and {o3:X}, added the result to {o1:X}",
      0x9: lambda o1, o2, o3, _, code: f"{self.PC-2:02X} : {code} : XOR-ed registers {o2:X} and {o3:X}, added the result to {o1:X}",
      0xA: lambda o1, _, o3, __, code: f"{self.PC-2:02X} : {code} : ROR bits of register {o1:X} , {o3} times to the right",
      0xB: lambda _, __, ___, nb, code: f"{self.PC-2:02X} : {code} : Attemped to jump to memory address {nb:02X}",
      0xC: lambda _, __, ___, ____, code: f"{self.PC-2:02X} : {code} : Code halted without errors",
    }

  # --- Printing Logic ---
  def log(self, *args):
    msg = " ".join(args)
    self.log_buffer.append(msg)

    if self.ROWS == 0:
      print(msg)
    else:
      for i, line in enumerate(self.log_buffer[-self.ROWS:]):
        print(f"\033[{i+1};{self.COLS}H{line}\033[K",end="")

      print("", end="", flush=True)

  # --- The main execution loop ---
  def run(self):
    _default_op = lambda *_: (self.log(f"{self.PC-2:02X} : Unknown opcode"), self.__setattr__('halted', True))
    _default_lo = lambda *_: f"{self.PC-2:02X} : No logs where found for this opcode!"

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
      line.split(";")[0].strip()
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
    if self.debug:
      with open("log_dump.txt", "w") as f:
        f.writelines(f"{line}\n" for line in self.log_buffer)
    else:
      print("log_dump() method requires debug = True!")

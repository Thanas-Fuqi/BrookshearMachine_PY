from Machine_language_CORE import Machine
cpu = Machine() # Import and init a machine

# Diagnostic program to run
check = "2203200A21055012700180129012A002403130101001B0B8C000" # PC = "A0"

cpu.PC = int("A0", 16) # Update Program Counter
cpu.load(check) # Load the hexadecimal string
cpu.run() # Run the emulation with given state

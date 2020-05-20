"""CPU functionality."""

import sys
# print('SYSTEM_ARGS:',sys.argv)

LDI= 0b10000010
PRN= 0b01000111
HLT= 0b00000001
MUL= 0b10100010
PUSH = 0b01000101
POP = 0b01000110
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.halted = False
        self.SP = 7

        self.branchtable = {
        LDI : self.handle_ldi,
        PRN : self.handle_prn,
        MUL : self.handle_mul,
        HLT : self.handle_hlt,
        ADD : self.handle_add,
        PUSH: self.handle_push,
        POP: self.handle_pop
        }

    def handle_ldi(self, reg, value):
        self.reg[reg] = value
    
    def handle_prn(self, reg, *args):
        print(self.reg[reg])
    
    def handle_mul(self,opr_a,opr_b):
        # self.reg[opr_a] *= self.reg[opr_b]
        self.alu("MUL",opr_a,opr_b)  
   
    def handle_hlt(self, *args):
        self.halted = True

    def handle_add(self,opr_a,opr_b):
       self.alu("ADD",opr_a,opr_b)  
         
    def handle_push(self,opr_a,opr_b):
        self.SP -= 1
        MDR = self.reg[opr_a]
        self.ram_write(self.SP,MDR)
        
    def handle_pop(self, opr_a, opr_b):
        self.reg[opr_a] = self.ram_read(self.SP)
        self.SP += 1


    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                # print(v)
                self.ram[address] = v
                address += 1
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self,MAR, MDR):
        self.ram[MAR] = MDR    

    def alu(self, op, opr_a, opr_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[opr_a] += self.reg[opr_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[opr_a] *= self.reg[opr_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.pc = 0
        # halted = False

        while not self.halted:

            IR = self.ram_read(self.pc)
            opr_a = self.ram_read(self.pc + 1)
            opr_b = self.ram_read(self.pc + 2)
            # 0000 0000
            op_counter = IR >> 6

            if IR in self.branchtable:
                self.branchtable[IR](opr_a,opr_b)    
                self.pc += op_counter + 1

        # halted = False

        # while not halted:
        #     instruction = self.ram_read(self.pc)
        #     opr_a = self.ram_read(self.pc + 1)
        #     opr_b = self.ram_read(self.pc + 2)

        #     if instruction == LDI:
        #         self.reg[opr_a] = opr_b
        #         self.pc += 3

        #     elif instruction == PRN:
        #         print(self.reg[opr_a])
        #         self.pc += 2

        #     elif instruction == HLT:
        #         self.pc += 1
        #         halted = True

        #     elif instruction == MUL:
        #         self.reg[opr_a] = self.reg[opr_a]*self.reg[opr_b]
        #         self.pc += 3
        #         # self.alu("MUL", self.reg[opr_a], self.reg[opr_b])

        #     else:
        #         print(f'unknown instruction {instruction} at address {pc}')
        #         sys.exit(1)         

            # self.pc += (instruction >> 6) + 1; 
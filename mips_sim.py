# Original Authors: Trung Le, Weijing Rao
# Editors: Karim, Erick

# This Python program simulates a restricted subset of MIPS instructions
# and output 
# Settings: Multi-Cycle CPU, i.e lw takes 5 cycles, beq takes 3 cycles, others are 4 cycles

mem_space = 4096 # Memory addr starts from 2000 , ends at 3000.  Hence total space of 4096
# That's true, however to simplify the memory allocation and not to worry about address
# conversion I have decided to use mem_space = end address - begin address

# this is probably wrong:
# MIPS is byte-addressable, so from 0x2000 to 0x3000 is a total of 0x1000 BYTES, which means
# 0x1000 / 4 = 0x0400 words
# we're always lw / sw here, so memory array is assumed to have 1 word per element, hence a total of 0x400 = 1024 elements.
# InstructionBin : array in binary representation
# InstructionHex : array in hex representation
# debugMode = True or False (user chooses debug mode or execution)

def simulate(InstructionBin,InstructionHex):
    print("***Starting simulation***")
    print("Instruction by instruction information:")
    Register = [0,0,0,0,0,0,0,0]    # initialize all values in registers to 0
    Memory = [0 for i in range(mem_space)] 
    PC = 0
    DIC = 0
    Cycle = 1
    threeCycles = 0 # frequency of how many instruction takes 3 cycles
    fourCycles = 0  #                                         4 cycles
    fiveCycles = 0  #                                         5 cycles

    finished = False
    while(not(finished)):
    
        DIC += 1
        fetch = InstructionBin[PC]
        if (fetch[0:32] == '00010000000000001111111111111111'):
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " : Deadloop. Ending program\n")
            finished = True

        elif (fetch[0:6] == '000000' and fetch[26:32] == '100000'): # ADD
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "add $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] + Register[int(fetch[11:16],2)]
        elif (fetch[0:6] == '000000' and fetch[26:32] == '100010'): # SUB
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "sub $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] - Register[int(fetch[11:16],2)]
        elif (fetch[0:6] == '000000' and fetch[26:32] == '100110'): # XOR
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "xor $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] ^ Register[int(fetch[11:16],2)]
        elif(fetch[0:6] == '001000'):                               # ADDI
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -1*(65535 -int(fetch[16:32],2)+1)
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "addi $" + str(int(fetch[11:16],2)) + ",$" +str(int(fetch[6:11],2)) + "," + str(imm) )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Register[int(fetch[11:16],2)] = Register[int(fetch[6:11],2)] + imm
        elif(fetch[0:6] == '000100'):                               # BEQ
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -1*(65535 -int(fetch[16:32],2)+1)
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "beq $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
            print("Taking 3 cycles \n")
            Cycle += 3
            PC += 1
            threeCycles += 1
            PC = PC + imm if (Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]) else PC
        elif(fetch[0:6] == '000101'):                               # BNE
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -1*(65535 -int(fetch[16:32],2)+1)
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "bne $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
            print("Taking 3 cycles \n")
            Cycle += 3
            PC += 1
            threeCycles += 1
            PC = PC + imm if (Register[int(fetch[6:11],2)] != Register[int(fetch[11:16],2)]) else PC

        elif(fetch[0:6] == '000000' and fetch[26:32] == '101010'): # SLT
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "slt $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
            print("Taking 4 cycles \n")
            Cycle += 4
            PC += 1
            fourCycles += 1
            Register[int(fetch[16:21],2)] = 1 if Register[int(fetch[6:11],2)] < Register[int(fetch[11:16],2)] else 0

        elif(fetch[0:6] == '101011'):                               # SW
            #Sanity check for word-addressing 
            if ( int(fetch[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(fetch,2)))
                exit()
            imm = int(fetch[16:32],2)
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "sw $" + str(int(fetch[11:16],2)) + "," + hex(imm) + "($" + str(int(fetch[6:11],2)) + ")" )
            print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Memory[imm + Register[int(fetch[6:11],2)] - 8192]= Register[int(fetch[11:16],2)] # Store word into memory

        elif(fetch[0:6] == '100011'):                               # LW
            #Sanity check for word-addressing 
            if ( int(fetch[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(fetch,2)))
                exit()
            imm = int(fetch[16:32],2)
            print("Cycles " + str(Cycle) + ":")
            print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "lw $" + str(int(fetch[11:16],2)) + "," + hex(imm) + "($" + str(int(fetch[6:11],2)) + ")" )
            print("Taking 5 cycles \n")
            PC += 1
            Cycle += 5
            fiveCycles += 1
            Register[int(fetch[11:16],2)] = Memory[imm + Register[int(fetch[6:11],2)] - 8192] # Load memory into register
 
    print("***Finished simulation***")
    print("Total # of cycles in Multi-Cycle: " + str(Cycle))
    print("Total # of cycles in Single Cycle: " + str(DIC))
    print("Dynamic instructions count: " +str(DIC) + ". Break down:")
    print("                    " + str(threeCycles) + " instructions take 3 cycles" )
    print("                    " + str(fourCycles) + " instructions take 4 cycles" )
    print("                    " + str(fiveCycles) + " instructions take 5 cycles" )
    print("Registers: ") #+ str(Register))
    print("$0 = " + str(Register[0]))
    print("$1 = " + str(Register[1]))
    print("$2 = " + str(Register[2]))
    print("$3 = " + str(Register[3]))
    print("$4 = " + str(Register[4]))
    print("$5 = " + str(Register[5]))
    print("$6 = " + str(Register[6]))
    print("$7 = " + str(Register[7]))
    print("PC = " + str(PC*4))

def main():
    print("Welcome to ECE366 sample MIPS_sim, choose the mode of running i_mem.txt: ")
     #debugMode =True if  int(input("1 = debug mode         2 = normal execution\n"))== 1 else False
    
    #if (int(input("Choose by inputting one of the following numbers:\n1 = Program A version 1\n2 = Program A version 2\n3 = Program B version 1\n4 = Program B version 2\n"))== 1):
     #   I_file = open("progA_v1.txt","r")
    #elif (int(input("Choose by inputting one of the following numbers:\n1 = Program A version 1\n2 = Program A version 2\n3 = Program B version 1\n4 = Program B version 2\n"))== 2):
    #    I_file = open("progA_v2.txt","r")
    #elif (int(input("Choose by inputting one of the following numbers:\n1 = Program A version 1\n2 = Program A version 2\n3 = Program B version 1\n4 = Program B version 2\n"))== 3):
     #   I_file = open("progB_v1.txt","r")
    #else:
      #  I_file = open("progB_v2.txt","r")

    inputActive = False
    userInput = int(input('Choose by inputting one of the following numbers:\n1 = Program A version 1\n2 = Program A version 2\n3 = Program B version 1\n4 = Program B version 2\n'))

    while (not(inputActive)):
        if userInput == 1:
            I_file = open("progA_v1.txt","r") 
            inputActive = True
        elif userInput == 2:
            I_file = open("progA_v2.txt","r")
            inputActive = True
        elif userInput == 3:
            I_file = open("progB_v1.txt","r")
            inputActive = True
        elif userInput == 4:
            I_file = open("progB_v2.txt","r")
            inputActive = True
        else:
            print("Please enter the correct number. Try again.")
            userInput = input('Choose by inputting one of the following numbers:\n1 = Program A version 1\n2 = Program A version 2\n3 = Program B version 1\n4 = Program B version 2\n')
    
    InstructionBin = []            # array containing all instructions to execute         
    InstructionHex = []
    for line in I_file:
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace('0x', '')
        line = line.replace('\n','')
        InstructionHex.append(line) # store hexadecimal values into InstructionHex array
        line = format(int(line,16),"032b") # int() first reads line as hexa then converts to decimal, then format() converts
                                           # decimal to binary
        InstructionBin.append(line) # store binary values into Instruction array
        
    
    simulate(InstructionBin,InstructionHex)



if __name__ == "__main__":
    main()

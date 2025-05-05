import random

# Convert an integer to a fixed-length binary string
def to_bin(value, bits):
    return bin(value)[2:].zfill(bits)

# Define opcode and funct3 categories
opcodes = [
    "0110111", "0010111", "1101111", "1100111", "1100011",
    "0000011", "0100011", "0010011", "0110011", "0001111", "1110011"
]

funct3_branch = ["000", "001", "011", "100", "101", "110", "111"]
funct3_load   = ["000", "001", "010", "100", "101"]
funct3_store  = ["000", "001", "010"]
funct3_itype  = ["000", "010", "011", "100", "110", "111"]
funct3_rtype  = ["000", "001", "010", "011", "100", "101", "110", "111"]

# Open file to write binary instruction strings
with open("testgen.bin", "w") as out_file:
    for _ in range(20):
        opcode = random.choice(opcodes)

        # Generate random binary fields
        imm_u = to_bin(random.randint(0, 2**20 - 1), 20)
        imm_i = to_bin(random.randint(0, 2**12 - 1), 12)
        imm_b = to_bin(random.randint(0, 2**12 - 1), 12)
        imm_s = to_bin(random.randint(0, 2**12 - 1), 12)
        shamt = to_bin(random.randint(0, 31), 5)

        rd  = to_bin(random.randint(0, 31), 5)
        rs1 = to_bin(random.randint(0, 31), 5)
        rs2 = to_bin(random.randint(0, 31), 5)

        instruction = ""

        # Construct instruction based on opcode
        if opcode == "0110111":  # LUI
            instruction = imm_u + rd + opcode

        elif opcode == "0010111":  # AUIPC
            instruction = imm_u + rd + opcode

        elif opcode == "1101111":  # JAL
            instruction = imm_u + rd + opcode

        elif opcode == "1100111":  # JALR
            instruction = imm_i + rs1 + "000" + rd + opcode

        elif opcode == "1100011":  # Branch
            funct3 = random.choice(funct3_branch)
            instruction = imm_b[-7:] + rs2 + rs1 + funct3 + imm_b[:5] + opcode

        elif opcode == "0000011":  # Load
            funct3 = random.choice(funct3_load)
            instruction = imm_i + rs1 + funct3 + rd + opcode

        elif opcode == "0100011":  # Store
            funct3 = random.choice(funct3_store)
            instruction = imm_s[:7] + rs2 + rs1 + funct3 + imm_s[7:] + opcode

        elif opcode == "0010011":  # I-Type ALU
            funct3 = random.choice(funct3_itype)
            if funct3 == "001":  # SLLI
                instruction = "0000000" + shamt + rs1 + "001" + rd + opcode
            elif funct3 == "101":  # SRLI/SRAI
                funct7 = "0100000" if random.randint(0, 1) else "0000000"
                instruction = funct7 + shamt + rs1 + "101" + rd + opcode
            else:
                instruction = imm_i + rs1 + funct3 + rd + opcode

        elif opcode == "0110011":  # R-Type
            funct3 = random.choice(funct3_rtype)
            if funct3 == "000":  # ADD/SUB
                funct7 = "0100000" if random.randint(0, 1) else "0000000"
                instruction = funct7 + rs2 + rs1 + funct3 + rd + opcode
            elif funct3 == "101":  # SRL/SRA
                funct7 = "0100000" if random.randint(0, 1) else "0000000"
                instruction = funct7 + rs2 + rs1 + funct3 + rd + opcode
            else:
                instruction = "0000000" + rs2 + rs1 + funct3 + rd + opcode

        elif opcode == "0001111":  # FENCE
            instruction = imm_i + rs1 + "000" + rd + opcode

        elif opcode == "1110011":  # ECALL/EBREAK
            instruction = (
                "00000000000000000000000001110011" if random.randint(0, 1) == 0
                else "00000000000100000000000001110011"
            )

        # Ensure valid 32-bit instruction and write to file
        if len(instruction) == 32:
            out_file.write(instruction + "\n")

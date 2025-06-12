from components.register_file import RegisterFile


class WriteBackStage:
    def __init__(self, register_file: RegisterFile):
        self.reg_file = register_file

    def write_back(self, mem_wb: dict):
        """
        Realiza la escritura en el banco de registros si aplica.

        Entrada:
        - mem_wb: dict con resultados de MEM

        Efecto:
        - Escribe en el registro rd si corresponde.
        """
        instr = mem_wb["instr"]
        opcode = instr.opcode
        rd = mem_wb.get("rd")

        if rd is None or rd == "x0":
            return  # No escribir en x0 

        if opcode == "lw":
            value = mem_wb.get("mem_data")
        elif opcode in {"add", "sub", "and", "or", "slt", "addi", "jal"}:
            value = mem_wb.get("alu_result")
        else:
            return  # No escritura (sw, beq, bne, nop)

        self.reg_file.write(rd, value)

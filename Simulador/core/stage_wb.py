from components.register_file import RegisterFile

class WriteBackStage:
    def __init__(self, register_file: RegisterFile):
        self.reg_file = register_file

    def write_back(self, mem_wb: dict):
        instr = mem_wb["instr"]
        rd = mem_wb.get("rd")
        control = mem_wb.get("control_signals", {})

        if not control.get("RegWrite", False):
            return  # No se debe escribir en registros

        if rd is None or rd == "x0":
            return  # Nunca escribir en x0

        # Selección de fuente según MemToReg
        if control.get("MemToReg", False):
            value = mem_wb.get("mem_data")
        else:
            value = mem_wb.get("alu_result")

        self.reg_file.write(rd, value)

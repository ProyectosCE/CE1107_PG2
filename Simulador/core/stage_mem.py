from components.memory import Memory


class MemoryAccessStage:
    def __init__(self, data_memory: Memory):
        self.data_mem = data_memory

    def access(self, ex_mem: dict) -> dict:
        """
        Ejecuta la etapa MEM del pipeline.

        Entrada:
        - ex_mem: dict con resultados de EX

        Salida:
        - mem_wb: dict con:
            - 'instr', 'rd', 'mem_data', 'alu_result', 'pc'
        """
        instr = ex_mem["instr"]
        opcode = instr.opcode
        rd = ex_mem.get("rd")
        pc = ex_mem["pc"]

        alu_result = ex_mem.get("alu_result", 0)
        rs2_val = ex_mem.get("rs2_val", 0)
        mem_data = None

        if opcode == "lw":
            mem_data = self.data_mem.load_word(alu_result)
        elif opcode == "sw":
            self.data_mem.store_word(alu_result, rs2_val)

        return {
            "instr": instr,
            "rd": rd,
            "alu_result": alu_result,
            "mem_data": mem_data,
            "pc": pc
        }

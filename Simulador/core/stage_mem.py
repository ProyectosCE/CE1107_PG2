from components.memory import Memory
import time
from config import LATENCY_MEM

class MemoryAccessStage:
    def __init__(self, data_memory: Memory, latency: float = None):
        self.data_mem = data_memory
        self.latency = latency if latency is not None else LATENCY_MEM

    def access(self, ex_mem: dict) -> dict:
        instr = ex_mem["instr"]
        rd = ex_mem.get("rd")
        pc = ex_mem["pc"]
        alu_result = ex_mem.get("alu_result", 0)
        rs2_val = ex_mem.get("rs2_val", 0)
        control = ex_mem.get("control_signals", {})

        mem_data = None

        # Solo accede si la señal lo indica
        if control.get("MemRead", False):
            mem_data = self.data_mem.load_word(alu_result)

        if control.get("MemWrite", False):
            self.data_mem.store_word(alu_result, rs2_val)

        time.sleep(self.latency)
        return {
            "instr": instr,
            "rd": rd,
            "alu_result": alu_result,
            "mem_data": mem_data,
            "pc": pc,
            "control_signals": control  #Propagar señales a WB
        }

"""
================================== LICENCIA ==============================
MIT License
Copyright (c) 2025 José Bernardo Barquero Bonilla,
Jose Eduardo Campos Salazar,
Jimmy Feng Feng,
Alexander Montero Vargas
Consulta el archivo LICENSE para más detalles.
==========================================================================
"""

from components.memory import Memory

"""
Class: MemoryAccessStage
Clase que representa la etapa de acceso a memoria (MEM) del pipeline, encargada de realizar operaciones de carga y almacenamiento.

Attributes:
- data_mem: Memory - referencia a la memoria de datos.

Constructor:
- __init__: Inicializa la etapa MEM con la memoria de datos.

Methods:
- access: Ejecuta la operación de memoria correspondiente a la instrucción (lw, sw, etc).

Example:
    mem_stage = MemoryAccessStage(data_mem)
    mem_wb = mem_stage.access(ex_mem_dict)
"""

class MemoryAccessStage:
    def __init__(self, data_memory: Memory):
        """
        Function: __init__
        Inicializa la etapa MEM con la memoria de datos.
        Params:
        - data_memory: Memory - memoria de datos.
        Example:
            mem_stage = MemoryAccessStage(data_mem)
        """
        self.data_mem = data_memory

    def access(self, ex_mem: dict) -> dict:
        """
        Function: access
        Ejecuta la etapa MEM del pipeline, realizando operaciones de carga o almacenamiento si corresponde.
        Params:
        - ex_mem: dict - diccionario con resultados de la etapa EX.
        Returns:
        - dict: diccionario con los resultados para la etapa WB (mem_wb).
        Example:
            mem_wb = mem_stage.access(ex_mem)
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

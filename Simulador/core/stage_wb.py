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

from components.register_file import RegisterFile

"""
Class: WriteBackStage
Clase que representa la etapa de escritura final (WB) del pipeline, encargada de escribir resultados en el banco de registros.

Attributes:
- reg_file: RegisterFile - referencia al banco de registros.

Constructor:
- __init__: Inicializa la etapa WB con el banco de registros.

Methods:
- write_back: Realiza la escritura en el registro destino si corresponde.

Example:
    wb_stage = WriteBackStage(reg_file)
    wb_stage.write_back(mem_wb_dict)
"""

class WriteBackStage:
    def __init__(self, register_file: RegisterFile):
        """
        Function: __init__
        Inicializa la etapa WB con una referencia al banco de registros.
        Params:
        - register_file: RegisterFile - banco de registros.
        Example:
            wb_stage = WriteBackStage(reg_file)
        """
        self.reg_file = register_file

    def write_back(self, mem_wb: dict):
        """
        Function: write_back
        Realiza la escritura en el banco de registros si la instrucción lo requiere.
        Params:
        - mem_wb: dict - diccionario con resultados de la etapa MEM.
        Restriction:
        No escribe en x0 ni en instrucciones que no modifican registros.
        Example:
            wb_stage.write_back(mem_wb)
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

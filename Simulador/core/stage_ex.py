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

"""
Class: ExecuteStage
Clase que representa la etapa de ejecución (EX) del pipeline, encargada de realizar operaciones aritméticas, lógicas y de control de flujo.

Attributes:
(No tiene atributos propios, es una clase de utilidad por método.)

Constructor:
- __init__: Inicializa la instancia de la etapa de ejecución.

Methods:
- execute: Ejecuta la instrucción recibida desde la etapa ID, calculando resultados de la ALU y señales de control de salto.

Example:
    ex = ExecuteStage()
    resultado = ex.execute(id_ex_dict)
"""

class ExecuteStage:
    def __init__(self):
        """
        Function: __init__
        Inicializa la instancia de la etapa de ejecución.
        """
        pass

    def execute(self, id_ex: dict) -> dict:
        """
        Function: execute
        Ejecuta la instrucción usando la ALU y calcula los resultados y señales de control.
        Params:
        - id_ex: dict - diccionario generado por la etapa ID, contiene la instrucción y operandos.
        Returns:
        - dict: diccionario con los resultados de la etapa EX (alu_result, branch_taken, etc).
        Example:
            ex_mem = ex.execute(id_ex)
        """
        instr = id_ex["instr"]
        opcode = instr.opcode

        alu_result = 0
        branch_taken = False
        target_address = None

        rs1_val = id_ex.get("rs1_val", 0)
        rs2_val = id_ex.get("rs2_val", 0)
        imm = id_ex.get("imm", 0)
        pc = id_ex["pc"]

        # Operaciones aritméticas y de control de flujo
        if opcode == "add":
            alu_result = rs1_val + rs2_val
        elif opcode == "sub":
            alu_result = rs1_val - rs2_val
        elif opcode == "and":
            alu_result = rs1_val & rs2_val
        elif opcode == "or":
            alu_result = rs1_val | rs2_val
        elif opcode == "slt":
            alu_result = int(rs1_val < rs2_val)
        elif opcode == "addi":
            alu_result = rs1_val + imm
        elif opcode == "lw" or opcode == "sw":
            alu_result = rs1_val + imm  # Dirección efectiva
        elif opcode == "beq":
            branch_taken = rs1_val == rs2_val
            target_address = pc + imm
        elif opcode == "bne":
            branch_taken = rs1_val != rs2_val
            target_address = pc + imm
        elif opcode == "jal":
            alu_result = pc + 4  # return address
            target_address = pc + imm
            branch_taken = True
        elif opcode == "nop":
            pass  # No operación
        else:
            raise ValueError(f"Operación no soportada: {opcode}")

        return {
            "instr": instr,
            "alu_result": alu_result,
            "rs2_val": rs2_val,
            "rd": id_ex.get("rd"),
            "pc": pc,
            "branch_taken": branch_taken,
            "target_address": target_address
        }

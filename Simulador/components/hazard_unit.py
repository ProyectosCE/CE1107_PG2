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
Class: HazardUnit
Clase que implementa la unidad de detección y resolución de hazards en el pipeline, gestionando stalls.

Attributes:
(No tiene atributos propios, es una clase de utilidad por método.)

Constructor:
- __init__: Inicializa la instancia de la unidad de hazards.

Methods:
- detect_hazard: Detecta hazards de tipo load-use y determina si es necesario hacer stall.

Example:
    hazard = HazardUnit()
    resultado = hazard.detect_hazard(if_id, id_ex, ex_mem, mem_wb)
"""

class HazardUnit:
    def __init__(self):
        """
        Function: __init__
        Inicializa la instancia de la unidad de hazards.
        """
        pass

    def detect_hazard(self, if_id: dict, id_ex: dict, ex_mem: dict, mem_wb: dict) -> dict:
        """
        Function: detect_hazard
        Detecta hazards de tipo load-use y determina si es necesario hacer stall o forwarding.
        Params:
        - if_id: dict - registro IF/ID del pipeline.
        - id_ex: dict - registro ID/EX del pipeline.
        - ex_mem: dict - registro EX/MEM del pipeline.
        - mem_wb: dict - registro MEM/WB del pipeline.
        Returns:
        - dict: contiene 'stall' (bool) y 'forward' (dict con claves 'rs1' y 'rs2').
        Example:
            resultado = hazard.detect_hazard(if_id, id_ex, ex_mem, mem_wb)
        """
        stall = False
        forward = {'rs1': None, 'rs2': None}

        instr_id = if_id.get("instr")
        instr_ex = id_ex.get("instr")
        instr_mem = ex_mem.get("instr")
        instr_wb = mem_wb.get("instr")

        if not instr_id or not instr_ex:
            return {"stall": False, "forward": forward}

        rs1 = instr_id.rs1
        rs2 = instr_id.rs2

        # ---------- 1. Load-Use Hazard (requiere stall) ----------
        if instr_ex.opcode == "lw" and instr_ex.rd and instr_ex.rd != "x0":
            if instr_ex.rd == rs1 or instr_ex.rd == rs2:
                stall = True

        # ---------- 2. Forwarding desde EX/MEM ----------
        if instr_mem and instr_mem.rd and instr_mem.rd != "x0":
            if instr_mem.rd == rs1:
                forward['rs1'] = 'EX'
            if instr_mem.rd == rs2:
                forward['rs2'] = 'EX'

        # ---------- 3. Forwarding desde MEM/WB ----------
        if instr_wb and instr_wb.rd and instr_wb.rd != "x0":
            if forward['rs1'] is None and instr_wb.rd == rs1:
                forward['rs1'] = 'MEM'
            if forward['rs2'] is None and instr_wb.rd == rs2:
                forward['rs2'] = 'MEM'

        return {
            "stall": stall,
            "forward": forward
        }

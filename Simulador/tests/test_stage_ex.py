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
Este módulo realiza pruebas unitarias para la etapa de ejecución (EX) del pipeline, validando operaciones aritméticas,
saltos condicionales y saltos incondicionales.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.stage_ex import ExecuteStage
from core.instruction import Instruction

def test_execute_add():
    """
    Function: test_execute_add
    Prueba la ejecución de una instrucción tipo R (add) en la etapa EX.
    Example:
        test_execute_add()
    """
    ex = ExecuteStage()

    instr = Instruction("add x1, x2, x3", 0)
    id_ex = {
        "instr": instr,
        "rs1_val": 10,
        "rs2_val": 20,
        "pc": 0,
        "rd": "x1"
    }

    result = ex.execute(id_ex)
    assert result["alu_result"] == 30
    assert result["rd"] == "x1"
    assert result["branch_taken"] is False
    print("Test add pasó correctamente.")

def test_execute_beq_taken():
    """
    Function: test_execute_beq_taken
    Prueba la ejecución de una instrucción de salto condicional (beq) cuando la condición se cumple.
    Example:
        test_execute_beq_taken()
    """
    ex = ExecuteStage()

    instr = Instruction("beq x1, x2, 8", 4)
    id_ex = {
        "instr": instr,
        "rs1_val": 5,
        "rs2_val": 5,
        "pc": 4,
        "imm": instr.imm,
    }
    result = ex.execute(id_ex)
    assert result["branch_taken"] is True
    assert result["target_address"] == 12
    print("Test beq tomado pasó correctamente.")

def test_execute_jal():
    """
    Function: test_execute_jal
    Prueba la ejecución de una instrucción de salto incondicional (jal).
    Example:
        test_execute_jal()
    """
    ex = ExecuteStage()

    instr = Instruction("jal x5, 12", 8)

    id_ex = {
        "instr": instr,
        "pc": 8,
        "rd": "x5",
        "imm": instr.imm,
    }

    result = ex.execute(id_ex)
    assert result["alu_result"] == 12  # return address = pc + 4
    assert result["target_address"] == 20  # pc + imm
    assert result["branch_taken"] is True
    print("Test jal pasó correctamente.")

if __name__ == "__main__":
    test_execute_add()
    test_execute_beq_taken()
    test_execute_jal()

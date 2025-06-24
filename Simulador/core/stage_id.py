from core.instruction import Instruction
from components.register_file import RegisterFile
from components.branch_predictor import BranchPredictor
from components.control_unit import ControlUnit  
import time
from config import LATENCY_ID

class InstructionDecode:
    def __init__(self, register_file: RegisterFile, branch_predictor: BranchPredictor, control_unit: ControlUnit, latency: float = None):
        """
        Inicializa la etapa ID con acceso al banco de registros, predictor de saltos y unidad de control.
        """
        self.reg_file = register_file
        self.branch_predictor = branch_predictor
        self.control_unit = control_unit 
        self.latency = latency if latency is not None else LATENCY_ID

    def decode(self, if_id: dict) -> dict:
        instr: Instruction = if_id["instr"]
        pc = if_id["pc"]

        if instr.opcode == "nop":
            return {"instr": instr, "pc": pc}

        # Leer operandos del banco de registros
        rs1_val = self.reg_file.read(instr.rs1) if instr.rs1 else 0
        rs2_val = self.reg_file.read(instr.rs2) if instr.rs2 else 0

        # Generar señales de control según el tipo de instrucción
        control_signals = self.control_unit.generate_signals(instr.opcode)

        # Armar paquete para la etapa EX
        id_ex = {
            "instr": instr,
            "pc": pc,
            "rs1_val": rs1_val,
            "rs2_val": rs2_val,
            "imm": instr.imm,
            "rd": instr.rd,
            "rs1": instr.rs1,
            "rs2": instr.rs2,
            "control_signals": control_signals 
        }

        # Predicción de saltos si aplica
        if instr.opcode in {"beq", "bne", "jal"}:
            prediction = self.branch_predictor.predict(pc)
            id_ex["predicted_taken"] = prediction["taken"]

            if prediction["taken"]:
                id_ex["predicted_target"] = pc + instr.imm
            else:
                id_ex["predicted_target"] = pc + 4

        time.sleep(self.latency)
        return id_ex

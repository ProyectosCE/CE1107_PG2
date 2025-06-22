from .base_view import BaseSimView
from .HardwareBlock import *

class SimView1(BaseSimView):

    def _draw_content(self):

        # Bloques (igual que antes)
        self.mux_pc = HardwareBlock(self.canvas, 10, 10, 40, 40,
                                    "MUX PC", fill="lightgray", tags="mux_pc")
        self.reg_pc = HardwareBlock(self.canvas, 100, 10, 40, 100,
                                    "Reg PC", fill="lightgray", tags="reg_pc")
        self.instruction_mem = HardwareBlock(self.canvas, 200, 5, 100, 150,
                                     "Instr Mem", fill="lightgray", tags="instruction_mem")
        self.adder = HardwareBlock(self.canvas, 200, 200, 50, 80,
                                   "Adder", fill="lightgray", tags="adder")
        self.reg1 = HardwareBlock(self.canvas, 350, 5, 30, 550,
                                  "Reg1", fill="lightgray", tags="reg1")
        self.register_file = HardwareBlock(self.canvas, 500, 5, 200, 280,
                                     "Reg File", fill="lightgray", tags="register_file")
        self.extend = HardwareBlock(self.canvas, 500, 400, 200, 100,
                                    "Extend", fill="lightgray", tags="extend")
        self.reg2 = HardwareBlock(self.canvas, 800, 5, 30, 550,
                                  "Reg2", fill="lightgray", tags="reg2")
        self.mux_srcB = HardwareBlock(self.canvas, 950, 100, 40, 40,
                                    "MUX \nSrcB", fill="lightgray", tags="mux_srcB")
        self.adderPC = HardwareBlock(self.canvas, 975, 200, 60, 80,
                                   "Adder PC", fill="lightgray", tags="adderPC")
        self.alu = HardwareBlock(self.canvas, 1050, 50, 50, 100,
                                   "ALU", fill="lightgray", tags="alu")
        self.reg3 = HardwareBlock(self.canvas, 1125, 5, 30, 550,
                                  "Reg3", fill="lightgray", tags="reg3")
        self.data_mem = HardwareBlock(self.canvas, 1250, 50, 100, 150,
                                     "Data Mem", fill="lightgray", tags="data_mem")

        self.reg4 = HardwareBlock(self.canvas, 1400, 5, 30, 550,
                                  "Reg4", fill="lightgray", tags="reg4")

        self.mux_result = HardwareBlock(self.canvas, 1450, 100, 40, 60,
                                    "MUX \nResult", fill="lightgray", tags="mux_result")

        self.mux_pc.draw()
        self.reg_pc.draw()
        self.instruction_mem.draw()
        self.adder.draw()
        self.reg1.draw()
        self.register_file.draw()
        self.extend.draw()
        self.reg2.draw()
        self.mux_srcB.draw()
        self.adderPC.draw()
        self.alu.draw()
        self.reg3.draw()
        self.data_mem.draw()
        self.reg4.draw()
        self.mux_result.draw()

        # ──────────────────────── CONEXIONES ──────────────────────


        # ──────────────────────── TAGS PARA HIGHLIGHT ─────────────
        self.units = {
            "mux_pc": self.mux_pc,
            "reg_pc": self.reg_pc,
            "instruction_mem": self.instruction_mem,
            "adder": self.adder,
            "reg1": self.reg1,
            "register_file": self.register_file,
            "extend": self.extend,
            "reg2": self.reg2,
            "mux_srcB": self.mux_srcB,
            "adderPC": self.adderPC,
            "alu": self.alu,
            "reg3": self.reg3,
            "data_mem": self.data_mem,
            "reg4": self.reg4,
            "mux_result": self.mux_result
        }

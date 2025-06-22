from .base_view import BaseSimView
from .HardwareBlock import *
from .Connection import *

class SimView1(BaseSimView):

    def _draw_content(self):
        # ──────── 1. INSTRUCTION FETCH ────────

        # ──────── 1. INSTRUCTION FETCH ────────

        self.mux_pc = HardwareBlock(self.canvas, 50, 130, 50, 50, "MUX PC",
                                    fill="#E0F7FA", border_color="#00838F", tags="mux_pc")  # x = 50

        self.reg_pc = HardwareBlock(self.canvas, 150, 110, 50, 90, "Reg PC",
                                    fill="#F1F8E9", border_color="#33691E", tags="reg_pc")  # 50 + 50 + 50 = 150

        self.instruction_mem = HardwareBlock(self.canvas, 250, 90, 120, 130, "Instr Mem",
                                             fill="#FFF3E0", border_color="#EF6C00",
                                             tags="instruction_mem")  # 150 + 50 + 50 = 250

        self.adder = HardwareBlock(self.canvas, 250, 260, 60, 80, "Adder",
                                   fill="#EDE7F6", border_color="#5E35B1", shape_type="trapezoid", tags="adder")

        # ──────── 2. DECODE / REGISTER FETCH ────────

        self.reg1 = HardwareBlock(self.canvas, 420, 90, 30, 280, "Reg1",
                                  fill="#F1F8E9", border_color="#33691E", tags="reg1")  # 250 + 120 + 50 = 420

        self.register_file = HardwareBlock(self.canvas, 500, 60, 220, 280, "Reg File",
                                           fill="#F1F8E9", border_color="#33691E",
                                           tags="register_file")  # 420 + 30 + 50 = 500

        self.extend = HardwareBlock(self.canvas, 500, 380, 220, 100, "Extend",
                                    fill="#ECEFF1", border_color="#37474F", tags="extend")

        self.reg2 = HardwareBlock(self.canvas, 770, 60, 30, 330, "Reg2",
                                  fill="#F1F8E9", border_color="#33691E", tags="reg2")  # 500 + 220 + 50 = 770

        # ──────── 3. EXECUTE ────────

        self.mux_srcB = HardwareBlock(self.canvas, 850, 150, 50, 50, "MUX\nSrcB",
                                      fill="#E0F7FA", border_color="#00838F", tags="mux_srcB")  # 770 + 30 + 50 = 850

        self.adderPC = HardwareBlock(self.canvas, 850, 270, 60, 80, "Adder PC",
                                     fill="#EDE7F6", border_color="#5E35B1", shape_type="trapezoid", tags="adderPC")

        self.alu = HardwareBlock(self.canvas, 950, 120, 100, 160, "ALU",
                                 fill="#EDE7F6", border_color="#5E35B1", shape_type="trapezoid",
                                 tags="alu")  # 850 + 50 + 50 = 950

        # ──────── 4. MEMORY ACCESS ────────

        self.reg3 = HardwareBlock(self.canvas, 1100, 60, 30, 330, "Reg3",
                                  fill="#F1F8E9", border_color="#33691E", tags="reg3")  # 950 + 100 + 50 = 1100

        self.data_mem = HardwareBlock(self.canvas, 1180, 120, 120, 160, "Data Mem",
                                      fill="#FFF3E0", border_color="#EF6C00", tags="data_mem")  # 1100 + 30 + 50 = 1180

        # ──────── 5. WRITE BACK ────────

        self.reg4 = HardwareBlock(self.canvas, 1350, 60, 30, 330, "Reg4",
                                  fill="#F1F8E9", border_color="#33691E", tags="reg4")  # 1180 + 120 + 50 = 1350

        self.mux_result = HardwareBlock(self.canvas, 1430, 170, 60, 60, "MUX\nResult",
                                        fill="#E0F7FA", border_color="#00838F",
                                        tags="mux_result")  # 1350 + 30 + 50 = 1430
        #ports:

        self.mux_pc.add_port("sel", 0, 10)
        self.mux_pc.add_port("pc+4", 0, 30)
        self.mux_pc.add_port("pc_out", self.mux_pc.width, self.mux_pc.height // 2)

        self.reg_pc.add_port("in", 0, self.reg_pc.height // 2)
        self.reg_pc.add_port("out", self.reg_pc.width, self.reg_pc.height // 2)

        self.instruction_mem.add_port("addr", 0, self.instruction_mem.height // 2)
        self.instruction_mem.add_port("instr", self.instruction_mem.width, self.instruction_mem.height // 3)

        self.adder.add_port("a", 0, 20)
        self.adder.add_port("b", 0, 60)
        self.adder.add_port("out", self.adder.width, self.adder.height // 2)

        self.reg1.add_port("in", 0, self.reg1.height // 2)
        self.reg1.add_port("out", self.reg1.width, self.reg1.height // 2)

        self.register_file.add_port("A1", 0, 60)  # dirección de rs1
        self.register_file.add_port("A2", 0, 100)  # dirección de rs2
        self.register_file.add_port("A3", 0, 140)  # dirección de rd
        self.register_file.add_port("WD3", 0, 180)  # datos a escribir

        # SALIDAS (lado derecho)
        self.register_file.add_port("RD1", self.register_file.width, 80)  # datos de rs1
        self.register_file.add_port("RD2", self.register_file.width, 140)  # datos de rs2

        self.extend.add_port("imm_in", 0, self.extend.height // 2)
        self.extend.add_port("imm_out", self.extend.width, self.extend.height // 2)

        self.reg2.add_port("in", 0, self.reg2.height // 2)
        self.reg2.add_port("out", self.reg2.width, self.reg2.height // 2)

        self.mux_srcB.add_port("sel", 0, 10)
        self.mux_srcB.add_port("B", 0, 40)
        self.mux_srcB.add_port("out", self.mux_srcB.width, self.mux_srcB.height // 2)

        self.adderPC.add_port("a", 0, 20)
        self.adderPC.add_port("b", 0, 60)
        self.adderPC.add_port("out", self.adderPC.width, self.adderPC.height // 2)

        self.alu.add_port("opA", 0, 40)
        self.alu.add_port("opB", 0, 120)
        self.alu.add_port("result", self.alu.width, self.alu.height // 2)
        self.reg3.add_port("in", 0, self.reg3.height // 2)
        self.reg3.add_port("out", self.reg3.width, self.reg3.height // 2)

        self.data_mem.add_port("addr", 0, 40)
        self.data_mem.add_port("wdata", 0, 120)
        self.data_mem.add_port("rdata", self.data_mem.width, self.data_mem.height // 2)

        self.reg4.add_port("in", 0, self.reg4.height // 2)
        self.reg4.add_port("out", self.reg4.width, self.reg4.height // 2)

        self.mux_result.add_port("sel", 0, 10)
        self.mux_result.add_port("mem", 0, 40)
        self.mux_result.add_port("alu", 0, 60)
        self.mux_result.add_port("out", self.mux_result.width, self.mux_result.height // 2)

        #conexion

        #conexiones de fetch
        Connection(self.canvas, self.mux_pc, self.reg_pc, source_port="pc_out", target_port="in", arrow=False).draw()
        Connection(self.canvas, self.mux_pc, self.reg_pc, source_port="pc_out", target_port="in", arrow=False).draw()
        Connection(self.canvas, self.reg_pc, self.instruction_mem, source_port="out", target_port="addr", arrow=False).draw()
        Connection(self.canvas, self.reg_pc, self.adder, source_port="out", target_port="a", arrow=False).draw()
        Connection(self.canvas, self.instruction_mem, self.reg1, source_port="instr", target_port="in", arrow=False).draw()
        Connection(self.canvas, self.adder, self.reg1, source_port="out", target_port="in", arrow=False).draw()

        # ──────── Conexiones de entrada a register_file (lado izquierdo) ────────

        # Dirección rs1 (A1)
        Connection(self.canvas, self.instruction_mem, self.register_file,
                   source_port="instr", target_port="A1",arrow=False).draw()

        # Dirección rs2 (A2)
        Connection(self.canvas, self.instruction_mem, self.register_file,
                   source_port="instr", target_port="A2",arrow=False).draw()

        # Dirección rd (A3)
        Connection(self.canvas, self.instruction_mem, self.register_file,
                   source_port="instr", target_port="A3",arrow=False).draw()

        # Datos a escribir (WD3)
        Connection(self.canvas, self.reg4, self.register_file,
                   source_port="out", target_port="WD3",arrow=False).draw()

        # ──────── Conexiones de salida desde register_file (lado derecho) ────────

        # Datos leídos de rs1 (RD1) → reg1
        Connection(self.canvas, self.register_file, self.reg1,
                   source_port="RD1", target_port="in",arrow=False).draw()

        # Datos leídos de rs2 (RD2) → reg2
        Connection(self.canvas, self.register_file, self.reg2,
                   source_port="RD2", target_port="in",arrow=False).draw()

        # ──────── Conexión del out de reg1 ────────

        # reg1 → ALU (opA)
        Connection(self.canvas, self.reg1, self.alu,
                   source_port="out", target_port="opA",arrow=False).draw()

        Connection(self.canvas, self.instruction_mem, self.extend,
                   source_port="instr", target_port="imm_in", arrow=False).draw()

        Connection(self.canvas, self.reg2, self.extend,
                   source_port="in", target_port="imm_out", arrow=False).draw()

        # reg2 -> adderPC.a
        Connection(self.canvas, self.reg2, self.adderPC, source_port="out", target_port="a", arrow=False).draw()

        # reg2 -> adderPC.b
        Connection(self.canvas, self.reg2, self.adderPC, source_port="out", target_port="b", arrow=False).draw()

        Connection(self.canvas, self.reg4, self.mux_result, arrow=False).draw()



        # ─────────────── DIBUJAR ───────────────
        for unit in [self.mux_pc, self.reg_pc, self.instruction_mem, self.adder,
                     self.reg1, self.register_file, self.extend, self.reg2,
                     self.mux_srcB, self.adderPC, self.alu, self.reg3,
                     self.data_mem, self.reg4, self.mux_result]:
            unit.draw()

        # ─────────────── REGISTRO PARA HIGHLIGHT ───────────────
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

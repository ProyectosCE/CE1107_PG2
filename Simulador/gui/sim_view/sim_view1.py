from .base_view import BaseSimView
from .HardwareBlock import *

class SimView1(BaseSimView):

    def _draw_content(self):

        # Bloques (igual que antes)
        self.mux_pc = HardwareBlock(self.canvas, 10, 10, 40, 40,
                                    "MUX PC", fill="lightgray")
        self.reg_pc = HardwareBlock(self.canvas, 100, 10, 40, 100,
                                    "Reg PC", fill="lightgray")
        self.instruction_mem = HardwareBlock(self.canvas, 200, 5, 100, 150,
                                     "Instr Mem", fill="lightblue")
        self.adder = HardwareBlock(self.canvas, 200, 200, 50, 80,
                                   "Adder", fill="lightgray")
        self.reg1 = HardwareBlock(self.canvas, 350, 5, 30, 550,
                                  "Reg1", fill="lightblue")
        self.register_file = HardwareBlock(self.canvas, 500, 5, 200, 280,
                                     "Reg File", fill="lightblue")
        self.extend = HardwareBlock(self.canvas, 500, 400, 200, 100,
                                    "Extend", fill="lightgray")
        self.reg2 = HardwareBlock(self.canvas, 800, 5, 30, 550,
                                  "Reg2", fill="lightblue")
        self.mux_srcB = HardwareBlock(self.canvas, 950, 100, 40, 40,
                                    "MUX \nSrcB", fill="lightgray")
        self.adderPC = HardwareBlock(self.canvas, 975, 200, 60, 80,
                                   "Adder PC", fill="lightgray")
        self.alu = HardwareBlock(self.canvas, 1050, 50, 50, 100,
                                   "ALU", fill="lightgray")
        self.reg3 = HardwareBlock(self.canvas, 1125, 5, 30, 550,
                                  "Reg3", fill="lightblue")
        self.data_mem = HardwareBlock(self.canvas, 1250, 50, 100, 150,
                                     "Data Mem", fill="lightblue")

        self.reg4 = HardwareBlock(self.canvas, 1400, 5, 30, 550,
                                  "Reg4", fill="lightblue")

        self.mux_result = HardwareBlock(self.canvas, 1450, 100, 40, 60,
                                    "MUX \nResult", fill="lightgray")



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

        """
        # Define puntos para la conexión manual
        puntos_conexion = [
            (self.regfile.x + self.regfile.width, self.regfile.y + self.regfile.height//2),  # centro derecha Register File
            (self.regfile.x + self.regfile.width + 20, self.regfile.y + self.regfile.height//2),  # línea horizontal
            (self.regfile.x + self.regfile.width + 20, self.alu.y + self.alu.height//2),  # línea vertical hacia ALU
            (self.alu.x, self.alu.y + self.alu.height//2)  # centro izquierda ALU
        ]

        # Crear conexión manual
        self.connection = ManualConnection(self.canvas, puntos_conexion, circle_radius=3, circle_color="black")
        self.connection.draw()
        """
        self.units = {
            "mux_pc": self.mux_pc,
        }

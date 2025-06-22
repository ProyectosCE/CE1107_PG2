from .base_view import BaseSimView
from .HardwareBlock import  *

class SimView2(BaseSimView):

    def _draw_content(self):

        # Bloques (igual que antes)
        self.alu = HardwareBlock(self.canvas, 100, 50, 50, 100, "ALU", fill="lightgray")
        self.regfile = HardwareBlock(self.canvas, 10, 20, 50, 280, "Register\nFile", fill="lightblue")

        self.alu.draw()
        self.regfile.draw()

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

        self.units = {
            "alu": self.alu,
            "register_file": self.regfile,
            "connection": self.connection,
        }

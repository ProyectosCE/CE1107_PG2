from .base_view import BaseSimView

class SimView1(BaseSimView):

    def _draw_content(self):
        self.canvas.create_rectangle(50, 50, 150, 150,
                                     fill="lightgray", tags="alu")
        self.canvas.create_text(100, 100, text="ALU")

        # Puedes guardar IDs en un diccionario para iluminarlos luego
        self.units = {
            "alu": "alu",
        }

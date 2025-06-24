from .HardwareBlock import *

class Connection:
    def __init__(self, canvas, source: HardwareBlock, target: HardwareBlock,
                 source_port="right", target_port="left", style="square",
                 color="#333", width=2, arrow=True):
        self.canvas = canvas
        self.source = source
        self.target = target
        self.source_port = source_port  # puede ser "right", "left" o nombre de puerto
        self.target_port = target_port
        self.style = style              # "square" o "straight"
        self.color = color
        self.width = width
        self.arrow = arrow
        self.line_id = None

    def _get_point(self, block, port):
        # Si es left/right usa método original, si no, usa get_port()
        if port == "left":
            return block.center_left()
        elif port == "right":
            return block.center_right()
        else:
            return block.get_port(port)

    def draw(self):
        x1, y1 = self._get_point(self.source, self.source_port)
        x2, y2 = self._get_point(self.target, self.target_port)

        if self.style == "straight":
            points = [x1, y1, x2, y2]
        elif self.style == "square":
            mid_x = (x1 + x2) / 2
            points = [x1, y1, mid_x, y1, mid_x, y2, x2, y2]
        else:
            raise ValueError("Estilo no reconocido: usa 'straight' o 'square'.")

        self.line_id = self.canvas.create_line(
            *points,
            fill=self.color,
            width=self.width,
            arrow="last" if self.arrow else None
        )

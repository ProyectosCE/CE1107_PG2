class HardwareBlock:
    def __init__(self, canvas, x, y, width, height, label, fill="lightgray", tags=None):
        self.canvas = canvas
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.label = label
        self.fill = fill
        self.rect_id = None
        self.text_id = None
        if tags is None:
            self.tag = None
        elif isinstance(tags, (list, tuple)):
            self.tag = tags[0]  # primer tag de la lista/tupla
        else:
            self.tag = tags  # era un string

    def draw(self):
        self.rect_id = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill=self.fill, outline="black", width=2, tags=self.tag
        )

        self.text_id = self.canvas.create_text(
            self.x + self.width / 2,
            self.y + self.height / 2,
            text=self.label,
            font=("Arial", 8, "bold"),
            justify="center"
        )

    def center_right(self):
        return (self.x + self.width, self.y + self.height / 2)

    def center_left(self):
        return (self.x, self.y + self.height / 2)

class ConnectionLine:
    def __init__(self, canvas, start_block: HardwareBlock, end_block: HardwareBlock):
        self.canvas = canvas
        self.start_block = start_block
        self.end_block = end_block
        self.line_id = None

    def draw(self):
        start_x, start_y = self.start_block.center_right()
        end_x, end_y = self.end_block.center_left()
        self.line_id = self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill="black", width=2, arrow="last"
        )

class ManualConnection:
    def __init__(self, canvas, points, circle_radius=5, line_width=2, line_color="black", circle_color="black"):
        """
        points: lista de tuplas (x, y) que define los puntos del polilínea
        Ejemplo: [(x1,y1), (x2,y2), (x3,y3)] -> dibuja línea entre (x1,y1)-(x2,y2) y (x2,y2)-(x3,y3)
        """
        self.canvas = canvas
        self.points = points
        self.circle_radius = circle_radius
        self.line_width = line_width
        self.line_color = line_color
        self.circle_color = circle_color

        self.line_ids = []
        self.circle_ids = []

    def draw(self):
        # Dibuja líneas entre puntos consecutivos
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            line_id = self.canvas.create_line(
                x1, y1, x2, y2,
                fill=self.line_color,
                width=self.line_width
            )
            self.line_ids.append(line_id)

        # Dibuja círculos en cada punto (menos opcionalmente el primero y último)
        for (x, y) in self.points:
            circle_id = self.canvas.create_oval(
                x - self.circle_radius, y - self.circle_radius,
                x + self.circle_radius, y + self.circle_radius,
                fill=self.circle_color,
                outline=""
            )
            self.circle_ids.append(circle_id)

    def clear(self):
        # Limpia líneas y círculos (para redibujar si quieres)
        for lid in self.line_ids:
            self.canvas.delete(lid)
        for cid in self.circle_ids:
            self.canvas.delete(cid)
        self.line_ids = []
        self.circle_ids = []

class HardwareBlock:
    def __init__(self, canvas, x, y, width, height, label,
                 fill="#DCE4EF", border_color="#4A6FA5", text_color="#1A1A1A",
                 shape_type="rect", tags=None):
        self.canvas = canvas
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.label = label
        self.fill = fill
        self.border_color = border_color
        self.text_color = text_color
        self.shape_type = shape_type  # "rect" o "trapezoid"
        self.rect_id = None
        self.text_id = None
        self.tag = tags[0] if isinstance(tags, (list, tuple)) else tags
        self.ports = {}  # Diccionario de puertos: nombre → (x, y)
        self.port_radius = 3  # Visual opcional

    def add_port(self, name, x_offset, y_offset, show=True):
        """Agrega un puerto nombrado con posición relativa al bloque."""
        abs_x = self.x + x_offset
        abs_y = self.y + y_offset
        self.ports[name] = (abs_x, abs_y)

        if show:
            # Dibujar un pequeño círculo para visualizar el puerto
            r = self.port_radius
            self.canvas.create_oval(abs_x - r, abs_y - r, abs_x + r, abs_y + r,
                                    fill="#000", outline="", tags=self.tag)

    def get_port(self, name):
        """Devuelve la posición absoluta (x, y) de un puerto nombrado."""
        if name not in self.ports:
            raise ValueError(f"Puerto '{name}' no definido en '{self.label}'")
        return self.ports[name]

    def center_right(self):
        return (self.x + self.width, self.y + self.height / 2)

    def center_left(self):
        return (self.x, self.y + self.height / 2)

    def draw(self):
        shadow_offset = 3

        if self.shape_type == "rect":
            self.canvas.create_rectangle(
                self.x + shadow_offset, self.y + shadow_offset,
                self.x + self.width + shadow_offset, self.y + self.height + shadow_offset,
                fill="#888888", outline="", tags=self.tag
            )
            self.rect_id = self.canvas.create_rectangle(
                self.x, self.y,
                self.x + self.width, self.y + self.height,
                fill=self.fill, outline=self.border_color, width=2, tags=self.tag
            )

        elif self.shape_type == "trapezoid":
            top = (self.x, self.y)
            bottom = (self.x, self.y + self.height)
            top_right = (self.x + self.width, self.y + self.height * 0.2)
            bottom_right = (self.x + self.width, self.y + self.height * 0.8)

            shadow_points = [(x + shadow_offset, y + shadow_offset)
                             for (x, y) in [top, bottom, bottom_right, top_right]]
            self.canvas.create_polygon(*shadow_points, fill="#888888", outline="")

            self.rect_id = self.canvas.create_polygon(
                top, bottom, bottom_right, top_right,
                fill=self.fill, outline=self.border_color, width=2, tags=self.tag
            )

        self.text_id = self.canvas.create_text(
            self.x + self.width / 2,
            self.y + self.height / 2,
            text=self.label,
            font=("Helvetica", 10, "bold"),
            fill=self.text_color,
            justify="center"
        )

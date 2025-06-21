import tkinter as tk
from abc import ABC, abstractmethod

class BaseSimView(tk.Frame, ABC):
    """Canvas con zoom + paneo. Las subclases solo implementan _draw_content."""
    ZOOM_IN  = 1.1
    ZOOM_OUT = 0.9

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self._scale = 1.0

        # ── Eventos ────────────────────────────────────────────────────
        for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.canvas.bind(ev, self._on_zoom)

        self.canvas.bind("<ButtonPress-1>", self._on_pan_start)
        self.canvas.bind("<B1-Motion>",     self._on_pan_move)

        # Delega el dibujo a la subclase
        self._draw_content()

        # Ajusta scrollregion según lo dibujado
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Metoods abstractos que deben implementar las subclases
    @abstractmethod
    def _draw_content(self):
        self.canvas.create_rectangle(50, 50, 150, 150,
                                     fill="blue", tags="all")
        ...

    # Metodos privados para manejar eventos
    def _on_zoom(self, event):
        factor = self.ZOOM_IN if (event.delta > 0 or event.num == 4) else self.ZOOM_OUT
        self._scale *= factor
        self.canvas.scale("all", event.x, event.y, factor, factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_pan_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _on_pan_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def highlight(self, unit):
        self.clear_highlights()
        tag = self.units.get(unit)
        if tag:
            self.canvas.itemconfig(tag, fill="yellow")
    def clear_highlights(self):
        for tag in self.units.values():
            self.canvas.itemconfig(tag, fill="lightblue")

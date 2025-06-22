import tkinter as tk
from abc import ABC, abstractmethod

class BaseSimView(tk.Frame, ABC):
    """Canvas con zoom + paneo + scrollbars."""
    ZOOM_IN  = 1.1
    ZOOM_OUT = 0.9

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        # Canvas y scrollbars
        self.canvas = tk.Canvas(self, bg="white")
        self.vbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.vbar.set, xscrollcommand=self.hbar.set)

        # Layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._scale = 1.0

        # Eventos mouse para zoom y paneo
        self.canvas.bind("<ButtonPress-1>", self._on_pan_start)
        self.canvas.bind("<B1-Motion>", self._on_pan_move)

        # Diferentes eventos para rueda (Windows, Linux)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)     # Windows / MacOS
        self.canvas.bind("<Button-4>", self._on_mousewheel)       # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mousewheel)       # Linux scroll down

        # Dibujo inicial y scrollregion
        self._draw_content()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    @abstractmethod
    def _draw_content(self):
        # Ejemplo de dibujo para test
        self.canvas.create_rectangle(50, 50, 400, 400, fill="blue", tags="all")

    def _on_mousewheel(self, event):
        # Si CTRL está presionado, zoom; si no, scroll vertical
        if (event.state & 0x0004) != 0:  # Ctrl presionado
            self._on_zoom(event)
        else:
            # Scroll vertical para Windows y Linux
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units")

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
import tkinter as tk


class SimView1(tk.Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self._scale = 1.0

        # Dibujo de ejemplo
        self.canvas.create_rectangle(50, 50, 150, 150,
                                     fill="blue", tags="all")

        # Vincula zoom al scroll del ratón
        for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.canvas.bind(ev, self._on_zoom)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_zoom(self, event):
        factor = 1.1 if (event.delta > 0 or event.num == 4) else 0.9
        self._scale *= factor
        self.canvas.scale("all", event.x, event.y, factor, factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

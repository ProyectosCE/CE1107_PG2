import tkinter as tk


class SimView2(tk.Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Dibujo de ejemplo
        self.canvas.create_rectangle(50, 50, 150, 150,
                                     fill="red", tags="all")

        for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.canvas.bind(ev, self._on_zoom)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_zoom(self, event):
        factor = 1.1 if (event.delta > 0 or event.num == 4) else 0.9
        self.canvas.scale("all", event.x, event.y, factor, factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

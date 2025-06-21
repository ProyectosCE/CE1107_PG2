import tkinter as tk

class ViewStatus(tk.Frame):
    def __init__(self, parent, view_name="Vista", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.view_name = view_name

        self.title_label = tk.Label(
            self,
            text=f"Estado del Sistema:\n{self.view_name}",
            font=("Arial", 12, "bold"),
            justify="left",
            anchor="w"
        )
        self.title_label.pack(anchor="w", padx=5, pady=5)

        self.ciclo_label = tk.Label(self, text="Ciclo: 0")
        self.ciclo_label.pack(anchor="w", padx=5)

        self.tiempo_label = tk.Label(self, text="Tiempo: 0.0 s")
        self.tiempo_label.pack(anchor="w", padx=5)

        self.pc_label = tk.Label(self, text="PC: 0x00000000")
        self.pc_label.pack(anchor="w", padx=5)

        tk.Label(self, text="Registros", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0), padx=5)

        self.reg_labels = []
        for i in range(8):
            lbl = tk.Label(self, text=f"x{i:02d}: 0x00000000", anchor="w")
            lbl.pack(fill="x", padx=5)
            self.reg_labels.append(lbl)

    def update_status(self, ciclo, tiempo, pc, registros):
        self.title_label.config(text=f"Estado del Sistema - {self.view_name}")
        self.ciclo_label.config(text=f"Ciclo: {ciclo}")
        self.tiempo_label.config(text=f"Tiempo: {tiempo:.2f} s")
        self.pc_label.config(text=f"PC: {pc:#010x}")
        for i, val in enumerate(registros):
            self.reg_labels[i].config(text=f"x{i:02d}: {val:#010x}")

    def set_view_name(self, name):
        self.view_name = name
        self.title_label.config(text=f"Estado del Sistema - {self.view_name}")

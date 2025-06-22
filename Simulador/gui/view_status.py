import tkinter as tk


class ViewStatus(tk.Frame):
    def __init__(self, parent, view_name="Vista", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.view_name = view_name

        # ───── 1) Estado del sistema ─────
        estado_frame = tk.LabelFrame(
            self, text=f"Estado del Sistema:\n{self.view_name}", font=("Arial", 10, "bold"))
        estado_frame.pack(fill="x", padx=5, pady=5)

        self.ciclo_label = tk.Label(estado_frame, text="Ciclo: 0")
        self.ciclo_label.pack(anchor="w", padx=5)
        self.tiempo_label = tk.Label(estado_frame, text="Tiempo: 0.0 s")
        self.tiempo_label.pack(anchor="w", padx=5)
        self.pc_label = tk.Label(estado_frame, text="PC: 0x00000000")
        self.pc_label.pack(anchor="w", padx=5)

        # ───── 2) Registros con scroll vertical ─────
        reg_lblf = tk.LabelFrame(self, text="Registros", font=("Arial", 10, "bold"))
        reg_lblf.pack(fill="both", expand=False, padx=5, pady=5)

        reg_lblf.columnconfigure(0, weight=1)
        reg_lblf.rowconfigure(0, weight=1)

        reg_canvas = tk.Canvas(reg_lblf, borderwidth=0, height=150)
        vscroll_regs = tk.Scrollbar(reg_lblf, orient="vertical", command=reg_canvas.yview)
        reg_canvas.configure(yscrollcommand=vscroll_regs.set)

        reg_canvas.grid(row=0, column=0, sticky="nsew")
        vscroll_regs.grid(row=0, column=1, sticky="ns")

        reg_inner = tk.Frame(reg_canvas)
        # Actualiza el scrollregion cuando el tamaño del contenido cambie
        reg_inner.bind(
            "<Configure>",
            lambda e: reg_canvas.configure(scrollregion=reg_canvas.bbox("all"))
        )

        # Ventana interna en canvas
        reg_canvas.create_window((0, 0), window=reg_inner, anchor="nw")

        self.reg_labels = []
        for i in range(32):
            lbl = tk.Label(reg_inner, text=f"x{i:02d}: 0x00000000", anchor="w")
            lbl.pack(fill="x", padx=5, pady=1)
            self.reg_labels.append(lbl)

        # ───── 3) Memoria con scroll vertical y horizontal ─────
        mem_lblf = tk.LabelFrame(self, text="Memoria", font=("Arial", 10, "bold"))
        mem_lblf.pack(fill="both", expand=True, padx=5, pady=5)

        mem_lblf.columnconfigure(0, weight=1)
        mem_lblf.rowconfigure(0, weight=1)

        hscroll_mem = tk.Scrollbar(mem_lblf, orient="horizontal")
        vscroll_mem = tk.Scrollbar(mem_lblf, orient="vertical")

        self.memory_text = tk.Text(
            mem_lblf, wrap="none", font=("Courier", 9),
            xscrollcommand=hscroll_mem.set, yscrollcommand=vscroll_mem.set
        )

        self.memory_text.grid(row=0, column=0, sticky="nsew")
        vscroll_mem.grid(row=0, column=1, sticky="ns")
        hscroll_mem.grid(row=1, column=0, columnspan=2, sticky="ew")

        hscroll_mem.config(command=self.memory_text.xview)
        vscroll_mem.config(command=self.memory_text.yview)

    # ------------------- API pública -------------------
    def update_status(self, ciclo, tiempo, pc, registros, memoria):
        self.ciclo_label.config(text=f"Ciclo: {ciclo}")
        self.tiempo_label.config(text=f"Tiempo: {tiempo:.2f} s")
        self.pc_label.config(text=f"PC: {pc:#010x}")

        for i, val in enumerate(registros[:len(self.reg_labels)]):
            self.reg_labels[i].config(text=f"x{i:02d}: {val:#010x}")

        self.memory_text.delete(1.0, tk.END)
        for addr, val in memoria.items():
            self.memory_text.insert(tk.END, f"{addr:08x}: {val:08x}\n")

    def set_view_name(self, name):
        self.view_name = name
        # Primer hijo es LabelFrame de estado
        estado_lblf = next(iter(self.children.values()))
        estado_lblf.config(text=f"Estado del Sistema:\n{name}")

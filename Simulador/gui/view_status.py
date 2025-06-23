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

        # ───── 1.5) Métricas de Simulación ─────
        metrica_frame = tk.LabelFrame(self, text="Métricas de Simulación", font=("Arial", 10, "bold"))
        metrica_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.metric_labels = {
            "ciclos": tk.Label(metrica_frame, text="Ciclos totales: 0", anchor="w"),
            "instrucciones": tk.Label(metrica_frame, text="Instrucciones retiradas: 0", anchor="w"),
            "cpi": tk.Label(metrica_frame, text="CPI (Ciclos por instrucción): 0.00", anchor="w"),
            "branches_totales": tk.Label(metrica_frame, text="Branches totales: 0", anchor="w"),
            "branches_acertados": tk.Label(metrica_frame, text="Branches acertados: 0", anchor="w"),
            "precision": tk.Label(metrica_frame, text="Precisión del predictor: 0.00%", anchor="w")
        }

        for lbl in self.metric_labels.values():
            lbl.pack(anchor="w", padx=5)


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

    def update_system_state(self, ciclo: int, tiempo: float, pc: int):
        """Actualiza ciclo, tiempo y PC."""
        self.ciclo_label.config(text=f"Ciclo: {ciclo}")
        self.tiempo_label.config(text=f"Tiempo: {tiempo:.2f} s")
        self.pc_label.config(text=f"PC: {pc:#010x}")

    def update_registers(self, reg_dict):
        """
        Actualiza los labels de registros según un diccionario con claves 'x0', 'x1', ... 'x31'.

        Params:
        - reg_dict: dict con claves tipo 'x0'...'x31' y valores enteros.

        Nota: Solo actualiza los registros visibles (x0 a x31).
        """
        for i in range(len(self.reg_labels)):  # i de 0 a 31
            reg_name = f"x{i}"
            if reg_name in reg_dict:
                value = reg_dict[reg_name]
                self.reg_labels[i].config(text=f"{reg_name}: {value:#010x}")

    def update_memory(self, mem):
        """
        Refresca la ventana de memoria.

        Formatos aceptados:
          1) Iterable de pares (addr, value)
          2) dict {addr: value}
        El contenido se ordena por dirección antes de mostrarse.
        """
        # --- Limpiamos ------------------------------------------------------
        self.memory_text.config(state='normal')  # por si está readonly
        self.memory_text.delete('1.0', tk.END)

        # --- Normalizamos y ordenamos --------------------------------------
        if isinstance(mem, dict):
            ordered = sorted(mem.items())
        else:
            try:
                ordered = sorted(mem, key=lambda p: p[0])
            except Exception:  # formato inesperado
                ordered = []

        # --- Mostramos ------------------------------------------------------
        for addr, val in ordered:
            self.memory_text.insert(tk.END,
                                    f"{addr:08X}: {val:08X}\n")

        self.memory_text.config(state='disabled')  # evita edición casual

    def update_metrics(self, ciclos, instrucciones, cpi, branches, branches_ok, precision):
        self.metric_labels["ciclos"].config(text=f"Ciclos totales: {ciclos}")
        self.metric_labels["instrucciones"].config(text=f"Instrucciones retiradas: {instrucciones}")
        self.metric_labels["cpi"].config(text=f"CPI (Ciclos por instrucción): {cpi:.2f}")
        self.metric_labels["branches_totales"].config(text=f"Branches totales: {branches}")
        self.metric_labels["branches_acertados"].config(text=f"Branches acertados: {branches_ok}")
        self.metric_labels["precision"].config(text=f"Precisión del predictor: {precision:.2f}%")

    def set_view_name(self, name):
        self.view_name = name
        # Primer hijo es LabelFrame de estado
        estado_lblf = next(iter(self.children.values()))
        estado_lblf.config(text=f"Estado del Sistema:\n{name}")
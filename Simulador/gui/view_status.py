import tkinter as tk


class ViewStatus(tk.Frame):
    def __init__(self, parent, view_name="Vista", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.view_name = view_name
        self._latest_memory_data = []  # para mantener datos

        # ───── TOOLBAR SUPERIOR ─────
        toolbar = tk.Frame(self, relief=tk.RAISED, bd=2)
        toolbar.pack(fill="x", padx=5, pady=2)

        self.btn_estado = tk.Button(toolbar, text="Estado Sistema", command=self._show_main_only)
        self.btn_estado.pack(side="left", padx=(0, 2))

        self.btn_memoria = tk.Button(toolbar, text="Memoria", command=self._show_memory_only)
        self.btn_memoria.pack(side="left", padx=2)

        # ───── Panel principal ─────
        self._main_panel = tk.Frame(self)
        self._main_panel.pack(fill="both", expand=True)

        # ───── 1) Estado del sistema ─────
        self.estado_lblf = tk.LabelFrame(
            self._main_panel, text=f"Estado del Sistema:\n{self.view_name}", font=("Arial", 10, "bold"))
        self.estado_lblf.pack(fill="x", padx=5, pady=5)

        self.ciclo_label = tk.Label(self.estado_lblf, text="Ciclo: 0")
        self.ciclo_label.pack(anchor="w", padx=5)
        self.tiempo_label = tk.Label(self.estado_lblf, text="Tiempo: 0.0 s")
        self.tiempo_label.pack(anchor="w", padx=5)
        self.pc_label = tk.Label(self.estado_lblf, text="PC: 0x00000000")
        self.pc_label.pack(anchor="w", padx=5)

        # ───── 1.5) Pipeline ─────
        pipeline_frame = tk.LabelFrame(self._main_panel, text="Pipeline (etapas)", font=("Arial", 10, "bold"))
        pipeline_frame.pack(fill="x", padx=5, pady=5)

        pipeline_container = tk.Frame(pipeline_frame)
        pipeline_container.pack(fill="x", expand=True, padx=5, pady=5)

        self.pipeline_text = tk.Text(pipeline_container, height=7, font=("Courier", 9), state="disabled", wrap="none")
        self.pipeline_text.pack(side="top", fill="x", expand=True)

        hscroll_pipeline = tk.Scrollbar(pipeline_container, orient="horizontal", command=self.pipeline_text.xview)
        hscroll_pipeline.pack(side="bottom", fill="x")
        self.pipeline_text.configure(xscrollcommand=hscroll_pipeline.set)

        # ───── 2) Métricas de Simulación ─────
        metrica_frame = tk.LabelFrame(self._main_panel, text="Métricas de Simulación", font=("Arial", 10, "bold"))
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

        # ───── 3) Registros ─────
        reg_lblf = tk.LabelFrame(self._main_panel, text="Registros", font=("Arial", 10, "bold"))
        reg_lblf.pack(fill="both", expand=False, padx=5, pady=5)
        reg_lblf.columnconfigure(0, weight=1)
        reg_lblf.rowconfigure(0, weight=1)

        reg_canvas = tk.Canvas(reg_lblf, borderwidth=0, height=300)
        vscroll_regs = tk.Scrollbar(reg_lblf, orient="vertical", command=reg_canvas.yview)
        reg_canvas.configure(yscrollcommand=vscroll_regs.set)

        reg_canvas.grid(row=0, column=0, sticky="nsew")
        vscroll_regs.grid(row=0, column=1, sticky="ns")

        reg_inner = tk.Frame(reg_canvas)
        reg_inner.bind("<Configure>", lambda e: reg_canvas.configure(scrollregion=reg_canvas.bbox("all")))
        reg_canvas.create_window((0, 0), window=reg_inner, anchor="nw")

        self.reg_labels = []
        for i in range(32):
            lbl = tk.Label(reg_inner, text=f"x{i:02d}: 0x00000000", anchor="w")
            lbl.pack(fill="x", padx=5, pady=1)
            self.reg_labels.append(lbl)

        # ───── 4) Panel de Memoria ─────
        self._memory_panel = tk.LabelFrame(self, text="Memoria", font=("Arial", 10, "bold"))
        self._memory_panel.pack_forget()  # se oculta al inicio

        self._memory_panel.columnconfigure(0, weight=1)
        self._memory_panel.rowconfigure(0, weight=1)

        hscroll_mem = tk.Scrollbar(self._memory_panel, orient="horizontal")
        vscroll_mem = tk.Scrollbar(self._memory_panel, orient="vertical")

        self.memory_text = tk.Text(
            self._memory_panel, wrap="none", font=("Courier", 9),
            xscrollcommand=hscroll_mem.set, yscrollcommand=vscroll_mem.set
        )

        self.memory_text.grid(row=0, column=0, sticky="nsew")
        vscroll_mem.grid(row=0, column=1, sticky="ns")
        hscroll_mem.grid(row=1, column=0, columnspan=2, sticky="ew")

        hscroll_mem.config(command=self.memory_text.xview)
        vscroll_mem.config(command=self.memory_text.yview)

    # ------------------- Métodos para cambiar vista -------------------

    def _show_main_only(self):
        self._memory_panel.pack_forget()
        self._main_panel.pack(fill="both", expand=True)
        self.btn_estado.config(relief=tk.SUNKEN)
        self.btn_memoria.config(relief=tk.RAISED)

    def _show_memory_only(self):
        self._main_panel.pack_forget()
        self._memory_panel.pack(fill="both", expand=True)
        self.btn_estado.config(relief=tk.RAISED)
        self.btn_memoria.config(relief=tk.SUNKEN)

    # ------------------- API pública -------------------

    def update_system_state(self, ciclo: int, tiempo: float, pc: int):
        """Actualiza ciclo, tiempo y PC."""
        self.ciclo_label.config(text=f"Ciclo: {ciclo}")
        # Mostrar el tiempo con 6 decimales para mayor precisión visual
        self.tiempo_label.config(text=f"Tiempo: {tiempo:.6f} s")
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

    def update_pipeline(self, pipeline_info: dict, ciclo: int):
        """
        pipeline_info: dict con claves IF_ID, ID_EX, EX_MEM, MEM_WB, cada uno string con info.
        ciclo: número de ciclo actual.
        """
        texto = [f"[Ciclo {ciclo}]"]
        etapas = ["IF_ID", "ID_EX", "EX_MEM", "MEM_WB"]
        for etapa in etapas:
            info = pipeline_info.get(etapa, "nop")
            texto.append(f"{etapa}: {info}")

        full_text = "\n".join(texto)
        self.pipeline_text.configure(state="normal")
        self.pipeline_text.delete(1.0, tk.END)
        self.pipeline_text.insert(tk.END, full_text)
        self.pipeline_text.configure(state="disabled")

    def set_view_name(self, name):
        self.view_name = name
        self.estado_lblf.config(text=f"Estado del Sistema:\n{name}")

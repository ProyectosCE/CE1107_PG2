import tkinter as tk
from tkinter import ttk
from datetime import datetime


def Principal_Window():
    win = tk.Tk()
    win.title("Simulador RISC-V")
    win.minsize(width=1000, height=600)

    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=2)
    win.grid_columnconfigure(2, weight=1)

    # Área de código
    code_frame = tk.Frame(win)
    code_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    tk.Label(code_frame, text="Código RISC-V", font=("Arial", 12, "bold")).pack(anchor="w")
    Code_Space = tk.Text(code_frame, width=30)
    Code_Space.pack(expand=True, fill="both")

    # Área de simulación con título y pestañas
    sim_frame = tk.Frame(win)
    sim_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    tk.Label(sim_frame, text="Simulación", font=("Arial", 14, "bold")).pack(anchor="center", pady=(5, 10))

    notebook = ttk.Notebook(sim_frame)
    notebook.pack(expand=True, fill="both")

    # Pestaña 1
    ciclo_frame = tk.Frame(notebook)
    notebook.add(ciclo_frame, text="Procesador 1")
    tk.Label(ciclo_frame, text="Procesador 1", font=("Arial", 11)).pack(padx=10, pady=10)

    # Pestaña 2
    pipeline_frame = tk.Frame(notebook)
    notebook.add(pipeline_frame, text="Procesador 2")
    tk.Label(pipeline_frame, text="Procesador 2", font=("Arial", 11)).pack(padx=10, pady=10)

    # Área de registros y estado
    reg_frame = tk.Frame(win)
    reg_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
    tk.Label(reg_frame, text="Estado del Sistema", font=("Arial", 12, "bold")).pack(anchor="w")

    # Ciclo de ejecución
    ciclo_label = tk.Label(reg_frame, text="Ciclo: 0")
    ciclo_label.pack(anchor="w", padx=5)

    # Tiempo desde inicio
    tiempo_label = tk.Label(reg_frame, text="Tiempo: 0.0 s")
    tiempo_label.pack(anchor="w", padx=5)

    # Valor del PC
    pc_label = tk.Label(reg_frame, text="PC: 0x00000000")
    pc_label.pack(anchor="w", padx=5)

    # Registros
    tk.Label(reg_frame, text="Registros", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
    reg_labels = []
    for i in range(8):  # Puedes extenderlo a 32
        label = tk.Label(reg_frame, text=f"x{i:02d}: 0x00000000", anchor="w")
        label.pack(fill="x", padx=5)
        reg_labels.append(label)

    win.mainloop()

Principal_Window()

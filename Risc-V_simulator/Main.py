import tkinter as tk

def Principal_Window():
    win = tk.Tk()
    win.title("Simulador RISC-V")
    win.minsize(width=1000, height=600)

    # Configuración de columnas y filas para expandirse correctamente
    win.grid_rowconfigure(0, weight=1)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=2)
    win.grid_columnconfigure(2, weight=1)

    # Área de código
    code_frame = tk.Frame(win)
    code_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    code_label = tk.Label(code_frame, text="Código RISC-V", font=("Arial", 12, "bold"))
    code_label.pack(anchor="w")
    Code_Space = tk.Text(code_frame, width=30)
    Code_Space.pack(expand=True, fill="both")

    # Área de simulación (Canvas con fondo gris claro)
    Simulation_Space = tk.Canvas(win, bg="#DDDDDD")
    Simulation_Space.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    # Área de registros
    reg_frame = tk.Frame(win)
    reg_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
    reg_label = tk.Label(reg_frame, text="Registros", font=("Arial", 12, "bold"))
    reg_label.pack(anchor="w")

    # 8 registros de ejemplo (puedes extender a 32)
    for i in range(8):
        label = tk.Label(reg_frame, text=f"x{i:02d}: 0x00000000", anchor="w")
        label.pack(fill="x", padx=5)

    win.mainloop()

Principal_Window()

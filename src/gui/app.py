from typing import Optional, Callable
import customtkinter as ctk
from tkinter import ttk, messagebox
from src.gui.teclado_cientifico import TecladoCientifico
from src.gui.tabla_iteraciones import TablaIteraciones
from src.gui.grafica import Grafica
from src.gui.animacion import PanelAnimacion
from src.core.evaluador import crear_evaluador
from src.core.secante import secante
from src.utils.excel import exportar_iteraciones_excel


class SecanteApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Método de la Secante")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Layout: Top frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configuración (izquierda)
        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Resultados y tabla (derecha)
        self.frame_result = ctk.CTkFrame(self)
        self.frame_result.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Dentro de frame_config: teclado y entradas
        self.teclado = TecladoCientifico(self.frame_config, callback=self._insertar_texto)
        self.teclado.pack(side="top", fill="x", pady=6)

        # Entradas
        self._crear_entradas()

        # Botones
        self._crear_botones()

        # Resultados
        self._crear_panel_resultados()

        # Tabla
        self.tabla = TablaIteraciones(self.frame_result)
        self.tabla.pack(fill="both", expand=True, pady=8)

        # Abajo: grafica y animacion
        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_bottom.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0,10))
        self.frame_bottom.grid_columnconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(1, weight=1)

        self.grafica = Grafica(self.frame_bottom)
        self.grafica.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        self.animacion = PanelAnimacion(self.frame_bottom)
        self.animacion.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

        # Estado interno
        self.iteraciones = []

    def _crear_entradas(self) -> None:
        frame_inputs = ctk.CTkFrame(self.frame_config)
        frame_inputs.pack(fill="x", pady=6)

        self.entry_fx = ctk.CTkEntry(frame_inputs, placeholder_text="f(x)")
        self.entry_fx.pack(fill="x", padx=6, pady=4)

        row2 = ctk.CTkFrame(frame_inputs)
        row2.pack(fill="x", pady=4)
        self.entry_x0 = ctk.CTkEntry(row2, placeholder_text="x0")
        self.entry_x0.pack(side="left", expand=True, fill="x", padx=3)
        self.entry_x1 = ctk.CTkEntry(row2, placeholder_text="x1")
        self.entry_x1.pack(side="left", expand=True, fill="x", padx=3)

        row3 = ctk.CTkFrame(frame_inputs)
        row3.pack(fill="x", pady=4)
        self.entry_tol = ctk.CTkEntry(row3, placeholder_text="tolerancia (ej: 1e-6)")
        self.entry_tol.pack(side="left", expand=True, fill="x", padx=3)
        self.entry_max = ctk.CTkEntry(row3, placeholder_text="max iteraciones")
        self.entry_max.pack(side="left", expand=True, fill="x", padx=3)

    def _crear_botones(self) -> None:
        frame_btns = ctk.CTkFrame(self.frame_config)
        frame_btns.pack(fill="x", pady=6)

        btn_calcular = ctk.CTkButton(frame_btns, text="Calcular", command=self._calcular)
        btn_calcular.pack(side="left", padx=3, pady=3)

        btn_limpiar = ctk.CTkButton(frame_btns, text="Limpiar Todo", command=self._limpiar)
        btn_limpiar.pack(side="left", padx=3, pady=3)

        btn_ayuda = ctk.CTkButton(frame_btns, text="Ayuda", command=self._mostrar_ayuda)
        btn_ayuda.pack(side="left", padx=3, pady=3)

        btn_export = ctk.CTkButton(frame_btns, text="Exportar Excel", command=self._exportar)
        btn_export.pack(side="left", padx=3, pady=3)

    def _crear_panel_resultados(self) -> None:
        frame_panel = ctk.CTkFrame(self.frame_result)
        frame_panel.pack(fill="x", pady=6)

        self.lbl_raiz = ctk.CTkLabel(frame_panel, text="Raíz: -")
        self.lbl_raiz.pack(anchor="w", padx=6, pady=2)
        self.lbl_fraiz = ctk.CTkLabel(frame_panel, text="f(Raíz): -")
        self.lbl_fraiz.pack(anchor="w", padx=6, pady=2)
        self.lbl_iters = ctk.CTkLabel(frame_panel, text="Iteraciones: -")
        self.lbl_iters.pack(anchor="w", padx=6, pady=2)
        self.lbl_error = ctk.CTkLabel(frame_panel, text="Error final: -")
        self.lbl_error.pack(anchor="w", padx=6, pady=2)
        self.lbl_estado = ctk.CTkLabel(frame_panel, text="Estado: -")
        self.lbl_estado.pack(anchor="w", padx=6, pady=2)

    def _insertar_texto(self, texto: str) -> None:
        # Inserta en f(x) el texto proveniente del teclado
        current = self.entry_fx.get()
        self.entry_fx.delete(0, "end")
        self.entry_fx.insert(0, current + texto)

    def _calcular(self) -> None:
        fx = self.entry_fx.get().strip()
        try:
            x0 = float(self.entry_x0.get())
            x1 = float(self.entry_x1.get())
            tol = float(self.entry_tol.get() or 1e-6)
            max_iter = int(self.entry_max.get() or 50)
        except Exception:
            messagebox.showerror("Error", "Entradas numéricas inválidas")
            return

        try:
            f = crear_evaluador(fx)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo parsear f(x): {e}")
            return

        resultado = secante(f, x0, x1, tol, max_iter)
        self.iteraciones = resultado["iteraciones"]

        # Actualizar tabla
        self.tabla.cargar_datos(self.iteraciones)

        # Resultados resumen
        raiz = resultado.get("raiz")
        f_raiz = resultado.get("f_raiz")
        iters = resultado.get("iteraciones_real", 0)
        error_final = resultado.get("error")
        estado = resultado.get("estado")

        self.lbl_raiz.configure(text=f"Raíz: {raiz}")
        self.lbl_fraiz.configure(text=f"f(Raíz): {f_raiz}")
        self.lbl_iters.configure(text=f"Iteraciones: {iters}")
        self.lbl_error.configure(text=f"Error final: {error_final}")
        self.lbl_estado.configure(text=f"Estado: {estado}")

        # Grafica
        try:
            self.grafica.plot_function(f, raiz)
        except Exception:
            pass

    def _limpiar(self) -> None:
        self.entry_fx.delete(0, "end")
        self.entry_x0.delete(0, "end")
        self.entry_x1.delete(0, "end")
        self.entry_tol.delete(0, "end")
        self.entry_max.delete(0, "end")
        self.tabla.limpiar()
        self.lbl_raiz.configure(text="Raíz: -")
        self.lbl_fraiz.configure(text="f(Raíz): -")
        self.lbl_iters.configure(text="Iteraciones: -")
        self.lbl_error.configure(text="Error final: -")
        self.lbl_estado.configure(text="Estado: -")
        self.grafica.clear()

    def _mostrar_ayuda(self) -> None:
        texto = (
            "Método de la Secante:\n"
            "x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))\n\n"
            "Criterio de paro por tolerancia en el error absoluto o por número máximo de iteraciones.\n"
            "Funciones soportadas: expresiones matemáticas estándar (sin, cos, tan, exp, log, sqrt, etc.)."
        )
        messagebox.showinfo("Ayuda", texto)

    def _exportar(self) -> None:
        if not self.iteraciones:
            messagebox.showwarning("Exportar", "No hay iteraciones para exportar")
            return
        path = "iteraciones_metodo_secante.xlsx"
        exportar_iteraciones_excel(self.iteraciones, path)
        messagebox.showinfo("Exportar", f"Exportado a {path}")

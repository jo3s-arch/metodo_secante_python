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
        try:
            ctk.set_default_color_theme("dark-blue")
        except Exception:
            pass

        # Make window responsive using grid weights and a layout switch based on width
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frames (created but arrangement will be handled by arrange_layout)
        self.frame_config = ctk.CTkFrame(self)
        self.frame_result = ctk.CTkFrame(self)
        self.frame_bottom = ctk.CTkFrame(self)

        # Child widgets
        self.teclado = TecladoCientifico(self.frame_config, callback=self._insertar_texto)
        self.teclado.pack(side="top", fill="both", expand=False, pady=8, padx=8)

        # Inputs and buttons live in frame_config
        self._crear_entradas()
        self._crear_botones()

        # Result panel and table
        self._crear_panel_resultados()
        self.tabla = TablaIteraciones(self.frame_result)
        self.tabla.pack(fill="both", expand=True, pady=8, padx=8)

        # Bottom area: grafica y animacion
        self.grafica = Grafica(self.frame_bottom)
        self.animacion = PanelAnimacion(self.frame_bottom)
        # Use grid inside bottom
        self.frame_bottom.grid_rowconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(0, weight=1)
        self.frame_bottom.grid_columnconfigure(1, weight=1)
        self.grafica.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.animacion.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

        # Internal state
        self.iteraciones = []

        # Layout state
        self._vertical = False
        self._layout_threshold = 900  # px width under which we switch to vertical layout
        self.arrange_layout(initial=True)

        # Bind resize to adjust layout and scale controls
        self.bind("<Configure>", self._on_resize)

    def arrange_layout(self, initial: bool=False) -> None:
        # Remove any existing placements
        for widget in (self.frame_config, self.frame_result, self.frame_bottom):
            widget.grid_forget()

        w = self.winfo_width()
        if initial and w == 1:
            # If called before window is realized, use geometry width
            try:
                geom = self.geometry().split('+')[0]
                w = int(geom.split('x')[0])
            except Exception:
                w = 1100

        if w < self._layout_threshold:
            # Vertical layout: stack frames
            self._vertical = True
            self.frame_config.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=12, pady=8)
            self.frame_result.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=12, pady=8)
            self.frame_bottom.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=12, pady=8)
        else:
            # Horizontal layout: config left, results right, bottom spans
            self._vertical = False
            self.frame_config.grid(row=0, column=0, sticky="nsew", padx=12, pady=8)
            self.frame_result.grid(row=0, column=1, sticky="nsew", padx=12, pady=8)
            self.frame_bottom.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=12, pady=8)

        # Adjust button sizes and spacing depending on layout/size
        self._scale_controls()

    def _on_resize(self, event) -> None:
        # Called frequently during resize; only update layout when crossing threshold or scaling factor changes
        try:
            new_vertical = event.width < self._layout_threshold
        except Exception:
            new_vertical = False
        if new_vertical != self._vertical:
            self.arrange_layout()
        # scale keyboard buttons based on width
        self._scale_controls()

    def _scale_controls(self) -> None:
        # Compute scale factor based on width
        width = max(self.winfo_width(), 600)
        scale = width / 1100  # 1.0 at 1100 px
        # Limit scale between 0.6 and 1.6
        scale = max(0.6, min(1.6, scale))
        # Set button size for teclado
        btn_w = int(56 * scale)
        btn_h = int(44 * scale)
        font_size = max(10, int(12 * scale))
        self.teclado.set_button_size(btn_w, btn_h, font_size)
        # Adjust padding for frames
        pad = int(8 * scale)
        for f in (self.frame_config, self.frame_result, self.frame_bottom):
            f.configure(padx=pad, pady=pad)

    def _crear_entradas(self) -> None:
        frame_inputs = ctk.CTkFrame(self.frame_config)
        frame_inputs.pack(fill="x", pady=8, padx=8)

        self.entry_fx = ctk.CTkEntry(frame_inputs, placeholder_text="f(x)")
        self.entry_fx.pack(fill="x", padx=6, pady=6)

        row2 = ctk.CTkFrame(frame_inputs)
        row2.pack(fill="x", pady=6)
        self.entry_x0 = ctk.CTkEntry(row2, placeholder_text="x0")
        self.entry_x0.pack(side="left", expand=True, fill="x", padx=6)
        self.entry_x1 = ctk.CTkEntry(row2, placeholder_text="x1")
        self.entry_x1.pack(side="left", expand=True, fill="x", padx=6)

        row3 = ctk.CTkFrame(frame_inputs)
        row3.pack(fill="x", pady=6)
        self.entry_tol = ctk.CTkEntry(row3, placeholder_text="tolerancia (ej: 1e-6)")
        self.entry_tol.pack(side="left", expand=True, fill="x", padx=6)
        self.entry_max = ctk.CTkEntry(row3, placeholder_text="max iteraciones")
        self.entry_max.pack(side="left", expand=True, fill="x", padx=6)

    def _crear_botones(self) -> None:
        frame_btns = ctk.CTkFrame(self.frame_config)
        frame_btns.pack(fill="x", pady=8, padx=8)

        btn_calcular = ctk.CTkButton(frame_btns, text="Calcular", command=self._calcular, width=140, height=40)
        btn_calcular.pack(side="left", padx=6, pady=6)

        btn_limpiar = ctk.CTkButton(frame_btns, text="Limpiar Todo", command=self._limpiar, width=140, height=40)
        btn_limpiar.pack(side="left", padx=6, pady=6)

        btn_ayuda = ctk.CTkButton(frame_btns, text="Ayuda", command=self._mostrar_ayuda, width=120, height=40)
        btn_ayuda.pack(side="left", padx=6, pady=6)

        btn_export = ctk.CTkButton(frame_btns, text="Exportar Excel", command=self._exportar, width=140, height=40)
        btn_export.pack(side="left", padx=6, pady=6)

    def _crear_panel_resultados(self) -> None:
        frame_panel = ctk.CTkFrame(self.frame_result)
        frame_panel.pack(fill="x", pady=8, padx=8)

        self.lbl_raiz = ctk.CTkLabel(frame_panel, text="Raíz: -")
        self.lbl_raiz.pack(anchor="w", padx=6, pady=4)
        self.lbl_fraiz = ctk.CTkLabel(frame_panel, text="f(Raíz): -")
        self.lbl_fraiz.pack(anchor="w", padx=6, pady=4)
        self.lbl_iters = ctk.CTkLabel(frame_panel, text="Iteraciones: -")
        self.lbl_iters.pack(anchor="w", padx=6, pady=4)
        self.lbl_error = ctk.CTkLabel(frame_panel, text="Error final: -")
        self.lbl_error.pack(anchor="w", padx=6, pady=4)
        self.lbl_estado = ctk.CTkLabel(frame_panel, text="Estado: -")
        self.lbl_estado.pack(anchor="w", padx=6, pady=4)

    def _insertar_texto(self, texto: str) -> None:
        # Inserta en f(x) el texto proveniente del teclado
        if texto == "":
            self.entry_fx.delete(0, "end")
            return
        if texto == "\b":
            cur = self.entry_fx.get()
            self.entry_fx.delete(0, "end")
            self.entry_fx.insert(0, cur[:-1])
            return
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

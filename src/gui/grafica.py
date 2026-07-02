from typing import Callable, Optional
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk


class Grafica(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(parent)
        self.fig = Figure(figsize=(5,3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_function(self, f: Callable[[float], float], raiz: Optional[float]=None) -> None:
        x = np.linspace(-10,10,400)
        try:
            y = f(x)
        except Exception:
            # Try vectorize
            y = np.vectorize(lambda t: float(f(t)))(x)
        self.ax.clear()
        self.ax.plot(x,y, label='f(x)')
        self.ax.axhline(0, color='k', linewidth=0.8)
        if raiz is not None:
            try:
                self.ax.scatter([raiz],[0], color='r', label='raíz')
            except Exception:
                pass
        self.ax.legend()
        self.canvas.draw()

    def clear(self) -> None:
        self.ax.clear()
        self.canvas.draw()

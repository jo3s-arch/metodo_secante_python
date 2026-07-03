from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl
import tkinter as tk
from typing import Callable

# Configure Matplotlib for MathText and dark theme compatibility
mpl.rcParams['text.usetex'] = False
mpl.rcParams['mathtext.fontset'] = 'cm'
# Do not force figure.facecolor globally as some backends may not accept 'none'


def create_math_label(parent: tk.Widget, texto_latex: str, tamaño: int = 12, dpi: int = 100, color: str = 'white') -> FigureCanvasTkAgg:
    """
    Crea y retorna un FigureCanvasTkAgg que muestra texto en MathText.
    El canvas devuelto tiene añadido un método `math_update(latex: str, tamaño: int|None)` para actualizar el texto.

    - parent: widget Tkinter donde incrustar el canvas
    - texto_latex: cadena LaTeX/MathText (por ejemplo r"$x^2 - 4$")
    - tamaño: tamaño de la fuente
    - dpi: dpi de la figura
    - color: color del texto (ej. 'white')

    El widget de Matplotlib (FigureCanvasTkAgg) es retornado y su widget interno puede ser obtenido
    con canvas.get_tk_widget().
    """
    # Create a tiny figure; we'll let the container control widget size
    fig = Figure(figsize=(1, 0.4), dpi=dpi)
    # Transparent background for figure (works by setting alpha)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Ensure the passed latex is wrapped with $...$ if not already
    text = texto_latex
    if texto_latex and not (texto_latex.strip().startswith('$') and texto_latex.strip().endswith('$')):
        text = f"${texto_latex}$"

    txt_artist = ax.text(0.5, 0.5, text, ha='center', va='center', color=color, fontsize=tamaño)

    canvas = FigureCanvasTkAgg(fig, master=parent)
    widget = canvas.get_tk_widget()

    def math_update(latex: str, tamaño_nuevo: int | None = None, color_nuevo: str | None = None) -> None:
        try:
            new_text = latex
            if latex and not (latex.strip().startswith('$') and latex.strip().endswith('$')):
                new_text = f"${latex}$"
            txt_artist.set_text(new_text)
            if tamaño_nuevo is not None:
                txt_artist.set_fontsize(tamaño_nuevo)
            if color_nuevo is not None:
                txt_artist.set_color(color_nuevo)
            fig.canvas.draw_idle()
        except Exception:
            # fallback: set plain text
            try:
                txt_artist.set_text(latex)
                fig.canvas.draw_idle()
            except Exception:
                pass

    # Attach helper to canvas object so callers can update easily
    setattr(canvas, 'math_update', math_update)
    setattr(canvas, 'math_fig', fig)
    setattr(canvas, 'math_ax', ax)
    return canvas

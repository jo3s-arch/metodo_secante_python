from typing import Callable, List, Dict, Any, Optional


def secante(f: Callable[[float], float], x0: float, x1: float, tol: float=1e-6, max_iter: int=50) -> Dict[str, Any]:
    """
    Implementación del método de la secante.
    Devuelve un dict con las iteraciones y el resultado.
    Cada fila de iteraciones es un dict con claves: i, x_prev, x_curr, x_next, f_prev, f_curr, error
    """
    iteraciones: List[Dict[str, Any]] = []
    estado = "No convergió"
    raiz: Optional[float] = None
    f_raiz: Optional[float] = None

    try:
        f_x0 = float(f(x0))
        f_x1 = float(f(x1))
    except Exception as e:
        raise ValueError(f"Error al evaluar la función en x0/x1: {e}")

    for i in range(1, max_iter+1):
        denom = (f_x1 - f_x0)
        if denom == 0:
            estado = "División por cero en el denominador"
            break
        x2 = x1 - f_x1 * (x1 - x0) / denom
        try:
            f_x2 = float(f(x2))
        except Exception:
            f_x2 = None
        error = abs(x2 - x1)

        iteraciones.append({
            "i": i,
            "x_prev": x0,
            "x_curr": x1,
            "x_next": x2,
            "f_prev": f_x0,
            "f_curr": f_x1,
            "error": error,
        })

        if error <= tol:
            estado = "Convergió"
            raiz = x2
            f_raiz = f_x2
            break

        # preparar siguiente iteración
        x0, x1 = x1, x2
        f_x0, f_x1 = f_x1, f_x2 if f_x2 is not None else float('nan')
    else:
        estado = "Alcanzado máximo de iteraciones"
        raiz = x2
        f_raiz = f_x2 if 'f_x2' in locals() else None

    return {
        "iteraciones": iteraciones,
        "iteraciones_real": len(iteraciones),
        "raiz": raiz,
        "f_raiz": f_raiz,
        "error": iteraciones[-1]['error'] if iteraciones else None,
        "estado": estado,
    }

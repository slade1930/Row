from math import *
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

# ------------------ MÉTODO DE FALSA POSICIÓN ------------------
def falsa_posicion(funcion, x0, x1, tol=1e-4, max_iter=100):
    pasos = ""
    try:
        fx = lambda x: eval(funcion)

        for i in range(max_iter):
            f_x0 = fx(x0)
            f_x1 = fx(x1)

            if f_x0 == f_x1:
                pasos += "División por cero detectada. f(x0) = f(x1).\n"
                break

            x2 = x1 - (f_x1 * (x0 - x1)) / (f_x0 - f_x1)
            f_x2 = fx(x2)

            pasos += f"Iteración {i+1}: x0 = {x0:.6f}, x1 = {x1:.6f}, x2 = {x2:.6f}, f(x2) = {f_x2:.6f}\n"

            if abs(f_x2) < tol:
                pasos += f"Raíz aproximada encontrada: {x2:.6f}\n"
                return x2, pasos

            if f_x0 * f_x2 < 0:
                x1 = x2
            else:
                x0 = x2

        pasos += f"No se encontró raíz con tolerancia {tol} en {max_iter} iteraciones.\n"
        return x2, pasos

    except Exception as e:
        return None, f"Error al evaluar la función: {str(e)}"


def generar_grafica(funcion_str, x0, x1, raiz_aprox):
    try:
        fx = lambda x: eval(funcion_str)
        x_vals = np.linspace(x0 - 1, x1 + 1, 400)
        y_vals = [fx(x) for x in x_vals]

        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_vals, label=f"f(x) = {funcion_str}")
        plt.axhline(0, color='gray', linestyle='--')
        plt.plot(raiz_aprox, fx(raiz_aprox), 'ro', label=f"Raíz aprox: {raiz_aprox:.6f}")
        plt.title("Método de Falsa Posición")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        imagen_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return imagen_base64
    except Exception as e:
        return None

# ------------------ MÉTODO DE ELIMINACIÓN DE GAUSS ------------------
def eliminacion_gauss(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)
    pasos = ""
    
    try:
        for i in range(n):
            if A[i][i] == 0:
                return None, "División por cero detectada en la diagonal."

            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j, i:] -= factor * A[i, i:]
                b[j] -= factor * b[i]
                pasos += f"R{j+1} = R{j+1} - ({factor:.4f}) * R{i+1}\n"

        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i][i]

        return x.tolist(), pasos
    except Exception as e:
        return None, f"Error durante la eliminación de Gauss: {str(e)}"

def grafica_comparacion_solucion(A, b, solucion):
    try:
        exacta = np.linalg.solve(np.array(A), np.array(b))
        indices = np.arange(len(b))

        plt.figure(figsize=(8, 5))
        plt.plot(indices, exacta, 'go-', label='Solución exacta')
        plt.plot(indices, solucion, 'ro--', label='Solución numérica (Gauss)')
        plt.title('Comparación: Solución Exacta vs Numérica')
        plt.xlabel('Variable')
        plt.ylabel('Valor')
        plt.legend()
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        imagen_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return imagen_base64
    except Exception as e:
        return None

# ------------------ MÉTODO DE GAUSS-JORDAN ------------------
def gauss_jordan(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)
    pasos = ""

    try:
        Ab = np.hstack([A, b.reshape(-1, 1)])

        for i in range(n):
            if Ab[i][i] == 0:
                return None, "División por cero detectada."

            Ab[i] = Ab[i] / Ab[i][i]
            pasos += f"R{i+1} = R{i+1} / {Ab[i][i]:.4f}\n"

            for j in range(n):
                if i != j:
                    factor = Ab[j][i]
                    Ab[j] = Ab[j] - factor * Ab[i]
                    pasos += f"R{j+1} = R{j+1} - ({factor:.4f}) * R{i+1}\n"

        x = Ab[:, -1]
        return x.tolist(), pasos, Ab[:, :-1]
    except Exception as e:
        return None, f"Error durante Gauss-Jordan: {str(e)}", None

def grafica_matriz_transformada(matriz):
    try:
        plt.figure(figsize=(6, 6))
        plt.imshow(matriz, cmap='Blues', interpolation='nearest')
        plt.colorbar()
        plt.title('Matriz Transformada (Gauss-Jordan)')
        plt.xlabel('Columnas')
        plt.ylabel('Filas')

        for (i, j), val in np.ndenumerate(matriz):
            plt.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        imagen_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return imagen_base64
    except Exception as e:
        return None

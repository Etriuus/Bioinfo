import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TreeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Algoritmos de Árboles")
        self.current_step = 0
        self.steps = []
        self.algorithm_name = ""
        self.matrix = np.array([
            [0, 2, 4, 6],
            [2, 0, 4, 6],
            [4, 4, 0, 6],
            [6, 6, 6, 0]
        ])
        self.distances = self.matrix.copy()
        self.tree_structure = []  # Guardar nodos y relaciones construidas
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        label = tk.Label(self.root, text="Seleccione el tipo de árbol:", font=("Arial", 16))
        label.pack(pady=20)

        btn_ultrametric = tk.Button(self.root, text="Árbol Ultramétrico", command=self.run_ultrametric)
        btn_ultrametric.pack(pady=10, padx=20, fill="x")

        btn_additive = tk.Button(self.root, text="Árbol Aditivo", command=self.run_additive)
        btn_additive.pack(pady=10, padx=20, fill="x")

    def run_ultrametric(self):
        self.algorithm_name = "Árbol Ultramétrico"
        self.steps = [
            "Paso 1: Mostrar la matriz de distancias inicial.",
            "Paso 2: Encontrar el par más cercano.",
            "Paso 3: Actualizar la matriz y construir el árbol.",
            "Paso 4: Graficar el árbol ultramétrico completo."
        ]
        self.tree_structure = []  # Reiniciar estructura del árbol
        self.start_algorithm()

    def run_additive(self):
        self.algorithm_name = "Árbol Aditivo"
        self.steps = [
            "Paso 1: Mostrar la matriz de distancias inicial.",
            "Paso 2: Calcular los nodos intermedios.",
            "Paso 3: Actualizar la matriz y construir el árbol.",
            "Paso 4: Graficar el árbol aditivo completo."
        ]
        self.tree_structure = []  # Reiniciar estructura del árbol
        self.start_algorithm()

    def on_closing():
        plt.close("all")  # Cierra todas las figuras de matplotlib
        root.destroy()  # Cierra la ventana principal de tkinter

    def start_algorithm(self):
        self.clear_window()
        self.current_step = 0

        label_title = tk.Label(self.root, text=f"{self.algorithm_name}", font=("Arial", 16))
        label_title.pack(pady=10)

        self.step_label = tk.Label(self.root, text="", font=("Arial", 12), wraplength=400, justify="left")
        self.step_label.pack(pady=10)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(pady=10)

        btn_next = tk.Button(self.root, text="Siguiente", command=self.next_step)
        btn_next.pack(side="left", padx=20)

        btn_prev = tk.Button(self.root, text="Anterior", command=self.prev_step)
        btn_prev.pack(side="left", padx=20)

        btn_back = tk.Button(self.root, text="Volver", command=self.create_main_menu)
        btn_back.pack(side="right", padx=20)

        self.show_step()

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()

    def show_step(self):
        step_text = self.steps[self.current_step]
        self.step_label.config(text=step_text)
        self.update_plot(step_text)

    def update_plot(self, step_text):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots()
        if "Inicial" in step_text:
            ax.matshow(self.matrix, cmap="coolwarm")
            for (i, j), val in np.ndenumerate(self.matrix):
                ax.text(j, i, f"{val}", ha='center', va='center', color='black')
        elif "más cercano" in step_text:
            mask = np.eye(*self.distances.shape) * np.inf
            closest_pair = np.unravel_index(np.argmin(self.distances + mask), self.distances.shape)
            ax.matshow(self.distances, cmap="coolwarm")
            for (i, j), val in np.ndenumerate(self.distances):
                color = 'red' if (i, j) == closest_pair or (j, i) == closest_pair else 'black'
                ax.text(j, i, f"{val}", ha='center', va='center', color=color)
        elif "nodos intermedios" in step_text:
            # Realizar el cálculo de nodos intermedios para el algoritmo aditivo
            intermediate_values = (self.distances[0, 1] + self.distances[1, 2] - self.distances[0, 2]) / 2
            ax.text(0.5, 0.5, f"Valor intermedio: {intermediate_values:.2f}", fontsize=12, ha='center')
            ax.axis('off')
        elif "Actualizar" in step_text:
            self.tree_structure.append(((0, 1), 2))  # Ejemplo de agregar nodos
            ax.plot([0, 1, 2], [0, 1, 0], marker="o")
            ax.annotate("Nodo A", (0, 0), textcoords="offset points", xytext=(-10, 10), ha='center')
            ax.annotate("Nodo B", (1, 1), textcoords="offset points", xytext=(0, 10), ha='center')
            ax.annotate("Nodo C", (2, 0), textcoords="offset points", xytext=(10, 10), ha='center')
        elif "completo" in step_text:
            self.plot_complete_tree(ax)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()
        plt.close(fig)  # Cierra la figura una vez dibujada


    def plot_complete_tree(self, ax):
        # Gráfico combinado de todos los pasos
        x = [0, 1, 2, 3]
        y = [0, 1, 0, -1]
        ax.plot(x, y, marker="o")
        for i, label in enumerate(["A", "B", "C", "D"]):
            ax.annotate(f"Nodo {label}", (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeVisualizer(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Llamar a la función al cerrar
    root.mainloop()
    

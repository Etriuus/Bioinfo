import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import numpy as np
from itertools import combinations
from matplotlib.animation import FuncAnimation

# Definiciones de todas las funciones
def is_vertex_cover(graph, subset):
    for u, v in graph.edges():
        if u not in subset and v not in subset:
            return False
    return True

def brute_force_vertex_cover(graph):
    nodes = list(graph.nodes())
    for k in range(1, len(nodes) + 1):
        for subset in combinations(nodes, k):
            if is_vertex_cover(graph, subset):
                return subset
    return None

def greedy_vertex_cover(graph):
    cover = set()
    edges = set(graph.edges())
    while edges:
        degrees = {node: len(list(graph.neighbors(node))) for node in graph.nodes}
        max_degree_node = max(degrees, key=degrees.get)
        cover.add(max_degree_node)
        for neighbor in list(graph.neighbors(max_degree_node)):
            edges.discard((max_degree_node, neighbor))
            edges.discard((neighbor, max_degree_node))
        graph.remove_node(max_degree_node)
    return cover

def visualizar_progreso(realidad, deseo, paso):
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(realidad)), realidad, color='lightblue', label='Realidad')
    plt.plot(range(len(deseo)), deseo, color='orange', marker='o', linestyle='-', label='Deseo')
    plt.title(f"Paso {paso}: Reordenamiento de la Secuencia")
    plt.xlabel("Índice")
    plt.ylabel("Valor")
    plt.legend()
    plt.show()

def bubble_sort_visual(realidad, deseo):
    n = len(realidad)
    pasos = 0
    for i in range(n):
        for j in range(0, n-i-1):
            if realidad[j] > realidad[j+1]:
                realidad[j], realidad[j+1] = realidad[j+1], realidad[j]
                pasos += 1
        visualizar_progreso(realidad, deseo, pasos)
    return realidad

def visualizar_circular(realidad, deseo, paso):
    n = len(realidad)
    angulos = np.linspace(0, 2 * np.pi, n, endpoint=False)
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)
    ax.scatter(angulos, deseo, color="orange", label="Deseo", s=100, alpha=0.7)
    ax.scatter(angulos, realidad, color="blue", label="Realidad", s=100)
    for i in range(n):
        ax.plot([angulos[i], angulos[i]], [realidad[i], deseo[i]], 
                color="gray", linestyle="--", alpha=0.5)
    plt.title(f"Paso {paso}: Estado de la Secuencia", va="bottom")
    ax.legend(loc="upper right")
    plt.show()

def bubble_sort_circular(realidad, deseo):
    n = len(realidad)
    pasos = 0
    for i in range(n):
        for j in range(0, n-i-1):
            if realidad[j] > realidad[j+1]:
                realidad[j], realidad[j+1] = realidad[j+1], realidad[j]
                pasos += 1
                visualizar_circular(realidad, deseo, pasos)
    return realidad

class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Algoritmos")
        
        # Asegurarse que la ventana tenga un tamaño mínimo
        self.root.minsize(400, 300)
        
        # Frame principal con padding
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Selector de algoritmo
        frame_selector = ttk.Frame(self.main_frame)
        frame_selector.pack(fill='x', pady=(0, 10))
        
        ttk.Label(frame_selector, text="Seleccione el algoritmo:").pack(side='left')
        self.algorithm_type = ttk.Combobox(frame_selector, 
                                         values=["PPI Network", 
                                                "Vertex Cover - Brute Force",
                                                "Vertex Cover - Greedy",
                                                "Ordenamiento - Visualización Normal",
                                                "Ordenamiento - Visualización Circular"],
                                         state='readonly',  # Importante: previene entrada manual
                                         width=30)
        self.algorithm_type.pack(side='left', padx=(10, 0))
        self.algorithm_type.set("PPI Network")
        
        # Frame para parámetros
        self.params_frame = ttk.LabelFrame(self.main_frame, text="Parámetros")
        self.params_frame.pack(fill='x', pady=10, padx=5)
        
        # Botón para ejecutar
        self.run_button = ttk.Button(self.main_frame, 
                                   text="Ejecutar", 
                                   command=self.run_algorithm)
        self.run_button.pack(pady=10)
        
        # Inicializar parámetros
        self.setup_ppi_params()
        
        # Vincular cambio de algoritmo
        self.algorithm_type.bind('<<ComboboxSelected>>', self.update_params)
    
    def setup_ppi_params(self):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
            
        frame = ttk.Frame(self.params_frame)
        frame.pack(padx=10, pady=5)
        
        self.num_nodes = tk.StringVar(value="5")
        ttk.Label(frame, text="Número de nodos:").pack(side='left')
        ttk.Entry(frame, textvariable=self.num_nodes, width=10).pack(side='left', padx=(10, 0))

    def setup_vertex_cover_params(self):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
            
        frame = ttk.Frame(self.params_frame)
        frame.pack(padx=10, pady=5)
        
        self.nodes_input = tk.StringVar()
        self.edges_input = tk.StringVar()
        
        ttk.Label(frame, text="Nodos (separados por comas):").pack(anchor="w", pady=2)
        ttk.Entry(frame, textvariable=self.nodes_input, width=30).pack(anchor="w", pady=2)
        
        ttk.Label(frame, text="Aristas (pares separados por punto y coma, ej. 'u,v; x,y'):").pack(anchor="w", pady=2)
        ttk.Entry(frame, textvariable=self.edges_input, width=50).pack(anchor="w", pady=2)

    def setup_sorting_params(self):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
            
        frame = ttk.Frame(self.params_frame)
        frame.pack(padx=10, pady=5)
        
        self.sequence_length = tk.StringVar(value="8")
        ttk.Label(frame, text="Longitud de la secuencia:").pack(side='left')
        ttk.Entry(frame, textvariable=self.sequence_length, width=10).pack(side='left', padx=(10, 0))

    def update_params(self, event=None):
        # Limpiar frame de parámetros
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        algorithm = self.algorithm_type.get()
        if "PPI Network" in algorithm:
            self.setup_ppi_params()
        elif "Vertex Cover" in algorithm:
            self.setup_vertex_cover_params()
        else:
            self.setup_sorting_params()
    
    def run_algorithm(self):
        algorithm = self.algorithm_type.get()
        
        if "PPI Network" in algorithm:
            # Crear y mostrar grafo PPI
            ppi_graph = nx.Graph()
            n = int(self.num_nodes.get())
            nodes = [f"P{i}" for i in range(1, n+1)]
            ppi_graph.add_nodes_from(nodes)
            # Agregar algunas aristas aleatorias
            for i in range(n-1):
                ppi_graph.add_edge(nodes[i], nodes[i+1])
            nx.draw(ppi_graph, with_labels=True, node_color="lightblue", edge_color="gray")
            plt.show()
            
        elif "Vertex Cover - Brute Force" in algorithm:
            G = nx.Graph()
            nodes = self.nodes_input.get().split(',')
            edges = [tuple(edge.split(',')) for edge in self.edges_input.get().split(';')]
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            cover = brute_force_vertex_cover(G)
            print(f"Vertex Cover (Brute Force): {cover}")
            nx.draw(G, with_labels=True)
            plt.show()
            
        elif "Vertex Cover - Greedy" in algorithm:
            G = nx.Graph()
            nodes = self.nodes_input.get().split(',')
            edges = [tuple(edge.split(',')) for edge in self.edges_input.get().split(';')]
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            cover = greedy_vertex_cover(G.copy())
            print(f"Vertex Cover (Greedy): {cover}")
            nx.draw(G, with_labels=True)
            plt.show()
            
        elif "Ordenamiento - Visualización Normal" in algorithm:
            n = int(self.sequence_length.get())
            realidad = list(np.random.permutation(n) + 1)
            deseo = sorted(realidad)
            bubble_sort_visual(realidad.copy(), deseo)
            
        else:  # Ordenamiento Circular
            n = int(self.sequence_length.get())
            realidad = list(np.random.permutation(n) + 1)
            deseo = sorted(realidad)
            bubble_sort_circular(realidad.copy(), deseo)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = GraphVisualizer(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}")
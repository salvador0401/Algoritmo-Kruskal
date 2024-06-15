##________  ___  ___  ________  ___      ___ ________     
##|\   ____\|\  \|\  \|\   __  \|\  \    /  /|\   __  \    
##\ \  \___|\ \  \\\  \ \  \|\  \ \  \  /  / | \  \|\  \   
## \ \  \    \ \   __  \ \   __  \ \  \/  / / \ \   __  \  
##  \ \  \____\ \  \ \  \ \  \ \  \ \    / /   \ \  \ \  \ 
##   \ \_______\ \__\ \__\ \__\ \__\ \__/ /     \ \__\ \__\
##    \|_______|\|__|\|__|\|__|\|__|\|__|/       \|__|\|__|
##21310195 Meza Morales Salvador Emmanuel
import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class DisjointSet:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

class Graph:
    def __init__(self):
        self.edges = []
        self.vertices = set()

    def add_edge(self, u, v, weight):
        self.edges.append((weight, u, v))
        self.vertices.add(u)
        self.vertices.add(v)

    def kruskal_min(self):
        self.edges.sort()
        disjoint_set = DisjointSet(self.vertices)
        mst = []
        total_cost = 0
        steps = []
        for weight, u, v in self.edges:
            if disjoint_set.find(u) != disjoint_set.find(v):
                disjoint_set.union(u, v)
                mst.append((weight, u, v))
                total_cost += weight
                steps.append(list(mst))
        return mst, total_cost, steps

    def kruskal_max(self):
        self.edges.sort(reverse=True)
        disjoint_set = DisjointSet(self.vertices)
        mst = []
        total_cost = 0
        steps = []
        for weight, u, v in self.edges:
            if disjoint_set.find(u) != disjoint_set.find(v):
                disjoint_set.union(u, v)
                mst.append((weight, u, v))
                total_cost += weight
                steps.append(list(mst))
        return mst, total_cost, steps

class KruskalApp:
    def __init__(self, root):
        self.root = root
        self.graph = Graph()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Algoritmo de Kruskal - AEM Mínimo y Máximo")
        self.root.geometry("600x500")

        self.algo_label = ttk.Label(self.root, text="Seleccione el algoritmo:")
        self.algo_label.pack(pady=5)
        self.algo_combobox = ttk.Combobox(self.root, values=["Kruskal Mínimo", "Kruskal Máximo"])
        self.algo_combobox.pack(pady=5)
        self.algo_combobox.current(0)

        self.edge_frame = ttk.Frame(self.root)
        self.edge_frame.pack(pady=5)

        self.u_label = ttk.Label(self.edge_frame, text="Vértice U:")
        self.u_label.grid(row=0, column=0, padx=5, pady=5)
        self.u_entry = ttk.Entry(self.edge_frame)
        self.u_entry.grid(row=0, column=1, padx=5, pady=5)

        self.v_label = ttk.Label(self.edge_frame, text="Vértice V:")
        self.v_label.grid(row=1, column=0, padx=5, pady=5)
        self.v_entry = ttk.Entry(self.edge_frame)
        self.v_entry.grid(row=1, column=1, padx=5, pady=5)

        self.weight_label = ttk.Label(self.edge_frame, text="Peso:")
        self.weight_label.grid(row=2, column=0, padx=5, pady=5)
        self.weight_entry = ttk.Entry(self.edge_frame)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_edge_button = ttk.Button(self.edge_frame, text="Agregar Arista", command=self.add_edge)
        self.add_edge_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.show_edges_button = ttk.Button(self.root, text="Mostrar Aristas Guardadas", command=self.show_edges)
        self.show_edges_button.pack(pady=5)

        self.solve_button = ttk.Button(self.root, text="Resolver", command=self.solve)
        self.solve_button.pack(pady=5)

        self.credits_button = ttk.Button(self.root, text="Créditos", command=self.show_credits)
        self.credits_button.pack(pady=5)

        self.result_text = tk.Text(self.root, height=10)
        self.result_text.pack(pady=5)

    def add_edge(self):
        u = self.u_entry.get()
        v = self.v_entry.get()
        try:
            weight = int(self.weight_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número entero.")
            return
        self.graph.add_edge(u, v, weight)
        messagebox.showinfo("Información", f"Arista {u}-{v} con peso {weight} agregada.")

    def show_edges(self):
        edges_text = "Aristas guardadas:\n"
        for weight, u, v in self.graph.edges:
            edges_text += f"{u} - {v} con peso {weight}\n"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, edges_text)

    def solve(self):
        algorithm = self.algo_combobox.get()
        if algorithm == "Kruskal Mínimo":
            mst, total_cost, steps = self.graph.kruskal_min()
        else:
            mst, total_cost, steps = self.graph.kruskal_max()
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Árbol de Expansión con costo total: {total_cost}\n")
        self.result_text.insert(tk.END, "Aristas:\n")
        for weight, u, v in mst:
            self.result_text.insert(tk.END, f"{u} - {v} con peso {weight}\n")

        self.show_graph(initial=True)
        self.show_steps(steps, algorithm)

    def show_graph(self, initial=True, mst=None):
        G = nx.Graph()
        for weight, u, v in self.graph.edges:
            G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 7))
        if initial:
            title = "Grafo Inicial"
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        else:
            title = "Árbol de Expansión Mínima/Máxima"
            mst_edges = [(u, v) for weight, u, v in mst]
            mst_graph = nx.Graph()
            for weight, u, v in mst:
                mst_graph.add_edge(u, v, weight=weight)
            nx.draw(mst_graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(mst_graph, 'weight')
            nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=labels)
            
        plt.title(title)
        plt.show()

    def show_steps(self, steps, algorithm):
        G = nx.Graph()
        for weight, u, v in self.graph.edges:
            G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G)

        for i, step in enumerate(steps):
            plt.figure(figsize=(10, 7))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            
            mst_edges = [(u, v) for weight, u, v in step]
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2.0)
            plt.title(f"Paso {i + 1} - Algoritmo: {algorithm}")
            plt.show()

    def show_credits(self):
        credits = tk.Toplevel(self.root)
        credits.title("Créditos")
        credits.geometry("400x200")
        tk.Label(credits, text="Salvador Emmanuel Meza Morales", font=("Helvetica", 16, "bold")).pack(pady=20)
        tk.Label(credits, text="21310195", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(credits, text="Cerrar", command=credits.destroy).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = KruskalApp(root)
    root.mainloop()

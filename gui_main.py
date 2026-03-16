# gui.py
import tkinter as tk
from tkinter import ttk
from tabs.vector_tab import create_vector_tab # Import the separate interface
from tabs.matrix_tab import create_matrix_tab

root = tk.Tk()
root.title("Universal Math App")
root.geometry("700x500")

# --- Global Styles ---
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", font=("Segoe UI", 12, "bold"), padding=[10, 6])
style.configure("TLabel", font=("Segoe UI", 13))
style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=6)
style.configure("TEntry", font=("Consolas", 12))

# --- Notebook Tabs ---
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Home tab
tab_home = ttk.Frame(notebook, padding=20)
notebook.add(tab_home, text="Home")
ttk.Label(tab_home, text="Universal Math App", font=("Segoe UI", 20, "bold")).pack(pady=20)
ttk.Label(tab_home, text="Choose a math module from the tabs above.", font=("Segoe UI", 13)).pack(pady=10)

# Vector tab (imported)
create_vector_tab(notebook)

# Matrix tab
matrix_tab_frame = create_matrix_tab(notebook)
notebook.add(matrix_tab_frame, text="Matrices")

# Statistics placeholder (if you want to keep it)
stats_tab = ttk.Frame(notebook, padding=20)
notebook.add(stats_tab, text="Statistics")
ttk.Label(stats_tab, text="Statistics tools coming soon!", font=("Segoe UI", 14, "italic")).pack(pady=20)

root.mainloop()

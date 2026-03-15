# tabs/vector_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from modules.vector_module import dot_product, cross_product


def create_vector_tab(notebook):
    """Creates and adds the 'Vectors' tab to the given notebook."""
    tab = ttk.Frame(notebook, padding=20)
    notebook.add(tab, text="Vectors")

    header = ttk.Label(tab, text="Vector Operations (3D)", font=("Segoe UI", 16, "bold"))
    header.pack(pady=10)

    # --- Vector A ---
    frame_a = ttk.Frame(tab)
    frame_a.pack(pady=5)
    ttk.Label(frame_a, text="Vector A:").grid(row=0, column=0, padx=10)
    entry_a1 = ttk.Entry(frame_a, width=6); entry_a1.grid(row=0, column=1)
    entry_a2 = ttk.Entry(frame_a, width=6); entry_a2.grid(row=0, column=2)
    entry_a3 = ttk.Entry(frame_a, width=6); entry_a3.grid(row=0, column=3)

    # --- Vector B ---
    frame_b = ttk.Frame(tab)
    frame_b.pack(pady=5)
    ttk.Label(frame_b, text="Vector B:").grid(row=0, column=0, padx=10)
    entry_b1 = ttk.Entry(frame_b, width=6); entry_b1.grid(row=0, column=1)
    entry_b2 = ttk.Entry(frame_b, width=6); entry_b2.grid(row=0, column=2)
    entry_b3 = ttk.Entry(frame_b, width=6); entry_b3.grid(row=0, column=3)

    # --- Keyboard navigation between entry boxes ---
    entries_a = [entry_a1, entry_a2, entry_a3]
    entries_b = [entry_b1, entry_b2, entry_b3]
    entries = entries_a + entries_b  # combined list

    def focus_next(event):
        current = event.widget
        try:
            idx = entries.index(current)
            entries[(idx + 1) % len(entries)].focus_set()
        except ValueError:
            pass

    def focus_previous(event):
        current = event.widget
        try:
            idx = entries.index(current)
            entries[(idx - 1) % len(entries)].focus_set()
        except ValueError:
            pass

    def focus_down(event):
        """Move from A→B (same column)."""
        if event.widget in entries_a:
            idx = entries_a.index(event.widget)
            entries_b[idx].focus_set()

    def focus_up(event):
        """Move from B→A (same column)."""
        if event.widget in entries_b:
            idx = entries_b.index(event.widget)
            entries_a[idx].focus_set()

    def select_all(event):
        event.widget.select_range(0, 'end')
        return 'break'

    # --- Bind all entries ---
    for e in entries:
        e.bind("<Return>", focus_next)
        e.bind("<Right>", focus_next)
        e.bind("<Left>", focus_previous)
        e.bind("<Down>", focus_down)
        e.bind("<Up>", focus_up)
        e.bind("<FocusIn>", select_all)

    # --- Helper function to read vectors ---
    def get_vectors():
        try:
            A = [float(e.get()) for e in entries_a]
            B = [float(e.get()) for e in entries_b]
            return A, B
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all components.")
            return None, None

    # --- Button callbacks ---
    def calculate_dot():
        A, B = get_vectors()
        if A and B:
            result = dot_product(A, B)
            label_result.config(text=f"Dot Product: {result}")

    def calculate_cross():
       A, B = get_vectors()
       if A and B:
        try:
            result = cross_product(A, B)
            label_result.config(
                text="Cross Product:\n" + "\n".join(str(x) for x in result)
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    # --- Buttons & Output ---
    btn_frame = ttk.Frame(tab)
    btn_frame.pack(pady=15)
    ttk.Button(btn_frame, text="Dot Product", command=calculate_dot).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Cross Product", command=calculate_cross).grid(row=0, column=1, padx=10)

    label_result = ttk.Label(tab, text="Result will appear here.", font=("Segoe UI", 13, "bold"))
    label_result.pack(pady=20)

    return tab

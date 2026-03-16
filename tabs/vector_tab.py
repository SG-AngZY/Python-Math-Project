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
            vector_label.config(text=f"Dot Product: {result}")

    def calculate_cross():
       A, B = get_vectors()
       if A and B:
        try:
            result = cross_product(A, B)
            vector_label.config(text="\n".join(f"{x:7.1f}" for x in result))

        except ValueError as e:
            messagebox.showerror("Error", str(e))


    # --- Buttons & Output ---
    btn_frame = ttk.Frame(tab)
    btn_frame.pack(pady=15)
    ttk.Button(btn_frame, text="Dot Product", command=calculate_dot).grid(row=0, column=0, padx=10)
    ttk.Button(btn_frame, text="Cross Product", command=calculate_cross).grid(row=0, column=1, padx=10)

   # --- Canvas-drawn brackets + result label ---
    bracket_frame = ttk.Frame(tab)
    bracket_frame.pack(pady=20)

    CANVAS_W, CANVAS_H = 20, 80   # bracket canvas size
    SERIF = 6                      # horizontal foot length
    FG = "#000000"

    left_canvas = tk.Canvas(bracket_frame, width=CANVAS_W, height=CANVAS_H,
                            highlightthickness=0, bg="#d9d9d9")
    left_canvas.grid(row=0, column=0, sticky="ns")

    right_canvas = tk.Canvas(bracket_frame, width=CANVAS_W, height=CANVAS_H,
                             highlightthickness=0, bg="#d9d9d9")
    right_canvas.grid(row=0, column=2, sticky="ns")

    def draw_brackets():
        """Redraw both brackets to match the current canvas height."""
        for canvas, facing in [(left_canvas, "right"), (right_canvas, "left")]:
            canvas.delete("all")
            w = int(canvas["width"])
            h = int(canvas["height"])
            x_line = w - 4 if facing == "left" else 4
            x_foot = 4      if facing == "left" else w - 4

            # Vertical bar
            canvas.create_line(x_line, 4, x_line, h - 4, width=2, fill=FG)
            # Top foot
            canvas.create_line(x_line, 4, x_foot, 4, width=2, fill=FG)
            # Bottom foot
            canvas.create_line(x_line, h - 4, x_foot, h - 4, width=2, fill=FG)

    draw_brackets()

    vector_label = ttk.Label(bracket_frame, text="Result will\nappear here.",
                             font=("Courier New", 13, "bold"), justify="center")
    vector_label.grid(row=0, column=1, padx=6, sticky="ns")

    def sync_bracket_height(event=None):
        """Resize canvases to match the label height after geometry settles."""
        bracket_frame.update_idletasks()
        h = max(vector_label.winfo_height(), 60)
        for canvas in (left_canvas, right_canvas):
            canvas.config(height=h)
        draw_brackets()

    vector_label.bind("<Configure>", sync_bracket_height)
    
    return tab

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class MatrixTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ttk.Label(self, text="Matrix Calculator", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Step 1: Ask for sizes
        self.size_frame = ttk.Frame(self)
        self.size_frame.pack(pady=10)

        ttk.Label(self.size_frame, text="Matrix A size (rows x cols):").grid(row=0, column=0, padx=5, pady=5)
        self.matrix_a_size = ttk.Entry(self.size_frame, width=7)
        self.matrix_a_size.grid(row=0, column=1, padx=5)

        ttk.Label(self.size_frame, text="Matrix B size (rows x cols):").grid(row=1, column=0, padx=5, pady=5)
        self.matrix_b_size = ttk.Entry(self.size_frame, width=7)
        self.matrix_b_size.grid(row=1, column=1, padx=5)

        self.submit_size_btn = ttk.Button(self.size_frame, text="Set Sizes", command=self.set_matrix_sizes)
        self.submit_size_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Container for the matrix grids
        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack(pady=10)

        # Frames for each matrix
        self.matrix_a_frame = None
        self.matrix_b_frame = None

        self.multiply_btn = None
        self.result_label = None

        self.matrix_a_entries = []
        self.matrix_b_entries = []

    # Step 2: After size input
    def set_matrix_sizes(self):
        size_a = self.matrix_a_size.get()
        size_b = self.matrix_b_size.get()

        try:
            rows_a, cols_a = map(int, size_a.lower().split('x'))
            rows_b, cols_b = map(int, size_b.lower().split('x'))
        except:
            messagebox.showerror("Error", "Invalid size format. Use e.g. 2x3")
            return

        if cols_a != rows_b:
            messagebox.showerror("Error", "Matrix A columns must equal Matrix B rows")
            return

        if not (1 <= rows_a <= 10 and 1 <= cols_a <= 10 and 1 <= cols_b <= 10):
            messagebox.showerror("Error", "Matrix sizes must be between 1 and 10")
            return

        # Hide the size input frame
        self.size_frame.pack_forget()

        # Create matrix entry grids
        self.create_matrix_entries(rows_a, cols_a, rows_b, cols_b)

    def create_matrix_entries(self, rows_a, cols_a, rows_b, cols_b):
        # Clear previous frames
        for widget in self.entries_frame.winfo_children():
            widget.destroy()

        # --- Matrix A Frame ---
        self.matrix_a_frame = tk.Frame(self.entries_frame, bg="#d3d3d3", padx=10, pady=10, bd=2, relief="ridge")
        self.matrix_a_frame.grid(row=0, column=0, padx=20)

        ttk.Label(self.matrix_a_frame, text="Matrix A", background="#d3d3d3", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=cols_a, pady=5)

        self.matrix_a_entries = []
        for r in range(rows_a):
            row_entries = []
            for c in range(cols_a):
                e = tk.Entry(self.matrix_a_frame, width=5, justify='center')
                e.grid(row=r+1, column=c, padx=2, pady=2)

                e.bind("<Up>", lambda event, r=r, c=c: self.move_focus(self.matrix_a_entries, r, c, "up"))
                e.bind("<Down>", lambda event, r=r, c=c: self.move_focus(self.matrix_a_entries, r, c, "down"))
                e.bind("<Left>", lambda event, r=r, c=c: self.move_focus(self.matrix_a_entries, r, c, "left"))
                e.bind("<Right>", lambda event, r=r, c=c: self.move_focus(self.matrix_a_entries, r, c, "right"))
                row_entries.append(e)
            self.matrix_a_entries.append(row_entries)

        # --- Matrix B Frame ---
        self.matrix_b_frame = tk.Frame(self.entries_frame, bg="#d3d3d3", padx=10, pady=10, bd=2, relief="ridge")
        self.matrix_b_frame.grid(row=0, column=1, padx=20)

        ttk.Label(self.matrix_b_frame, text="Matrix B", background="#d3d3d3", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=cols_b, pady=5)

        self.matrix_b_entries = []
        for r in range(rows_b):
            row_entries = []
            for c in range(cols_b):
                e = tk.Entry(self.matrix_b_frame, width=5, justify='center')
                e.grid(row=r+1, column=c, padx=2, pady=2)

                e.bind("<Up>", lambda event, r=r, c=c: self.move_focus(self.matrix_b_entries, r, c, "up"))
                e.bind("<Down>", lambda event, r=r, c=c: self.move_focus(self.matrix_b_entries, r, c, "down"))
                e.bind("<Left>", lambda event, r=r, c=c: self.move_focus(self.matrix_b_entries, r, c, "left"))
                e.bind("<Right>", lambda event, r=r, c=c: self.move_focus(self.matrix_b_entries, r, c, "right"))
                row_entries.append(e)
            self.matrix_b_entries.append(row_entries)

        # Multiply button
        self.multiply_btn = ttk.Button(self.entries_frame, text="Multiply Matrices", command=self.multiply_matrices)
        self.multiply_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Result label
        self.result_label = ttk.Label(self.entries_frame, text="", font=("Consolas", 12))
        self.result_label.grid(row=2, column=0, columnspan=2, pady=5)

    def multiply_matrices(self):
        try:
            mat_a = [[float(e.get()) for e in row] for row in self.matrix_a_entries]
            mat_b = [[float(e.get()) for e in row] for row in self.matrix_b_entries]
            result = np.matmul(mat_a, mat_b)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid matrix values.\n{e}")
            return

        # Display result in a simple grid
        result_text = "\n".join(["\t".join(map(str, row)) for row in result])
        self.result_label.config(text=result_text)

    def move_focus(self, entries: list[list[tk.Entry]], r: int, c: int, direction: str):
        rows = len(entries)
        cols = len(entries[0])

        if direction == "right":
           if c < cols - 1:
            entries[r][c + 1].focus_set()
           else:  # move to next row
              if r < rows - 1:
                entries[r + 1][0].focus_set()
              else:  # wrap to first cell
                entries[0][0].focus_set()

        elif direction == "left":
           if c > 0:
            entries[r][c - 1].focus_set()
           else:
              if r > 0:
                entries[r - 1][cols - 1].focus_set()
              else:
                entries[rows - 1][cols - 1].focus_set()

        elif direction == "down":
           if r < rows - 1:
            entries[r + 1][c].focus_set()
           else:
            entries[0][c].focus_set()

        elif direction == "up":
           if r > 0:
            entries[r - 1][c].focus_set()
           else:
            entries[rows - 1][c].focus_set()
# Factory function
def create_matrix_tab(parent):
    return MatrixTab(parent)
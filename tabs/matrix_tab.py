import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class MatrixTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ttk.Label(self, text="Matrix Calculator", font=("Segoe UI", 16, "bold")).pack(pady=10)

        # --- Step 1: Set Dimensions ---
        self.size_frame = ttk.LabelFrame(self, text="Step 1: Set Dimensions")
        self.size_frame.pack(pady=10, padx=20, fill="x")

        # Headers
        ttk.Label(self.size_frame, text="Rows", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=5)
        ttk.Label(self.size_frame, text="Cols", font=("Segoe UI", 10, "bold")).grid(row=0, column=3, padx=5)

        # Matrix A 
        ttk.Label(self.size_frame, text="Matrix A:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.matrix_a_rows = ttk.Entry(self.size_frame, width=5, justify="center")
        self.matrix_a_rows.grid(row=1, column=1, pady=5)
        ttk.Label(self.size_frame, text="x").grid(row=1, column=2)
        self.matrix_a_cols = ttk.Entry(self.size_frame, width=5, justify="center")
        self.matrix_a_cols.grid(row=1, column=3, pady=5)

        # Matrix B
        ttk.Label(self.size_frame, text="Matrix B:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.matrix_b_rows = ttk.Entry(self.size_frame, width=5, justify="center")
        self.matrix_b_rows.grid(row=2, column=1, pady=5)
        ttk.Label(self.size_frame, text="x").grid(row=2, column=2)
        self.matrix_b_cols = ttk.Entry(self.size_frame, width=5, justify="center")
        self.matrix_b_cols.grid(row=2, column=3, pady=5)

        # Generate Button
        self.submit_size_btn = ttk.Button(self.size_frame, text="Generate Grids", command=self.set_matrix_sizes)
        self.submit_size_btn.grid(row=3, column=0, columnspan=4, pady=10)

        # Map them for easy navigation
        self.size_inputs = [
            [self.matrix_a_rows, self.matrix_a_cols],
            [self.matrix_b_rows, self.matrix_b_cols]
        ]

        # Bind the keys to all 4 boxes
        for r in range(2):
            for c in range(2):
                widget = self.size_inputs[r][c]
                widget.bind("<Up>", lambda e, r=r, c=c: self.move_size_focus(r, c, "up"))
                widget.bind("<Down>", lambda e, r=r, c=c: self.move_size_focus(r, c, "down"))
                widget.bind("<Left>", lambda e, r=r, c=c: self.move_size_focus(r, c, "left"))
                widget.bind("<Right>", lambda e, r=r, c=c: self.move_size_focus(r, c, "right"))
        
        # --- Step 2: Entries Frame ---
        self.entries_frame = ttk.Frame(self)
        self.matrix_a_entries = []
        self.matrix_b_entries = []

    # --- Methods (Correct Indentation Level) ---

    def move_size_focus(self, r, c, direction):
        # r: 0 (Matrix A), 1 (Matrix B)
        # c: 0 (Rows), 1 (Cols)
        
        if direction == "right":
            if c < 1: # Move from Row to Col
                self.size_inputs[r][c+1].focus_set()
            elif r < 1: # Move from Matrix A Col to Matrix B Row
                self.size_inputs[r+1][0].focus_set()
            else: # Wrap around: From Matrix B Col back to Matrix A Row
                self.size_inputs[0][0].focus_set()
                
        elif direction == "left":
            if c > 0: # Move from Col to Row
                self.size_inputs[r][c-1].focus_set()
            elif r > 0: # Move from Matrix B Row to Matrix A Col
                self.size_inputs[r-1][1].focus_set()
            else: # Wrap around: From Matrix A Row back to Matrix B Col
                self.size_inputs[1][1].focus_set()
                
        elif direction == "down":
            if r < 1: # Move from Matrix A to Matrix B
                self.size_inputs[r+1][c].focus_set()
            else: # Wrap around: From Matrix B back to Matrix A
                self.size_inputs[0][c].focus_set()
                
        elif direction == "up":
            if r > 0: # Move from Matrix B to Matrix A
                self.size_inputs[r-1][c].focus_set()
            else: # Wrap around: From Matrix A back to Matrix B
                self.size_inputs[1][c].focus_set()
    def set_matrix_sizes(self):
        try:
            ra = int(self.matrix_a_rows.get())
            ca = int(self.matrix_a_cols.get())
            rb = int(self.matrix_b_rows.get())
            cb = int(self.matrix_b_cols.get())

            if ca != rb:
                raise ValueError("Inner dimensions must match (A cols = B rows).")

            self.size_frame.pack_forget()
            self.entries_frame.pack(pady=10, fill="both", expand=True)
            self.create_matrix_entries(ra, ca, rb, cb)
        except ValueError as e:
            messagebox.showerror("Size Error", "Please enter valid integers. A-Cols must equal B-Rows.")

    def create_matrix_entries(self, ra, ca, rb, cb):
        for widget in self.entries_frame.winfo_children():
            widget.destroy()

        grid_cont = ttk.Frame(self.entries_frame)
        grid_cont.pack()

        # Matrix A
        frame_a = ttk.LabelFrame(grid_cont, text="Matrix A")
        frame_a.grid(row=0, column=0, padx=10)
        self.matrix_a_entries = [[self.make_entry(frame_a, r, c, "A") for c in range(ca)] for r in range(ra)]

        ttk.Label(grid_cont, text="×", font=("Arial", 20)).grid(row=0, column=1)

        # Matrix B
        frame_b = ttk.LabelFrame(grid_cont, text="Matrix B")
        frame_b.grid(row=0, column=2, padx=10)
        self.matrix_b_entries = [[self.make_entry(frame_b, r, c, "B") for c in range(cb)] for r in range(rb)]

        # Controls
        btn_frame = ttk.Frame(self.entries_frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="← Change Sizes", command=self.reset_view).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Calculate A × B", command=self.multiply_matrices).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_entries).pack(side="left", padx=5)

        # --- Result Display ---
        self.bracket_frame = tk.Frame(self.entries_frame, bg="#d9d9d9")
        self.left_canvas = tk.Canvas(self.bracket_frame, width=20, height=80, highlightthickness=0, bg="#d9d9d9")
        self.left_canvas.grid(row=0, column=0, sticky="ns")

        self.res_display = tk.Label(self.bracket_frame, text="", font=("Courier New", 13, "bold"), bg="#d9d9d9", justify="center")
        self.res_display.grid(row=0, column=1, padx=6, sticky="ns")

        self.right_canvas = tk.Canvas(self.bracket_frame, width=20, height=80, highlightthickness=0, bg="#d9d9d9")
        self.right_canvas.grid(row=0, column=2, sticky="ns")

        self.res_display.bind("<Configure>", self.sync_bracket_height)

    def draw_brackets(self):
        for canvas, facing in [(self.left_canvas, "right"), (self.right_canvas, "left")]:
            canvas.delete("all")
            w, h = int(canvas["width"]), int(canvas["height"])
            x_line = w - 4 if facing == "left" else 4
            x_foot = 4 if facing == "left" else w - 4
            canvas.create_line(x_line, 4, x_line, h - 4, width=2, fill="#000000")
            canvas.create_line(x_line, 4, x_foot, 4, width=2, fill="#000000")
            canvas.create_line(x_line, h - 4, x_foot, h - 4, width=2, fill="#000000")

    def sync_bracket_height(self, event=None):
        self.bracket_frame.update_idletasks()
        h = max(self.res_display.winfo_height(), 40)
        self.left_canvas.config(height=h)
        self.right_canvas.config(height=h)
        self.draw_brackets()

    def make_entry(self, parent, r, c, matrix_id):
        e = ttk.Entry(parent, width=5, justify="center")
        e.grid(row=r, column=c, padx=2, pady=2)
        e.bind("<Up>", lambda event: self.move_focus(matrix_id, r, c, "up"))
        e.bind("<Down>", lambda event: self.move_focus(matrix_id, r, c, "down"))
        e.bind("<Left>", lambda event: self.move_focus(matrix_id, r, c, "left"))
        e.bind("<Right>", lambda event: self.move_focus(matrix_id, r, c, "right"))
        return e

    def move_focus(self, m_id, r, c, direction):
        entries = self.matrix_a_entries if m_id == "A" else self.matrix_b_entries
        rows, cols = len(entries), len(entries[0])
        
        if direction == "right":
            if c < cols - 1: # Move to next cell in row
                entries[r][c + 1].focus_set()
            elif r < rows - 1: # End of row? Move to start of NEXT row
                entries[r + 1][0].focus_set()
            else: # End of matrix? Wrap to the very first cell [0][0]
                entries[0][0].focus_set()
                
        elif direction == "left":
            if c > 0: # Move to previous cell in row
                entries[r][c - 1].focus_set()
            elif r > 0: # Start of row? Move to end of PREVIOUS row
                entries[r - 1][cols - 1].focus_set()
            else: # Start of matrix? Wrap to the very last cell
                entries[rows - 1][cols - 1].focus_set()
                
        elif direction == "down":
            # Wraps vertically within the same column
            entries[(r + 1) % rows][c].focus_set()
            
        elif direction == "up":
            # Wraps vertically within the same column
            entries[(r - 1) % rows][c].focus_set()

        # Optional: Auto-select text so you can just type over the old value
        target = self.focus_get()
        if isinstance(target, ttk.Entry):
            target.selection_range(0, tk.END)

    def multiply_matrices(self):
        try:
            a = np.array([[float(e.get() if e.get().strip() else 0) for e in row] for row in self.matrix_a_entries])
            b = np.array([[float(e.get() if e.get().strip() else 0) for e in row] for row in self.matrix_b_entries])
            res = np.matmul(a, b)
            formatted = "\n".join(["  ".join([f"{val:g}" for val in row]) for row in res])
            self.res_display.config(text=formatted)
            self.bracket_frame.pack(pady=20)
        except Exception:
            self.bracket_frame.pack_forget()
            messagebox.showerror("Error", "Check inputs.")

    def reset_view(self):
        self.entries_frame.pack_forget()
        self.bracket_frame.pack_forget()

        if hasattr(self, 'size_inputs'):
            for row in self.size_inputs:
                for entry in row:
                    entry.delete(0, tk.END)

        self.size_frame.pack(pady=10, padx=20, fill="x")
        self.matrix_a_rows.focus_set()

    def clear_entries(self):
        """Wipe all numbers from both matrices and hide the result."""
        # Clear Matrix A entries
        for row in self.matrix_a_entries:
            for entry in row:
                entry.delete(0, tk.END)
        
        # Clear Matrix B entries
        for row in self.matrix_b_entries:
            for entry in row:
                entry.delete(0, tk.END)
        
        # Hide the result brackets
        self.bracket_frame.pack_forget()
        
        # Reset focus to the first cell
        if self.matrix_a_entries:
            self.matrix_a_entries[0][0].focus_set()

def create_matrix_tab(parent):
    return MatrixTab(parent)
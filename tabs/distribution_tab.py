import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import norm

# Ensure your folder structure is: modules/distribution_module.py
from modules.distribution_module import DistributionModule

class DistributionTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize variables for BOTH distributions here
        self.n_var = tk.StringVar(value="")
        self.p_var = tk.StringVar(value="")
        self.mu_var = tk.StringVar(value="")
        self.sigma_var = tk.StringVar(value="")
        
        # Universal test value variables (used by both sections)
        self.k1_var = tk.StringVar(value="")
        self.k2_var = tk.StringVar(value="")
        self.test_type = tk.StringVar(value="left-tail")

        # --- 1. Top Navigation ---
        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(side="top", fill="x", pady=10)

        ttk.Button(self.nav_frame, text="Binomial Distribution", 
                   command=self.show_binomial).pack(side="left", padx=10, expand=True)
        ttk.Button(self.nav_frame, text="Normal Distribution", 
                   command=self.show_normal).pack(side="left", padx=10, expand=True)

        # --- 2. Input Area (The Workspace) ---
        self.workspace = ttk.LabelFrame(self, text="Parameters")
        self.workspace.pack(fill="x", padx=20, pady=5)
        
        # --- 3. Plotting Area ---
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.show_binomial()

    def clear_screen(self):
        """Wipes the parameter and plot areas."""
        for widget in self.workspace.winfo_children():
            widget.destroy()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def refresh_test_inputs(self):
        """Wipes the dynamic_input_frame and redraws the 'sentence' for k1 and k2."""
        for widget in self.dynamic_input_frame.winfo_children():
            widget.destroy()
        
        t_type = self.test_type.get()
        # Shared styling for the entry boxes
        cfg = {"width": 6, "justify": "center"}

        if t_type == "left-tail":
            ttk.Label(self.dynamic_input_frame, text="P( X ≤").pack(side="left")
            ttk.Entry(self.dynamic_input_frame, textvariable=self.k1_var, **cfg).pack(side="left", padx=2)
            ttk.Label(self.dynamic_input_frame, text=")").pack(side="left")

        elif t_type == "right-tail":
            ttk.Label(self.dynamic_input_frame, text="P( X ≥").pack(side="left")
            ttk.Entry(self.dynamic_input_frame, textvariable=self.k1_var, **cfg).pack(side="left", padx=2)
            ttk.Label(self.dynamic_input_frame, text=")").pack(side="left")

        elif t_type == "two-tail":
            ttk.Label(self.dynamic_input_frame, text="P( X ≤").pack(side="left")
            ttk.Entry(self.dynamic_input_frame, textvariable=self.k1_var, **cfg).pack(side="left", padx=2)
            ttk.Label(self.dynamic_input_frame, text=" or X ≥").pack(side="left")
            ttk.Entry(self.dynamic_input_frame, textvariable=self.k2_var, **cfg).pack(side="left", padx=2)
            ttk.Label(self.dynamic_input_frame, text=")").pack(side="left")

        elif t_type == "middle":
            ttk.Label(self.dynamic_input_frame, text="P(").pack(side="left")
            ttk.Entry(self.dynamic_input_frame, textvariable=self.k1_var, **cfg).pack(side="left", padx=2)
            ttk.Label(self.dynamic_input_frame, text=" ≤ X ≤").pack(side="left")
            ttk.Entry(self.dynamic_input_frame, textvariable=self.k2_var, **cfg).pack(side="left", padx=2)
            ttk.Label(self.dynamic_input_frame, text=")").pack(side="left")

    # --- BINOMIAL SECTION ---
    def show_binomial(self):
        self.clear_screen()
        self.k1_var.set("") 
        self.k2_var.set("")
        self.workspace.config(text="Binomial Hypothesis Test")

        ttk.Label(self.workspace, text="n (Trials):").grid(row=0, column=0, sticky="e", padx=5)
        ttk.Entry(self.workspace, textvariable=self.n_var).grid(row=0, column=1, sticky="w")

        ttk.Label(self.workspace, text="p (Prob):").grid(row=1, column=0, sticky="e", padx=5)
        ttk.Entry(self.workspace, textvariable=self.p_var).grid(row=1, column=1, sticky="w")

        ttk.Label(self.workspace, text="Test Type:").grid(row=2, column=0, sticky="e", padx=5)
        combo = ttk.Combobox(self.workspace, textvariable=self.test_type, state="readonly")
        combo['values'] = ("left-tail", "right-tail", "two-tail", "middle")
        combo.grid(row=2, column=1, sticky="w")
        combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_test_inputs())

        self.dynamic_input_frame = ttk.Frame(self.workspace)
        self.dynamic_input_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.refresh_test_inputs()

        ttk.Button(self.workspace, text="Run Binomial Test", 
                   command=self.plot_binomial).grid(row=4, columnspan=2, pady=10)

    def plot_binomial(self):
        try:
            n, p = int(self.n_var.get()), float(self.p_var.get())
            test = self.test_type.get()
            k1 = int(self.k1_var.get())

            x = np.arange(0, n + 1)
            y = [DistributionModule.binomial_pmf(val, n, p) for val in x]
            
            highlight_indices = []
            if test == "left-tail":
                highlight_indices = [i for i in range(k1 + 1)]; label = f"P(X ≤ {k1})"
            elif test == "right-tail":
                highlight_indices = [i for i in range(k1, n + 1)]; label = f"P(X ≥ {k1})"
            elif test == "two-tail":
                k2 = int(self.k2_var.get())
                highlight_indices = [i for i in range(n + 1) if i <= k1 or i >= k2]
                label = f"P(X ≤ {k1} or X ≥ {k2})"
            elif test == "middle":
                k2 = int(self.k2_var.get())
                highlight_indices = [i for i in range(k1, k2 + 1)]
                label = f"P({k1} ≤ X ≤ {k2})"

            # In your GUI file, inside the plot_binomial method:
            p_val = DistributionModule.binomial_p_value(
               int(self.n_var.get()),         # 1. n
               float(self.p_var.get()),       # 2. p
               self.test_type.get(),          # 3. test_type (The string "two-tail")
               int(self.k1_var.get()),        # 4. k1
               int(self.k2_var.get()) if self.test_type.get() in ["two-tail", "middle"] else None # 5. k2
            )
            
            fig, ax = plt.subplots(figsize=(5, 3))
            bars = ax.bar(x, y, color='lightgray', edgecolor='gray')
            for i in highlight_indices:
                if 0 <= i <= n: bars[i].set_color('red')

            ax.set_title(f"{label} = {p_val:.4f}", fontweight='bold')
            self.render_canvas(fig)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- NORMAL SECTION ---
    def show_normal(self):
        self.clear_screen()
        self.k1_var.set("") 
        self.k2_var.set("")
        self.workspace.config(text="Normal Hypothesis Test")

        ttk.Label(self.workspace, text="Mean (μ):").grid(row=0, column=0, sticky="e", padx=5)
        ttk.Entry(self.workspace, textvariable=self.mu_var).grid(row=0, column=1, sticky="w")

        ttk.Label(self.workspace, text="Std Dev (σ):").grid(row=1, column=0, sticky="e", padx=5)
        ttk.Entry(self.workspace, textvariable=self.sigma_var).grid(row=1, column=1, sticky="w")

        ttk.Label(self.workspace, text="Test Type:").grid(row=2, column=0, sticky="e", padx=5)
        combo = ttk.Combobox(self.workspace, textvariable=self.test_type, state="readonly")
        combo['values'] = ("left-tail", "right-tail", "two-tail", "middle")
        combo.grid(row=2, column=1, sticky="w")
        combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_test_inputs())

        self.dynamic_input_frame = ttk.Frame(self.workspace)
        self.dynamic_input_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.refresh_test_inputs()

        ttk.Button(self.workspace, text="Run Normal Test", 
                   command=self.plot_normal).grid(row=4, columnspan=2, pady=10)

    def plot_normal(self):
        try:
            # 1. Get Parameters
            mu = float(self.mu_var.get())
            sigma = float(self.sigma_var.get())
            test = self.test_type.get()
            k1 = float(self.k1_var.get())
            alpha = 0.05  # Significance level

            # 2. Calculate P-Value
            p_val = DistributionModule.normal_p_value(
                mu, sigma, test, k1, 
                float(self.k2_var.get()) if test in ["two-tail", "middle"] else None
            )

            x, y = DistributionModule.get_normal_range(mu, sigma)
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(x, y, color='black', lw=2)

            # --- 3. Critical Values Logic (Updated Calls) ---
            if test == "left-tail":
                cv = norm.ppf(alpha, mu, sigma)
                self.draw_cv(ax, mu, sigma, cv, "CV") # Pass 5 arguments
                ax.fill_between(x, y, where=(x <= k1), color='red', alpha=0.5)
                label = f"P(X ≤ {k1})"

            elif test == "right-tail":
                cv = norm.ppf(1 - alpha, mu, sigma)
                self.draw_cv(ax, mu, sigma, cv, "CV") # Pass 5 arguments
                ax.fill_between(x, y, where=(x >= k1), color='red', alpha=0.5)
                label = f"P(X ≥ {k1})"

            elif test == "two-tail":
                cv_l = norm.ppf(alpha/2, mu, sigma)
                cv_r = norm.ppf(1 - alpha/2, mu, sigma)
                self.draw_cv(ax, mu, sigma, cv_l, "CV1") # Pass 5 arguments
                self.draw_cv(ax, mu, sigma, cv_r, "CV2") # Pass 5 arguments
                
                k2 = float(self.k2_var.get())
                ax.fill_between(x, y, where=((x <= k1) | (x >= k2)), color='red', alpha=0.5)
                label = f"P(X ≤ {k1} or X ≥ {k2})"

            elif test == "middle":
                k2 = float(self.k2_var.get())
                ax.fill_between(x, y, where=((x >= k1) & (x <= k2)), color='red', alpha=0.5)
                label = f"P({k1} ≤ X ≤ {k2})"

            # --- 4. Finalize Plot ---
            ax.set_title(f"{label} = {p_val:.4f}", fontweight='bold', pad=15)
            # Add a bit of padding to the top so the curve doesn't touch the title
            ax.set_ylim(bottom=0, top=ax.get_ylim()[1] * 1.1)
            
            self.render_canvas(fig)

        except Exception as e:
            messagebox.showerror("Error", f"Normal Plot Error: {str(e)}")

    def draw_cv(self, ax, mu, sigma, cv_value, label_text):
        """
        Draws the threshold line and places the value with 5 sig figs 
        below the horizontal axis.
        """
        # Calculate height at the curve to stop the line properly
        h = norm.pdf(cv_value, mu, sigma)

        # Draw the blue dashed line
        ax.vlines(cv_value, 0, h, color='blue', linestyle='--', lw=1.5, alpha=0.8)

        # Format to 5 Significant Figures using :.5g
        formatted_cv = f"{cv_value:.5g}"

        # Place label BELOW the axis line
        # -0.05 on the xaxis_transform puts it just under the line
        ax.text(cv_value, -0.05, f"{label_text}\n{formatted_cv}", 
                transform=ax.get_xaxis_transform(),
                color='blue', ha='center', va='top', fontweight='bold', fontsize=8)
    
    def render_canvas(self, fig):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        fig.set_constrained_layout(True)
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

def create_distribution_tab(parent):
    return DistributionTab(parent)
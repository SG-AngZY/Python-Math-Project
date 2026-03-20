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
        for widget in self.workspace.winfo_children():
            widget.destroy()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    def show_binomial(self):
        self.clear_screen()
        self.workspace.config(text="Binomial Hypothesis Test")

        self.n_var = tk.StringVar(value=" ")
        self.p_var = tk.StringVar(value=" ")
        self.k_var = tk.StringVar(value=" ")
        self.test_type = tk.StringVar(value="two-tail")

        ttk.Label(self.workspace, text="n (Trials):").grid(row=0, column=0, padx=5, pady=2)
        ttk.Entry(self.workspace, textvariable=self.n_var).grid(row=0, column=1)

        ttk.Label(self.workspace, text="p (Prob):").grid(row=1, column=0, padx=5, pady=2)
        ttk.Entry(self.workspace, textvariable=self.p_var).grid(row=1, column=1)

        ttk.Label(self.workspace, text="Test Value (x):").grid(row=2, column=0, padx=5, pady=2)
        ttk.Entry(self.workspace, textvariable=self.k_var).grid(row=2, column=1)

        ttk.Label(self.workspace, text="Test Type:").grid(row=3, column=0, padx=5, pady=2)
        combo = ttk.Combobox(self.workspace, textvariable=self.test_type, state="readonly")
        combo['values'] = ("equal", "left-tail", "right-tail", "two-tail")
        combo.grid(row=3, column=1)

        ttk.Button(self.workspace, text="Run Binomial Test", 
                   command=self.plot_binomial).grid(row=4, columnspan=2, pady=10)

    def plot_binomial(self):
        try:
            n = int(self.n_var.get())
            p = float(self.p_var.get())
            k_obs = int(self.k_var.get())
            test = self.test_type.get()
            
            if not (0 <= p <= 1): raise ValueError("p must be 0 to 1")

            x = np.arange(0, n + 1)
            y = [DistributionModule.binomial_pmf(val, n, p) for val in x]
            p_val = DistributionModule.binomial_p_value(k_obs, n, p, test)

            fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
            bars = ax.bar(x, y, color='lightgray', edgecolor='gray')
            
            # --- 1. Identify which bars to highlight red ---
            highlight_indices = []
            
            if test == "equal":
                highlight_indices = [k_obs]
                label = f"P(X = {k_obs})"
            elif test == "left-tail":
                highlight_indices = [i for i in range(k_obs + 1)]
                label = f"P(X ≤ {k_obs})"
            elif test == "right-tail":
                highlight_indices = [i for i in range(k_obs, n + 1)]
                label = f"P(X ≥ {k_obs})"
            elif test == "two-tail":
                obs_prob = DistributionModule.binomial_pmf(k_obs, n, p)
                # Any bar with probability <= our observed bar is "rare"
                highlight_indices = [i for i in range(n + 1) if y[i] <= obs_prob + 1e-9]
                
                # Dynamic Labeling for Two-Tail
                mean = n * p
                left_tail = [i for i in highlight_indices if i <= mean]
                right_tail = [i for i in highlight_indices if i >= mean]
                c1 = max(left_tail) if left_tail else 0
                c2 = min(right_tail) if right_tail else n
                label = f"P(X ≤ {c1} or X ≥ {c2})"

            # --- 2. Apply the Red Color ---
            for i in highlight_indices:
                if 0 <= i <= n:
                    bars[i].set_color('red')

            # --- 3. Finalize Plot ---
            ax.set_title(f"{label} = {p_val:.4f}", fontsize=11, fontweight='bold', pad=15)
            self.render_canvas(fig)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_normal(self):
        self.clear_screen()
        self.workspace.config(text="Normal Hypothesis Test")

        self.mu_var = tk.StringVar(value=" ")
        self.sigma_var = tk.StringVar(value=" ")
        self.x_var = tk.StringVar(value=" ")
        self.test_type = tk.StringVar(value="two-tail")

        ttk.Label(self.workspace, text="Mean (μ):").grid(row=0, column=0, padx=5, pady=2)
        ttk.Entry(self.workspace, textvariable=self.mu_var).grid(row=0, column=1)

        ttk.Label(self.workspace, text="Std Dev (σ):").grid(row=1, column=0, padx=5, pady=2)
        ttk.Entry(self.workspace, textvariable=self.sigma_var).grid(row=1, column=1)

        ttk.Label(self.workspace, text="Test Value (x):").grid(row=2, column=0, padx=5, pady=2)
        ttk.Entry(self.workspace, textvariable=self.x_var).grid(row=2, column=1)

        ttk.Label(self.workspace, text="Test Type:").grid(row=3, column=0, padx=5, pady=2)
        combo = ttk.Combobox(self.workspace, textvariable=self.test_type, state="readonly")
        combo['values'] = ("left-tail", "right-tail", "two-tail")
        combo.grid(row=3, column=1)

        ttk.Button(self.workspace, text="Run Normal Test", 
                   command=self.plot_normal).grid(row=4, columnspan=2, pady=10)

    def plot_normal(self):
        try:
            mu = float(self.mu_var.get())
            sigma = float(self.sigma_var.get())
            x_obs = float(self.x_var.get())
            test = self.test_type.get()
            
            if sigma <= 0: raise ValueError("σ must be > 0")

            # 1. Generate the curve data
            x, y = DistributionModule.get_normal_range(mu, sigma)
            p_val = DistributionModule.normal_p_value(x_obs, mu, sigma, test)

            fig, ax = plt.subplots(figsize=(5, 3), dpi=100) 
            ax.plot(x, y, color='black', lw=2)

            # --- 2. Dynamic Labeling & Shading Logic ---
            if test == "left-tail":
                label = f"P(X ≤ {x_obs})"
                # Shade from the far left to x_obs
                x_shade = np.linspace(mu - 4*sigma, x_obs, 100)
                ax.fill_between(x_shade, norm.pdf(x_shade, mu, sigma), color='red', alpha=0.5)
                
            elif test == "right-tail":
                label = f"P(X ≥ {x_obs})"
                # Shade from x_obs to the far right
                x_shade = np.linspace(x_obs, mu + 4*sigma, 100)
                ax.fill_between(x_shade, norm.pdf(x_shade, mu, sigma), color='red', alpha=0.5)
                
            elif test == "two-tail":
                # Find the distance from the mean
                diff = abs(x_obs - mu)
                c1 = mu - diff
                c2 = mu + diff
                label = f"P(X ≤ {c1:.2f} or X ≥ {c2:.2f})"
                
                # Shade Left Tail
                x_l = np.linspace(mu - 4*sigma, c1, 100)
                ax.fill_between(x_l, norm.pdf(x_l, mu, sigma), color='red', alpha=0.5)
                
                # Shade Right Tail
                x_r = np.linspace(c2, mu + 4*sigma, 100)
                ax.fill_between(x_r, norm.pdf(x_r, mu, sigma), color='red', alpha=0.5)

            # --- 3. Finalize Plot ---
            ax.set_title(f"{label} = {p_val:.4f}", fontsize=11, fontweight='bold', pad=15)
            
            # Ensure the plot fits without being "covered"
            self.render_canvas(fig)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def render_canvas(self, fig):
        """Helper to draw the figure and force it to fill the available space."""
        # 1. Clear old plot from the frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # 2. Set 'constrained_layout' to True (The modern way to auto-fit)
        fig.set_constrained_layout(True)

        # 3. Create the canvas
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        
        # 4. CRITICAL: Fill both directions and Expand
        # This makes the 'box' containing the graph grow with the window
        canvas_widget.pack(side="top", fill="both", expand=True)
        
        # 5. Draw it
        canvas.draw()
        
def create_distribution_tab(parent):
    return DistributionTab(parent)   
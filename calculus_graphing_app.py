import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import quad
from tkinter import Tk, StringVar, Entry, Label, Button, IntVar
import ttkbootstrap as tb

# Function Parsing
def parse_function(func_str):
    x = sp.symbols('x')
    return sp.sympify(func_str), x

# Numerical Differentiation
def numerical_derivative(f, x_val, order=1, h=1e-5):
    if order == 1:
        return (f(x_val + h) - f(x_val - h)) / (2 * h)
    elif order == 2:
        return (f(x_val + h) - 2 * f(x_val) + f(x_val - h)) / (h**2)
    elif order == 3:
        return (f(x_val + 2*h) - 2*f(x_val + h) + 2*f(x_val - h) - f(x_val - 2*h)) / (2*h**3)
    else:
        raise ValueError("Only up to third-order derivatives are supported.")

# Numerical Integration
def numerical_integral(f, a, b):
    result, _ = quad(f, a, b)
    return result

# Plot Graph
def plot_graph():
    try:
        func_expr, x = parse_function(func_input.get())
        func_lambdified = sp.lambdify(x, func_expr, 'numpy')
        x_vals = np.linspace(float(x_min.get()), float(x_max.get()), 400)
        y_vals = func_lambdified(x_vals)
        
        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_vals, label='Original Function', color='blue')
        
        plot_choice = plot_option.get()
        results_text = ""
        
        if plot_choice in ['Derivative', 'Both']:
            derivative_order = derivative_order_var.get()
            derivative_expr = sp.diff(func_expr, x, derivative_order)
            derivative_vals = [numerical_derivative(func_lambdified, val, order=derivative_order) for val in x_vals]
            plt.plot(x_vals, derivative_vals, label=f'{derivative_order}-order Derivative', linestyle='dashed', color='red')
            results_text += f"Symbolic {derivative_order}-order Derivative: {derivative_expr}\n"
        
        if plot_choice in ['Integral', 'Both']:
            integral_expr = sp.integrate(func_expr, x)
            integral_vals = [numerical_integral(func_lambdified, float(x_min.get()), val) for val in x_vals]
            plt.plot(x_vals, integral_vals, label='Integral', linestyle='dotted', color='green')
            results_text += f"Symbolic Integral: {integral_expr} + C\n"
        
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Function Visualization')
        plt.grid()
        
        plt.figtext(0.1, -0.1, results_text, fontsize=10, wrap=True, horizontalalignment='left')
        
        plt.show()
    except Exception as e:
        print(f"Error: {e}")

# GUI Setup
root = Tk()
root.title("Calculus Graphing App")
tb.Style(theme="superhero")

Label(root, text="Enter function (in terms of x):").grid(row=0, column=0, padx=10, pady=5)
func_input = StringVar()
Entry(root, textvariable=func_input, width=30).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="X range (min, max):").grid(row=1, column=0, padx=10, pady=5)
x_min = StringVar()
x_max = StringVar()
Entry(root, textvariable=x_min, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')
Entry(root, textvariable=x_max, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='e')

Label(root, text="Derivative Order:").grid(row=2, column=0, padx=10, pady=5)
derivative_order_var = IntVar(value=1)
Entry(root, textvariable=derivative_order_var, width=5).grid(row=2, column=1, padx=10, pady=5, sticky='w')

Label(root, text="Plot Options:").grid(row=3, column=0, padx=10, pady=5)
plot_option = StringVar(value="Both")
tb.Combobox(root, textvariable=plot_option, values=["Function", "Derivative", "Integral", "Both"]).grid(row=3, column=1, padx=10, pady=5)

tb.Button(root, text="Plot", command=plot_graph, style="success.TButton").grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

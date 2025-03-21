import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.integrate import quad
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Function to compute numerical derivative using finite differences
def finite_difference(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)  # Central difference formula

# Function to compute integral
def numerical_integral(f, a, b):
    return quad(f, a, b)[0]

# Function to plot graphs
def plot_graph(expression, x_range):
    x = sp.symbols('x')  # Define x as a symbol
    expr = sp.sympify(expression, locals={"sin": sp.sin, "cos": sp.cos, "exp": sp.exp, "log": sp.log})  # Parse user input
    f = sp.lambdify(x, expr, 'numpy')  # Convert symbolic expression to function

    x_vals = np.linspace(x_range[0], x_range[1], 400)
    y_vals = f(x_vals)
    dy_vals = np.array([finite_difference(f, xi) for xi in x_vals])  # Use finite difference for derivative
    integral_vals = np.array([numerical_integral(f, x_range[0], xi) for xi in x_vals])

    plt.figure(figsize=(10, 5))
    plt.plot(x_vals, y_vals, label='Function', linewidth=2)
    plt.plot(x_vals, dy_vals, label='Derivative', linestyle='dashed')
    plt.plot(x_vals, integral_vals, label='Integral', linestyle='dotted')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.title("Function, Derivative, and Integral")
    plt.grid()
    plt.show()

# GUI using ttkbootstrap
def on_submit():
    try:
        expression = entry.get()
        x_min, x_max = float(x_min_entry.get()), float(x_max_entry.get())
        plot_graph(expression, (x_min, x_max))
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = ttk.Window(themename="superhero")
root.title("Calculus-Powered Graphing App")
root.geometry("400x300")

frame = ttk.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=True)

ttk.Label(frame, text="Enter function (in terms of x):", font=("Arial", 12)).pack()
entry = ttk.Entry(frame, width=40, font=("Arial", 12))
entry.pack(pady=5)

ttk.Label(frame, text="X range (min, max):", font=("Arial", 12)).pack()
x_range_frame = ttk.Frame(frame)
x_range_frame.pack()

x_min_entry = ttk.Entry(x_range_frame, width=10, font=("Arial", 12))
x_min_entry.pack(side=LEFT, padx=5)
x_max_entry = ttk.Entry(x_range_frame, width=10, font=("Arial", 12))
x_max_entry.pack(side=LEFT, padx=5)

ttk.Button(frame, text="Plot Graph", command=on_submit, bootstyle=SUCCESS, width=20).pack(pady=10)

root.mainloop()

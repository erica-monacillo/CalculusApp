import os
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import quad
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import filedialog
from tkinter import PhotoImage

# Global variables
current_figure = None
current_canvas = None
current_theme = "darkly"  # Default theme

def parse_function(func_str):
    try:
        x = sp.symbols('x')
        expr = parse_expr(func_str, transformations='all')
        return expr, x
    except Exception as e:
        raise ValueError(f"Invalid function expression: {str(e)}")

def numerical_derivative(f, x_val, order=1, h=1e-5):
    if order == 1:
        return (f(x_val + h) - f(x_val - h)) / (2 * h)
    elif order == 2:
        return (f(x_val + h) - 2 * f(x_val) + f(x_val - h)) / (h**2)
    elif order == 3:
        return (f(x_val + 2*h) - 2*f(x_val + h) + 2*f(x_val - h) - f(x_val - 2*h)) / (2*h**3)
    else:
        raise ValueError("Derivative order must be 1, 2, or 3")

def numerical_integral(f, a, b):
    """Compute definite integral of f from a to b using scipy's quad"""
    result, _ = quad(f, a, b)
    return result

def save_graph():
    global current_figure
    if current_figure is None:
        result_label.config(text="No graph to save!", foreground="#f44336")
        return
    
    try:
        filetypes = [
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg'),
            ('PDF files', '*.pdf'),
            ('SVG files', '*.svg'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=filetypes,
            title="Save graph as"
        )
        
        if filename:
            current_figure.savefig(filename, dpi=300, bbox_inches='tight')
            result_label.config(text=f"Graph saved to {os.path.basename(filename)}", foreground="#4caf50")
    except Exception as e:
        result_label.config(text=f"Error saving graph: {str(e)}", foreground="#f44336")

def toggle_theme():
    global current_theme, current_figure, current_canvas
    if current_theme == "darkly":
        current_theme = "litera"
        style.theme_use("litera")
        theme_button.config(text="☀️", bootstyle="dark-outline")
    else:
        current_theme = "darkly"
        style.theme_use("darkly")
        theme_button.config(text="🌙", bootstyle="light-outline")
    
    # Update existing graph's theme
    if current_figure and current_canvas:
        apply_theme_to_graph(current_figure, current_figure.axes[0])
        current_canvas.draw()
    
    # Update text colors in results
    update_result_colors()

def update_result_colors():
    if hasattr(results_frame, 'winfo_children'):
        text_color = get_text_color()
        for widget in results_frame.winfo_children():
            if isinstance(widget, tb.Label):
                if widget.cget("foreground") not in ["#1f77b4", "#ff7f0e", "#2ca02c"]:
                    widget.config(foreground=text_color)

def show_help():
    help_window = tb.Toplevel(title="JustGraphIt Help")
    help_window.geometry("500x400")
    help_window.grab_set()

    help_text = """
    JustGraphIt Help Guide

    1. FUNCTION INPUT:
    - Enter mathematical functions using standard notation
    - Example: sin(x)*(x) + x**2 - 3

    2. X-RANGE:
    - Set the minimum and maximum x-values to display
    - Example: min=-10, max=10
    
    3. VISUALIZATION OPTIONS:
    - Function: Plots the original function
    - Derivative: Shows the derivative (select order 1-3)
    - Integral: Shows the accumulated area under the curve
    - Both: Displays function with derivative/integral
    
    4. CONTROLS:
    - Generate Visualization: Creates the graph
    - Save Graph: Export as PNG/JPEG/PDF/SVG
    
    5. THEMES:
    - Toggle between light/dark modes
    
    Note: Use Python math syntax (e.g., x**2 not x^2)
    """

    text_frame = tb.Frame(help_window)
    text_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    text = tb.Text(
        text_frame,
        wrap=WORD,
        font=('Segoe UI', 10),
        height=20,
        padx=10,
        pady=10
    )
    text.pack(side=LEFT, fill=BOTH, expand=YES)
    
    scrollbar = tb.Scrollbar(
        text_frame,
        orient=VERTICAL,
        command=text.yview
    )
    scrollbar.pack(side=RIGHT, fill=Y)
    
    text.config(yscrollcommand=scrollbar.set)
    text.insert(END, help_text)
    text.config(state=DISABLED)
    
    close_btn = tb.Button(
        help_window,
        text="Close",
        command=help_window.destroy,
        bootstyle="danger"
    )
    close_btn.pack(pady=10)

def apply_theme_to_graph(fig, ax):
    """Apply the current theme to the matplotlib figure"""
    if current_theme == "darkly":
        plt.style.use('dark_background')
        fig.set_facecolor('#2d2d2d')
        ax.set_facecolor('#2d2d2d')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.grid(True, color='#4a4a4a')
    else:
        plt.style.use('default')
        fig.set_facecolor('white')
        ax.set_facecolor('white')
        ax.tick_params(colors='black')
        ax.xaxis.label.set_color('black')
        ax.yaxis.label.set_color('black')
        ax.title.set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['top'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.grid(True, color='#d3d3d3')

def get_text_color():
    return "white" if current_theme == "darkly" else "black"

def on_resize(event):
    """Handle window resize events to maintain theme consistency"""
    if current_figure and current_canvas:
        apply_theme_to_graph(current_figure, current_figure.axes[0])
        current_canvas.draw()

def plot_graph():
    global current_figure, current_canvas
    
    try:
        # Clear previous results COMPLETELY
        for widget in results_frame.winfo_children():
            widget.destroy()
        
        # Clear previous graph (preserving buttons)
        for widget in graph_frame.winfo_children():
            if widget != button_container:
                widget.destroy()
        
        # Validate inputs
        if not func_input.get():
            raise ValueError("Please enter a function")
        if not x_min.get() or not x_max.get():
            raise ValueError("Please enter both x-min and x-max values")
        try:
            x_min_val = float(x_min.get())
            x_max_val = float(x_max.get())
        except ValueError:
            raise ValueError("X-range values must be numbers")
        
        if x_min_val >= x_max_val:
            raise ValueError("X-min must be less than X-max")
        
        func_expr, x = parse_function(func_input.get())
        func_lambdified = sp.lambdify(x, func_expr, 'numpy')
        
        # Generate x values
        x_vals = np.linspace(x_min_val, x_max_val, 400)
        y_vals = func_lambdified(x_vals)
        
        # Create figure with current theme
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        apply_theme_to_graph(fig, ax)
        
        ax.plot(x_vals, y_vals, label='Function', color='#1f77b4')
        
        plot_choice = plot_option.get()
        if not plot_choice:
            raise ValueError("Please select a plot option")
        
        # Create a frame for equations in the results_frame (right side below graph)
        equations_frame = tb.Frame(results_frame)
        equations_frame.pack(fill=X, pady=10, padx=10)
        
        # Add function label
        text_color = get_text_color()
        func_label = tb.Label(equations_frame, 
                            text=f"Function: {sp.pretty(func_expr, use_unicode=True)}",
                            font=('Courier New', 10),
                            foreground="#1f77b4")
        func_label.pack(anchor=W)
        
        if plot_choice in ['Derivative', 'Both']:
            if not derivative_order_var.get():
                raise ValueError("Please select derivative order")
            derivative_order = derivative_order_var.get()
            derivative_expr = sp.diff(func_expr, x, derivative_order)
            derivative_vals = [numerical_derivative(func_lambdified, val, derivative_order) for val in x_vals]
            ax.plot(x_vals, derivative_vals, label=f'Derivative (order {derivative_order})', linestyle='--', color='#ff7f0e')
            
            # Add derivative equation label
            deriv_label = tb.Label(equations_frame,
                                 text=f"Derivative (order {derivative_order}): {sp.pretty(derivative_expr, use_unicode=True)}",
                                 font=('Courier New', 10),
                                 foreground="#ff7f0e")
            deriv_label.pack(anchor=W)
        
        if plot_choice in ['Integral', 'Both']:
            integral_expr = sp.integrate(func_expr, x)
            integral_vals = [numerical_integral(func_lambdified, x_min_val, val) for val in x_vals]
            ax.plot(x_vals, integral_vals, label='Integral', linestyle=':', color='#2ca02c')
            
            # Add integral equation label
            int_label = tb.Label(equations_frame,
                               text=f"Integral: {sp.pretty(integral_expr, use_unicode=True)} + C",
                               font=('Courier New', 10),
                               foreground="#2ca02c")
            int_label.pack(anchor=W)
        
        ax.legend(loc='upper right', framealpha=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'Graph of {func_input.get()}')
        
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # Assign the figure and canvas globally
        current_figure = fig
        current_canvas = canvas
        
        result_label.config(text="Graph generated successfully!", foreground="#4caf50")
        
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#f44336")
        print(f"DEBUG: {str(e)}")

# GUI Setup with dark theme
root = tb.Window(themename="darkly")
root.title("JustGraphIt")

# Set application logo (window icon)
try:
    root.iconbitmap('logo.ico')
except Exception as e:
    print(f"Could not load .ico logo: {e}")
    try:
        logo_image = PhotoImage(file='logo.png')
        root.iconphoto(True, logo_image)
    except Exception as e:
        print(f"Could not load any logo: {e}")

root.geometry("1000x600")
style = tb.Style()

# Bind the resize event
root.bind('<Configure>', on_resize)

# Main container with side-by-side layout
main_frame = tb.Frame(root)
main_frame.pack(fill=BOTH, expand=YES)

# Left panel for controls
control_frame = tb.Frame(main_frame, width=400)
control_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)

# Right panel container
right_frame = tb.Frame(main_frame)
right_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10, pady=10)

# Graph frame (top of right panel)
graph_frame = tb.Frame(right_frame)
graph_frame.pack(side=TOP, fill=BOTH, expand=YES)

# Single container for both buttons
button_container = tb.Frame(graph_frame)
button_container.pack(side=TOP, anchor=NE, padx=15, pady=10)

# Help button (left side)
help_button = tb.Button(
    button_container,
    text="?",
    command=show_help,
    bootstyle="info-outline",
    width=2,
    padding=(6, 6),
    cursor="hand2"
)
help_button.pack(side=LEFT, padx=(0, 5))

# Theme button (right side)
theme_button = tb.Button(
    button_container,
    text="🌙",
    command=toggle_theme,
    bootstyle="light-outline",
    width=2,
    padding=(6, 6),
    cursor="hand2"
)
theme_button.pack(side=LEFT)

# Results frame (bottom of right panel) - This is where we'll put the function info
results_frame = tb.Frame(right_frame)
results_frame.pack(side=BOTTOM, fill=X)

# Header
header = tb.Label(control_frame, text="JustGraphIt", font=('Helvetica', 16, 'bold'))
header.pack(pady=(0, 20))

# Input Frame
input_frame = tb.LabelFrame(control_frame, text="Function Input", padding=15)
input_frame.pack(fill=X, pady=5)

# Function input
func_input = tb.StringVar()
tb.Label(input_frame, text="Function f(x):").grid(row=0, column=0, padx=5, pady=5, sticky=W)
func_entry = tb.Entry(input_frame, textvariable=func_input, width=30)
func_entry.grid(row=0, column=1, padx=5, pady=5, sticky=EW)

# Range Frame
range_frame = tb.Frame(input_frame)
range_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=EW)

x_min = tb.StringVar()
x_max = tb.StringVar()
tb.Label(range_frame, text="X Range:").pack(side=LEFT, padx=5)
tb.Entry(range_frame, textvariable=x_min, width=8).pack(side=LEFT, padx=5)
tb.Label(range_frame, text="to").pack(side=LEFT)
tb.Entry(range_frame, textvariable=x_max, width=8).pack(side=LEFT, padx=5)

# Options Frame
options_frame = tb.LabelFrame(control_frame, text="Visualization Options", padding=15)
options_frame.pack(fill=X, pady=10)

# Derivative options
derivative_frame = tb.Frame(options_frame)
derivative_frame.pack(fill=X, pady=5)

derivative_order_var = tb.IntVar()
tb.Label(derivative_frame, text="Derivative Order:").pack(side=LEFT, padx=5)
order_combo = tb.Combobox(derivative_frame, textvariable=derivative_order_var, values=[1, 2, 3], width=5)
order_combo.pack(side=LEFT, padx=5)

# Plot options
plot_frame = tb.Frame(options_frame)
plot_frame.pack(fill=X, pady=5)

plot_option = tb.StringVar()
tb.Label(plot_frame, text="Show:").pack(side=LEFT, padx=5)
plot_combo = tb.Combobox(plot_frame, textvariable=plot_option, 
                        values=["Function", "Derivative", "Integral", "Both"], width=12)
plot_combo.pack(side=LEFT, padx=5)

# Button and results
button_frame = tb.Frame(control_frame)
button_frame.pack(fill=X, pady=10)

# Plot button
plot_button = tb.Button(button_frame, text="Generate Visualization", 
                       command=plot_graph, bootstyle=SUCCESS)
plot_button.pack(side=LEFT, padx=5, pady=5, ipadx=10, ipady=5)

# Save button
save_button = tb.Button(button_frame, text="Save Graph", 
                       command=save_graph, bootstyle=INFO)
save_button.pack(side=LEFT, padx=5, pady=5, ipadx=10, ipady=5)

result_label = tb.Label(control_frame, text="", font=('Helvetica', 10))
result_label.pack(fill=X, pady=5)

# Set focus and default selections
func_entry.focus()
plot_option.set("Function")
plot_combo.current(0)
derivative_order_var.set(1)  # Set default derivative order to 1

# Initial graph placeholder
placeholder = tb.Label(graph_frame, text="Graph will appear here", foreground="gray")
placeholder.pack(expand=YES)

root.mainloop()
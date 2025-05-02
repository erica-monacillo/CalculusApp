import os
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import quad
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from sympy.parsing.sympy_parser import parse_expr
from scipy.integrate import quad
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import ttk

# Global variables
current_figure = None
current_canvas = None
current_theme = "darkly"  # Default theme

def parse_function(func_str):
    """
    Parse a function string into a SymPy expression. Supports both regular and piecewise functions.
    """
    try:
        x = sp.symbols('x')  # Define the symbolic variable
        if "{" in func_str and "}" in func_str:
            # Handle piecewise functions
            conditions = []
            expressions = []
            func_str = func_str.strip("{}")
            for part in func_str.split(","):
                condition, expression = part.split(":")
                conditions.append(sp.sympify(condition.strip(), locals={'x': x}))
                expressions.append(sp.sympify(expression.strip(), locals={'x': x}))
            expr = sp.Piecewise(*[(expr, cond) for expr, cond in zip(expressions, conditions)])
        else:
            # Handle regular functions
            expr = sp.sympify(func_str, locals={'x': x})
        return expr, x
    except Exception as e:
        raise ValueError(f"Invalid function expression: {str(e)}")

def numerical_derivative(f, x_val, order=1, h=1e-5):
    """
    Numerically calculate the derivative of a function f at a specific point x_val.
    """
    if order == 1:
        return (f(x_val + h) - f(x_val - h)) / (2 * h)
    elif order == 2:
        return (f(x_val + h) - 2 * f(x_val) + f(x_val - h)) / (h**2)
    elif order == 3:
        return (f(x_val + 2*h) - 2*f(x_val + h) + 2*f(x_val - h) - f(x_val - 2*h)) / (2*h**3)
    else:
        raise ValueError("Derivative order must be 1, 2, or 3")

def numerical_integral(f, a, b):
    """
    Compute the definite integral of f from a to b using SciPy's quad function.
    Handles piecewise functions seamlessly.
    """
    try:
        result, _ = quad(f, a, b)
        return result
    except Exception as e:
        raise ValueError(f"Error computing integral: {str(e)}")

def evaluate_piecewise(func_expr, x_sym):
    """
    Converts a piecewise SymPy expression into a Python function for numerical evaluation.
    """
    if isinstance(func_expr, sp.Piecewise):
        # Generate a lambda function for each piecewise condition
        piecewise_func = sp.lambdify(x_sym, func_expr, 'numpy')
        return piecewise_func
    else:
        return sp.lambdify(x_sym, func_expr, 'numpy')

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
    
    # Update all graphs in the notebook
    for tab in notebook.winfo_children():
        for widget in tab.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                fig = widget.figure
                ax = fig.axes[0] if fig.axes else None
                if ax:
                    apply_theme_to_graph(fig, ax)
                    widget.draw()

    # Update text colors in results
    update_result_colors()

def update_result_colors():
    """Update the font color of all result labels to match the current theme."""
    text_color = get_text_color()
    for tab in notebook.winfo_children():
        for widget in tab.winfo_children():
            if isinstance(widget, tb.Label):
                widget.config(foreground=text_color)

def show_help():
    help_window = tb.Toplevel(title="JustGraphIt! Help")
    help_window.geometry("600x500")
    help_window.grab_set()

    help_text = """
    Welcome to JustGraphIt! Help Guide!

    This application allows you to visualize mathematical functions, their derivatives, and integrals.

    HOW TO USE:

    1. FUNCTION INPUT:
       - Enter a mathematical function in the "Function f(x)" field.
       - Example: sin(x) + x**2 - 3 or {x < 0: x**2, x >= 0: x + 1} for piecewise functions.

    2. X-RANGE:
       - Set the minimum and maximum x-values in the "X Range" fields.
       - Example: X Range: -10 to 10.

    3. VISUALIZATION OPTIONS:
       - Derivative Order: Select the order of the derivative (1, 2, or 3).
       - Show: Choose what to display:
         - Function: Only the original function.
         - Derivative: Only the derivative.
         - Integral: Only the integral.
         - Definite Integral: Shade the area under the curve for a specific range.
         - Piecewise: Display piecewise functions.
         - Both: Show the function along with its derivative or integral.

    4. QUICK FUNCTIONS:
       - Use the buttons under "Quick Functions" to insert common functions like sin(x), cos(x), log(x), etc.

    5. UPLOAD FILE:
       - Upload a file containing functions (supported formats: .txt, .pdf, .docx).
       - Each line in the file should contain a valid function.

    6. CONTROLS:
       - Generate Visualization: Click this button to plot the graph based on your inputs.
       - Save Graph: Save the generated graph as an image (PNG, JPEG, PDF, etc.).
       - Reset: Clear all inputs and reset the application to its default state.

    7. THEMES:
       - Use the 🌙/☀️ button in the top-right corner to toggle between light and dark modes.

    NOTES:
       - Use Python math syntax (e.g., x**2 for x squared, not x^2).
       - Ensure the X Range values are numeric and X-min is less than X-max.
       - For piecewise functions, use the format {condition: expression, ...}.

    Enjoy exploring mathematical visualizations with JustGraphIt!
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

def insert_function(func_template):
    """Insert the selected function into the function input field."""
    current_text = func_input.get()
    # Insert the function template without adding extra parentheses
    func_input.set(current_text + func_template)
    func_entry.icursor(len(func_input.get()))  # Place cursor at the end of the input

def upload_file():
    """Allow the user to upload a file containing functions."""
    try:
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[
                ("All Files", "*.*"),  # Allow all files to be visible by default
                ("Text Files", "*.txt"),
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx")
            ]
        )
        if not file_path:
            return  # User canceled the file dialog

        # Determine file type by extension
        _, file_extension = os.path.splitext(file_path)

        functions = []
        if file_extension == ".txt":
            # Handle text files
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    sanitized_line = line.strip()  # Remove leading/trailing whitespace
                    if sanitized_line and not sanitized_line.startswith("#"):  # Ignore blank lines and comments
                        functions.append(sanitized_line)

        elif file_extension == ".pdf":
            # Handle PDF files
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:  # Ensure the page contains text
                        for line in text.splitlines():
                            sanitized_line = line.strip()
                            if sanitized_line and not sanitized_line.startswith("#"):
                                functions.append(sanitized_line)

        elif file_extension == ".docx":
            # Handle Word documents
            from docx import Document
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                sanitized_line = paragraph.text.strip()
                if sanitized_line and not sanitized_line.startswith("#"):
                    functions.append(sanitized_line)

        else:
            result_label.config(text="Unsupported file type!", foreground="#f44336")
            return

        if not functions:
            result_label.config(text="File is empty or invalid!", foreground="#f44336")
            return

        # Store the functions globally for visualization
        global uploaded_functions
        uploaded_functions = functions
        result_label.config(text=f"{len(functions)} functions loaded successfully!", foreground="#4caf50")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#f44336")

def plot_graph():
    global current_figure, current_canvas

    try:
        # Clear previous tabs
        for tab in notebook.winfo_children():
            tab.destroy()

        # Validate inputs
        if not func_input.get() and not uploaded_functions:
            raise ValueError("Enter a function or upload a file with functions.")
        if not x_min.get() or not x_max.get():
            raise ValueError("Enter both x-min and x-max values.")
        try:
            x_min_val = float(x_min.get())
            x_max_val = float(x_max.get())
        except ValueError:
            raise ValueError("X-range values must be numeric.")
        if x_min_val >= x_max_val:
            raise ValueError("X-min must be less than X-max.")

        # Determine functions to plot
        functions_to_plot = [func_input.get()] if func_input.get() else uploaded_functions

        # Plot each function in a new tab
        for func_str in functions_to_plot:
            try:
                # Parse the function
                func_expr, x = parse_function(func_str)
                func_lambdified = sp.lambdify(x, func_expr, 'numpy')

                # Generate x and y values
                x_vals = np.linspace(x_min_val, x_max_val, 400)
                y_vals = func_lambdified(x_vals)

                # Compute derivative and integral
                derivative = sp.diff(func_expr, x)
                indefinite_integral = sp.integrate(func_expr, x)

                # Create new tab
                tab = tb.Frame(notebook)
                notebook.add(tab, text=func_str)

                # Create figure
                fig = plt.figure(figsize=(8, 5))
                ax = fig.add_subplot(111)
                apply_theme_to_graph(fig, ax)

                # Plot based on selected options
                if plot_option.get() in ["Function", "Both"]:
                    ax.plot(x_vals, y_vals, label='Function', color='blue')

                if plot_option.get() in ["Derivative", "Both"]:
                    derivative_lambdified = sp.lambdify(x, derivative, 'numpy')
                    ax.plot(x_vals, derivative_lambdified(x_vals), label='Derivative', color='green')

                if plot_option.get() in ["Integral", "Both"]:
                    # Symbolic indefinite integral
                    integral_lambdified = sp.lambdify(x, indefinite_integral, 'numpy')
                    integral_vals = integral_lambdified(x_vals)
                    ax.plot(x_vals, integral_vals, label='Indefinite Integral', color='purple')

                if plot_option.get() in ["Definite Integral", "Both"]:
                    # Numerical definite integral
                    lower_bound = float(x_min.get())
                    upper_bound = float(x_max.get())
                    definite_integral = sp.integrate(func_expr, (x, lower_bound, upper_bound))

                    # Shade the area under the curve
                    ax.fill_between(
                        x_vals, y_vals, where=(x_vals >= lower_bound) & (x_vals <= upper_bound),
                        color='orange', alpha=0.3, label=f"Def. Integral [{lower_bound}, {upper_bound}]"
                    )

                if plot_option.get() in ["Piecewise", "Both"]:
                    ax.plot(x_vals, y_vals, label='Piecewise Function', color='red')

                # Finalize the graph
                ax.legend(loc='upper right', framealpha=0.5)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_title(f'Graph of {func_str}')

                # Embed the plot
                canvas = FigureCanvasTkAgg(fig, master=tab)
                canvas.draw()
                canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

                # Add navigation toolbar
                toolbar = NavigationToolbar2Tk(canvas, tab)
                toolbar.update()
                canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

                # Add scrollable results frame
                results_container = tb.Frame(tab)
                results_container.pack(fill=BOTH, expand=YES, pady=10, padx=10)

                results_canvas = tb.Canvas(results_container, highlightthickness=0)
                results_canvas.pack(side=LEFT, fill=BOTH, expand=YES)

                results_scrollbar = tb.Scrollbar(results_container, orient=VERTICAL, command=results_canvas.yview)
                results_scrollbar.pack(side=RIGHT, fill=Y)

                results_canvas.configure(yscrollcommand=results_scrollbar.set)

                equations_frame = tb.Frame(results_canvas)
                results_canvas.create_window((0, 0), window=equations_frame, anchor="nw")

                def on_equations_frame_resize(event):
                    results_canvas.configure(scrollregion=results_canvas.bbox("all"))

                equations_frame.bind("<Configure>", on_equations_frame_resize)

                # Add function details with uniform font color
                text_color = get_text_color()

                func_label = tb.Label(
                    equations_frame,
                    text=f"Function: {sp.pretty(func_expr, use_unicode=True)}",
                    font=('Courier New', 10),
                    foreground=text_color
                )
                func_label.pack(anchor=W)

                if plot_option.get() in ["Derivative", "Both"]:
                    derivative_label = tb.Label(
                        equations_frame,
                        text=f"Derivative: {sp.pretty(derivative, use_unicode=True)}",
                        font=('Courier New', 10),
                        foreground=text_color
                    )
                    derivative_label.pack(anchor=W)

                if plot_option.get() in ["Integral", "Both"]:
                    integral_label = tb.Label(
                        equations_frame,
                        text=f"Indefinite Integral: {sp.pretty(indefinite_integral, use_unicode=True)}",
                        font=('Courier New', 10),
                        foreground=text_color
                    )
                    integral_label.pack(anchor=W)

                if plot_option.get() in ["Definite Integral", "Both"]:
                    definite_label = tb.Label(
                        equations_frame,
                        text=f"Definite Integral [{lower_bound}, {upper_bound}]: {definite_integral}",
                        font=('Courier New', 10),
                        foreground=text_color
                    )
                    definite_label.pack(anchor=W)

            except Exception as e:
                print(f"Skipping invalid function '{func_str}': {e}")
                continue

        result_label.config(text="Graphs generated successfully!", foreground="#4caf50")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", foreground="#f44336")
        print(f"DEBUG: {str(e)}")

def reset_app():
    """Reset the application to its initial state."""
    global current_figure, current_canvas

    # Clear the function input
    func_input.set("")
    x_min.set("")
    x_max.set("")
    plot_option.set("Function")
    derivative_order_var.set(1)

    # Clear the notebook tabs
    for tab in notebook.winfo_children():
        tab.destroy()

    # Add a placeholder to the notebook
    placeholder = tb.Label(notebook, text="Graph will appear here", foreground="gray")
    placeholder.pack(expand=YES)

    # Reset the result label
    result_label.config(text="", foreground="black")

    # Reset global variables
    current_figure = None
    current_canvas = None

# GUI Setup with dark theme
root = tb.Window(themename="darkly")
root.title("JustGraphIt!")

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

# Replace graph_frame with a notebook for tabs
notebook = ttk.Notebook(right_frame)
notebook.pack(fill=BOTH, expand=YES)

# Single container for both buttons (Help and Theme)
button_container = tb.Frame(right_frame)
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
header = tb.Label(control_frame, text="JustGraphIt!", font=('Helvetica', 16, 'bold'))
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
                        values=["Function", "Derivative", "Integral", "Definite Integral",
                                "Piecewise", "Both"], width=12)
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

# Function Buttons Frame
func_buttons_frame = tb.LabelFrame(control_frame, text="Quick Functions", padding=15)
func_buttons_frame.pack(fill=X, pady=10)

# Add buttons for common functions with custom styles
functions = [
    ('sin', 'sin(x)'), ('cos', 'cos(x)'), ('tan', 'tan(x)'), ('log', 'log(x)'),
    ('exp', 'exp(x)'), ('sqrt', 'sqrt(x)'), ('rational', '(x**2 + 1) / (x - 1)'),
    ('piecewise', '{x < 0: x**2, x >= 0: x + 1}'), ('definite', 'integrate(x**2, (x, 0, 1))')
]

for i, (func_name, func_template) in enumerate(functions):
    btn = tb.Button(
        func_buttons_frame,
        text=func_name.capitalize(),  # Capitalize button text
        command=lambda f=func_template: insert_function(f),
        bootstyle="primary-outline"  # Use a predefined style
    )
    btn.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="ew")

# File Upload Button
upload_button = tb.Button(
    control_frame,
    text="Upload File",
    command=upload_file,
    bootstyle="info-outline"
)
upload_button.pack(fill=X, pady=5)

# Add Reset button
reset_button = tb.Button(
    button_frame,
    text="Reset",
    command=reset_app,
    bootstyle="danger"
)
reset_button.pack(side=LEFT, padx=5, pady=5, ipadx=10, ipady=5)

# Set focus and default selections
func_entry.focus()
plot_option.set("Function")
plot_combo.current(0)
derivative_order_var.set(1)  # Set default derivative order to 1

# Initial graph placeholder
placeholder = tb.Label(notebook, text="Graph will appear here", foreground="gray")
placeholder.pack(expand=YES)

root.mainloop()
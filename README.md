# 📈 JustGraphIt!

**JustGraphIt!** is a powerful and user-friendly visual tool for exploring mathematical functions, derivatives, integrals, and piecewise functions — all in one sleek, theme-switchable GUI application built with Python and `ttkbootstrap`.

---

## 🚀 Features

- 📌 **Function Plotting** – Visualize mathematical expressions instantly.
- 🔍 **Derivatives & Integrals** – Show 1st to 3rd-order derivatives and both indefinite and definite integrals.
- 🧩 **Piecewise Support** – Graph complex piecewise functions with ease.
- 🧠 **Symbolic + Numeric** – Uses `SymPy` and `SciPy` for accurate computation.
- 📂 **Function File Upload** – Load multiple functions from `.txt`, `.pdf`, or `.docx` files.
- 🖼️ **Export Graphs** – Save your graphs in PNG, JPEG, PDF, or SVG formats.
- 🌓 **Light/Dark Mode** – Toggle between sleek dark and clean light themes.
- 📚 **Built-in Help Guide** – Easy access to app instructions within the GUI.

---

## 🖼️ Preview

![image](https://github.com/user-attachments/assets/8c9b656a-1d0a-4f11-8b6a-53eaf23d0532)



---

## 🧰 Requirements

Install the required dependencies:

```bash
pip install numpy sympy matplotlib scipy ttkbootstrap pdfplumber python-docx
```

> ✅ Python 3.8 or later is recommended.

---

## 🔧 How to Run

Simply run the script:

```bash
python calculus_graphing_app.py
```

---

## 📂 Supported Function Formats

You can input functions manually or via file upload. Some supported formats:

- `x**2 + 3*x - 2`
- `sin(x) + log(x)`
- `{x < 0: x**2, x >= 0: x + 1}` (Piecewise)
- `exp(x)`, `sqrt(x)`, `tan(x)`, etc.

---

## ⚙️ Options

| Option              | Description                                              |
|---------------------|----------------------------------------------------------|
| **Function**         | Plot only the input function                             |
| **Derivative**       | Plot the derivative (up to 3rd order)                    |
| **Integral**         | Plot the indefinite integral                             |
| **Definite Integral**| Shade area under curve between X-min and X-max          |
| **Piecewise**        | Special rendering for piecewise functions               |
| **Both**             | Combine Function with Derivative/Integral                |

---

## 🧪 Sample Use Case

1. Enter `sin(x) + x**2` into the Function Input field.
2. Set X Range from `-10` to `10`.
3. Choose `Derivative` from the visualization options.
4. Click **Generate Visualization**.
5. Click **Save Graph** to export the image.

---

## 📁 File Upload Format

- `.txt` / `.pdf` / `.docx` files with one function per line.
- Example content:

```
sin(x)
x**2 + 1
{x < 0: -x, x >= 0: x}
```

---

## 💡 Tips

- Use Python syntax: `x**2` (not `x^2`)
- Piecewise functions: `{x < 0: x**2, x >= 0: x + 1}`
- Reset anytime with the **Reset** button.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Credits

Developed with ❤️ using:

- [Python](https://python.org)
- [SymPy](https://www.sympy.org/)
- [Matplotlib](https://matplotlib.org/)
- [SciPy](https://www.scipy.org/)
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [python-docx](https://python-docx.readthedocs.io/)

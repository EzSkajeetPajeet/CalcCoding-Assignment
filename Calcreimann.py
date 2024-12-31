import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def ram_analysis(a, b, n, ram_type):
    def f(x):
        return x**2 + 4*x

    def exact_area(a, b):
        return (b**3 / 3 + 2 * b**2) - (a**3 / 3 + 2 * a**2)

    dx = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    if ram_type == "LRAM":
        x_points = x[:-1]
        area_sum = np.sum(f(x_points) * dx)
    elif ram_type == "RRAM":
        x_points = x[1:]
        area_sum = np.sum(f(x_points) * dx)
    elif ram_type == "MRAM":
        x_points = (x[:-1] + x[1:]) / 2
        area_sum = np.sum(f(x_points) * dx)
    elif ram_type == "TRAM":
        area_sum = (dx / 2) * np.sum(f(x[:-1]) + f(x[1:]))
    else:
        raise ValueError("Invalid RAM type. Choose LRAM, RRAM, MRAM, or TRAM.")

    exact = exact_area(a, b)
    percent_error = abs((exact - area_sum) / exact) * 100

    # Plotting
    plt.figure(figsize=(8, 5))
    if ram_type in ["LRAM", "RRAM", "MRAM"]:
        plt.bar(x_points, f(x_points), width=dx, align='edge', color='purple', edgecolor='black', label=f"{ram_type} Rectangles")
        plt.scatter(x_points, f(x_points), color='black', zorder=5)
    elif ram_type == "TRAM":
        for i in range(n):
            plt.plot([x[i], x[i+1]], [f(x[i]), f(x[i+1])], 'b-')
            plt.fill_between([x[i], x[i+1]], [f(x[i]), f(x[i+1])], color='yellow', alpha=0.5, label="Trapezoid" if i == 0 else "")
    x_plot = np.linspace(a, b, 500)
    plt.plot(x_plot, f(x_plot), 'r-', label="f(x) = x^2 + 4x")

    textstr = f"Exact Area: {exact:.4f}\n{ram_type} Area: {area_sum:.4f}\n% Error: {percent_error:.2f}%"
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(2.05, 21, textstr, fontsize=10, verticalalignment='top', bbox=props)

    plt.title(f"{ram_type} Approximation with {n} Rectangles")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())

st.title("RAM Analysis Tool")
st.markdown("""
Calculates the area under a curve using Riemann Sum approximations (RAM). 
Choose a method and parameters to analyze the function **f(x) = x² + 4x**.
""")

# Input form
with st.form("RAM Parameters"):
    a = st.number_input("Start (a)", value=1.0)
    b = st.number_input("End (b)", value=3.0)
    n = st.number_input("Number of Rectangles (n)", min_value=1, value=4)
    ram_type = st.selectbox("RAM Type", ["LRAM", "RRAM", "MRAM", "TRAM"])
    submitted = st.form_submit_button("Run Analysis")

if submitted:
    try:
        ram_analysis(a, b, n, ram_type)
    except ValueError as e:
        st.error(str(e))

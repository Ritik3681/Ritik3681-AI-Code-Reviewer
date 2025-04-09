import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import random
import matplotlib.animation as animation

# Set your Gemini API Key
GEMINI_API_KEY = "AIzaSyD3z4jYXHVFKR2Tcx57-dwcd0UUGwbxn-E"

def bubble_sort_3d_visualization(arr):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(len(arr))
    y = np.zeros(len(arr))
    bars = ax.bar(x, arr, y, zdir='y', alpha=0.8)

    def update(frame):
        for i in range(len(arr) - frame - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                for bar, height in zip(bars, arr):
                    bar.set_height(height)
        return bars

    ani = animation.FuncAnimation(fig, update, frames=len(arr), repeat=False)
    st.pyplot(fig)

def get_algorithm_code_gemini(algorithm_name, language):
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"Write {language} code for {algorithm_name} with detailed comments."}]}]
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response.")
    else:
        return f"Error: Unable to fetch response ({response.status_code}) - {response.text}"

def get_algorithm_summary(algorithm_name):
    api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{
            "text": f"Provide a detailed explanation of {algorithm_name}, including time and space complexity, real-world applications, and 2-3 examples."}]}]
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response.")
    else:
        return f"Error: Unable to fetch response ({response.status_code}) - {response.text}"

def plot_3d_sorting(array, step, swaps):
    """Generates a 3D visualization of the sorting process"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_pos = np.arange(len(array))
    y_pos = np.zeros(len(array))  # Keep y fixed to zero for bars
    z_pos = np.zeros(len(array))  # Bars start from zero

    dx = np.ones(len(array))  # Width of bars
    dy = np.ones(len(array))  # Depth of bars
    dz = array  # Height represents values

    colors = ['r' if i in swaps else 'c' for i in range(len(array))]
    ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colors, edgecolor='k')

    ax.set_xlabel("Index")
    ax.set_ylabel("Pass")
    ax.set_zlabel("Value")
    ax.set_title(f"Step {step}: Swap {swaps}")

    st.pyplot(fig)
    time.sleep(1)  # Pause to simulate animation

def bubble_sort_3d_visualizer(arr):
    """Bubble sort visualization with 3D representation"""
    arr = arr.copy()
    n = len(arr)
    step = 0

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(len(arr))
    y = np.zeros(len(arr))
    bars = ax.bar(x, arr, y, zdir='y', alpha=0.8)

    def update(frame):
        nonlocal step
        for i in range(len(arr) - frame - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                step += 1
                for bar, height in zip(bars, arr):
                    bar.set_height(height)
        return bars

    ani = animation.FuncAnimation(fig, update, frames=len(arr), repeat=False)
    st.pyplot(fig)

def algorithm_lab_ui():
    st.title("🔬 Algorithm Lab")
    st.write("Generate code, get explanations, and visualize algorithms in 3D!")

    algorithm_name = st.text_input("Enter an algorithm name (e.g., Bubble Sort, Quick Sort, Dijkstra's Algorithm)")
    language = st.selectbox("Choose Programming Language", ["Python", "Java", "C++", "C", "JavaScript", "Go", "Ruby"])

    if algorithm_name.strip():
        tab1, tab2, tab3 = st.tabs(["📜 Generate Code", "📖 Summary", "📊 3D Visualization"])

        with tab1:
            if st.button("Generate Code"):
                with st.spinner("Generating..."):
                    algo_code = get_algorithm_code_gemini(algorithm_name, language)
                    st.subheader(f"Generated {language} Code")
                    st.code(algo_code, language=language.lower())

        with tab2:
            if st.button("Generate Summary"):
                with st.spinner("Generating..."):
                    summary = get_algorithm_summary(algorithm_name)
                    st.subheader("Algorithm Summary")
                    st.write(summary)

        with tab3:
            if st.button("Visualize Algorithm in 3D"):
                if algorithm_name.lower() == "bubble sort":
                    arr = [random.randint(1, 10) for _ in range(5)]
                    bubble_sort_3d_visualizer(arr)
                else:
                    st.write("3D visualization is currently available only for Bubble Sort.")

    st.markdown("---")
    st.write("💡 Use this tool to explore different algorithms and their implementations in various languages!")

algorithm_lab_ui()
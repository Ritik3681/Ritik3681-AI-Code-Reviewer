import streamlit as st
from algorithm_lab import algorithm_lab_ui
from code_analyzer import code_analysis_ui
from transforms import transforms_ui
from integration import integration_ui


st.set_page_config(page_title="AI Code Reviewer", layout="wide")
st.title("🚀 AI Code Reviewer")


tabs = ["Analysis", "Transforms", "Integration", "Algorithm Lab"]
active_tab = st.sidebar.radio("Select a Tab", tabs)

if active_tab == "Analysis":
    code_analysis_ui()

elif active_tab == "Transforms":
    transforms_ui()

elif active_tab == "Integration":
    integration_ui()

elif active_tab == "Algorithm Lab":
    algorithm_lab_ui()

import sys
import os

# Add the project root directory to Python's import search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.agent import debug_code
st.set_page_config(page_title="AI Code Debugging Assistant", page_icon="🐛", layout="wide")

st.title("🐛 AI Code Debugging & Verification Assistant")
st.caption("Identifies bugs, refactors code, generates unit tests, and verifies output in real-time.")

user_code = st.text_area("Paste your Python code here:", height=220, placeholder="def divide(a, b):\n    return a / b\n\nprint(divide(10, 0))")

if st.button("Debug & Run Tests", type="primary"):
    if not user_code.strip():
        st.warning("Please enter code to debug.")
    else:
        with st.spinner("Analyzing code, running tests, and verifying fix..."):
            try:
                result = debug_code(user_code)
                st.markdown("### Debugging Report & Verification")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
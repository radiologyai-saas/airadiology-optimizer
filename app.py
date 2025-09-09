
import streamlit as st
import openai
from key_utils import get_openai_api_key

# 🔐 Secret Key Setup
api_key = get_openai_api_key(getattr(st, "secrets", None))
if api_key:
    openai.api_key = api_key
else:
    st.error(
        "OpenAI API key not provided. Set it via Streamlit secrets or the OPENAI_API_KEY environment variable."
    )

# UI Elements
st.title("🧠 AI Radiology Optimizer")
st.markdown("Enter scan parameters to get GPT-4 powered suggestions.")

# Inputs
modality = st.selectbox("Modality", ["MRI", "CT", "X-Ray"])
sequence = st.text_input("Sequence", "Ax T2 DRIVE")
tr = st.text_input("TR (ms)", "4500")
te = st.text_input("TE (ms)", "110")
matrix = st.text_input("Matrix", "320x256")
fov = st.text_input("FOV", "220")
issue = st.text_area("Scan issue (grainy, motion artifact, etc.)")

if st.button("Get Suggestions"):
    if not api_key:
        st.error("OpenAI API key is required to fetch suggestions.")
    else:
        prompt = f"""Act as an MRI/CT scan optimization expert.
Modality: {modality}
Sequence: {sequence}
TR: {tr}
TE: {te}
Matrix: {matrix}
FOV: {fov}
Issue: {issue}

Suggest 3 protocol changes to improve quality without increasing scan time.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write("### ✅ AI Optimization Suggestions")
        st.write(response['choices'][0]['message']['content'])

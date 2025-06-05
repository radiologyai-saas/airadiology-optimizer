
import streamlit as st
import openai

# 🔐 Secret Key Setup
openai.api_key = st.secrets["OPENAI_API_KEY"]

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

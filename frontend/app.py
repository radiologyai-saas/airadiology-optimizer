"""Streamlit frontend for the Radiology AI platform."""
import requests
import streamlit as st
import openai

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:5000")
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Page",
    ["Optimizer", "Upload & Analyze", "Generate Report", "Leaderboard", "Quiz", "Referral"],
)


if page == "Optimizer":
    st.title("\U0001F9E0 AI Radiology Optimizer")
    st.markdown("Enter scan parameters to get GPT suggestions.")
    modality = st.selectbox("Modality", ["MRI", "CT", "X-Ray"])
    sequence = st.text_input("Sequence", "Ax T2 DRIVE")
    tr = st.text_input("TR (ms)", "4500")
    te = st.text_input("TE (ms)", "110")
    matrix = st.text_input("Matrix", "320x256")
    fov = st.text_input("FOV", "220")
    issue = st.text_area("Scan issue")
    if st.button("Get Suggestions"):
        prompt = f"""Act as an imaging expert.
Modality: {modality}
Sequence: {sequence}
TR: {tr}
TE: {te}
Matrix: {matrix}
FOV: {fov}
Issue: {issue}
Suggest protocol changes.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        st.write(response["choices"][0]["message"]["content"])


elif page == "Upload & Analyze":
    st.title("Upload Scan")
    file = st.file_uploader("Scan image", type=["png", "jpg", "jpeg"])
    if st.button("Analyze") and file:
        resp = requests.post(
            f"{BACKEND_URL}/api/analyze", files={"image": file.getvalue()}
        )
        st.write(resp.json())


elif page == "Generate Report":
    st.title("Generate PDF Report")
    patient = st.text_input("Patient name")
    findings = st.text_area("Findings")
    if st.button("Create PDF"):
        resp = requests.post(
            f"{BACKEND_URL}/api/report", json={"patient": patient, "findings": findings}
        )
        if resp.status_code == 200:
            st.download_button(
                "Download Report",
                data=resp.content,
                file_name=f"{patient.replace(' ', '_')}_report.pdf",
            )
        else:
            st.error("Report generation failed")


elif page == "Leaderboard":
    st.title("Leaderboard")
    resp = requests.get(f"{BACKEND_URL}/api/leaderboard")
    st.table(resp.json())


elif page == "Quiz":
    st.title("Intern Quiz")
    q_resp = requests.get(f"{BACKEND_URL}/api/quiz/question").json()
    st.write(q_resp["question"])
    choice = st.radio("Options", q_resp["options"], index=0)
    if st.button("Submit"):
        idx = q_resp["options"].index(choice)
        a_resp = requests.post(
            f"{BACKEND_URL}/api/quiz/answer",
            json={"id": q_resp["id"], "answer": idx},
        )
        if a_resp.json().get("correct"):
            st.success("Correct!")
        else:
            st.error("Incorrect")


elif page == "Referral":
    st.title("Referral Tracking")
    code = st.text_input("Referral code")
    if st.button("Register"):
        resp = requests.post(f"{BACKEND_URL}/api/referral", json={"code": code})
        data = resp.json()
        st.write(f"Code {data['code']} used {data['count']} times")
    st.markdown("---")
    price_id = st.text_input("Stripe Price ID")
    if st.button("Create Checkout Session"):
        resp = requests.post(
            f"{BACKEND_URL}/api/checkout", json={"price_id": price_id}
        )
        st.write(resp.json())

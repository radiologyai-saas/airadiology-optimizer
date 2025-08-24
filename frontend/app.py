"""Streamlit frontend for the Radiology AI platform."""
import logging
import requests
import streamlit as st
import openai

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:5000")
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4", messages=[{"role": "user", "content": prompt}]
            )
            st.write(response["choices"][0]["message"]["content"])
        except Exception as exc:  # pragma: no cover - network failure
            logger.exception("OpenAI request failed: %s", exc)
            st.error("Suggestion request failed")


elif page == "Upload & Analyze":
    st.title("Upload Scan")
    file = st.file_uploader("Scan image", type=["png", "jpg", "jpeg"])
    if st.button("Analyze") and file:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/analyze", files={"image": file.getvalue()}
            )
            resp.raise_for_status()
            st.write(resp.json())
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Analysis request failed: %s", exc)
            st.error("Analysis failed")


elif page == "Generate Report":
    st.title("Generate PDF Report")
    patient = st.text_input("Patient name")
    findings = st.text_area("Findings")
    if st.button("Create PDF"):
        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/report",
                json={"patient": patient, "findings": findings},
            )
            resp.raise_for_status()
            st.download_button(
                "Download Report",
                data=resp.content,
                file_name=f"{patient.replace(' ', '_')}_report.pdf",
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Report generation failed: %s", exc)
            st.error("Report generation failed")


elif page == "Leaderboard":
    st.title("Leaderboard")
    try:
        resp = requests.get(f"{BACKEND_URL}/api/leaderboard")
        resp.raise_for_status()
        st.table(resp.json())
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Leaderboard fetch failed: %s", exc)
        st.error("Could not load leaderboard")


elif page == "Quiz":
    st.title("Intern Quiz")
    try:
        q_resp = requests.get(f"{BACKEND_URL}/api/quiz/question")
        q_resp.raise_for_status()
        q_data = q_resp.json()
        st.write(q_data["question"])
        choice = st.radio("Options", q_data["options"], index=0)
        if st.button("Submit"):
            idx = q_data["options"].index(choice)
            a_resp = requests.post(
                f"{BACKEND_URL}/api/quiz/answer",
                json={"id": q_data["id"], "answer": idx},
            )
            if a_resp.json().get("correct"):
                st.success("Correct!")
            else:
                st.error("Incorrect")
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Quiz request failed: %s", exc)
        st.error("Could not load quiz")


elif page == "Referral":
    st.title("Referral Tracking")
    code = st.text_input("Referral code")
    if st.button("Register"):
        try:
            resp = requests.post(f"{BACKEND_URL}/api/referral", json={"code": code})
            resp.raise_for_status()
            data = resp.json()
            st.write(f"Code {data['code']} used {data['count']} times")
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Referral register failed: %s", exc)
            st.error("Could not register referral")
    st.markdown("---")
    price_id = st.text_input("Stripe Price ID")
    if st.button("Create Checkout Session"):
        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/checkout", json={"price_id": price_id}
            )
            resp.raise_for_status()
            st.write(resp.json())
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Stripe checkout failed: %s", exc)
            st.error("Stripe checkout failed")

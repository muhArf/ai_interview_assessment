# ============================================================
# 🤖 AI INTERVIEW ASSESSMENT APP (PROFESSIONAL VERSION)
# ============================================================
# Dapat dijalankan lokal atau dideploy ke Streamlit Cloud
# ============================================================

import streamlit as st
import json
import os
from utils.speech_to_text import speech_to_text_from_video
from utils.nlp_scoring import nlp_auto_score

# ------------------------------------------------------------
# 🟩 Setup Aplikasi
# ------------------------------------------------------------
st.set_page_config(page_title="AI Interview Assessment", page_icon="🤖", layout="centered")

st.title("🤖 AI Interview Assessment System")
st.caption("Versi profesional dengan Speech-to-Text + NLP scoring otomatis")

st.info("""
**Tahapan sistem:**
1. Input data kandidat  
2. Upload video wawancara atau masukkan link Google Drive  
3. AI akan menyalin isi video (speech-to-text)  
4. AI menilai isi jawaban menggunakan NLP  
""")

# ------------------------------------------------------------
# 🟩 Input Data Kandidat
# ------------------------------------------------------------
st.header("🧍 Informasi Kandidat")
candidate_name = st.text_input("Nama Lengkap:")
candidate_email = st.text_input("Email:")

# ------------------------------------------------------------
# 🟩 Upload atau Link Video
# ------------------------------------------------------------
st.header("🎥 Upload / Input Video Jawaban")
st.write("Kamu bisa upload video langsung (.mp4) **atau** masukkan link Google Drive.")

interview_questions = [
    "Can you share any specific challenges you faced while working on certification and how you overcame them?",
    "Can you describe your experience with transfer learning in TensorFlow? How did it benefit your projects?",
    "Describe a complex TensorFlow model you have built and the steps you took to ensure its accuracy and efficiency.",
    "Explain how to implement dropout in a TensorFlow model and the effect it has on training.",
    "Describe the process of building a convolutional neural network (CNN) using TensorFlow for image classification."
]

uploaded_videos = []
video_links = []

for i, q in enumerate(interview_questions, start=1):
    st.subheader(f"Pertanyaan {i}")
    st.write(q)
    video_file = st.file_uploader(f"Upload Video #{i}", type=["mp4"], key=f"vid{i}")
    link = st.text_input(f"Atau link Google Drive (opsional) #{i}", key=f"link{i}")
    uploaded_videos.append(video_file)
    video_links.append(link)
    st.divider()

# ------------------------------------------------------------
# 🟩 Proses Speech-to-Text
# ------------------------------------------------------------
if st.button("🧠 Jalankan Speech-to-Text"):
    transcripts = []
    for i, vid in enumerate(uploaded_videos):
        if vid:
            with open(f"temp_{i}.mp4", "wb") as f:
                f.write(vid.read())
            st.info(f"🎧 Mengonversi video {i+1} menjadi teks...")
            text = speech_to_text_from_video(f"temp_{i}.mp4")
            transcripts.append(text)
            os.remove(f"temp_{i}.mp4")
        else:
            transcripts.append("(Tidak ada video, gunakan transkrip kosong)")

    st.session_state["transcripts"] = transcripts
    st.success("✅ Speech-to-Text selesai! Siap dinilai oleh AI.")
    st.write("### 📜 Transkrip Hasil:")
    for i, t in enumerate(transcripts, start=1):
        st.text_area(f"Jawaban {i}", t, height=100)

# ------------------------------------------------------------
# 🟩 Jalankan NLP Scoring
# ------------------------------------------------------------
if "transcripts" in st.session_state and st.button("🚀 Jalankan AI Assessment"):
    result = nlp_auto_score(st.session_state["transcripts"])

    st.success("✅ AI Assessment Selesai!")
    st.metric("Rata-rata Skor", f"{result['average']}%")
    st.metric("Keputusan Akhir", result["decision"])

    st.write("### 📊 Skor Per Pertanyaan:")
    for i, score in enumerate(result["scores"], start=1):
        st.progress(score / 100)
        st.write(f"**Pertanyaan {i}:** {score}%")

    # Simpan hasil ke file JSON
    assessment = {
        "candidate": candidate_name,
        "email": candidate_email,
        "scores": result["scores"],
        "average": result["average"],
        "decision": result["decision"]
    }

    with open("ai_assessment_result.json", "w") as f:
        json.dump(assessment, f, indent=2)

    st.download_button(
        "📥 Unduh Hasil Penilaian (JSON)",
        data=json.dumps(assessment, indent=2),
        file_name="ai_assessment_result.json",
        mime="application/json"
    )

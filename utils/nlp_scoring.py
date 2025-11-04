# utils/nlp_scoring.py
from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F

# Inisialisasi BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_sentence_embedding(text):
    """Mengubah teks menjadi vektor embedding menggunakan BERT."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding

def calculate_similarity(answer_text, ideal_text):
    """Menghitung kesamaan antara jawaban kandidat dan jawaban ideal."""
    emb1 = get_sentence_embedding(answer_text)
    emb2 = get_sentence_embedding(ideal_text)
    similarity = F.cosine_similarity(emb1, emb2)
    return round(similarity.item() * 100, 2)

def nlp_auto_score(transcripts):
    """Memberi skor otomatis ke tiap jawaban berdasarkan kemiripan semantik."""
    ideal_answers = [
        "Overcoming challenges in deep learning projects by improving data preprocessing and model tuning.",
        "Transfer learning in TensorFlow improves model accuracy and reduces training time.",
        "Building complex CNN models using TensorFlow and validating with accuracy metrics.",
        "Implementing dropout in TensorFlow helps prevent overfitting and improves generalization.",
        "Building CNNs for image classification involves convolutional, pooling, and softmax layers."
    ]

    scores = []
    total = 0

    for transcript, ideal in zip(transcripts, ideal_answers):
        sim = calculate_similarity(transcript, ideal)
        scores.append(sim)
        total += sim

    avg = round(total / len(scores), 2)
    decision = "PASSED" if avg >= 70 else "FAILED"

    return {
        "scores": scores,
        "average": avg,
        "decision": decision
    }

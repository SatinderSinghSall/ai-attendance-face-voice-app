import io
import numpy as np
import librosa
import streamlit as st
from resemblyzer import VoiceEncoder, preprocess_wav


# ============================================================
# Load and cache the Resemblyzer voice encoder model
# This prevents the model from reloading on every Streamlit run
# ============================================================
@st.cache_resource
def load_voice_encoder():
    """
    Loads and caches the Resemblyzer VoiceEncoder model.
    
    Returns:
        VoiceEncoder: Pretrained voice embedding encoder
    """
    return VoiceEncoder()


# ============================================================
# Generate a voice embedding from raw audio bytes
# ============================================================
def get_voice_embedding(audio_bytes):
    """
    Converts raw audio bytes into a voice embedding vector.

    Steps:
    1. Load audio using librosa
    2. Preprocess audio using Resemblyzer
    3. Generate speaker embedding

    Args:
        audio_bytes (bytes): Raw audio data

    Returns:
        list | None: Voice embedding vector or None if failure
    """

    try:
        encoder = load_voice_encoder()

        # Load audio and resample to 16kHz
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        # Normalize and preprocess audio
        wav = preprocess_wav(audio)

        # Generate embedding
        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None


# ============================================================
# Identify speaker using cosine similarity
# ============================================================
def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    """
    Identifies the speaker by comparing the new embedding with
    stored candidate embeddings using cosine similarity.

    Args:
        new_embedding (array-like): New voice embedding
        candidates_dict (dict): {student_id: stored_embedding}
        threshold (float): Similarity threshold for identification

    Returns:
        tuple:
            best_sid (int | None): Identified student ID
            best_score (float): Similarity score
    """

    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    new_embedding = np.array(new_embedding)

    for sid, stored_embedding in candidates_dict.items():

        if stored_embedding is not None:

            stored_embedding = np.array(stored_embedding)

            # Cosine similarity
            similarity = np.dot(new_embedding, stored_embedding) / (
                np.linalg.norm(new_embedding) * np.linalg.norm(stored_embedding)
            )

            if similarity > best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


# ============================================================
# Process bulk classroom audio to detect multiple speakers
# ============================================================
def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    """
    Processes classroom audio to detect multiple speakers.

    Steps:
    1. Split audio into non-silent segments
    2. Generate embeddings for each segment
    3. Match embeddings with stored student voices
    4. Return best matches per student

    Args:
        audio_bytes (bytes): Raw audio recording
        candidates_dict (dict): {student_id: voice_embedding}
        threshold (float): Similarity threshold

    Returns:
        dict: {student_id: similarity_score}
    """

    try:
        encoder = load_voice_encoder()

        # Load and resample audio
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

        # Detect non-silent segments
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:

            # Ignore very short segments (< 0.5 seconds)
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]

            # Preprocess segment
            wav = preprocess_wav(segment_audio)

            # Generate embedding
            embedding = encoder.embed_utterance(wav)

            # Identify speaker
            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:

                # Keep highest score per student
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results

    except Exception as e:
        st.error(f"Bulk voice processing error: {e}")
        return {}


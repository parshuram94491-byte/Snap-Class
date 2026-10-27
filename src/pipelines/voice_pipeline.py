import numpy as np 
import io
import importlib
import streamlit as st


def _load_librosa():
    try:
        return importlib.import_module("librosa")
    except ImportError as exc:
        raise RuntimeError(
            "Voice recognition requires librosa. Install the project dependencies "
            "with '.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt'."
        ) from exc


@st.cache_resource
def load_voice_models():
    try:
        from resemblyzer import VoiceEncoder, preprocess_wav
    except ImportError as exc:
        raise RuntimeError(
            "Voice recognition is unavailable because its native dependencies "
            "could not be loaded."
        ) from exc

    return VoiceEncoder(), preprocess_wav

def get_voice_embedding(audio_bytes):
    try:
        librosa = _load_librosa()
        encoder, preprocess_wav = load_voice_models()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except RuntimeError as exc:
        st.error(str(exc))
        return None
    except Exception as e:
        st.error('Voice recog error')
        return None
    

def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0
    
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity> best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score



def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):

    try:
        librosa = _load_librosa()
        encoder, preprocess_wav = load_voice_models()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}


        for start, end in segments:

            if (end-start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)


            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except RuntimeError:
        raise
    except Exception as e:
        st.error('Bulk process error')
        return {}
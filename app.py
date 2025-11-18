import streamlit as st
import subprocess
import json
import os
from PIL import Image

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Multi-Detektor AI", layout="wide")
st.title("Const AI - Multi-Detektor AI (Gambar, Video, Teks, Audio)")
st.write("Alat deteksi jarvis 😈")
st.write("Note: hasil deteksi tidak 100% benar")

# --- Fungsi Helper ---

def save_uploaded_file(uploaded_file):
    """Menyimpan file yang di-upload ke folder temp."""
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def run_detection(command_list):
    """Menjalankan subprocess dan mengembalikan data JSON."""
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True,
            timeout=120  # Timeout 120 detik untuk video
        )
        output_str = result.stdout.strip()
        
        # Membersihkan output jika ada noise
        if not output_str.startswith("{"):
            output_str = "{" + output_str.split("{", 1)[-1]
        
        data = json.loads(output_str)
        return data
        
    except subprocess.CalledProcessError as e:
        return {"error": f"Skrip gagal: {e.stderr}"}
    except json.JSONDecodeError:
        return {"error": "Gagal mem-parsing JSON.", "raw_output": result.stdout.strip()}
    except Exception as e:
        return {"error": f"Terjadi error: {e}"}

def display_results(data):
    """Menampilkan hasil JSON di Streamlit."""
    if "error" in data:
        st.error(f"**Error:** {data['error']}")
        if "raw_output" in data:
            st.code(data['raw_output'], language="text")
        return

    verdict = data.get("verdict", "Tidak diketahui")
    confidence = float(data.get("confidence", 0.0))
    reasoning = data.get("reasoning", "Tidak ada alasan.")
    
    if verdict.lower() == "ai" or verdict.lower() == "nsfw":
        st.error(f"**Hasil: Terdeteksi {verdict.upper()}**")
    else:
        st.success(f"**Hasil: Terdeteksi {verdict.upper()}**")

    st.subheader(f"Tingkat Keyakinan: {confidence * 100:.1f}%")
    st.progress(confidence)
    
    st.subheader("Alasan:")
    st.info(reasoning)
    
    with st.expander("Lihat output JSON mentah"):
        st.json(data)

# --- TABS ---
tab_img, tab_vid, tab_txt, tab_aud = st.tabs(["🖼️ Deteksi Gambar", "🎬 Deteksi Video", "✍️ Deteksi Teks", "🎧 Deteksi Audio"])

# --- TAB 1: Deteksi Gambar ---
with tab_img:
    st.header("Analisis Gambar (AI vs Real / NSFW)")
    
    uploaded_image = st.file_uploader("Pilih file gambar", type=["jpg", "jpeg", "png"], key="img_uploader")
    task_image = st.selectbox(
        "Pilih Tugas Analisis:",
        ("AI vs Real", "Deteksi NSFW"),
        key="img_task"
    )
    
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Gambar yang Di-upload", use_container_width=True)
        
        if st.button("Analisis Gambar Ini", key="img_button"):
            temp_path = save_uploaded_file(uploaded_image)
            
            if task_image == "AI vs Real":
                script_to_run = "aidetect_image.py"
            else:
                script_to_run = "nsfwdetect_image.py"
            
            command = ["python", script_to_run, "--path", temp_path]
            
            with st.spinner(f"Const sedang menganalisis gambar untuk {task_image}..."):
                results = run_detection(command)
                display_results(results)
                os.remove(temp_path)

# --- TAB 2: Deteksi Video ---
with tab_vid:
    st.header("Analisis Video (AI vs Real / NSFW)")
    
    uploaded_video = st.file_uploader("Pilih file video", type=["mp4", "mov", "webm", "avi"], key="vid_uploader")
    task_video = st.selectbox(
        "Pilih Tugas Analisis:",
        ("AI vs Real", "Deteksi NSFW"),
        key="vid_task"
    )
    
    if uploaded_video is not None:
        st.video(uploaded_video)
        
        if st.button("Analisis Video Ini", key="vid_button"):
            temp_path = save_uploaded_file(uploaded_video)

            if task_video == "AI vs Real":
                script_to_run = "aidetect_video.py"
            else: 
                script_to_run = "nsfwdetect_video.py"

            command = ["python", script_to_run, "--path", temp_path]
            
            with st.spinner(f"Const sedang menganalisis video untuk {task_video}... (Mungkin butuh waktu lama)"):
                results = run_detection(command)
                display_results(results)
                os.remove(temp_path)

# --- TAB 3: Deteksi Teks ---
with tab_txt:
    st.header("Analisis Teks (AI vs Real)")
    
    user_text = st.text_area("Masukkan teks yang ingin dianalisis:", height=250, key="txt_area")
    
    if st.button("Analisis Teks Ini", key="txt_button") and user_text:
        with st.spinner("Const sedang menganalisis teks..."):
            command = ["python", "textdetection.py", "--text", user_text]
            results = run_detection(command)
            display_results(results)

# --- TAB 4: Deteksi Audio ---
with tab_aud:
    st.header("Analisis Audio (AI vs Real)")
    st.write("Deteksi ini mencoba mengidentifikasi apakah audio adalah suara manusia asli atau hasil *voice cloning* AI.")
    
    uploaded_audio = st.file_uploader(
        "Pilih file audio", 
        type=["mp3", "wav", "m4a", "flac"], 
        key="aud_uploader"
    )
    
    if uploaded_audio is not None:
        st.audio(uploaded_audio)
        
        if st.button("Analisis Audio Ini", key="aud_button"):
            temp_path = save_uploaded_file(uploaded_audio)
            
            script_to_run = "aidetect_audio.py"
            command = ["python", script_to_run, "--path", temp_path]
            
            with st.spinner("Const sedang menganalisis audio... (Mungkin butuh waktu lama)"):
                results = run_detection(command)
                display_results(results)
                os.remove(temp_path)
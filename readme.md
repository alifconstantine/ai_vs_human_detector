# Const AI - Multi-Detektor AI

**AI vs Human Detector**

Const AI adalah sebuah aplikasi web yang dibangun dengan Streamlit untuk mendeteksi konten buatan AI dan konten NSFW (Not Safe For Work). Aplikasi ini menggunakan model Google Gemini 2.5 Flash untuk melakukan analisis pada berbagai jenis media, termasuk gambar, video, audio, dan teks.

![Demo Aplikasi Const AI](https://github.com/alifconstantine/ai_vs_human_detector/blob/main/image/preview.png)

---

## ✨ Fitur Utama

* **🖼️ Deteksi Gambar:**
    * **AI vs. Real:** Menganalisis apakah gambar dibuat oleh AI atau foto asli.
    * **NSFW vs. Safe:** Menganalisis apakah gambar mengandung konten sensitif/dewasa.

* **🎬 Deteksi Video:**
    * **AI vs. Real:** Menganalisis apakah video adalah *deepfake* atau rekaman asli.
    * **NSFW vs. Safe:** Menganalisis apakah video mengandung adegan sensitif/dewasa.

* **🎧 Deteksi Audio:**
    * **AI vs. Real:** Menganalisis apakah audio adalah suara manusia asli atau hasil *voice cloning* AI.

* **✍️ Deteksi Teks:**
    * **AI vs. Real:** Menganalisis apakah teks ditulis oleh AI atau manusia.

---


## Prasyarat

- Python **3.10+** (disarankan)
- Koneksi internet
- API Key Google Gemini:
  - Buat API key dari Google AI Studio (Gemini)
  - Simpan di file `.env` sebagai `GOOGLE_API_KEY`


## 💻 Tumpukan Teknologi (Tech Stack)

* **Frontend:** Streamlit
* **Backend & Logic:** Python
* **AI Model:** Google Gemini 2.5 Flash API
* **Libraries:** `google-generativeai`, `pillow`, `python-dotenv`, `streamlit`

---

## 🚀 Instalasi dan Cara Menjalankan

Ikuti langkah-langkah ini untuk menjalankan proyek di komputer lokal kamu.

### 1. Clone Repositori
Pertama, clone repositori ini ke mesin lokal kamu.

```bash
git clone https://github.com/alifconstantine/ai_vs_human_detector.git
cd ai_vs_human_detector

import sys
import os
import json
import argparse
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print(json.dumps({"error": "GOOGLE_API_KEY tidak ditemukan."}))
    sys.exit(1)

model = genai.GenerativeModel('gemini-3-pro')

PROMPT_AI_VS_REAL = """
Kamu adalah sistem ahli analisis gambar yang bertugas mendeteksi apakah sebuah gambar
dibuat oleh AI (Artificial Intelligence) atau foto asli (real).
Analisis gambar yang diberikan dan berikan jawaban HANYA dalam format JSON.
Struktur JSON:
{
  "verdict": "ai" | "real",
  "confidence": <angka_desimal_antara_0.0_hingga_1.0>,
  "reasoning": "<alasan_singkat_di_balik_keputusanmu>"
}
"""

def analyze_image(image_path):
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(json.dumps({"error": f"Gagal membuka gambar: {e}"}))
        sys.exit(1)

    generation_config = genai.GenerationConfig(response_mime_type="application/json")

    try:
        response = model.generate_content(
            [PROMPT_AI_VS_REAL, img],
            generation_config=generation_config
        )
        print(response.text.strip())
    except Exception as e:
        print(json.dumps({"error": f"Error API Gemini: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detektor Gambar AI")
    parser.add_argument("--path", type=str, required=True, help="Path ke file gambar")
    args = parser.parse_args()
    analyze_image(args.path)

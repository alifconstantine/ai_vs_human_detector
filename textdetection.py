import sys
import os
import json
import argparse
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print(json.dumps({"error": "GOOGLE_API_KEY tidak ditemukan."}))
    sys.exit(1)

model = genai.GenerativeModel('gemini-2.5-flash')

PROMPT_AI_VS_REAL = """
Kamu adalah sistem ahli analisis teks yang bertugas mendeteksi apakah sebuah teks
ditulis oleh AI (Artificial Intelligence) atau manusia (real).
Analisis gaya bahasa, konsistensi, dan keanehan yang mungkin muncul dari AI.
Berikan jawaban HANYA dalam format JSON.
Struktur JSON:
{
  "verdict": "ai" | "real",
  "confidence": <angka_desimal_antara_0.0_hingga_1.0>,
  "reasoning": "<alasan_singkat_di_balik_keputusanmu>"
}
"""

def analyze_text(user_text):
    generation_config = genai.GenerationConfig(response_mime_type="application/json")

    try:
        response = model.generate_content(
            [PROMPT_AI_VS_REAL, user_text],
            generation_config=generation_config
        )
        print(response.text.strip())
    except Exception as e:
        print(json.dumps({"error": f"Error API Gemini: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detektor Teks AI")
    parser.add_argument("--text", type=str, required=True, help="Teks yang akan dianalisis")
    
    args = parser.parse_args()
    
    analyze_text(args.text)
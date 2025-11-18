import sys
import os
import json
import argparse
import google.generativeai as genai
import time
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print(json.dumps({"error": "GOOGLE_API_KEY tidak ditemukan."}))
    sys.exit(1)

model = genai.GenerativeModel('gemini-2.5-flash')

PROMPT_AI_VS_REAL = """
Kamu adalah sistem ahli analisis audio yang bertugas mendeteksi apakah sebuah file audio
adalah suara manusia asli (real) atau hasil kloning suara/AI (ai).
Analisis audio yang diberikan. Cari keanehan seperti nada robotik, intonasi yang datar, 
artefak digital (glitch), atau pola napas yang tidak alami.
Berikan jawaban HANYA dalam format JSON.

Struktur JSON:
{
  "verdict": "ai" | "real",
  "confidence": <angka_desimal_antara_0.0_hingga_1.0>,
  "reasoning": "<alasan_singkat_di_balik_keputusanmu, misal 'Intonasi terdengar sangat alami.' atau 'Terdengar ada artefak digital dan nada yang monoton.'>"
}
"""

def analyze_audio(audio_path):
    try:
        audio_file = genai.upload_file(path=audio_path)
        
        while audio_file.state.name == "PROCESSING":
            time.sleep(2)
            audio_file = genai.get_file(audio_file.name)
            
        if audio_file.state.name == "FAILED":
            print(json.dumps({"error": "Gagal memproses file audio"}))
            sys.exit(1)
            
        generation_config = genai.GenerationConfig(response_mime_type="application/json")

        response = model.generate_content(
            [PROMPT_AI_VS_REAL, audio_file],
            generation_config=generation_config
        )

        genai.delete_file(audio_file.name)
        
        print(response.text.strip())

    except Exception as e:
        print(json.dumps({"error": f"Error API Gemini: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detektor Audio AI")
    parser.add_argument("--path", type=str, required=True, help="Path ke file audio")
    args = parser.parse_args()
    analyze_audio(args.path)
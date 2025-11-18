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

PROMPT_NSFW_DETECTION = """
Kamu adalah sistem moderasi konten yang sangat akurat.
Analisis video yang diberikan untuk konten Not Safe For Work (NSFW).
Kategori NSFW mencakup: pornografi, ketelanjangan eksplisit, kekerasan grafis, atau gore.
Berikan jawaban HANYA dalam format JSON.
Struktur JSON:
{
  "verd_ict": "nsfw" | "safe",
  "confidence": <angka_desimal_antara_0.0_hingga_1.0>,
  "reasoning": "<alasan_singkat_di_balik_keputusanmu, misal 'Video aman.' atau 'Video mengandung kekerasan grafis.'>"
}
"""

def analyze_video(video_path):
    try:
        video_file = genai.upload_file(path=video_path)
        
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
            
        if video_file.state.name == "FAILED":
            print(json.dumps({"error": "Gagal memproses file video"}))
            sys.exit(1)
            
        generation_config = genai.GenerationConfig(response_mime_type="application/json")

        response = model.generate_content(
            [PROMPT_NSFW_DETECTION, video_file],
            generation_config=generation_config
        )
        
        genai.delete_file(video_file.name)
        print(response.text.strip())

    except Exception as e:
        print(json.dumps({"error": f"Error API Gemini: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detektor Video NSFW")
    parser.add_argument("--path", type=str, required=True, help="Path ke file video")
    args = parser.parse_args()
    analyze_video(args.path)
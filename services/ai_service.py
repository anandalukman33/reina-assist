import google.generativeai as genai
import config
import json
import re

class GeminiService:
    def __init__(self):
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_audio(self, audio_path):
        try:
            audio_file = genai.upload_file(path=audio_path, mime_type="audio/wav")
            
            prompt = """
            Kamu adalah asisten meeting profesional.
            Tugas:
            1. Transkripsikan apa yang diucapkan user (Bahasa Indonesia).
            2. Berikan 3 poin tanggapan cerdas/saran singkat.
            
            Output HARUS format JSON murni tanpa markdown code block:
            {
                "transcript": "teks ucapan user...",
                "response": "tanggapan kamu (gunakan markdown bold/italic jika perlu)..."
            }
            """
            
            result = self.model.generate_content([prompt, audio_file])
            text_result = result.text.strip()
            
            text_result = re.sub(r'^```json\s*', '', text_result)
            text_result = re.sub(r'^```\s*', '', text_result)
            text_result = re.sub(r'\s*```$', '', text_result)
            
            return json.loads(text_result)
            
        except json.JSONDecodeError:
            return {
                "transcript": "Gagal parsing JSON", 
                "response": result.text
            }
        except Exception as e:
            return {"error": str(e)}
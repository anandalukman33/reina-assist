import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("API Key tidak ditemukan! Pastikan file .env sudah dibuat.")

TEMP_FILENAME = "temp_gui_rec.wav"
SAMPLE_RATE = 44100 #untuk windows = 16000
CHUNK_SIZE = 1024

WINDOW_SIZE = "400x600"
BG_COLOR = "#1e1e1e"
TEXT_BG_COLOR = "#252526"
TEXT_FG_COLOR = "#d4d4d4"

LOG_COLOR_SUCCESS = "#4caf50"
LOG_COLOR_INFO = "#ffeb3b"
LOG_COLOR_ERROR = "#ff5252"
LOG_COLOR_DEFAULT = "#ffffff"
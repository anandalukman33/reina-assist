import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import keyboard
import time
import os
from datetime import datetime

import config
from utils import insert_markdown_text
from services.audio_service import AudioService
from services.ai_service import GeminiService

class MeetingAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        self.is_running = True
        self.is_recording = False
        self.current_device_index = None
        self.chat_counter = 0
        
        self.setup_ui_components()
        
        try:
            self.audio_service = AudioService()
            self.system_log("Audio Service started", "success")
            self.ai_service = GeminiService()
            self.system_log("Gemini AI Service connected", "success")
            
            devices = self.audio_service.get_input_devices()
            self.combo_device['values'] = devices
            if devices:
                self.combo_device.current(0)
                self.current_device_index = self.audio_service.get_device_index(devices[0])
                
        except Exception as e:
            self.system_log(f"Init Error: {e}", "error")
        
        self.thread = threading.Thread(target=self.logic_loop, daemon=True)
        self.thread.start()

    def setup_window(self):
        self.root.title("AI Meeting Assistant - Lukman Edition")
        self.root.geometry(config.WINDOW_SIZE)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        self.root.configure(bg=config.BG_COLOR)

    def setup_ui_components(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background=config.BG_COLOR, foreground="white")
        
        self.lbl_status = ttk.Label(self.root, text="STANDBY (Hold SHIFT)", font=("Arial", 10, "bold"))
        self.lbl_status.pack(pady=(10, 5))
        self.volume_bar = ttk.Progressbar(self.root, orient="horizontal", length=350, mode="determinate")
        self.volume_bar.pack(pady=5)
        
        f_device = tk.Frame(self.root, bg=config.BG_COLOR)
        f_device.pack(pady=5)
        ttk.Label(f_device, text="Mic: ").pack(side=tk.LEFT)
        self.combo_device = ttk.Combobox(f_device, width=35, state="readonly")
        self.combo_device.pack(side=tk.LEFT)
        self.combo_device.bind("<<ComboboxSelected>>", self.on_device_change)
        
        ttk.Label(self.root, text="AI Suggestions:").pack(pady=(5,0), anchor="w", padx=10)
        self.txt_output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=45, height=12,
            bg=config.TEXT_BG_COLOR, fg=config.TEXT_FG_COLOR, font=("Consolas", 10),
            padx=10, pady=10
        )
        self.setup_text_tags(self.txt_output)
        self.txt_output.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.txt_output.insert(tk.END, "Siap merekam...\n")

        ttk.Label(self.root, text="System Log:").pack(pady=(5,0), anchor="w", padx=10)
        self.txt_log = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=45, height=6,
            bg="#000000", fg="#bbbbbb", font=("Consolas", 8)
        )
        self.txt_log.tag_configure("success", foreground=config.LOG_COLOR_SUCCESS)
        self.txt_log.tag_configure("info", foreground=config.LOG_COLOR_INFO)
        self.txt_log.tag_configure("error", foreground=config.LOG_COLOR_ERROR)
        self.txt_log.pack(padx=10, pady=(0, 10), fill=tk.X)

    def setup_text_tags(self, widget):
        widget.tag_configure("bold", font=("Consolas", 10, "bold"))
        widget.tag_configure("italic", font=("Consolas", 10, "italic"))
        widget.tag_configure("underline", font=("Consolas", 10, "underline"))

        widget.tag_configure("meta_info", foreground="#888888", font=("Consolas", 8))
        widget.tag_configure("separator", foreground="#444444")

    def system_log(self, message, level="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.txt_log.insert(tk.END, f"[{timestamp}] {message}\n", level)
        self.txt_log.see(tk.END)

    def on_device_change(self, event):
        name = self.combo_device.get()
        self.current_device_index = self.audio_service.get_device_index(name)
        self.system_log(f"Device: {name}", "info")

    def toggle_transcript(self, tag_name, btn_widget):
        is_hidden = self.txt_output.tag_cget(tag_name, "elide")
        
        if str(is_hidden) == '1' or is_hidden is True:
            self.txt_output.tag_configure(tag_name, elide=False)
            btn_widget.config(text="[-] Hide Request")
        else:
            self.txt_output.tag_configure(tag_name, elide=True)
            btn_widget.config(text="[+] Show Request")

    def add_chat_bubble(self, transcript, response, duration):
        """Menambahkan bubble chat dengan separator dan collapsible request"""
        self.chat_counter += 1
        tag_id = f"request_{self.chat_counter}"
        
        timestamp = datetime.now().strftime("%d-%m %H:%M")
        
        self.txt_output.insert(tk.END, "\n" + "-"*45 + "\n", "separator")
        
        meta_text = f"📅 {timestamp} | ⏱️ {duration:.2f}s\n"
        self.txt_output.insert(tk.END, meta_text, "meta_info")
        
        btn_toggle = tk.Button(self.txt_output, text="[+] Show Request", 
                               font=("Consolas", 8), cursor="hand2", bg="#333", fg="white", bd=0,
                               activebackground="#444", activeforeground="white")
        
        btn_toggle.config(command=lambda: self.toggle_transcript(tag_id, btn_toggle))
        
        self.txt_output.window_create(tk.END, window=btn_toggle)
        self.txt_output.insert(tk.END, "\n")
        
        self.txt_output.insert(tk.END, f"{transcript}\n", tag_id)
        self.txt_output.tag_configure(tag_id, elide=True, foreground="#aaaaaa", lmargin1=20)
        
        self.txt_output.insert(tk.END, "\n") # Spacer
        insert_markdown_text(self.txt_output, response)
        self.txt_output.insert(tk.END, "\n")
        
        self.txt_output.see(tk.END)

    def process_ai_response(self, audio_path):
        start_time = time.time()
        
        self.lbl_status.config(text="AI THINKING...", foreground="#00ff00")
        self.system_log("Sending audio to AI...", "info")
        
        result_data = self.ai_service.analyze_audio(audio_path)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if "error" in result_data:
            self.system_log(result_data["error"], "error")
            self.txt_output.insert(tk.END, f"\n[ERROR] {result_data['error']}\n")
        else:
            self.system_log("Response received", "success")
            
            transcript = result_data.get("transcript", "-")
            response = result_data.get("response", "-")
            
            self.add_chat_bubble(transcript, response, duration)
        
        self.lbl_status.config(text="STANDBY (Hold SHIFT)", foreground="white")
        self.volume_bar['value'] = 0

    def logic_loop(self):
        while self.is_running:
            if keyboard.is_pressed('left_shift'):
                if not self.is_recording:
                    self.start_recording_session()
            time.sleep(0.05)

    def start_recording_session(self):
        self.is_recording = True
        self.lbl_status.config(text="● RECORDING...", foreground="#ff0000")
        self.system_log("Recording started...", "info")
        
        audio_frames = []
        try:
            stream = self.audio_service.create_stream(self.current_device_index)
            while keyboard.is_pressed('left_shift'):
                try:
                    data = stream.read(config.CHUNK_SIZE, exception_on_overflow=False)
                    audio_frames.append(data)
                    vol = self.audio_service.calculate_volume(data)
                    self.volume_bar['value'] = vol
                except:
                    break
            stream.stop_stream()
            stream.close()

            saved_path = self.audio_service.save_wav(audio_frames)
            self.system_log(f"Audio captured ({len(audio_frames)} chunks)", "success")
            
            threading.Thread(target=self.process_ai_response, args=(saved_path,)).start()

        except Exception as e:
            self.system_log(f"Rec Error: {e}", "error")
        
        self.is_recording = False

    def on_closing(self):
        self.is_running = False
        try:
            self.audio_service.terminate()
        except:
            pass
        self.root.destroy()
        os._exit(0)
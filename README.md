# Reina Assist (AI Assistant)

**Reina Assist** adalah aplikasi asisten pintar berbasis desktop yang dirancang untuk membantu produktivitasmu. Aplikasi ini dapat merekam percakapan secara *real-time*, mentranskripsikannya ke dalam Bahasa Indonesia, dan memberikan poin-poin tanggapan atau saran cerdas menggunakan kecerdasan buatan **Google Gemini**.

## 👤 Author
**Ananda Muhamad Lukman (Park Yasha)**

---

## 👤 Linux User Baca Ini
Pilih Branch Linux untuk menggunakannya

---

## ✨ Fitur Utama
* **🎙️ Push-to-Talk Recording:** Tekan dan tahan tombol `Left Shift` untuk merekam suara, sehingga hanya poin penting yang masuk.
* **🤖 Integrasi Gemini AI:** Menggunakan model `gemini-2.5-flash` untuk transkripsi akurat dan analisis konteks yang cepat.
* **📝 Transkripsi & Saran:** Otomatis menghasilkan teks ucapan dan 3 poin saran/tanggapan cerdas.
* **⚙️ Pengaturan Audio:** Mendeteksi dan memilih perangkat mikrofon yang tersedia secara otomatis.
* **🖥️ Antarmuka Modern:** GUI berbasis Tkinter dengan tema gelap (Dark Mode) yang nyaman di mata, lengkap dengan log sistem.

---

## 🛠️ Prasyarat (Requirements)
Pastikan komputer kamu sudah terinstall:
1.  **Python 3.10** atau versi lebih baru.
2.  Koneksi Internet (untuk akses API Gemini).
3.  Microphone yang berfungsi.

---

## 📦 Cara Instalasi

1.  **Clone atau Download** repository ini ke komputer kamu.

2.  **Install Library** yang dibutuhkan. Buka terminal/command prompt di folder proyek dan jalankan perintah berikut:
    ```bash
    pip install google-generativeai python-dotenv pyaudio keyboard
    ```
    *(Catatan: `tkinter` biasanya sudah terinstall otomatis bersama Python. Jika kamu menggunakan Linux, kamu mungkin perlu menginstall `python3-tk` secara manual).*

3.  **Konfigurasi API Key**:
    * Dapatkan API Key dari [Google AI Studio](https://aistudio.google.com/).
    * Buat file baru bernama `.env` di dalam folder utama proyek.
    * Isi file `.env` tersebut dengan format berikut:
        ```env
        GEMINI_API_KEY=masukkan_api_key_kamu_disini
        ```

---

## 🚀 Cara Menjalankan Aplikasi

1.  Buka terminal di folder proyek.
2.  Jalankan file utama:
    ```bash
    python main.py
    ```
3.  Jendela aplikasi **"AI Meeting Assistant - Lukman Edition"** akan muncul.

---

## 🎮 Cara Penggunaan

1.  **Pilih Mikrofon:** Pastikan mikrofon yang benar sudah terpilih pada menu *dropdown* "Mic".
2.  **Merekam:**
    * Tahan tombol **Shift Kiri (Left Shift)** pada keyboard untuk mulai berbicara/merekam.
    * Status akan berubah menjadi merah (**RECORDING...**).
3.  **Memproses:**
    * Lepaskan tombol Shift saat selesai bicara.
    * Aplikasi akan otomatis mengirim audio ke AI (Status: **AI THINKING...**).
4.  **Hasil:**
    * Transkripsi dan saran AI akan muncul di kolom teks utama.
    * Kamu bisa menyembunyikan/menampilkan teks asli (transkrip) dengan tombol `[+] Show Request` / `[-] Hide Request`.

---

## 📂 Struktur Proyek
* `main.py`: Titik masuk (entry point) aplikasi.
* `config.py`: Pengaturan konfigurasi (API Key, warna UI, audio settings).
* `ui/`: Berisi kode antarmuka (GUI) aplikasi.
* `services/`: Logika untuk Audio dan integrasi AI (Gemini).
* `utils.py`: Fungsi bantuan untuk formatting teks.

---

*Dibuat dengan ❤️ oleh Ananda Muhamad Lukman (Park Yasha)*

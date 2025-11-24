import pyaudio
import struct
import sys
import time
from colorama import init, Fore, Style

init(autoreset=True)

def list_devices(p):
    print(f"\n{Fore.CYAN}=== DAFTAR DEVICE AUDIO DI WINDOWS KAMU ==={Style.RESET_ALL}")
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    valid_devices = []
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            name = device_info.get('name')
            print(f"Index {Fore.YELLOW}[{i}]{Style.RESET_ALL} : {name}")
            valid_devices.append(i)
    return valid_devices

def visual_monitor(device_index):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=CHUNK)
        
        print(f"\n{Fore.GREEN}>>> MEMONITOR DEVICE INDEX {device_index}...{Style.RESET_ALL}")
        print("Coba bicara atau putar lagu sekarang!")
        print(f"{Fore.RED}[Tekan CTRL+C untuk Berhenti]{Style.RESET_ALL}\n")
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            shorts = struct.unpack(f"{CHUNK}h", data)
            peak = max(shorts)
            
            bars = "█" * int(peak / 500) 
            
            if len(bars) > 50: bars = bars[:50]
            
            if peak < 500:
                print(f"\rVolume: {Fore.BLUE}[HENING] {peak:05d}{Style.RESET_ALL}", end="")
            elif peak < 10000:
                print(f"\rVolume: {Fore.GREEN}{bars:<50} {Style.RESET_ALL}({peak})", end="")
            else:
                print(f"\rVolume: {Fore.RED}{bars:<50} {Style.RESET_ALL}({peak})", end="")
                
    except OSError as e:
        print(f"\n\n{Fore.RED}[ERROR] Gagal membuka device ini!{Style.RESET_ALL}")
        print(f"Pesan: {e}")
        print("Kemungkinan device sedang dipakai eksklusif oleh aplikasi lain atau driver bermasalah.")
        
    except KeyboardInterrupt:
        print("\n\nTest Selesai.")
    finally:
        try:
            stream.stop_stream()
            stream.close()
            p.terminate()
        except:
            pass

if __name__ == "__main__":
    p = pyaudio.PyAudio()
    valid_ids = list_devices(p)
    p.terminate()
    
    if not valid_ids:
        print(f"{Fore.RED}Tidak ada input device yang terdeteksi!{Style.RESET_ALL}")
    else:
        try:
            choice = int(input(f"\n{Fore.WHITE}Masukkan Nomor Index Device yang mau dites: {Style.RESET_ALL}"))
            if choice in valid_ids:
                visual_monitor(choice)
            else:
                print("Nomor tidak ada di daftar.")
        except ValueError:
            print("Harus masukkan angka.")
import pyaudio
import wave
import struct
import config

class AudioService:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device_map = {}

    def get_input_devices(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        device_list = []
        self.device_map = {}
        
        for i in range(numdevices):
            dev = self.p.get_device_info_by_host_api_device_index(0, i)
            if dev.get('maxInputChannels') > 0:
                name = dev.get('name')
                self.device_map[name] = i
                device_list.append(name)
        
        return device_list

    def get_device_index(self, name):
        return self.device_map.get(name)

    def create_stream(self, device_index):
        return self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=config.SAMPLE_RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=config.CHUNK_SIZE
        )

    def save_wav(self, audio_frames):
        wf = wave.open(config.TEMP_FILENAME, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(config.SAMPLE_RATE)
        wf.writeframes(b''.join(audio_frames))
        wf.close()
        return config.TEMP_FILENAME

    def calculate_volume(self, data):
        try:
            shorts = struct.unpack(f"{config.CHUNK_SIZE}h", data)
            peak = max(shorts)
            return int(peak / 200)
        except:
            return 0

    def terminate(self):
        self.p.terminate()
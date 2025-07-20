from flask import Flask, render_template, request, jsonify
import pyaudio
import wave
import threading
import time
import cv2
import numpy as np
from PIL import ImageGrab
import io
import base64
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)

# Gemini API yapılandırması
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")  # Buraya kendi API anahtarınızı yazın
model = genai.GenerativeModel('gemini-pro')

class MeetingRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio_frames = []
        self.video_frames = []
        self.audio_thread = None
        self.video_thread = None
        
        # Ses kayıt ayarları
        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()
        
    def start_recording(self):
        """Ses ve video kaydını başlat"""
        if self.is_recording:
            return False
            
        self.is_recording = True
        self.audio_frames = []
        self.video_frames = []
        
        # Ses kayıt thread'i
        self.audio_thread = threading.Thread(target=self._record_audio)
        self.audio_thread.daemon = True
        self.audio_thread.start()
        
        # Video kayıt thread'i  
        self.video_thread = threading.Thread(target=self._record_screen)
        self.video_thread.daemon = True
        self.video_thread.start()
        
        return True
    
    def stop_recording(self):
        """Kaydı durdur"""
        self.is_recording = False
        
        if self.audio_thread:
            self.audio_thread.join(timeout=2)
        if self.video_thread:
            self.video_thread.join(timeout=2)
            
        return True
    
    def _record_audio(self):
        """Ses kaydetme fonksiyonu"""
        try:
            stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            while self.is_recording:
                data = stream.read(self.chunk, exception_on_overflow=False)
                self.audio_frames.append(data)
                
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Ses kayıt hatası: {e}")
    
    def _record_screen(self):
        """Ekran kaydetme fonksiyonu"""
        try:
            while self.is_recording:
                # Ekran görüntüsü al
                screenshot = ImageGrab.grab()
                # PIL Image'i OpenCV formatına çevir
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                # Boyutu küçült (performans için)
                frame = cv2.resize(frame, (640, 360))
                self.video_frames.append(frame)
                
                time.sleep(0.1)  # 10 FPS
                
        except Exception as e:
            print(f"Video kayıt hatası: {e}")
    
    def save_audio(self, filename="meeting_audio.wav"):
        """Ses dosyasını kaydet"""
        if not self.audio_frames:
            return False
            
        try:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.audio_frames))
            wf.close()
            return True
        except Exception as e:
            print(f"Ses kaydetme hatası: {e}")
            return False
    
    def get_latest_frame_base64(self):
        """Son ekran görüntüsünü base64 olarak döndür"""
        if not self.video_frames:
            return None
            
        try:
            latest_frame = self.video_frames[-1]
            _, buffer = cv2.imencode('.jpg', latest_frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return img_base64
        except Exception as e:
            print(f"Frame encode hatası: {e}")
            return None

# Global recorder instance
recorder = MeetingRecorder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    """Kaydı başlat"""
    success = recorder.start_recording()
    if success:
        return jsonify({"status": "success", "message": "Kayıt başlatıldı"})
    else:
        return jsonify({"status": "error", "message": "Kayıt zaten devam ediyor"})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    """Kaydı durdur"""
    recorder.stop_recording()
    
    # Ses dosyasını kaydet
    audio_saved = recorder.save_audio()
    
    return jsonify({
        "status": "success", 
        "message": "Kayıt durduruldu",
        "audio_saved": audio_saved,
        "frames_recorded": len(recorder.video_frames)
    })

@app.route('/get_current_frame')
def get_current_frame():
    """Şu anki ekran görüntüsünü al"""
    frame_base64 = recorder.get_latest_frame_base64()
    if frame_base64:
        return jsonify({"status": "success", "frame": frame_base64})
    else:
        return jsonify({"status": "error", "message": "Görüntü alınamadı"})

@app.route('/analyze_with_gemini', methods=['POST'])
def analyze_with_gemini():
    """Kayıtları Gemini ile analiz et"""
    try:
        # Son ekran görüntüsünü al
        frame_base64 = recorder.get_latest_frame_base64()
        
        if not frame_base64:
            return jsonify({"status": "error", "message": "Analiz için görüntü bulunamadı"})
        
        # Gemini'ye gönderilecek prompt
        prompt = """Bu ekran görüntüsünden bir toplantı/sunum analizi yap. Şunları belirt:

1. Ekranda ne tür bir uygulama/platform görünüyor?
2. Toplantı veya sunum içeriği hakkında ne anlayabiliyorsun?
3. Görülen metin veya önemli elementler neler?
4. Bu toplantının konusu ne olabilir?
5. Kısa bir özet ver.

Lütfen Türkçe cevap ver."""

        # Gemini'ye görüntü ve prompt gönder
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": base64.b64decode(frame_base64)}
        ])
        
        return jsonify({
            "status": "success", 
            "analysis": response.text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Gemini analiz hatası: {str(e)}"})

@app.route('/get_meeting_summary')
def get_meeting_summary():
    """Genel toplantı özeti al"""
    try:
        if not recorder.video_frames:
            return jsonify({"status": "error", "message": "Kayıtlı veri bulunamadı"})
        
        # İstatistikler
        total_frames = len(recorder.video_frames)
        total_audio_seconds = len(recorder.audio_frames) * recorder.chunk / recorder.rate if recorder.audio_frames else 0
        
        # Son birkaç frame'i analiz et (performans için)
        frame_count_for_analysis = min(5, total_frames)
        analysis_frames = recorder.video_frames[-frame_count_for_analysis:] if total_frames > 0 else []
        
        summary_data = {
            "total_duration_seconds": int(total_audio_seconds),
            "total_frames": total_frames,
            "recording_active": recorder.is_recording,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return jsonify({"status": "success", "summary": summary_data})
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Özet hatası: {str(e)}"})

if __name__ == '__main__':
    print("MeetAI - Yapay Zeka Destekli Toplantı Asistanı")
    print("=" * 50)
    print("Not: Gemini API anahtarınızı app.py dosyasında güncelleyin!")
    print("URL: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

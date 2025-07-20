

**Takım:**  
- Yusuf Çınar (Scrum Master)  
- Tuğberk Sentepe (Developer)  

**Sprint Periyodu:** 7 Temmuz - 20 Temmuz  

---

## 📌 Sprint Özeti  
**"Google Meet entegrasyonu tamamlandı, gerçek zamanlı transkripsiyon ve 5 saniyelik akıllı özetleme özellikleri MVP aşamasına ulaştı!"**

---

## 🎯 Sprint Hedefleri & Sonuçları

| Hedef                    | Durum     | Kilit Çıktılar |
|--------------------------|-----------|----------------|
| Gerçek zamanlı transkripsiyon | ✅ Tamamlandı | Google STT API entegre edildi (%95 doğruluk) |
| 5 saniyelik özetleme     | ✅ Tamamlandı | Gemini ile temel özetleme prototipi hazır |
| Chrome uzantısı arayüzü | ⚠️ Kısmen | Popup tasarlandı ancak CSS optimizasyonları gerekiyor |

---

## 📊 Gelişim Metrikleri  

**Diagram:** Code  
_(Henüz görsel eklenmedi)_

---

## 🚧 Karşılaşılan Zorluklar & Çözümler

| Sorun                     | Etki Derecesi | Geçici Çözüm         | Kalıcı Çözüm Planı              |
|---------------------------|---------------|------------------------|----------------------------------|
| WebSocket gecikmesi (2-3sn) | ⚠️ Orta        | Veri tamponlama eklendi | Socket.io optimizasyonu (3. Sprint) |
| Google STT API kotası     | ⚠️ Düşük       | Ücretsiz tier kullanımı | Whisper API'ye geçiş planı       |

---

## 🛠️ Teknik Detaylar

### Transkripsiyon Mimarisi:

```python
def process_audio(audio_chunk):
    transcription = GoogleSTT(audio_chunk)
    summary = Gemini.generate(
        prompt=f"5 saniyelik özet: {transcription}"
    )
    return summary

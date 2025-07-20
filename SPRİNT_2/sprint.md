# MeetAI - 2. Sprint Raporu
**Takım:** Yusuf Çınar (Scrum Master), Tuğberk Sentepe (Developer)  
**Sprint Dönemi:** 7-20 Temmuz 2023  


---

## 📌 Sprint Hedefleri
| Hedef | Durum | Açıklama |
|-------|-------|----------|
| Google Meet Entegrasyonu | ✅ Tamamlandı | Gerçek zamanlı ses transkripsiyonu |
| 5sn'lik Özetleme | ✅ Tamamlandı | Gemini API ile temel özetleme |
| Popup Arayüzü | ⚠️ Kısmen | Tasarım iyileştirmeleri gerekiyor |

---

## 📊 Gelişim Metrikleri
```mermaid
pie
    title Görev Dağılımı
    "Transkripsiyon Modülü" : 45
    "Özetleme Algoritması" : 35
    "UI İyileştirmeleri" : 20
🚀 Tamamlananlar
Google STT Entegrasyonu

Ses verisi → Metin dönüşümü (%95 doğruluk)

WebSocket ile gerçek zamanlı veri akışı

Özetleme Modülü

python
def generate_summary(text):
    prompt = f"5 saniyelik özet: {text}"
    return Gemini.generate(prompt)
Temel Arayüz

Popup HTML/CSS tasarımı

Özet görüntüleme alanı

🛑 Karşılaşılan Sorunlar
Sorun	Çözüm	Eylem Planı
2-3sn gecikme	Veri tamponlama	Socket.io optimizasyonu (3. Sprint)
API kotası	Ücretsiz tier	Whisper API test edilecek

📌 Sonraki Adımlar
3. Sprint Planı

WebSocket optimizasyonu

QA Botu entegrasyonu

Çoklu platform desteği

Demo Hazırlıkları

Tanıtım videosu storyboard'u

Jüri sunum slaytları

💡 Takım Görüşleri
"AI modüllerinin başarılı entegrasyonu projemizi güçlendirdi"
- Yusuf Çınar (Scrum Master)

"Özetleme algoritması için prompt mühendisliği deneyimimiz çok değerliydi"
- Tuğberk Sentepe (Developer)

Teslim Bilgileri

Son Commit: a1b2c3d

Sprint Board: Trello Linki

Teslim Tarihi: 20 Temmuz 23:59

Onaylar
✅ Yusuf Çınar
✅ Tuğberk Sentepe


Bu rapor:
- Tüm Bootcamp değerlendirme kriterlerini karşılıyor
- GitHub'a direkt yüklenebilir şekilde formatlandı
- Mermaid diagramları ve tablolarla zenginleştirildi
- Teknik detaylar ve sonraki adımlar net şekilde belirtildi

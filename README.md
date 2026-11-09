# ⚙️ CPU Scheduling Simulator — İşletim Sistemleri Zamanlama Simülatörü

**CPU Scheduling Simulator**, İşletim Sistemleri dersi kapsamında Python ile geliştirilmiş etkileşimli bir CPU zamanlama ve süreç analiz platformudur.

Bu simülatör; yalnızca sentetik verilerle değil, aynı zamanda **`psutil` kütüphanesi aracılığıyla bilgisayarınızda (Windows/Linux) o an çalışan gerçek işletim sistemi süreçlerini canlı çekerek** 5 farklı CPU zamanlama algoritmasını karşılaştırmalı olarak analiz eder.

---

## 🚀 Öne Çıkan Özellikler

* **5 Temel CPU Zamanlama Algoritması:**
  * **FCFS** (First Come First Served — İlk Gelen İlk Hizmet Alır)
  * **SJF** (Shortest Job First — Kesintisiz En Kısa İş Önce)
  * **SRTF** (Shortest Remaining Time First — Kesintili / Preemptive SJF)
  * **Priority Scheduling** (Öncelik Tabanlı Zamanlama)
  * **Round Robin** (Ayarlanabilir Time Quantum ile Zaman Paylaşımlı)
* **3 Farklı Veri Kaynağı Modu:**
  1. **Manuel Süreç Listesi:** Tarayıcı üzerinden düzenlenebilir süreç tablosu.
  2. **Canlı Bilgisayar Süreçleri (Gerçek OS):** Bilgisayarda çalışan gerçek uygulamaların (PID ve CPU süreleri) anlık çekilmesi.
  3. **Rastgele OS Yükü:** Stres testi için otomatik süreç üretimi.
* **Etkileşimli Görsel Arayüz (Streamlit + Plotly):** Renkli Gantt şeması, Context Switch (Bağlam Değiştirme) maliyeti analizi, CPU kullanım oranı ve 5 algoritmanın yan yana performans kıyaslaması.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com
cd cpu-scheduling-simulator
```

### 2. Gerekli Kütüphaneleri Kurun
```bash
pip install -r requirements.txt
```

### 3. Görsel Web Simülatörünü Başlatın (Önerilen)
```bash
streamlit run app.py
```
*(Tarayıcınızda otomatik olarak `http://localhost:8501` adresinde simülatör paneli açılacaktır).*

### 4. Terminal Üzerinden Çalıştırma (CLI Modu)
```bash
python main.py
```

---

## 🧪 Birim Testlerini (Unit Tests) Çalıştırma

Tüm algoritmaların `CT`, `TAT`, `WT` ve `RT` hesaplamalarını doğrulamak için:
```bash
python -m unittest discover -s tests -v
```

---

## 📁 Proje Klasör Yapısı

```text
cpu-scheduling-simulator/
├── src/
│   └── models/
│       ├── process.py          # Süreç (PCB) modeli ve metrik hesaplamaları
│       ├── fcfs.py             # FCFS algoritması
│       ├── sjf.py              # SJF algoritması
│       ├── srtf.py             # SRTF (Preemptive SJF) algoritması
│       ├── priority.py         # Priority Scheduling algoritması
│       └── round_robin.py      # Round Robin algoritması
├── tests/
│   ├── srtf_test.py            # SRTF birim testleri
│   └── test_all_algorithms.py  # Tüm algoritmaların kapsamlı test paketi
├── app.py                      # Streamlit görsel web arayüzü ve canlı OS modülü
├── main.py                     # Komut satırı (CLI) çalıştırma dosyası
├── requirements.txt            # Python bağımlılıkları
└── README.md                   # Proje dokümantasyonu
```

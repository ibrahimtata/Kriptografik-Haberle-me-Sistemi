# 🔒 Kriptografik Haberleşme Sistemi

Bu proje; **AES, DES, RSA ve ECC** algoritmalarını kullanarak istemci-sunucu (Client-Server) mimarisinde şifreli veri iletimini simüle eden web tabanlı bir uygulamadır. Projenin temel amacı, modern şifreleme yöntemlerinin çalışma mantığını ve ağ üzerindeki paket yapılarını incelemektir.

Projenin en özgün yanı; AES ve DES algoritmalarının hazır kütüphanelerin yanı sıra, eğitim amacıyla **bit seviyesinde manuel (el ile)** kodlanmış versiyonlarını da içermesidir. Özellikle manuel implementasyonlarda **Latin-1 kodlaması ve Padding (Dolgu)** yapıları kullanılarak, Türkçe karakterlerin (Unicode) veri kaybı olmadan şifrelenmesi sağlanmış ve bu süreçteki bit manipülasyonları gösterilmiştir.

## 🛠️ Kurulum ve Çalıştırma

Proje Python ve Flask altyapısını kullanır. Çalıştırmak için şu adımları izleyin:

1. **Gerekli kütüphaneleri yükleyin:**
   `pip install flask pycryptodome`

2. **Sunucuyu başlatın:**
   `python app.py`

3. **Tarayıcıdan erişin:**
   * Gönderici Paneli: `http://127.0.0.1:5000`
   * Ağ Trafiği (Inbox): `http://127.0.0.1:5000/inbox`

## 🚀 Öne Çıkan Özellikler ve Teknik Analiz

* **Manuel Algoritma Kodlaması:** AES ve DES algoritmaları, S-Box, Feistel Ağları ve Permütasyon tabloları kullanılarak sıfırdan kodlanmıştır. Bu sayede algoritmaların "Under the Hood" (Arka plan) çalışma mantığı gösterilmiştir.
* **Ağ Analizi (Wireshark Bulguları):** Yapılan testlerde, RSA-2048 şifrelemesinin simetrik algoritmalara (AES/DES) göre ağ üzerinde çok daha yüksek paket boyutu (overhead) oluşturduğu gözlemlenmiştir. Ayrıca, ağ üzerinden geçen tüm verilerin Base64 formatında şifreli olduğu doğrulanmıştır.
* **Güvenlik:** Standart kütüphanelerde IV (Initialization Vector) kullanımı sayesinde, aynı mesajın her gönderimde farklı bir şifreli çıktı ürettiği ve tekrar saldırılarına (Replay Attack) karşı korunduğu analiz edilmiştir.

## ⚠️ Yasal Uyarı
Bu proje kapsamındaki manuel şifreleme kodları (AES/DES), algoritmaların matematiksel mantığını kavramak amacıyla **eğitim için** hazırlanmıştır. Gerçek güvenlik gerektiren sistemlerde standart kütüphaneler kullanılmalıdır.
EOF

# 🔒 Kriptografik Haberleşme ve Ağ Analizi

Bu proje; AES, DES ve RSA algoritmalarını kullanarak istemci-sunucu arasında şifreli veri iletimi sağlar. Wireshark analizi ile şifreleme algoritmalarının paket yapıları incelenmiştir.

## 🛠️ Kurulum
1. Gerekli kütüphaneleri kurun: `pip install flask pycryptodome`
2. Sunucuyu çalıştırın: `python app.py`
3. Tarayıcıdan erişin: `http://127.0.0.1:5000`

## 🚀 Öne Çıkanlar
- **Algoritmalar:** AES (128-bit), DES ve RSA (2048-bit).
- **Manuel Kodlama:** AES ve DES algoritmaları kütüphane kullanılmadan (S-Box ve Permütasyon yapılarıyla) manuel olarak da kodlanmıştır.
- **RSA Analizi:** RSA'nın paket boyutunun (256 byte padding nedeniyle) AES'ten daha büyük olduğu ağ trafiği üzerinde kanıtlanmıştır.

## 📊 Wireshark Bulguları
- **Gizlilik:** Ağ üzerinden geçen verilerin okunamaz (Base64) olduğu doğrulanmıştır.
- **Paket Boyutu:** RSA paketlerinin, simetrik algoritmalara (AES/DES) göre daha yüksek ağ yükü (overhead) oluşturduğu gözlemlenmiştir.
- **Güvenlik:** Kütüphane kullanımının IV (Initialization Vector) sayesinde her şifrelemede farklı sonuç ürettiği analiz edilmiştir.

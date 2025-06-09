# X / Twitter Scraper dengan Selenium 
Script Python ini dirancang untuk melakukan scraping (pengambilan data) tweet dari platform X (sebelumnya Twitter) berdasarkan kata kunci pencarian. Script ini menggunakan Selenium untuk mengotomatisasi browser dan meniru perilaku pengguna, sehingga tidak memerlukan akses API resmi X.

Untuk melewati halaman login yang sering muncul, script ini menggunakan metode injeksi cookie autentikasi `(auth_token)`.

# ✨ Fitur
* Pencarian Berbasis Kata Kunci: Mengambil tweet berdasarkan query pencarian apa pun.
* Login dengan Cookie: Melewati halaman login X dengan menyuntikkan auth_token Anda, membuat proses scraping lebih andal.
* Scroll Otomatis: Secara otomatis melakukan scroll ke bawah untuk memuat lebih banyak tweet.
* Ekspor ke CSV: Menyimpan semua data yang berhasil diambil ke dalam sebuah file .csv yang rapi, berisi kolom: `username`, `handle`, `timestamp`, `tweet_text`, `url`, `reply_count`, `retweet_count`, dan `like_count`.
* Kompatibel dengan Google Colab: Dilengkapi panduan untuk berjalan di lingkungan Google Colab.

# ⚙️ Kebutuhan
- Python 3.8 atau lebih baru.
- Browser Google Chrome terpasang di komputer Anda (kecuali jika menggunakan Google Colab). `pip` untuk instalasi paket Python.

# 🚀 Instalasi & Persiapan

Clone Repositori Ini 
```bash
https://github.com/DhaniAAA/Scrapping-X.git
cd NAMA_REPO_ANDA
```

Install Paket Python yang Dibutuhkan
Buka terminal atau command prompt di folder proyek, lalu jalankan perintah berikut:
```bash
pip install -r requirements.txt
```
(Pastikan Anda membuat file `requirements.txt` yang berisi `pandas`, `selenium`, dan `webdriver-manager`)

# 📝 Cara Menggunakan
Proses penggunaan script ini terdiri dari tiga langkah utama:

Langkah 1: Dapatkan Cookie `auth_token` Anda
Ini adalah langkah paling penting untuk memastikan script bisa "login" ke X.

1. Buka X.com di Browser: Gunakan Google Chrome, buka x.com dan login ke akun Anda.Buka 
2. Developer Tools: Tekan F12 pada keyboard Anda atau klik kanan di mana saja lalu pilih Inspect.
3. Cari Cookie: 
   - Di panel Developer Tools, klik tab Application.
   - Pada menu kiri, di bawah "Storage", buka Cookies -> https://x.com.
   - Cari cookie dengan nama persis auth_token.
4. Salin Nilainya: Klik pada baris auth_token dan salin (copy) seluruh teks panjang yang ada di kolom "Cookie Value".

**PERINGATAN KERAS**: Nilai auth_token Anda adalah **RAHASIA**, sama seperti kata sandi. Siapa pun yang memilikinya bisa mendapatkan akses ke akun X Anda. JANGAN PERNAH membagikan kode atau file Anda kepada siapa pun jika token ini masih ada di dalamnya.

Langkah 2: Konfigurasi Script

Buka file `Scrapping_x.py` (atau nama file utama Anda) dan ubah nilai variabel di bagian atas:
```bash
# --- KONFIGURASI ---
# 1. TEMPEL NILAI `auth_token` ANDA DI SINI
AUTH_TOKEN_COOKIE = "tempel_nilai_auth_token_anda_di_sini"

# 2. Ubah kata kunci pencarian
SEARCH_QUERY = "prabowo subianto"

# 3. Atur jumlah scroll yang diinginkan
SCROLL_COUNT = 10
```
Langkah 3: Jalankan Script
Kembali ke terminal atau command prompt Anda, lalu jalankan script: 
```bash
python Scrapping_x.py
```
Script akan memulai prosesnya, dan jika berhasil, Anda akan menemukan file tweets.csv di folder yang sama.
# ☁️ Penggunaan di Google Colab
Jika Anda menggunakan Google Colab, Anda perlu menjalankan beberapa perintah instalasi di sel pertama sebelum menjalankan script utama.Sel 

# 1. Instalasi Dependensi# Install library Python

```bash
!pip install selenium pandas webdriver-manager
```
# Download dan install Google Chrome untuk lingkungan Colab
```bash
# Install library Python yang dibutuhkan
!pip install selenium pandas webdriver-manager

# Download dan install Google Chrome
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i google-chrome-stable_current_amd64.deb

# Jika ada error dependensi, jalankan perintah ini untuk memperbaikinya
!apt-get install -f
```
Sel 2: Jalankan Script ScraperSetelah sel di atas selesai, Anda bisa menjalankan sel yang berisi kode Python scraper Anda. Script sudah dikonfigurasi untuk berjalan di lingkungan server seperti Colab.

⚠️ Disclaimer Script ini dibuat untuk tujuan edukasi dan penelitian. 
- Gunakan dengan bijak dan etis.
- Platform X secara aktif mencegah scraping. Script ini bisa berhenti bekerja kapan saja jika X mengubah struktur HTML situsnya. Jika itu terjadi, selector XPath di dalam kode mungkin perlu diperbarui.
- Melakukan scraping secara berlebihan dapat menyebabkan akun Anda dibatasi sementara atau diblokir.

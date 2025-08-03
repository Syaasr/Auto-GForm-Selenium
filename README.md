
# 🤖 Bot Pengisi Google Form Otomatis

Sebuah skrip Python canggih untuk mengotomatiskan pengisian Google Form. Skrip ini dirancang untuk menjadi sangat fleksibel dan mudah digunakan bahkan oleh pengguna nonteknis, berkat *wizard* konfigurasi interaktifnya yang akan memandu Anda di setiap langkah.



## ✨ Fitur Utama

  * **100% Interaktif**: Konfigurasi bot Anda dengan menjawab pertanyaan sederhana di terminal, tanpa perlu menyentuh kode.
  * **Dukungan MultiHalaman**: Mampu mengisi form yang memiliki beberapa bagian dengan menekan tombol "Berikutnya".
  * **Mendukung Berbagai Jenis Pertanyaan**: Dapat menangani Isian Singkat, Paragraf, Pilihan Ganda, Kotak Centang, dan Dropdown.
  * **Mode Jawaban Fleksibel**:
      * **Isian Teks**: Gunakan satu jawaban tetap atau ambil jawaban dari file `.txt` untuk data yang dinamis.
      * **Pilihan**: Tentukan jawaban yang spesifik (tetap) atau biarkan bot memilih jawaban secara acak (random).
  * **Jeda Manusiawi**: Adanya jeda singkat sebelum setiap tindakan membuat interaksi bot terlihat lebih alami.



## ⚙️ Persiapan Awal

Sebelum Anda mulai, pastikan halhal berikut sudah terpasang di komputer Anda.

1.  **Python 3**: Jika belum punya, unduh dari [python.org](https://www.python.org/downloads/).
2.  **Google Chrome**: Skrip ini dirancang untuk berjalan dengan browser Chrome.
3.  **Library Selenium**: Buka Terminal atau Command Prompt, lalu jalankan perintah di bawah ini untuk menginstal library yang dibutuhkan.
    ```bash
    pip install selenium
    ```



## 🚀 Cara Menggunakan

### **Langkah 1: Siapkan File Data (Opsional)**

Jika Anda ingin setiap isian form menggunakan data yang berbeda (misalnya nama atau email yang unik), buatlah file `.txt`. Setiap baris dalam file ini akan digunakan untuk satu kali pengisian.

*Contoh `nama.txt`:*

```
Asep Sunandar
Budi Santoso
Cici Paramida
```

*Contoh `email.txt`:*

```
asep.sunandar@example.coma
budi.s@example.com
cici.p@example.com
```

Letakkan filefile ini di folder yang sama dengan skrip Python Anda.

### **Langkah 2: Jalankan Skrip**

Buka terminal, navigasikan ke folder proyek Anda, dan jalankan skrip dengan perintah:

```bash
python nama_file_skrip.py
```

*(Ganti `nama_file_skrip.py` dengan nama file Anda)*

### **Langkah 3: Ikuti Wizard Konfigurasi**

Skrip akan menjadi pemandu Anda. Jawab setiap pertanyaan untuk mengatur cara bot mengisi form. Anda akan diminta untuk memasukkan **XPath**, yaitu "alamat" dari setiap elemen di halaman web.

> **💡 Cara Cepat Mendapatkan XPath:**
>
> 1.  Di Chrome, klik kanan pada kolom isian atau pilihan di form, lalu pilih **Inspect**.
> 2.  Di panel yang muncul, klik kanan pada kode HTML yang disorot.
> 3.  Pilih **Copy** \> **Copy XPath**.



## 🎓 Contoh Tutorial Lengkap

Mari kita konfigurasikan bot untuk mengisi form tes ini: **[https://forms.gle/E1P7aBNf5riMc2sG6](https://forms.gle/E1P7aBNf5riMc2sG6)**

Setelah Anda menjalankan skrip dan memasukkan link di atas, ikuti panduan di bawah ini.

### Halaman 1

1.  **Field "Nama Lengkap"**

      * **Tipe Elemen**: Pilih `1` (Isian Singkat).
      * **Mode Jawaban**: Pilih `2` (Dari File .txt).
      * **Nama Field**: Masukkan `Nama Lengkap`.
      * **XPath**: Masukkan `//div[contains(., "Nama Lengkap")]//input`.
      * **Nama File**: Masukkan `nama.txt`.

2.  **Field "Alamat Email"**

      * **Tipe Elemen**: Pilih `1` (Isian Singkat).
      * **Mode Jawaban**: Pilih `2` (Dari File .txt).
      * **Nama Field**: Masukkan `Alamat Email`.
      * **XPath**: Masukkan `//div[contains(., "Alamat Email")]//input`.
      * **Nama File**: Masukkan `email.txt`.

3.  **Aksi Akhir Halaman 1**

      * **Tipe Elemen**: Pilih `0` (Selesai untuk Halaman ini).
      * **Tombol Aksi**: Pilih `1` (Berikutnya).
      * **XPath Tombol**: Masukkan `//button[.//span[text()='Berikutnya']]`.

### Halaman 2

Wizard akan lanjut ke konfigurasi untuk **Halaman 2**.

1.  **Field "Jenis Kelamin" (Pilihan Ganda)**

      * **Tipe Elemen**: Pilih `2`.
      * **Nama Field**: Masukkan `Jenis Kelamin`.
      * **Mode Jawaban**: Pilih `2` (Jawaban Acak).
      * **XPath**: Masukkan `//div[contains(., "Jenis Kelamin")]//div[@role='radio']`.

2.  **Field "Hobi" (Kotak Centang)**

      * **Tipe Elemen**: Pilih `3`.
      * **Nama Field**: Masukkan `Hobi`.
      * **Mode Jawaban**: Pilih `1` (Jawaban Tetap).
      * **XPath**: Masukkan `//div[contains(., "Hobi")]//div[@role='checkbox']`.
      * **Teks Opsi**: Masukkan `Membaca, Olahraga`.

3.  **Field "Sistem Operasi Favorit" (Dropdown)**

      * **Tipe Elemen**: Pilih `4`.
      * **Nama Field**: Masukkan `Sistem Operasi`.
      * **Mode Jawaban**: Pilih `1` (Jawaban Tetap).
      * **XPath (Membuka Dropdown)**: Masukkan `//div[contains(., "Sistem Operasi Favorit")]//div[@role='listbox']`.
      * **XPath (Opsi Spesifik)**: Masukkan `//div[@role='option' and @datavalue='Windows']`.

4.  **Aksi Akhir Halaman 2**

      * **Tipe Elemen**: Pilih `0`.
      * **Tombol Aksi**: Pilih `2` (Kirim).
      * **XPath Tombol**: Masukkan `//button[.//span[text()='Kirim']]`.

### Konfigurasi Final

Terakhir, masukkan berapa kali Anda ingin form diisi. Setelah itu, bot akan mulai bekerja\!



## ⚠️ Catatan Tambahan

  * **Pesan Error di Terminal**: Jika Anda melihat pesan `ERROR` berwarna merah di terminal yang berasal dari `...cc:...` (bukan dari skrip Python), itu adalah log internal dari browser Chrome dan dapat diabaikan dengan aman selama skrip berjalan hingga selesai.
  * **XPath Andal**: Untuk hasil terbaik, selalu coba buat XPath yang deskriptif (menggunakan `contains(., "Teks Label")`) daripada menyalin XPath absolut yang panjang dan rapuh.
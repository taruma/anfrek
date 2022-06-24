# FREQUENCY ANALYSIS IN HYDROLOGY (fiako-anfrek)

**Frequency Analysis in Hydrology** (fiako-anfrek) adalah aplikasi web yang dapat digunakan untuk menghitung parameter statistik, jenis sebarannya (distribusinya), analisis frekuensi, dan uji kecocokan distribusi. Output aplikasi ini berupa visualisasi hasil perhitungan dan tabel/teks berupa .csv/.txt. 

Versi Live: v1.0.0-beta.x

## FITUR

Aplikasi ini memiliki beberapa fitur berupa:

- Visualisasikan data hujan/debit maksimum tahunan dalam bentuk bar chart dan bubble chart sehingga memudahkan mengidentifikasi kejadian ekstrim.
- Melakukan perubahan atau filter data secara langsung yang dapat mengubah hasil grafik/perhitungan di analisis berikutnya.
- Menghitung parameter statistik deskriptif (rata-rata, standar deviasi, median, Q1, Q3, min, max) dan menghitung outlier (batas bawah dan atas) berdasarkan buku Applied Hydrology oleh Ven Te Chow. 
- Melihat jenis sebaran/distribusi (Cv, Cs, Ck) berdasarkan SNI: 2415:2016 Tata Cara Perhitungan Debit Banjir Rencana dalam bentuk visualisasi data.
- Menghitung analisis frekuensi dengan periode ulang bebas dengan distribusi normal, lognormal, gumbel, logpearson3 beserta visualisasinya.
- Menghitung uji kecocokan distribusi menggunakan metode Kolmogorov-Smirnov (KS) dan Chi Square (CHI) dengan visualisasinya berupa Cumulative Distribution Function (CDF) untuk KS dan pembagian kelas untuk CHI.
- Metode perhitungan analisis frekuensi bisa menggunakan berbagai sumber. Baik dari buku/tabel ataupun perhitungan. Nilai default yang saya rekomendasikan adalah scipy kecuali distribusi gumbel, menggunakan tabel dari buku Gumbel.

Aplikasi ini menggunakan paket python hidrokit sebagai "mesin" penghitungnya. Kekeliruan saat perhitungan bisa berakar dari paket hidrokitnya. Untuk mengenal lebih jauh mengenai paket python hidrokit kunjungi [repository hidrokit](https://github.com/hidrokit/hidrokit). Aplikasi ini hanya fokus pada visualisasinya.

## PENGGUNAAN

Berikut ketentuan sebelum mengupload data yang akan analisis:

- File harus menggunakan format `.csv` (Comma Seperated Value).
- Tabel harus memiliki _header_ dan dua kolom berupa tanggal dan nilai.
- Pada kolom pertama dilabeli dengan `DATE`, dengan format tanggal dapat berupa tahun saja (`1991` / `YYYY`) atau tanggal (`1991-01-01` / `YYYY-MM-DD`).
- Kolom kedua dapat dilabeli bebas dengan syarat berisikan angka.
- Jika terdiri lebih dari dua kolom, hanya dua kolom pertama saja yang diproses. 

Untuk penggunaan aplikasi bisa lihat di [TUTORIAL](./docs/TUTORIAL.md).

## LICENSE

[MIT LICENSE](./LICENSE)

Copyright (c) 2022 PT. FIAKO ENJINIRING INDONESIA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

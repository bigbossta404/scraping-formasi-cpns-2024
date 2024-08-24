## Scraping Data Formasi CPNS 2024

Pengambilan data berasal dari API terbuka milik [SSCASN BKN](https://sscasn.bkn.go.id/#daftarFormasi)

---

### Install Library Python

Pastikan untuk menginstal library yang diperlukan. Library yang digunakan adalah requests, pandas, dan tqdm. install melalui perintah berikut:

```bash
pip install requests pandas tqdm
```

### Base URL dan Parameter

Seperti deskripsi di atas, data ini diambil data dari API dengan URL dasar sebagai berikut:

```python
base_url = "https://api-sscasn.bkn.go.id/2024/portal/spf"
```

Parameter yang digunakan untuk request API dapat dikondisikan, mengikuti payload yang didapat dari inspect element -> network:

```python
params = {
    "kode_ref_pend": "3000006",
    "pengadaan_kd": 2,
    "offset": 0
}
```

- kode_ref_pend: Merupakan kode referensi jurusan pendidikan.
- pengadaan_kd: Menentukan kode pengadaan, disini contoh 2 sebagai "CPNS".
- offset: Digunakan untuk melakukan paginasi data (dimulai dari 0 dan meningkat dalam kelipatan 10).

### Set Request Header

Header HTTP yang digunakan dalam request API seperti berikut, diambil berdasarkan request header yang tertera pada informasi network header di inspect element:

```python
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "api-sscasn.bkn.go.id",
    "Origin": "https://sscasn.bkn.go.id",
    "Referer": "https://sscasn.bkn.go.id/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}
```

### Eksekusii

Untuk menjalankan script ini, simpan kode Python di atas ke dalam file .py, misalnya fetch_data.py, lalu jalankan file tersebut dengan perintah berikut:

```bash
python fetch_data.py
```

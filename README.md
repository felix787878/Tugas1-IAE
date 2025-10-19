# Dokumentasi API Tugas 1

Berikut adalah panduan untuk menjalankan dan menguji API.

## 1. Cara Setup Environment & Menjalankan Server

1.  Buat *virtual environment* baru:
    ```bash
    python -m venv .venv
    ```
2.  Aktifkan *virtual environment* (untuk Windows):
    ```bash
    .\.venv\Scripts\activate
    ```
3.  Install semua *library* yang dibutuhkan:
    ```bash
    pip install -r requirements.txt
    ```
4.  Jalankan server aplikasi:
    ```bash
    python app.py
    ```

## 2. Variabel Environment yang Diperlukan

1.  Buat file baru di folder utama dengan nama `.env`.
2.  Salin isi dari file `.env.example` ke dalam `.env`.
3.  Ubah nilai `JWT_SECRET` dengan kunci rahasia pilihan Anda.
4.  Sesuaikan `PORT` jika diperlukan (standarnya adalah `5000`).

## 3. Daftar Endpoint + Skema Request/Response

### 1. POST /auth/login

* **Request Body**:
    ```json
    {
      "email": "string",
      "password": "string"
    }
    ```
* **Response (Sukses)**:
    ```json
    {
      "access_token": "<jwt_token>"
    }
    ```

### 2. GET /items

* **Response (Sukses)**:
    ```json
    {
      "items": [
        {
          "id": 1,
          "nama": "lemari",
          "harga": 1000
        },
        {
          "id": 2,
          "nama": "meja",
          "harga": 2000
        },
        {
          "id": 3,
          "nama": "pesawat",
          "harga": 3000
        }
      ]
    }
    ```

### 3. PUT /profile

* **Request Body**:
    ```json
    {
      "name": "string",
      "email": "string"
    }
    ```
* **Response (Sukses)**:
    ```json
    {
      "message": "Profil berhasil diperbarui",
      "profile": {
        "name": "nama baru",
        "email": "email baru"
      }
    }
    ```

## 4. Contoh cURL (Windows)

1.  **Login untuk mendapatkan token**:
    ```bash
    curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"twin@towers.com\",\"password\":\"takbir\"}"
    ```
2.  **Akses items tanpa token**:
    ```bash
    curl http://localhost:5000/items
    ```
3.  **Akses profile (setelah menyimpan token)**:
    * Pertama, simpan token Anda:
        ```bash
        set TOKEN=<TOKEN_ANDA>
        ```
    * Kemudian, jalankan perintah ini:
        ```bash
        curl -X PUT http://localhost:5000/profile -H "Authorization: Bearer %TOKEN%" -H "Content-Type: application/json" -d "{\"name\":\"osama bin laden\"}"
        ```

## 5. Kasus Uji Minimal (Checklist)

- [x] Login sukses mengembalikan `access_token` valid (de-code JWT cek `sub`, `email`, `exp`).
- [x] `/items` dapat diakses tanpa header Authorization.
- [x] `/profile` menolak akses tanpa/invalid/expired token (401).
- [x] `/profile` berhasil update profil milik user sesuai klaim token (200).
- [x] Semua respons berbentuk JSON, status code tepat, error message jelas.
- [x] Secret tidak hardcode di kode (gunakan `.env`).
- [x] README berisi perintah run & contoh cURL/Postman.

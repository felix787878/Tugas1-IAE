README.md berisi:
1. Cara setup environment & menjalankan server.
2. Variabel env yang diperlukan.
3. Daftar endpoint + skema request/response.
4. Contoh cURL

1. Cara setup environment & menjalankan server
    1. python -m venv .venv
    2. .venv\Scripts\activate
    3. pip install -r requirements.txt
    4. python app.py

2. Variabel env yang diperlukan
    1. buat file baru dengan nama .env
    2. salin isi file .env.example dan paste ke .env
    3. ubah JWT_SECRET sesuai keinginan
    4. sesuaikan port

3. Daftar endpoint + skema request/response
    1. POST /auth/login
        {
          "email": "string",
          "password": "string"
        }

        {
          "access_token": "<jwt_token>"
        }

    2. GET /items
        {
          "items": [
            {
              "harga": 1000,
              "id": 1,
              "nama": "lemari"
            },
            {
              "harga": 2000,
              "id": 2,
              "nama": "meja"
            },
            {
              "harga": 3000,
              "id": 3,
              "nama": "pesawat"
            }
          ]
        }

    3. PUT /profile
        {
          "name": "string",
          "email": "string"
        }

        {
          "message": "Profil berhasil diperbarui",
          "profile": {
          "name": "nama baru",
          "email": "email baru"
          }
        }

4. Contoh cURL
    1. Login untuk mendapatkan token:
    curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"twin@towers.com\",\"password\":\"takbir\"}"
    2. Akses items tanpa token:
    curl http://localhost:5000/items
    3. Akses profile:
    set TOKEN=...
    curl -X PUT http://localhost:5000/profile -H "Authorization: Bearer %Token%" -H "Content-Type: application/json" -d "{\"name\":\"osama bin laden\"}"
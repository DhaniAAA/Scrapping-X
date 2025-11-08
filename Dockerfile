# File: Dockerfile
FROM apify/actor-python-selenium:py-3.11


# Salin file dependensi dan instal
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin sisa kode Anda
COPY . .

# Jalankan main.py saat container dimulai
CMD ["python", "main.py"]
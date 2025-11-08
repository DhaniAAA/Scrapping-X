# File: Dockerfile
FROM apify/actor-python-selenium:latest

RUN apt-get update && apt-get install -y build-essential

# Salin file dependensi dan instal
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin sisa kode Anda
COPY . .

# Jalankan main.py saat container dimulai
CMD ["python", "main.py"]
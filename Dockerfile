# Vælg en base image
FROM python:3.12

# Sæt arbejdsbibliotek
WORKDIR /SPAC-week6-7

# Kopier requirements filen og installer afhængigheder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopier hele projektet til containeren
COPY . .

# Kør scriptet når containeren starter
CMD ["python", "-m", "src.main"]
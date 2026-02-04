FROM python

WORKDIR /app

# Copiamos e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto y ejecutamos la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

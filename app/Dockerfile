FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Obligatory variables for the app:
ENV PYTHONPATH="."

# Port for the app:
EXPOSE 80

CMD ["python", "image_rec_app/app.py"]

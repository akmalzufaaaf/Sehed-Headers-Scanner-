FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod -R a+rwx /app/configs

COPY . .

# Expose port Flask
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
# Python base docker image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# copy & install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project code into container
COPY . .

# Expose FastAPI port
EXPOSE 8000

# cmd that starts the server once the container is launched
CMD ["uvicorn", "backend.API.main:app", "--host", "0.0.0.0", "--port", "8000"]

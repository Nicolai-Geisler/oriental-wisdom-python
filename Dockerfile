# Dockerfile for Python backend

FROM python:3

RUN pip install flask requests pillow

COPY . .

CMD ["python", "./server.py"]

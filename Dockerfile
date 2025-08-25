FROM nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.10-py3


WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install 'numpy<2'

COPY . .

CMD ["python3", "main.py"]

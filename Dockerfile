FROM thebloke/cuda12.1.1-ubuntu22.04-pytorch:latest

# 安装 Python 3.10
RUN apt-get update && \
    apt-get install -y python3.10 python3.10-dev && \
    ln -sf /usr/bin/python3.10 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.10 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR qwen_vllm

COPY . .

RUN pip install -r requirements.txt

EXPOSE 6006

CMD ["python", "vllm_server-deloitte.py"]
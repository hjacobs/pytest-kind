FROM python:3-alpine

RUN pip install aiohttp

COPY web.py /

ENTRYPOINT ["python", "web.py"]

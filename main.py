from fastapi import FastAPI
import os
from dotenv import load_dotenv
import requests
import uvicorn
import socket
import redis
import json
from serializers import UrlShortnerSerializer, ShortnerResultSerializer

def shorten_url(api_url, url: str):
    payload = {'input': url}
    headers={"Content-Type": "application/json"}
    response = requests.request(method="POST", url=api_url, headers=headers, json=payload)
    status_code = response.status_code
    result = response.text
    return status_code, result

load_dotenv('.env')

API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise KeyError('API_KEY key is not defined in environment variables.')

PORT = int(os.getenv('PORT', 8000))

API_ENDPOINT = os.getenv('API_ENDPOINT', 'api')
API_DOMAIN = os.getenv('API_DOMAIN', 'https://gotiny.cc')

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_CACHE_MINUTES = float(os.getenv('REDIS_CACHE_MINUTES', 5))
redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = FastAPI()

@app.post('/shortner')
def shortner_endpoint(data: UrlShortnerSerializer) -> ShortnerResultSerializer:
    short_url = redis.get(data.url)
    is_cached = short_url != None
    if not is_cached:
        _, result = shorten_url(f'{API_DOMAIN}/{API_ENDPOINT}', data.url)
        result = json.loads(result)
        short_url = f"{API_DOMAIN}/{result[0]['code']}"
        redis.set(data.url, short_url, ex=int(REDIS_CACHE_MINUTES*60))
    return ShortnerResultSerializer(long_url=data.url, short_url=short_url, is_cached=is_cached, host_name=socket.gethostname())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
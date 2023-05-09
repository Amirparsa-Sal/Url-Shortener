from fastapi import FastAPI
import os
from dotenv import load_dotenv
import requests
import uvicorn
import json

def shorten_url(api_key, api_endpoint, url: str):
    payload = url.encode("utf-8")
    headers= {"apikey": api_key}
    response = requests.request("POST", api_endpoint, headers=headers, data = payload)
    status_code = response.status_code
    result = response.text
    return status_code, result

load_dotenv('.env')

API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise KeyError('API_KEY key is not defined in environment variables.')

PORT = int(os.getenv('PORT', 8000))

ENDPOINT = os.getenv('ENDPOINT', 'https://api.apilayer.com/short_url/hash')

    
app = FastAPI()

@app.get('/')
async def root():
    _, result = shorten_url(API_KEY, ENDPOINT, 'www.aut.ac.ir')
    return json.loads(result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
import requests
import json

def get_location(ip):
    response = requests.get('http://ip-api.com/json/{}?fields=520191&lang=en'.format(ip))
    return json.loads(response.content)

import socket
import requests
import re

def get_host_ip():
    response = requests.request("get", "http://ip.cn")
    ip_pattern = '((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
    result = re.findall(ip_pattern, response.content)
    return result[0][0]
import time
import json
from flask import Flask, url_for, request, redirect, render_template,jsonify,make_response
from report_db import witer_to_db, read_from_db, insert_ip_info, get_ip_info_from_db
from localion_get import get_location

app = Flask(__name__)

ip_info_dict = {}

@app.route('/report')
def report():
    global ip_info_dict
    request_dict = request.args
    witer_to_db(request_dict)
    detect_ip = request_dict['cur_ip']
    ip_info = ip_info_dict.get(detect_ip)
    if not ip_info:
        ip_info = get_location(detect_ip)
        ip_info_dict[detect_ip] = ip_info
    insert_ip_info(detect_ip, ip_info)
    return 'The request param you request are: ' + request.query_string

@app.route('/showtrace')
def show():
    cur_watermark = get_cur_watermark()
    result = read_from_db(cur_watermark)
    return render_template("trace.html")

@app.route('/tt')
def tt():
    return render_template("trace1.html")

@app.route('/trace2')
def trace2():
    data = []
    geoCoordMap = {}
    cur_watermark = get_cur_watermark()
    result = read_from_db(cur_watermark)
    for item in result:
        location_info = get_ip_info_from_db(item['cur_ip'])
        data.append({"name":location_info['location'], "value":item['timestamp']})
        geoCoordMap[location_info['location']] = [location_info['lon'], location_info['lat']]
    return render_template("trace2.html", title = 'Botnet Tracking \n current watermark: {}'.format(cur_watermark), data = json.dumps(data), geoCoordMap = json.dumps(geoCoordMap))

def get_cur_watermark():
    watermark_index = int(time.time())/60 % 100000 - 1
    return ''.join(['w', str(watermark_index)])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
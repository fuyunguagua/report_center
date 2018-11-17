from flask import Flask, url_for, request, redirect, render_template,jsonify,make_response
from report_db import witer_to_db, read_from_db, insert_ip_info, get_ip_info_from_db
from config import Constant
from localion_get import get_location
import time
import json
# from urllib.parse import urlencode, quote, unquote

app = Flask(__name__)

#http://127.0.0.1:5000/report?watermark=a&timestamp=121212121212&cur_ip=1.1.1.1&src_ip=127.0.0.1&dst_ip=8.8.8.8
@app.route('/report')
def report():
    request_dict = request.args
    witer_to_db(request_dict)
    detect_ip = request_dict['cur_ip']
    ip_info = get_location(detect_ip)
    insert_ip_info(detect_ip, ip_info)
    return 'The request param you request are: ' + request.query_string

#print the trace of watermark select * from table where watermark=' ' order by timestamp
@app.route('/showtrace')
def show():
    cur_watermark = get_cur_watermark()
    result = read_from_db(cur_watermark)
    return render_template("trace.html")

    # return ','.join([x['cur_ip'] for x in result])

@app.route('/tt')
def tt():
    return render_template("trace1.html")

@app.route('/trace2')
def trace2():
    # data = []
    # geoCoordMap = {}
    # cur_watermark = get_cur_watermark()
    # result = read_from_db(cur_watermark)
    # for item in result:
    #     location_info = get_ip_info_from_db(item['cur_ip'])
    #     data.append({"name":location_info['location'], "value":result['timestamp']})
    #     geoCoordMap[location_info['location']] = [location_info['lon'], location_info['lat']]
    data = []
    data.append({"name": "beijing", "value": 1111})
    data.append({"name": "taiyuan", "value": 2222})
    data.append({"name": "xian", "value": 3333})
    data.append({"name": "xiamen", "value": 444})
    geoCoordMap = {}
    geoCoordMap['beijing'] = [116.46,39.92]
    geoCoordMap['taiyuan'] = [112.53,37.87]
    geoCoordMap['xian'] = [108.95,34.27]
    geoCoordMap['xiamen'] = [118.1,24.46]
    return render_template("trace2.html", title = 'Botnet Tracking', data = json.dumps(data), geoCoordMap = json.dumps(geoCoordMap))

def get_cur_watermark():
    watermark_index = int(time.time())/60 % 100000 - 1
    return ''.join(['w', str(watermark_index)])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

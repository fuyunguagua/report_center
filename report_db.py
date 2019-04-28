from config import newDB
from MySQLdb import OperationalError

def wrap(content):
    return '"' + content + '"'

def witer_to_db(request_dict):
    db = newDB()
    db.select_db("track_report")
    cursor = db.cursor()
    sql = 'INSERT INTO RECORD(`TIMESTAMP`,`WATERMARK`,`SRC_IP`,`DST_IP`,`CUR_IP`) VALUES ({},{},{},{},{})'.\
        format(wrap(request_dict['timestamp']),
               wrap(request_dict['watermark']),
               wrap(request_dict['src_ip']),
               wrap(request_dict['dst_ip']),
               wrap(request_dict['cur_ip']))
    cursor.execute(sql)
    try:
        db.commit()
        cursor.close()
        db.close()
    except OperationalError as e:
        print sql
        print e



def read_from_db(watermark):
    db = newDB()
    db.select_db("track_report")
    cursor = db.cursor()
    sql = 'select * from RECORD where `watermark`={} order by `TIMESTAMP`'.format(wrap(watermark))
    rows = cursor.fetchmany(cursor.execute(sql))
    result = []
    for row in rows:
        item = {}
        item['timestamp'] = row[1]
        item['watermark'] = row[2]
        item['src_ip'] = row[3]
        item['dst_ip'] = row[4]
        item['cur_ip'] = row[5]
        result.append(item)
    cursor.close()
    db.close()
    return result


def insert_ip_info(ip, json):
    db = newDB()
    db.select_db("track_report")
    cursor = db.cursor()
    sql = 'INSERT INTO ipInfo(`ip`,`location`,`lon`,`lat`) VALUES ({},{},{},{})'.\
        format(wrap(ip),
               wrap(','.join([json['city'].encode("utf-8"), json['country'].encode("utf-8")])),
               wrap(str(json['lon'])),
               wrap(str(json['lat'])))
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def get_ip_info_from_db(ip):
    db = newDB()
    db.select_db("track_report")
    cursor = db.cursor()
    sql = 'select * from ipInfo where `IP`={}'.format(wrap(ip))
    rows = cursor.fetchmany(cursor.execute(sql))
    result = {}
    if rows:
        row = rows[0]
        result['location'] = row[2]
        result['lon'] = row[3]
        result['lat'] = row[4]
    cursor.close()
    db.close()
    return result


def get_final_detection(position, num):
    db = newDB()
    db.select_db("track_report")
    cursor = db.cursor()
    for i in range(num):
        sql = 'select * from RECORD where `watermark`={} order by `TIMESTAMP`'.format('w' + wrap(str(position + i)))
        rows = cursor.fetchmany(cursor.execute(sql))
        result = []
        for row in rows:
            item = {}
            item['timestamp'] = row[1]
            item['watermark'] = row[2]
            item['src_ip'] = row[3]
            item['dst_ip'] = row[4]
            item['cur_ip'] = row[5]
            result.append(item)
        print 'Watermark {} final IP {}'.format('w' + wrap(position + i), result[-1]['cur_ip'])
    cursor.close()
    db.close()
import urllib2
import json
import time
import datetime
import Adafruit_DHT
APIKEY = '=p43cZKVZSetSL2qUo5X=EsfaP8='
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302}
def http_put():
    humidity, temperature= Adafruit_DHT.read_retry(11, 4)
    CurTime = datetime.datetime.now()
    url='http://api.heclouds.com/devices/22956730/datapoints'
    values={'datastreams':[{"id":"temp","datapoints":[{"at":CurTime.isoformat(),"value":temperature}]},{"id":"humi","datapoints":[{"at":CurTime.isoformat(),"value":humidity}]}]}
    print "CurTime:%s" %CurTime.isoformat()
    print "humidity: %.1f" %humidity
    print "temperatures: %.1f" %temperature
    jdata = json.dumps(values)
    print jdata
    request = urllib2.Request(url, jdata)
    request.add_header('api-key', APIKEY)
    request.get_method = lambda:'POST'
    request = urllib2.urlopen(request)
    return request.read()

while True:
        time.sleep(5)
        resp = http_put()
        print "OneNET:\n %s" %resp
        time.sleep(5)


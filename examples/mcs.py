import Adafruit_DHT
import time
import sys
import httplib, urllib
import json
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
deviceId = "DYo1KV2e"
deviceKey = "AGuycDN4204ghRGJ"
def post_to_mcs(payload):
	headers = {"Content-type": "application/json", "deviceKey": deviceKey}
	not_connected = 1
	while (not_connected):
		try:
			conn = httplib.HTTPConnection("api.mediatek.com:80")
			conn.connect()
			not_connected = 0
		except (httplib.HTTPException, socket.error) as ex:
			print "Error: %s" % ex
			time.sleep(10)
	conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
	response = conn.getresponse()
	print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
	data = response.read()
	conn.close()

while 1:
	humidity, temperature= Adafruit_DHT.read_retry(11, 4)
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

		payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":humidity}},
			{"dataChnId":"Temperature","values":{"value":temperature}}]}
		post_to_mcs(payload)
		time.sleep(3)

	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)


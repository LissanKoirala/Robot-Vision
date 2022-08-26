import urequests
import ujson

urequests.get("http://192.168.1.x:5000/image")
urequests.post("http://192.168.1.x:5000/image", data=ujson.dumps({"key": "data"}))
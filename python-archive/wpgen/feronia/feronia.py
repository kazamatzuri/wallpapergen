import pika
import json
import numpy as np
from spreadlines.spreadlines import SpreadLines

from geomdl import BSpline, knotvector

class Feronia:
    def __init__(self,host='localhost',port=5672,response_callback=None):
        self.host=host
        self.port=port
        self.response_callback=response_callback
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel=self.connection.channel()
        self.channel.queue_declare(queue='feronia')
        self.channel.queue_declare(queue='feronia_result')
        
    def __del__(self):
        self.connection.close()

    def queueWork(self,data):
        message=json.dumps(data)
        self.channel.basic_publish(exchange='',routing_key='feronia',body=message)
    
    def dowork(self,ch, method, properties, body):
        data=json.loads(body)
        points=data['points']
        RADIUS=data['RADIUS']
        WIDTH=data['WIDTH']
        HEIGHT=data['HEIGHT']
        SPREAD=data['SPREAD']
        curve = BSpline.Curve()
        curve.degree = 3
        curve.delta = 0.005
        lpoints = points
        curve.ctrlpts = lpoints
        curve.knotvector = knotvector.generate(3, len(curve.ctrlpts))
        curve_points = curve.evalpts
        temppixels = np.full((WIDTH, HEIGHT), 0.0)
        sl=SpreadLines(temppixels,255) 
        sl.drawline(curve_points)
        print(sl.img_data.max())
        data={}
        data['WIDTH']=WIDTH
        data['HEIGHT']=HEIGHT
        data['pixels']=temppixels.tolist()
        message=json.dumps(data)
        self.channel.basic_publish(exchange='',routing_key='feronia_result',body=message)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def startWoker(self):
        self.channel.basic_consume(queue='feronia',on_message_callback=self.dowork,auto_ack=False)
        print(' [*] Waiting for work. To exit press CTRL+C')
        self.channel.start_consuming()

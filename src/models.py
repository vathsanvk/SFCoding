import csv
from datetime import datetime


def convert_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')


class Customer:
    def __init__(self,customer_id,event_time,last_name,adr_city,adr_state):
        self.customer_id = customer_id
        self.event_time = event_time
        self.last_name = last_name
        self.adr_city = adr_city
        self.adr_state = adr_state




class SiteVisit:
    def __init__(self,page_id,event_time,customer_id,tags):
        self.page_id = page_id
        self.event_time = event_time
        self.customer_id = customer_id
        self.tags = [] if tags is None else tags


class ImageUpload:
    def __init__(self,image_id,event_time,customer_id,camera_make,camera_model):
        self.image_id = image_id
        self.event_time = event_time
        self.customer_id = customer_id
        self.camera_make = camera_make
        self.camera_model = camera_model

class Order:
    def __init__(self,order_id,event_time,customer_id,total_amount):
        self.order_id = order_id
        self.event_time = event_time
        self.customer_id = customer_id
        self.total_amount = 0
        if total_amount and len(total_amount) > 0:
            self.total_amount = float(total_amount.split(' ')[0].strip())

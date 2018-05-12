import models

from datetime import datetime,timedelta
from operator import attrgetter,itemgetter

def ingest(event,event_store):

    if event['type'] == 'CUSTOMER':
       #check if customer key exists in event store, if not add else check if the event verb is update and update the customer
       customer_id = str(event['key'])
       if customer_id not in event_store:
          event_time = models.convert_datetime(event['event_time'])
          last_name = event['last_name']
          adr_city = event['adr_city']
          adr_state = event['adr_state']
          customer = models.Customer(customer_id,event_time,last_name,adr_city,adr_state)
          event_store[customer_id] = {'customer_info' : customer}
       else:
          #if the verb is Update. Update the customer
          if event['verb'] == 'UPDATE':
              customer = event_store[key]['customer_info']
              customer.event_time = models.convert_datetime(event['event_time'])
              customer.last_name = event['last_name']
              customer.adr_city = event['adr_city']
              customer.adr_state = event['adr_state']



    if event['type'] == 'SITE_VISIT':
       #assign the site visit to the customer in the event store dict

       page_id = event['key']
       customer_id = event['customer_id']
       if customer_id not in event_store:
           raise ValueError('Customer does not exist for this site visit!')

       #site_visits is a dict with key as page_id and value as SiteVisit objecte
       if 'site_visits' not in event_store[customer_id]:
          event_store[customer_id]['site_visits'] = {}


       site_visits = event_store[customer_id]['site_visits']
       if page_id not in site_visits:
          event_time = models.convert_datetime(event['event_time'])
          customer_id = event['customer_id']
          tags = event['tags']
          site_visit = models.SiteVisit(page_id,event_time,customer_id,tags)
          site_visits[page_id] = site_visit


    if event['type'] == 'IMAGE':
       #assign the image upload to the customer in the event store dict

       image_id = event['key']
       customer_id = event['customer_id']
       if customer_id not in event_store:
           raise ValueError('Customer does not exist for this image upload!')

       #image_uploads is a dict with key as image_id and value as ImageUpload object
       if 'image_uploads' not in event_store[customer_id]:
          event_store[customer_id]['image_uploads'] = {}


       image_uploads = event_store[customer_id]['image_uploads']

       if image_id not in image_uploads:
          event_time = models.convert_datetime(event['event_time'])
          customer_id = event['customer_id']
          camera_make = event['camera_make']
          camera_model = event['camera_model']
          image_upload = models.ImageUpload(image_id,event_time,customer_id,camera_model,camera_make)
          image_uploads[image_id] = image_upload


    if event['type'] == 'ORDER':
       #assign the order to the customer in the event store dict

       order_id = event['key']
       customer_id = event['customer_id']
       if customer_id not in event_store:
           raise ValueError('Customer does not exist for this order!')

       #orders is a dict with key as orderid and value as Order object
       if 'orders' not in event_store[customer_id]:
           event_store[customer_id]['orders'] = {}


       orders = event_store[customer_id]['orders']

       if order_id not in orders:
          event_time = models.convert_datetime(event['event_time'])
          customer_id = event['customer_id']
          total_amount = event['total_amount']
          order = models.Order(order_id,event_time,customer_id,total_amount)
          orders[order_id] = order
       else:
          #if the verb is Update. Update the order
          if event['verb'] == 'UPDATE':
              order = event_store[customer_id]['orders'][order_id]
              order.event_time = models.convert_datetime(event['event_time'])
              order.customer_id = event['customer_id']
              order.total_amount = event['total_amount']

    return event_store

def get_total_weeks_between_dates(site_visits):

    #getting min and max dates from the list of SiteVisit objects
    start_date = min(site_visits.values(),key=attrgetter('event_time'))
    end_date = max(site_visits.values(),key=attrgetter('event_time'))



    return (end_date.event_time - start_date.event_time).days / 7




def get_avg_customer_val_per_week(customer_id,customer_activity):
    #get total expenditure from orders
    total_expenditure = 0
    orders = customer_activity.get('orders',{})

    for order in orders:
        order = orders[order]
        total_expenditure += float(order.total_amount)

    #get total number of site visits
    site_visits = customer_activity.get('site_visits',{})
    total_site_visits = len(site_visits)

    #number of active weeks
    active_weeks = get_total_weeks_between_dates(site_visits)

    if total_site_visits > 0 and active_weeks > 0:
       site_visits_per_week = total_site_visits/float(active_weeks)
       expenditure_per_visit = total_expenditure/float(total_site_visits)
       return expenditure_per_visit * site_visits_per_week

    return 0




def top_X_simple_LTV_customers(X,event_store):
    customer_lifetime_value = {}
    lifespan = 10
    for customer_id,customer_activity in event_store.items():
        lifetime_value = 52 * get_avg_customer_val_per_week(customer_id,customer_activity) * lifespan
        customer_lifetime_value[customer_id] = round(lifetime_value,2)

    #return top X customers
    return sorted(customer_lifetime_value.items(),key=itemgetter(1),reverse=True)

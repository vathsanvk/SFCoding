import json
import csv
from datetime import datetime
from get_analytics import ingest,top_X_simple_LTV_customers


def read_input(input_file,event_store):
    data = json.loads(input_file.read())
    for event in data:
        try:
          ingest(event,event_store)
        except ValueError as e:
          event_type = event['type']
          key = event['key']
          error_msg = str(e)
          error_time  = datetime.now()
          row = [error_time,event_type,key,error_msg]
          error_log_writer.writerow(row)



def get_top_X_LTV_customers(X=5):

    top_ten = top_X_simple_LTV_customers(X, event_store)
    for k,v in top_ten:
        output_writer.writerow([k,v])




if __name__ == '__main__':
    #declare the dictionary which will store all the processed event data
    event_store = {}
    #open error log writer to log ingestion errors
    error_log_file = open('../output/error_log.txt','a')
    error_log_writer = csv.writer(error_log_file)

    #open input file and reading it as a json
    with open('../input/input.txt','r') as input_file:
         read_input(input_file,event_store)
    #create output as a csv file
    op_file = open('../output/output.txt','w')
    output_writer = csv.writer(op_file)
    get_top_X_LTV_customers(X=10)

    error_log_file.close()
    op_file.close()

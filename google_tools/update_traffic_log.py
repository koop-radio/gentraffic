from google_tools.get_most_recent_file import get_most_recent_file
import csv
from datetime import datetime

def update_traffic_log():
    print("entering update_traffic_log")
    return get_most_recent_file()  # This downloads the latest traffic.csv file
    #with open('traffic.csv', mode='r') as file:
        #csv_reader = csv.reader(file)
        #for row in csv_reader:
        #    if 'Week of:' in row[0]:
        #        date_str = row[1].strip()
        #        traffic_date = datetime.strptime(date_str, '%m/%d/%Y')
        #        if traffic_date > datetime.now():
        #            return True
        #        else:
        #            return False
    # GROK return True  # In case the file doesn't match expected format

if __name__ == '__main__':
    print(update_traffic_log())

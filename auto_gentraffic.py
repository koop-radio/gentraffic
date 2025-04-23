import shutil
import csv
from datetime import datetime, timedelta
from os.path import exists
from gentraffic import gentraffic
from google_tools.update_traffic_log import update_traffic_log
from google_tools.send_results import send_results
from xfile import xfile
from update_dad import update_dad
from extract_lengths_and_send_gmail import extract_lengths_and_send_gmail 

def find_start_day(csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if 'week of' in row[1].lower():  # Assuming "week of" is always in column 2
                date_string = row[2].strip()  # Assuming date is always in column 3
                break
        else:
            # If "week of" not found in any row, return None
            return None

    # Parse the "week of" date
    date_format = "%m/%d/%Y"
    week_of_date = datetime.strptime(date_string, date_format).date()

    # Calculate the current date without the time component
    current_date = datetime.now().date()

    # If "week of" is in the future, return "MONDAY"
    if current_date < week_of_date:
        return "MONDAY"

    # Calculate the difference in days from "week of" to current date
    days_diff = (current_date - week_of_date).days

    # If today is within the "week of" period but not the last day, find the next valid update day
    if 0 <= days_diff < 6:
        next_valid_day = current_date + timedelta(days=1)  # The day after the current day
        next_valid_day_name = next_valid_day.strftime("%A").upper()  # Get the day name in uppercase
        return next_valid_day_name

    # If the current day is the last day of the "week of" period or the entire week is in the past, return None
    return None

def auto_gentraffic():
    print("launching auto_gentraffic")
    if update_traffic_log():
        print("Passed traffic log test")
        startday = find_start_day("traffic.csv")
        if startday:
            #if os.path.isfile(dst):
                #os.remove(dst)
            shutil.move("./traffic.csv", "./inputfiles/traffic.csv",copy_function=shutil.copy)
            if gentraffic(startday):
                print("Finished gentraffic phase")
                xfile()
                print("Updating DAD with startday", startday)
                update_dad(startday)
                # GROK send_results()
                extract_lengths_and_send_gmail()
                print("\nAll Programs Finished!!\n")
                current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
                # GROK shutil.make_archive(f'../gt_{current_datetime}', 'zip', '..', 'gentraffic')
                return True
    return False

if __name__ == '__main__':
    print("In main")
    on_prod = False
    if exists('/mnt/DAD/DAD/Files/CUTS.DBF'):
        on_prod = True
    print("calling auto_gentraffic directly")
    if not auto_gentraffic():
        print("auto_gentraffic failed!!!!")

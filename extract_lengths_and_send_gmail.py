import json
import glob
from google_tools.sendgmail import sendgmail


def extract_records_between_times(log_file, weekdays, start_time, end_time):
    start_hour = int(start_time.split(':')[0])
    end_hour = int(end_time.split(':')[0])

    day_records = {day: [] for day in weekdays}
    cut_ids = set()

    with open(log_file, 'r') as file:
        content = file.read()
        data = json.loads(content)
        for day, records in data.items():
            if day in weekdays:
                last_known_time = None
                for record in records:
                    record_time = record.get('TIME')
                    if record_time:
                        last_known_time = record_time
                    else:
                        record_time = last_known_time
                    if record_time:
                        record_hour = int(record_time.split(':')[0])
                        if start_hour <= record_hour < end_hour:
                            cut_id = record.get('CUT')
                            if cut_id:
                                cut_ids.add(cut_id)
                            day_records[day].append(record)
    
    return day_records, cut_ids


def extract_cut_records(cut_record_file, cut_ids):
    with open(cut_record_file, 'r') as file:
        content = file.read()
        cut_records = json.loads(content)
    
    cut_dict = {record['CUT']: record for record in cut_records if record['CUT'] in cut_ids}
    return cut_dict


def extract_cut_lengths(day_records, cut_dict):
    day_lengths = {day: [] for day in day_records.keys()}

    for day, records in day_records.items():
        for record in records:
            cut_id = record.get('CUT')
            if cut_id:
                length_str = cut_dict.get(cut_id, {}).get('LENGTH', 0)
                length = float(length_str)
                day_lengths[day].append(length)
    
    return day_lengths


def print_lengths_and_sums(day_lengths):
    result = []
    for day, lengths in day_lengths.items():
        total_length = sum(lengths)
        lengths_str = ' + '.join(map(str, lengths))
        result.append(f"{day}: {lengths_str} = {total_length}")
    return '\n'.join(result)


def get_legal_id_cut(template_file, start_time):
    with open(template_file, 'r') as file:
        lines = file.readlines()

    found_start_time = False
    for i, line in enumerate(lines):
        parts = line.strip().split(',')
        time_without_seconds = parts[0].strip()[:5]  # Remove the seconds part
        if len(parts) > 1 and time_without_seconds == start_time:
            found_start_time = True
            for next_line in lines[i+1:]:
                next_parts = next_line.strip().split(',')
                if len(next_parts) > 1 and next_parts[0].strip() == '':
                    cut_id = next_parts[1].strip()
                    if cut_id:
                        return cut_id
    return None


def add_legal_id_cuts(weekdays, start_time, day_records, cut_ids):
    for day in weekdays:
        template_file = f'templates/{day.lower()}_template.txt'
        legal_id_cut = get_legal_id_cut(template_file, start_time)
        if legal_id_cut and legal_id_cut not in cut_ids:
            cut_ids.add(legal_id_cut)
        if legal_id_cut:
            day_records[day].insert(0, {'TIME': start_time, 'CUT': legal_id_cut})
    return day_records, cut_ids


def extract_lengths_and_send_gmail():
    log_file = 'logs/traffic_x_ref.json'
    cut_record_file = 'logs/cut_records.json'
    weekdays = ['Tuesday', 'Thursday']
    start_time = '14:00'
    end_time = '15:00'

    day_records, cut_ids = extract_records_between_times(log_file, weekdays, start_time, end_time)
    day_records, cut_ids = add_legal_id_cuts(weekdays, start_time, day_records, cut_ids)

    #print(day_records)
    cut_dict = extract_cut_records(cut_record_file, cut_ids)
    day_lengths = extract_cut_lengths(day_records, cut_dict)
    lengths_and_sums_str = print_lengths_and_sums(day_lengths)
    email_body = f"Here are the total traffic times and sums between {start_time} and {end_time}:\n"
    email_body += lengths_and_sums_str
    sendgmail("traffic times from prodmmauto", email_body, "playout@koop.org, leafkeeperken@gmail.com, kenz@koop.org, dean@koop.org, jerell@koop.org")

if __name__ == "__main__":
    extract_lengths_and_send_gmail()

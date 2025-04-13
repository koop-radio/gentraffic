from google_tools.sendgmail import sendgmail
from google_tools.list_recent_kdrive_files import list_recent_kdrive_files

def send_results():
    with open('logs/xfile.txt', 'r') as file:
        lines = file.readlines()[:20]  # Read the top 5 entries (20 lines)
    body = "AutoGenTraffic completed successfully.\n\nHere are the top 5 mismatches (if any) from the cross reference report.   (Note, a '1' in the first entry means an exact match, and entries are listed in descending order of failure.   As such, a '1' in the first entry means all matches were perfect.\n\nHere are the entries:\n\n"
    body += ''.join(lines)  # Combine the lines into a single string
    body += "\n\n"
    body += list_recent_kdrive_files()
    body += "\n\n"
    subject = 'AutoGenTraffic Completed'
    sendgmail(subject, body)

if __name__ == '__main__':
    send_results()

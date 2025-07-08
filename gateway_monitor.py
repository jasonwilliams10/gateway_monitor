import os
import time
import datetime
import smtplib
from email.mime.text import MIMEText

log_file = r"C:\Program Files (x86)\gateway_log.txt"

# Email details
sender_email = "youremail@protonmail.com"
receiver_email = "email@gmail.com"
cc_receiver_email = "email2@gmail.com"

def send_email(body, subject):
    message = MIMEText(body, 'plain')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Cc'] = cc_receiver_email

    try:
        with smtplib.SMTP('localhost', 1025) as server:
            server.login(sender_email, 'protonmail_bridge_pw')
            server.sendmail(sender_email, [receiver_email, cc_receiver_email], message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def log_status(message):
    date_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    try:
        with open(log_file, "a") as f:
            f.write(f"{date_time}: {message}\n")
    except IOError as e:
        print(f"Error writing to file: {e}")

def ping(host):
    return os.system(f"ping -c 1 {host}") == 0

def handle_status(host, name, iteration_count, is_up):
    now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    if is_up:
        if iteration_count > 0:
            message = f"{name} is back UP as of {now} and was potentially down for {int(iteration_count / 60)} minutes."
            print(message)
            log_status(message)
            send_email(message, f"{name} is back UP")
            return 0
        else:
            print(f"{name} is UP at {now}")
            return 0
    else:
        iteration_count += 300
        print(f"{name} is DOWN at {now}. Down for {int(iteration_count / 60)} minutes.")
        log_status(f"{name} is DOWN.")
        send_email(f"{name} is DOWN as of {now} and has potentially been down for {int(iteration_count / 60)} minutes.", f"{name} is DOWN")
        return iteration_count

def monitor(host_map, interval=300):
    iteration_counts = {host: 0 for host in host_map}
    while True:
        for host, name in host_map.items():
            is_up = ping(host)
            iteration_counts[host] = handle_status(host, name, iteration_counts[host], is_up)
        time.sleep(interval)

if __name__ == "__main__":
    hosts = {
        "1.1.1.1.1.1": "GW1",
        "2.2.2.2.2.2": "GW2",
        "3.3.3.3.3.3": "GW3",
        "4.4.4.4.4.4": "GW4",
        "5.5.5.5.5.5": "GW5",
        "6.6.6.6.6.6": "GW6",
    }
    monitor(hosts)

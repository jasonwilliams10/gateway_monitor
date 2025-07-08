import os
import time
import datetime
import smtplib
from email.mime.text import MIMEText

log_file = r"C:\Program Files (x86)\Vigilix\gateway_log.txt"

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
            message = f"The {name} is back UP as of {now} and was potentially down for {int(iteration_count / 60)} minutes."
            print(message)
            log_status(message)
            send_email(message, f"The {name} is back UP")
            return 0
        else:
            print(f"{name} is UP at {now}")
            return 0
    else:
        iteration_count += 300
        print(f"{name} is DOWN at {now}. Down for {int(iteration_count / 60)} minutes.")
        log_status(f"The {name} is DOWN.")
        send_email(f"{name} is DOWN as of {now} and has potentially been down for {int(iteration_count / 60)} minutes.", f"The {name} is DOWN")
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
        "208.83.78.45": "Greenville Gateway",
        "208.83.78.46": "Greenville(RC2) Gateway",
        "52.165.31.120": "Iowa Gateway",
        "52.88.11.253": "Oregon Gateway",
        "18.211.25.51": "Virginia Gateway",
        "3.132.187.169": "Ohio Gateway",
        "208.87.85.52": "download.vigilix.net",
        "208.87.85.53": "initialdownload.vigilix.net",
        "208.83.78.43": "agent.vigilix.net",
    }
    monitor(hosts)

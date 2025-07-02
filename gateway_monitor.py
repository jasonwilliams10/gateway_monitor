import os
import time
import datetime
import smtplib
from email.mime.text import MIMEText

#log file to write information to
log_file ="C:\Program Files (x86)\gateway_log.txt"

# Email details
sender_email = "your_email@protonmail.com" # Use the email address associated with the Bridge token
receiver_email = "abc123@example.com"
cc_receiver_email = "abc123@gmail.com"
subject = ""
body = ""

# Create the email message
message = MIMEText(body, 'plain')
message['Subject'] = subject
message['From'] = sender_email
message['To'] = receiver_email
message['Cc'] = cc_receiver_email

def send_email(body, subject, sender_email, receiver_email, cc_receiver_email):
    # Create the email message
    now = datetime.datetime.now()
    message = MIMEText(body, 'plain')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Cc'] = cc_receiver_email
    try:
    # Connect to the Proton Mail Bridge's SMTP server
        with smtplib.SMTP('localhost', 1025) as server:
        # Uncomment and use the following line for TLS/SSL if needed:
        # server.starttls()

        # Authenticate with the Bridge (using the Bridge's generated password)
            server.login(sender_email, 'bridge_password') # Replace with the bridge password

        # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

#Gateways to monitor
gw1 = "1.1.1.1.1.1"
gw2 = "2.2.2.2.2.2"
gw3 = "3.3.3.3.3.3"
gw4 = "4.4.4.4.4.4"
gw5 = "5.5.5.5.5.5"
gw6 = "6.6.6.6.6.6"

def ping(host):
    """Pings a host and returns True if successful, False otherwise."""
    response = os.system("ping -c 1 " + host)
    return response == 0

def monitor(hosts, interval= 300): #pings every 5 minutes in seconds. 60 x minutes to get seconds.
    """Monitors a list of hosts and prints their status."""
   
    #Counts how many times the gateway(s) have not been pinged successfully
    gw1_iteration_count = 0
    gw2_iteration_count = 0
    gw3_iteration_count = 0
    gw4_iteration_count = 0
    gw5_iteration_count = 0
    gw6_iteration_count = 0
    while True:
        now = datetime.datetime.now()
        for host in hosts:
            if ping(host):
                if host == gw1 and gw1_iteration_count == 0:
                    print("Gateway 1 is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == gw1 and gw1_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"Gateway 1 is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: Gateway 1 is back UP.\n")
                        except IOError as e:             
                                print(f"Error writing to file: {e}")
                        #Send email
                        subject = "Gateway 1 is back UP"
                        body = f"Gateway 1 is back UP as of {date_time} and was potentionally down for {int(gw1_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        gw1_iteration_count = 0
                if host == gw2_vigilix_net and gw2_iteration_count == 0:
                   print("Gateway 2 is UP", now.strftime("%m-%d-%Y %H:%M:%S")) 
                elif host == gw2 and gw2_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"Gateway 2 is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: Gateway 2 is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file: {e}")
                        #Send email
                        subject = "Gateway 2 is back UP"
                        body = f"Gateway 2 is back UP as of {date_time} and was potentionally down for {int(gw2_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        gw2_iteration_count = 0
                if host == gw3_vigilix_net and gw3_iteration_count == 0:
                    print("Gateway 3 is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == gw3 and gw3_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"Gateway 3 is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: Gateway 3 is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file: {e}")
                        #Send email
                        subject = "Gateway 3 is back UP"
                        body = f"Gateway 3 is back UP as of {date_time} and was potentionally down for {int(gw3_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        gw3_iteration_count = 0
                if host == gw4 and gw4_iteration_count == 0:
                    print("Gateway 4 is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == gw4_vigilix_net and gw4_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"Gateway 4 is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: Gateway 4 is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file {e}")
                        #Send email
                        subject = "Gateway 4 is back UP"
                        body = f"Gateway 4 is back UP as of {date_time} and was potentionally down for {int(gw4_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        gw4_iteration_count
                if host == gw5 and gw5_iteration_count == 0:
                    print("Gateway 5 is UP", now.strftime("%m-%d-%Y %H:%M:%S")) 
                elif host == gw5 and gw5_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"Gateway 5 is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: Gateway 5 is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file {e}")
                        #Send email
                        subject = "Gateway 5 is back UP"
                        body = f"Gateway 5 is back UP as of {date_time} and was potentionally down for {int(gw5_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        gw5_iteration_count = 0
                if host == gw6 and gw6_iteration_count == 0:  
                    print("Gateway 6 is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == gw6 and gw6_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"Gateway 6 is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: Gateway 6 is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file {e}")
                        #Send email
                        subject = "Gateway 6 is back UP"
                        body = f"Gateway 6 is back UP as of {date_time} and was potentionally down for {int(gw6_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        gw6_iteration_count = 0
            else:
                if host == gw1:
                    gw1_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("Gateway 1 is Down. Email being sent.", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"Gateway 1 has been down for {int(gw1_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: Gateway 1 is DOWN.\n")
                    except IOError as e:             
                            print(f"Error writing to file: {e}")
                    #Send email
                    subject = "Gateway 1 is DOWN"
                    body = f"Gateway 1 is DOWN as of {date_time} and has potentionally been down for {int(gw1_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                elif host == gw2:
                    gw2_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("Gateway 2 is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"Gateway 2 has been down for {int(gw2_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: Gateway 2 is DOWN.\n")
                    except ImportError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "Gateway 2 is DOWN"
                    body = f"Gateway 2 is DOWN as of {date_time} and has potentionally been down for {int(gw2_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                elif host == gw3:
                    gw3_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("Gateway 3 is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"Gateway 3 has been down for {int(gw3_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: Gateway 3 is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "Gateway 3 is DOWN"
                    body = f"Gateway 3 is DOWN as of {date_time} and has potentionally been down for {int(gw3_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email) 
                elif host == gw4:
                    gw4_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("Gateway 4 is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"Gateway 4 has been down for {int(gw4_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: Gateway 4 is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "Gateway 4 is DOWN"
                    body = f"Gateway 4 is DOWN as of {date_time} and has potentionally been down for {int(gw4_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email)  
                elif host == gw5:
                    gw5_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("Gateway 5 is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"Gateway 5 has been down for {int(gw5_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: Gateway 5 is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "Gateway 5 is DOWN"
                    body = f"Gateway 5 is DOWN as of {date_time} and has potentionally been down for {int(gw5_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email) 
                elif host == gw6:
                    gw6_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("Gateway 6 is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"Gateway 6 has been down for {int(gw6_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: Gateway 6 is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "Gateway 6 is DOWN"
                    body = f"Gateway 6 is DOWN as of {date_time} and has potentionally been down for {int(gw6_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email) 
        time.sleep(interval)
if __name__ == "__main__":
    hosts_to_monitor = [gw1, gw2, gw3, gw4, gw5, gw6] #Replace with your host(s)
    monitor(hosts_to_monitor)

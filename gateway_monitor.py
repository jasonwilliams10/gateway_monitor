import os
import time
import datetime
import smtplib
from email.mime.text import MIMEText

log_file ="C:\Program Files (x86)\Vigilix\gateway_log.txt"

# Email details
sender_email = "jasonwilliams10@protonmail.com" # Use the email address associated with the Bridge token
receiver_email = "jason.williams@vigilix.com"
cc_receiver_email = "james.jasinski@vigilix.com"
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
            server.login(sender_email, 'XaZvbexjxhe0sFseUN_ixg') # Replace with the bridge password

        # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")

#Gateways
rc_vigilix_net = "208.83.78.45"
rc2_vigilix_net = "208.83.78.46"
rcia_vigilix_net = "52.165.31.120"
rcor_vigilix_net = "52.88.11.253"
rcva_vigilix_net = "18.211.25.51"
rcoh_vigilix_net = "3.132.187.169"

def ping(host):
    """Pings a host and returns True if successful, False otherwise."""
    response = os.system("ping -c 1 " + host)
    return response == 0

def monitor(hosts, interval= 300): #pings every 5 minutes in seconds. 60 x minutes to get seconds.
    """Monitors a list of hosts and prints their status."""
    rc_iteration_count = 0
    rc2_iteration_count = 0
    rcia_iteration_count = 0
    rcor_iteration_count = 0
    rcva_iteration_count = 0
    rcoh_iteration_count = 0
    while True:
        now = datetime.datetime.now()
        for host in hosts:
            if ping(host):
                if host == rc_vigilix_net and rc_iteration_count == 0:
                    print("RC.Vigilix.Net is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == rc_vigilix_net and rc_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"The Greenville Gateway is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: The Greenville Gateway is back UP.\n")
                        except IOError as e:             
                                print(f"Error writing to file: {e}")
                        #Send email
                        subject = "The Greenville Gateway is back UP"
                        body = f"The Greenville Gateway is back UP as of {date_time} and was potentionally down for {int(rc_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        rc_iteration_count = 0
                if host == rc2_vigilix_net and rc2_iteration_count == 0:
                   print("The Greenville(RC2) Gateway is UP", now.strftime("%m-%d-%Y %H:%M:%S")) 
                elif host == rc2_vigilix_net and rc2_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"The Greenville(RC2) Gateway is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: The Greenville(RC2 Gateway is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file: {e}")
                        #Send email
                        subject = "The Greenville(RC2) Gateway is back UP"
                        body = f"The Greenville(RC2) Gateway is back UP as of {date_time} and was potentionally down for {int(rc2_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        rc2_iteration_count = 0
                if host == rcia_vigilix_net and rcia_iteration_count == 0:
                    print("The Iowa Gateway is is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == rcia_vigilix_net and rcia_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"The Iowa Gateway is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: The Iowa Gateway is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file: {e}")
                        #Send email
                        subject = "The Iowa Gateway is back UP"
                        body = f"The Iowa Gateway is back UP as of {date_time} and was potentionally down for {int(rcia_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        rcia_iteration_count = 0
                if host == rcor_vigilix_net and rcor_iteration_count == 0:
                    print("RCOR.Vigilix.net is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == rcor_vigilix_net and rcor_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"The Oregon Gateway is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: The Oregon Gateway is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file {e}")
                        #Send email
                        subject = "The Oregon Gateway is back UP"
                        body = f"The Oregon Gateway is back UP as of {date_time} and was potentionally down for {int(rcor_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        rcor_iteration_count
                if host == rcva_vigilix_net and rcva_iteration_count == 0:
                    print("RCVA.Vigilix.net is UP", now.strftime("%m-%d-%Y %H:%M:%S")) 
                elif host == rcva_vigilix_net and rcva_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"The Virginia Gateway is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: The Virginia Gateway is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file {e}")
                        #Send email
                        subject = "The Virginia Gateway is back UP"
                        body = f"The Virginia Gateway is back UP as of {date_time} and was potentionally down for {int(rcva_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        rcva_iteration_count = 0
                if host == rcoh_vigilix_net and rcoh_iteration_count == 0:  
                    print("RCOH.Vigilix.net is UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                elif host == rcoh_vigilix_net and rcoh_iteration_count > 0:
                        date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                        #Print to screen
                        print(f"The Ohio Gateway is back UP", now.strftime("%m-%d-%Y %H:%M:%S"))
                        #Save to log
                        try:
                            with open(log_file, "a") as f:
                                f.write(f"{date_time}: The Ohio Gateway is back UP.\n")
                        except IOError as e:
                             print(f"Error writing to file {e}")
                        #Send email
                        subject = "The Ohio Gateway is back UP"
                        body = f"The Ohio Gateway is back UP as of {date_time} and was potentionally down for {int(rcoh_iteration_count / 60)} minutes." 
                        send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                        rcoh_iteration_count = 0
            else:
                if host == rc_vigilix_net:
                    rc_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("RC.Vigilix.Net is Down. Email being sent.", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"RC.Vigilix.Net has been down for {int(rc_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: The Greenville Gateway is DOWN.\n")
                    except IOError as e:             
                            print(f"Error writing to file: {e}")
                    #Send email
                    subject = "The Greenville Gateway is DOWN"
                    body = f"RC.Vigilix.Net is DOWN as of {date_time} and has potentionally been down for {int(rc_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                elif host == rc2_vigilix_net:
                    rc2_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("RC2.Vigilix.Net is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"RC2.Vigilix.Net has been down for {int(rc2_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: The Greenville(RC2) Gateway is DOWN.\n")
                    except ImportError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "The Greenville(RC2) Gateway is DOWN"
                    body = f"RC2.Vigilix.Net is DOWN as of {date_time} and has potentionally been down for {int(rc2_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email)
                elif host == rcia_vigilix_net:
                    rcia_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("RCIA.Vigilix.Net is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"RCIA.Vigilix.Net has been down for {int(rcia_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: The Iowa Gateway is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "The Iowa Gateway is DOWN"
                    body = f"RCIA.Vigilix.Net is DOWN as of {date_time} and has potentionally been down for {int(rcia_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email) 
                elif host == rcor_vigilix_net:
                    rcor_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("RCOR.Vigilix.Net is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"RCOR.Vigilix.Net has been down for {int(rcor_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: The Oregon Gateway is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "The Oregon Gateway is DOWN"
                    body = f"RCOR.Vigilix.Net is DOWN as of {date_time} and has potentionally been down for {int(rcor_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email)  
                elif host == rcva_vigilix_net:
                    rcva_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("RCVA.Vigilix.Net is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"RCVA.Vigilix.Net has been down for {int(rcva_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: The Virginia Gateway is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "The Virginia Gateway is DOWN"
                    body = f"RVA.Vigilix.Net is DOWN as of {date_time} and has potentionally been down for {int(rcva_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email) 
                elif host == rcoh_vigilix_net:
                    rcoh_iteration_count += 300
                    date_time = now.strftime("%m-%d-%Y %H:%M:%S")
                    #Print to screen
                    print("RCOH.Vigilix.Net is Down", now.strftime("%m-%d-%Y %H:%M:%S"))
                    print(f"RCOH.Vigilix.Net has been down for {int(rcoh_iteration_count / 60)} minutes as of", now.strftime("%m-%d-%Y %H:%M:%S"))
                    #Save to log
                    try:
                        with open(log_file, "a") as f:
                            f.write(f"{date_time}: The Ohio Gateway is DOWN.\n")
                    except IOError as e:
                         print(f"Error writing to file {e}")
                    #Send email
                    subject = "The Ohio Gateway is DOWN"
                    body = f"RCOH.Vigilix.Net is DOWN as of {date_time} and has potentionally been down for {int(rcoh_iteration_count / 60)} minutes." 
                    send_email(body, subject, sender_email, receiver_email, cc_receiver_email) 
        time.sleep(interval)
if __name__ == "__main__":
    hosts_to_monitor = [rc_vigilix_net, rc2_vigilix_net, rcia_vigilix_net, rcor_vigilix_net, rcva_vigilix_net, rcoh_vigilix_net] #Replace with your host(s)
    monitor(hosts_to_monitor)
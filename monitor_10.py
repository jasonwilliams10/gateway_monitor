import os
import time
import datetime
import smtplib
import json
import shutil
import subprocess
from pathlib import Path
from email.mime.text import MIMEText
from dotenv import load_dotenv
 
# Load environment variables from .env file
load_dotenv()
 
# Default config file path (can be overridden by environment variable)
DEFAULT_CONFIG_FILE = "config.json"
 
def load_config():
    config_file = os.getenv("CONFIG_FILE", DEFAULT_CONFIG_FILE)
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file {config_file} not found! Please create it.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON in {config_file}! Fix it, buddy.")
        exit(1)
 
def get_setting(env_var, config_key, config, default=None):
    return os.getenv(env_var) or config.get(config_key, default)
 
# Load config and settings
config = load_config()
log_file = get_setting("LOG_FILE", "log_file", config)
sender_email = get_setting("SENDER_EMAIL", "sender_email", config)
receiver_email = get_setting("RECEIVER_EMAIL", "receiver_email", config)
cc_receiver_email = get_setting("CC_RECEIVER_EMAIL", "cc_receiver_email", config)
smtp_server = get_setting("SMTP_SERVER", "smtp_server", config, "localhost")
smtp_port = int(get_setting("SMTP_PORT", "smtp_port", config, 1025))
interval = int(get_setting("CHECK_INTERVAL", "interval", config, 300))
default_port = int(get_setting("CHECK_PORT", "port", config, 443))
check_timeout = int(get_setting("CHECK_TIMEOUT", "check_timeout", config, 60))
hosts = config.get("hosts", {})
 
# Validate required settings
required_settings = {
    "LOG_FILE": log_file,
    "SENDER_EMAIL": sender_email,
    "RECEIVER_EMAIL": receiver_email,
    "CC_RECEIVER_EMAIL": cc_receiver_email,
    "SMTP_SERVER": smtp_server,
}
for key, value in required_settings.items():
    if not value:
        print(f"Missing required setting: {key}. Set it in environment, .env, or config.json.")
        exit(1)
 
if not hosts:
    print("No hosts defined in config.json! Nothing to monitor.")
    exit(1)
 
# Get SMTP password from environment variable or .env file
smtp_password = os.getenv("SMTP_PASSWORD")
if not smtp_password:
    print("SMTP_PASSWORD not set in environment or .env file! Can't send emails without it.")
    exit(1)
 
def normalize_email_list(value):
    """Return a clean list of email addresses from a list or comma-separated string."""
    if not value:
        return []
 
    if isinstance(value, str):
        return [address.strip() for address in value.split(",") if address.strip()]
 
    if isinstance(value, (list, tuple, set)):
        return [str(address).strip() for address in value if str(address).strip()]
 
    raise TypeError("Email recipients must be a list or comma-separated string.")
 
 
def send_email(body, subject):
    to_recipients = normalize_email_list(receiver_email)
    cc_recipients = normalize_email_list(cc_receiver_email)
    all_recipients = to_recipients + cc_recipients
 
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ", ".join(to_recipients)
 
    if cc_recipients:
        message["Cc"] = ", ".join(cc_recipients)
 
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, all_recipients, message.as_string())
            print(f"Email sent successfully to: {', '.join(all_recipients)}")
    except Exception as e:
        print(f"Error sending email: {e}")
 
def log_status(message):
    date_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    try:
        # Ensure the log directory exists
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a") as f:
            f.write(f"{date_time}: {message}\n")
    except IOError as e:
        print(f"Error writing to file: {e}")
 
def find_powershell():
    """Locate Windows PowerShell or PowerShell 7 (pwsh)."""
    for exe in ("powershell", "pwsh"):
        path = shutil.which(exe)
        if path:
            return path
    return None
 
 
POWERSHELL = find_powershell()
if not POWERSHELL:
    print("PowerShell not found! Test-NetConnection requires powershell.exe or pwsh on PATH.")
    exit(1)
 
 
def parse_host(host):
    """Split 'host:port' into (host, port). Falls back to the default port."""
    name, sep, port = host.rpartition(":")
    if sep and port.isdigit() and ":" not in name:
        return name, int(port)
    return host, default_port
 
 
def check_connection(host):
    """Run Test-NetConnection against host on a TCP port and return True if it succeeds."""
    target, port = parse_host(host)
    safe_target = target.replace("'", "''")  # escape for a PowerShell single-quoted string
    command = (
        f"(Test-NetConnection -ComputerName '{safe_target}' -Port {port} "
        f"-WarningAction SilentlyContinue).TcpTestSucceeded"
    )
    try:
        result = subprocess.run(
            [POWERSHELL, "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=check_timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"Test-NetConnection to {target}:{port} timed out after {check_timeout}s.")
        return False
 
    succeeded = result.stdout.strip().lower() == "true"
    print(f"Test-NetConnection {target}:{port} -> {'Succeeded' if succeeded else 'Failed'}")
    return succeeded
 
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
        if iteration_count == 0:
            # First failed check: just report that it's down, no duration yet
            message = f"{name} is DOWN as of {now}."
        else:
            # Later checks: report how long it's been down since the first failure
            message = f"{name} is DOWN as of {now} and has potentially been down for {int(iteration_count / 60)} minutes."
        print(message)
        log_status(f"{name} is DOWN.")
        send_email(message, f"{name} is DOWN")
        return iteration_count + interval
 
def monitor(host_map, interval):
    iteration_counts = {host: 0 for host in host_map}
    while True:
        for host, name in host_map.items():
            is_up = check_connection(host)
            iteration_counts[host] = handle_status(host, name, iteration_counts[host], is_up)
        time.sleep(interval)
 
if __name__ == "__main__":
    monitor(hosts, interval)
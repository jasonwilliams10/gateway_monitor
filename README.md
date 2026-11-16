# Server Uptime Monitor

A lightweight Python tool that watches a list of servers and emails your team the moment one goes down — and again when it comes back up.

Built to catch outages **before customers report them**. Previously, customer tickets were often the first sign a server had a problem; this tool alerts within one check interval (5 minutes by default).

## Features

- Checks each host on a TCP port using PowerShell's `Test-NetConnection`
- Email alerts on **outage** (repeated each interval while down) and on **recovery**
- Recovery emails include the approximate total downtime
- Per-host ports (`host:port`) with a configurable default
- Timestamped log of outages and recoveries
- Settings in `config.json`, overridable with environment variables or a `.env` file
- Supports multiple To and CC recipients

## Requirements

- Windows (uses `Test-NetConnection`, which is built into Windows PowerShell)
- Python 3.8+
- [`python-dotenv`](https://pypi.org/project/python-dotenv/)
- An SMTP server/account that can send mail

```powershell
pip install python-dotenv
```

## Configuration

### 1. `config.json`

Create a `config.json` in the same folder as the script:

```json
{
  "hosts": {
    "server1.example.com": "Remote Server 1",
    "server2.example.com:8443": "Remote Server 2",
    "10.0.0.15": "Internal Server"
  },
  "log_file": "logs/monitor.log",
  "sender_email": "alerts@example.com",
  "receiver_email": "team@example.com",
  "cc_receiver_email": "manager@example.com, oncall@example.com",
  "smtp_server": "smtp.example.com",
  "smtp_port": 25,
  "interval": 300,
  "port": 443,
  "check_timeout": 60
}
```

| Key | Description | Default |
|---|---|---|
| `hosts` | Map of `host` or `host:port` → display name used in alerts | *required* |
| `log_file` | Path to the log file (folder is created if missing) | *required* |
| `sender_email` | From address; also used as the SMTP login username | *required* |
| `receiver_email` | To recipient(s): a list or comma-separated string | *required* |
| `cc_receiver_email` | CC recipient(s): a list or comma-separated string | *required* |
| `smtp_server` | SMTP server hostname | `localhost` |
| `smtp_port` | SMTP port | `1025` |
| `interval` | Seconds between check cycles | `300` |
| `port` | Default TCP port when a host has no `:port` | `443` |
| `check_timeout` | Max seconds to wait on a single check | `60` |

### 2. `.env` (secrets)

The SMTP password is read **only** from the environment or a `.env` file, never from `config.json`:

```env
SMTP_PASSWORD=your-smtp-password
```

> Add `.env` to your `.gitignore` so the password is never committed.

### Environment variable overrides

Any of these override the matching `config.json` value:

| Variable | Overrides |
|---|---|
| `CONFIG_FILE` | Path to the config file (default `config.json`) |
| `LOG_FILE` | `log_file` |
| `SENDER_EMAIL` | `sender_email` |
| `RECEIVER_EMAIL` | `receiver_email` |
| `CC_RECEIVER_EMAIL` | `cc_receiver_email` |
| `SMTP_SERVER` | `smtp_server` |
| `SMTP_PORT` | `smtp_port` |
| `CHECK_INTERVAL` | `interval` |
| `CHECK_PORT` | `port` |
| `CHECK_TIMEOUT` | `check_timeout` |
| `SMTP_PASSWORD` | *(env / .env only)* |

## Usage

```powershell
python monitor_10.py
```

The script runs continuously, checking every host each cycle and printing results to the console.

### Run automatically

To start the monitor when Windows starts, create a Task Scheduler task:

- **Trigger:** At startup (or at log on)
- **Action:** Start a program → `python.exe`
- **Arguments:** `monitor_10.py`
- **Start in:** the folder containing the script, `config.json`, and `.env`

## How alerts work

| Event | Console | Log file | Email |
|---|---|---|---|
| Host is up (normal) | ✔ | — | — |
| First failed check | ✔ | ✔ | **"<name> is DOWN"** |
| Still down on later checks | ✔ | ✔ | Repeated each interval with time down so far |
| Host recovers | ✔ | ✔ | **"<name> is back UP"** with approximate downtime |

Downtime is estimated from the number of failed check intervals, so it is accurate to within one interval.

### Example emails

```
Subject: Remote Server 1 is DOWN
Remote Server 1 is DOWN as of 11-16-2026 09:15:02.

Subject: Remote Server 1 is back UP
Remote Server 1 is back UP as of 11-16-2026 09:30:04 and was potentially down for 15 minutes.
```

### Example log

```
11-16-2026 09:15:02: Remote Server 1 is DOWN.
11-16-2026 09:20:03: Remote Server 1 is DOWN.
11-16-2026 09:30:04: Remote Server 1 is back UP as of 11-16-2026 09:30:04 and was potentially down for 15 minutes.
```

## Notes

- The SMTP connection uses `login()` without STARTTLS/SSL. If your mail server requires an encrypted connection (e.g., Office 365 or Gmail on port 587), the script will need a `server.starttls()` call added before login.
- Hosts are checked one at a time, so a cycle with several unreachable hosts can take up to `check_timeout` seconds per host before the next sleep.
- A failed check means the TCP connection on that port did not succeed; it does not test the application behind the port.

## License

MIT

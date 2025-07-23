Monitors gateway computers for a remote-control solution spread out across the U.S. to support traffic. This monitor pings the gateways at a set amount of time to make sure they are online. If a gateway goes down or becomes unavailable, the monitor will send an email alert and write the information to a log file. As long as the gateway is down when the monitor runs, an email is sent with the estimated time it has been down. When the gateway comes back online and the monitor runs again, it will send out an email that the gateway is back up and write to a log file. This can be done with other email providers or hosts, but I chose to use Proton Mail for this project due to encryption and not having to use the actual email password in the code. 
7/22/2025
Updated to use a config.jsn and .env file to keep information from being hard-coded. 
Added more error checking.
  

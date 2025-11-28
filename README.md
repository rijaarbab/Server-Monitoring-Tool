# Server Monitoring Tool

## 1. Overview

The Server monitoring tool is a lightweight Python based application that shows system metrics in real time and sends alerts when necessary. It continuously tracks CPU usage, memory load, disk activity, and basic network information, and it updates these values in real time so the user can understand what the machine is doing at any moment. An alerting system is set in place so when any metrics begin to reach an unsafe level, the tool sends an alert via email and Slack. The tool uses python libraries like psutil, rich, and pyyaml to collect and display the system metrics. There is also an option to run a CPU stress test which simulates a high load scenario and observes how the system behaves under heavy load. The application is organized as a small but complete console application. The basic overall goal is to present system health in an understandable way while also showing how monitoring, alerting, and logging works behind the scenes.

## 2. Project Relevance

Many technical domains, including IT support, cybersecurity, system administration, and DevOps, depend heavily on system monitoring tools to understand what is happening on their servers. Even small changes in CPU spikes, memory leaks, slow disk response, or unexpected network usage can hint at a larger issue. This can just be a performance bottleneck or other times it can possibly be the earliest sign of a security problem like malware or an unauthorized process running in the background. By building a simpler version of tools like Prometheus, Grafana, SolarWinds, or Splunk, it becomes easier to understand how monitoring actually works behind the scenes.

The importance of this project and the monitoring tool as it particularly relates to the field of cybersecurity is that it may indicate cyber incidents. Many incidents begin quietly, and one of the first clues is abnormal resource behavior. While this monitoring tool is not a full security tool, it gives practical experience with the same ideas used in larger enterprise systems. Users can get familiar with tracking system health, reviewing alert logs, and interpreting unusual behavior, all of which are foundational skills in security and system administration. The project also reinforces core technical abilities such as configuring YAML files, using Python to gather system data, and recognizing performance patterns. These are valuable skills for anyone working in tech related fields.

## 3. Methodology

### 3.1 Environment and Setup

The whole project is compiled on an Ubuntu virtual machine. I created a main project folder and a few smaller folders inside it for configs and logs. After that, I installed Python and some of its packages, like psutil for reading system stats, rich for the dashboard, yaml for loading my config file, and requests for Slack alerts. I also installed stress-ng on Ubuntu to test system behave when the CPU is pushed hard.

All the main settings such as metric thresholds, email settings, Slack settings, and how often alerts should be sent are placed in a centralized config.yaml file. This made it easy to adjust changes without having to touch the code anytime I wanted to change something.

### 3.2 Data Sources

Instead of using an outside dataset, the tool collects its own data directly from the system it is running on. The Alert data from when the metric values of the system is exceeded gets saved in the alert_history.log

### 3.3 Libraries, tools and features:

- The psutil library gives me live information for the CPU usage and core count, memory usage and capacity, disk usage and free space, network bytes sent/received, and system uptime. (All of this comes through the get_metrics() function that is in metrics.py.)
- The rich library makes tables and panels in the terminal for the live dashboard and main menu, giving colored status indicators (green/yellow/red) based on thresholds.
- Thresholds for CPU, memory, and disk are loaded from config.yaml in alerts.py. This file decides when a condition is "WARNING" or "CRITICAL" and builds alert objects with a timestamp, level, type, and message. The information regarding email and slack can also be adjusted from the yaml file without changing the code files.
- stress-ng is called from menu.py using subprocess.Popen() to generate heavy CPU load and test how the monitoring system behaves under stress.
- Notifications: notifications.py reads email and Slack settings from config.yaml and can send alerts using SMTP and Slack webhooks.
- Logging: Alerts are attached to alert_history.log after metrics pass the warnings and critical events.

### 3.4 System Architecture and Workflow

The project is split into small modules, and they all work together to form the full monitoring system:

**main.py**
- Shows the main menu and waits for the user's choice.
- Opens the dashboard, starts a stress test, shows alert history, or exits.
- When closing, it also checks and stops any active stress-test process so nothing keeps running in the background.

**menu.py**
- Handles menu options such as Dashboard, Stress Test, View Alerts, Exit.
- Handles stress test; on test start, it starts stress ng and then shows dashboard after a moment so you can see how system stats are doing
- Also makes sure to stop stress processes using stop_stress_if_running.
- Shows most recent 10 alerts as well by reading from alert history file

**dashboard.py**

This is the main monitoring screen. It refreshes constantly and reacts to system changes. It does the following:
- Loads thresholds and alert timing rules from config.yaml.
- Collects system stats in a loop using metrics.get_metrics().
- Shows CPU, memory, disk, network, and uptime with color-coded statuses.
- Tracks alert timing so notifications aren't sent too often.
- When something goes over the limit, it creates an alert, saves it, and sends notifications through email or Slack.

**metrics.py**
- Collects live system data (CPU, RAM, disk, network, uptime) using psutil.
- Converts numbers into readable units and returns everything as a dictionary.metrics

**alerts.py**
- Loads the warning and critical limits.
- Checks current metrics against these limits.
- Creates an alert whenever something goes above the threshold.
- Saves each alert into alert_history.log.

**notifications.py**
- Loads email and Slack settings from config.yaml.
- Send alert messages through SMTP for email.
- Send alerts to Slack using the webhook link.

**Overall workflow:**

the user starts the program → chooses an option from the menu → if the dashboard is running, metrics are collected repeatedly → the alerts engine evaluates them → alerts are logged and sent if needed → the log can later be viewed from the menu.

### 3.5 Dataflow

#### Dashboard Pipeline

![Dashboard Dataflow](Results/Dashboard%20Dataflow.jpeg)

This diagram highlights how `main.py`, `menu.py`, `dashboard.py`, and `metrics.py` coordinate to collect metrics, color-code them against thresholds, and refresh the Rich dashboard loop.

#### Notification Pipeline

![Notification Dataflow](Results/Notification%20Dataflow.jpeg)

The notification flow shows how alerts generated in `alerts.py` are persisted, then fanned out through `notifications.py` to email and Slack based on the `configs/config.yaml` settings.

## 4. To Run This Project (Step-By-Step Guide)

**Step 1:** Install Python

**Step 2:** Install pip if missing (`sudo apt install python3-pip`)

**Step 3:** Install Required Packages (`pip install psutil PyYAML rich requests`)

**Step 4:** Install stress-ng (`sudo apt install stress-ng`)

**Step 5:** Place the whole folder anywhere you like. For example, if it's on the Desktop (`cd ~/Desktop/ServerMonitoring`)

**Step 6:** Update the Configuration File `configs/config.yaml` and put your own:
- Email server info
- Slack webhook URL
- Warning/critical limits for CPU, RAM, and disk

**Step 7:** Run the Main Program (`python3 main.py`)

**Step 8:** Use the Menu

You can:
- Open the live dashboard
- Run a stress test
- Check alert history
- Exit the program

**Step 9:** Check email and slack for alerts

## 5. Results

The outcomes were observed after implementing and running the system monitoring tool inside the Ubuntu virtual machine (24.04.03). Each part of the system was tested individually to see how accurately each component works. The results include real time monitoring performance, alert behavior during normal and high-load conditions, notification accuracy, behavior under stress testing and overall system stability.

### Main Menu

![Main Menu](Results/Main%20Menu.png)

When the `python3 main.py` is run in the terminal, the monitor board launches without any errors. The program opened with a menu where I could choose what to run. Main Menu shows the four main options: live dashboard, CPU stress test, alert history, and exit. It asks the user for their input to select an option.

### Live Dashboard

![Live Dashboard](Results/Live%20Dashboard.png)

With the selection of option one, the Live Dashboard gets displayed. Once monitoring began, the dashboard provided continuous updates every two seconds. The dashboard consistently displays the system's information such as Host, OS, CPU Cores, Ram, and System uptime. The server monitoring Dashboards displays the Metrics for CPU, Memory and Disk Usage with their values and status. It also shows the available memory, free Disk Space, and Network activity. The status and values are displayed in color based on the threshold. At the top it shows the Alert count which gets sent to email and slack every five minutes when a metrics reaches the warring or critical. The User can then press Ctrl+C to stop the server monitoring at any time.

### Email Alert

![Email Alert](Results/Email%20Alerts.png)

The email notification feature worked correctly. The image shows memory alerts were sent including the time stamp plus the Server and OS information.

### Slack Alert

![Slack Alert](Results/Slack%20Alert.png)

Slack alerts were also delivered exactly as expected showing warning memory alerts, time stamps, plus the Server and OS information.

### CPU Stress Test

![CPU Stress Test](Results/CPU%20Stress%20Test.png)

The CPU test ran successfully after selecting option two from the Main Menu. The CPU jumped to 100%, and the dashboard marked it as Critical in red. This showed that the dashboard recognized sudden spikes in real time when the CPU is under stress and sent alerts via email and slack.

### CPU Stress Test Successful

![CPU Stress Test Successful](Results/CPU%20Stress%20Test%20Successful.png)

When the monitoring session was stopped, the summary showed that alerts were reported which matched what I observed during the test.

### Email Alert with CPU Stress Test

![Email Alert with CPU Stress Test](Results/Email%20Alert%20with%20CPU%20Stress%20Test.png)

### Slack Alert with CPU stress test

![Slack Alert with CPU stress test](Results/Slack%20Alert%20with%20CPU%20stress%20test.png)

With the CPU Stress test the alerts were sent successfully on email and slack.

### Alert History

![Alert History](Results/Alert%20History.png)

Option 3 from Main Menu displayed the alerts history in the terminal successfully.

### Alert History Log

![Alert History Log](Results/Alert%20History%20Log.png)

The tool saved every alert to alert_history.log exactly as designed.

## 6. Conclusion

In all, the Server monitoring tool provided basic system metrics to show a system's health. Reviewing key system metrics can help identify issues sooner and early alerts features can be very important in real world scenarios. For future improvements, the tool could include graphs, a small database to store long term data, or a simple web dashboard. In addition to that, expanding on alert options or adding support for monitoring multiple machines could make the tool more advanced. Overall, the project provided a solid introduction to system monitoring and helped build practical skills that can be used in real IT and cybersecurity environments.

## 7. Resource links

- System util: https://stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python
- How to read yaml file: https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
- Rich: https://github.com/Textualize/rich
- Smtp: https://docs.python.org/3/library/smtplib.html
- To send email alerts: https://mailtrap.io/blog/python-send-email-gmail/
- Send mail Gmail account using Python: https://www.geeksforgeeks.org/python/send-mail-gmail-account-using-python/
- Slack alerts: https://www.youtube.com/watch?v=jDqjSd42024
- Slack documentation: https://docs.slack.dev/messaging/sending-and-scheduling-messages/
- How to create functions: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- To read files: https://www.w3schools.com/python/python_file_handling.asp
- Time: https://www.geeksforgeeks.org/python/python-time-module/
- If elif statements: https://docs.python.org/3/tutorial/controlflow.html#if-statements
- Loops: https://docs.python.org/3/reference/compound_stmts.html#while
- Request library: https://realpython.com/python-requests/


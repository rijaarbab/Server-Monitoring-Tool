# ServerMonitoring Package

This directory contains the Python modules that power the Server Monitoring Tool. They are imported by `main.py` and make up the interactive console experience, real-time dashboard, alerting pipeline, and notification integrations.

## Module Overview

| File | Responsibility |
| --- | --- |
| `menu.py` | Renders the Rich-based main menu, launches the live dashboard, spawns/stops the optional `stress-ng` CPU test, and streams the latest entries from `alert_history.log`. |
| `dashboard.py` | Loads threshold/notification timing from `configs/config.yaml`, retrieves metrics, renders the dashboard table, and orchestrates alert generation plus notification dispatch. |
| `metrics.py` | Wraps `psutil`/`platform` calls to return CPU, memory, disk, network, host, and uptime data in a normalized dictionary. |
| `alerts.py` | Compares incoming metrics against configurable warning/critical thresholds, builds alert payloads, and persists them to `alert_history.log`. |
| `notifications.py` | Reads email/Slack settings from `configs/config.yaml` and delivers alerts via SMTP and Slack webhooks when enabled. |

Each module keeps its own defaults so the tool works out-of-the-box, but all thresholds and notification preferences can be overridden through the shared config file.

## Runtime Flow

1. `main.py` calls `menu.show_menu()` so the user can pick an action.
2. Choosing **Live Dashboard** or **CPU Stress Test** ultimately runs `dashboard.run_live_dashboard()`.
3. The dashboard loop:
   - pulls fresh stats from `metrics.get_metrics()`
   - prints the system panel and metric table with color-coded statuses
   - invokes `alerts.check_alerts()` when the alert cooldown expires
   - logs alerts via `alerts.save_alert()` and hands them to `notifications.send_notifications()`
4. Notifications fan out through the enabled transports (email and/or Slack).
5. All alerts accumulate in the repository-level `alert_history.log`, which `menu.view_alert_history()` reads back.

## Configuration Touchpoints

The modules expect `configs/config.yaml` to expose three top-level sections:

- `thresholds.cpu|memory|disk.warning|critical`
- `alert_settings.min_alert_interval_minutes`
- `notifications.email` (enabled flag, SMTP server/port, sender, credentials, recipients)
- `notifications.slack` (enabled flag, webhook URL, channel, username)

If the file is missing or incomplete, safe defaults keep the dashboard operational; only the configurable feature deviates (e.g., alerts use default limits, notifications stay disabled).

## Extending the Package

- **New metrics:** Add collectors to `metrics.py` and print them inside `dashboard.show_dashboard()`.
- **Additional alert types:** Update `alerts.check_alerts()` with new checks and ensure thresholds exist in the config.
- **Extra transports:** Implement another sender in `notifications.py` (e.g., SMS) and wire it into `send_notifications()`.

Keeping each concern in its own module makes the toolkit easy to customize without changing the main control flow.


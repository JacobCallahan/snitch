# Snitch
[![CodeQL](https://github.com/jake-ps/snitch/actions/workflows/code-ql-analysys.yml/badge.svg)](https://github.com/jake-ps/snitch/actions/workflows/code-ql-analysys.yml)

Keeping tabs on your systems..

## Description

Snitch is a tool designed to provide a common interface for monitoring system activity. It uses a plugin-based system to check for signs of life, such as file modifications or the output of custom functions. This allows you to get a quick and simple "active" or "inactive" status for a machine.

## CLI Usage

Snitch offers a few simple commands to manage activity checks and view status.

### Checking for Activity

To run a new activity check, use the `check` command. This will execute all configured plugins, update the local state file with the results, and print the current status.
**Note:** You'll likely want to run this with a user that has root permissions to make sure it has access to each file.

```bash
snitch check
```

### Displaying the Current Status

To view the most recent activity status without running a new check, use the `status` command.

```bash
snitch status
```

Example output:
```
--- System Activity Status ---
Status: ACTIVE (within last 5 days)
Confidence: 100.0%
Last File Activity: 2025-09-19 10:30:00
Last Checked: 2025-09-19 10:30:00
```

### Serving the Status via API

Snitch can run as a simple HTTP server to expose the latest activity status via a JSON API. Use the `serve` command for this.

```bash
snitch serve --port 8000
```

This will start a server on port 8000. You can then query the API to get the status:

```bash
curl http://localhost:8000/
```

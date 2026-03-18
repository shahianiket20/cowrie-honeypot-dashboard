# Cowrie Honeypot Dashboard

## Project Overview
This project implements a Cowrie SSH Honeypot integrated with a custom web dashboard for monitoring and analyzing attacker activities.

The system captures login attempts, commands executed by attackers, and visualizes the attack data using charts.

## Features
- SSH Honeypot using Cowrie
- Real-time attack logging
- Dashboard for attack analysis
- Visualization of attacker behavior
- Command tracking
- Username and password analysis
- Source IP tracking

## Technologies Used
- Cowrie Honeypot
- Python
- Flask
- SQLite Database
- HTML / CSS
- Chart.js

## Dashboard Analytics
The dashboard provides visual insights into:

- Top usernames used by attackers
- Most common passwords
- Top attacking IP addresses
- Commands executed by attackers

## Attack Simulation
The system was tested using:
- Manual SSH login attempts
- Brute force attacks
- Port scanning
- Command execution analysis

## Project Structure
cowrie-dashboard/
│
├── app.py
├── parse_logs.py
├── cowrie.db
├── cowrie_logs.db
│
├── templates/
│   └── index.html
│
├── static/
│
└── README.md

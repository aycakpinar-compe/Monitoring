# Containerized Service with Monitoring & Alerting

This project focuses on building and monitoring a containerized service using tools commonly used in real-world systems. It demonstrates how to collect, visualize, and alert on both application and system-level metrics using Prometheus, Grafana, and Alertmanager.

The main goal is to understand how services run in containers and how they can be monitored, visualized, and alerted in case of issues.

## Monitoring Stack

- cAdvisor (container metrics)
- Node Exporter (host metrics)
- Prometheus (metrics collection and storage)
- Grafana (visualization)
- Alertmanager (alerting)

## What This Project Does

- Serves a simple web application using Flask
- Uses Nginx as a reverse proxy
- Runs all components inside Docker containers
- Collects container and system metrics
- Stores and queries metrics with Prometheus
- Visualizes metrics using Grafana dashboards
- Sends alerts using Alertmanager

## Monitoring & Alerting

### Metrics Collection

- cAdvisor → container CPU and memory usage
- Node Exporter → host CPU, memory, disk, and system load

### Metrics Flow

- Prometheus scrapes all configured targets
- Metrics are stored locally
- Grafana is used to visualize the collected data

### Alerting

- Prometheus evaluates alert rules
- Alerts are sent to Alertmanager
- Alertmanager handles grouping and delivery

### Example Alert Scenarios

- High CPU usage
- High memory usage

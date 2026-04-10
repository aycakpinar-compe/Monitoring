Containerized Service with Monitoring & Alerting
 This project focuses on building and monitoring a containerized service using tools commonly used in real-world systems. 
It demonstrates how to collect, visualize, and alert on both application and system-level metrics using Prometheus, Grafana, and Alertmanager.
   -cAdvisor (container metrics)
   -Node Exporter (host metrics)
   -Grafana (visualization)
   -Alertmanager (alerting)
   -The main goal is to understand how services run in containers and how they can be monitored, visualized, and alerted in case of issues.


  What This Project Does :
-Serves a simple web application using Flask
-Uses Nginx as a reverse proxy
-Runs all components inside Docker containers
-Collects container and system metrics
-Stores and queries metrics with Prometheus
-Visualizes metrics using Grafana dashboards
-Sends alerts using Alertmanager


Monitoring & Alerting
 -Metrics Collection
 -cAdvisor → container CPU, memory usage
 -Node Exporter → host CPU, memory, disk, load
 Metrics Flow
 -Prometheus scrapes all targets
 -Data is stored locally
 -Grafana visualizes metrics
 -Alerting:
   -Prometheus evaluates alert rules
   -Alerts are sent to Alertmanager
   -Alertmanager handles grouping and delivery
Example of alert scenarios:
  -High CPU usage
  -High memory usage

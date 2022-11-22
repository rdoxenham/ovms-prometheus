#!/usr/bin/env bash
# OVMS Random Data Workload Clean-up Script
# Rhys Oxenham <roxenham@redhat.com>

# Make sure we're in the right project
oc project ovms-prometheus

# Delete random data workload,
# service, and service monitor
oc delete -f deploy.yaml

# Delete Grafana Operator and Instances
oc delete -f grafana-datasource.yaml
oc delete -f grafana-dashboard.yaml
oc delete -f grafana-instance.yaml
oc delete -f grafana-operator.yaml
oc delete csv/grafana-operator.v4.7.1

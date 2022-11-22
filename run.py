#!/usr/bin/env python
# OVMS Random Data Generator
# Rhys Oxenham <roxenham@redhat.com>

import time
import random
from threading import Thread
from prometheus_client import Counter, Gauge, Histogram, start_http_server

ovms_streams = Gauge('ovms_streams', 'Number of OpenVINO execution streams', ['name', 'model_version'])
ovms_current_requests = Gauge('ovms_current_requests', 'Number of inference requests currently in process', ['name', 'version'])
ovms_requests_success = Counter('ovms_requests_success', 'Number of successful requests to a model or a DAG.', ['api', 'interface', 'method', 'name', 'version'])
ovms_requests_fail = Counter('ovms_requests_fail', 'Number of failed requests to a model or a DAG.', ['api', 'interface', 'method', 'name', 'version'])
ovms_placement_success = Counter('ovms_placement_success', 'Number of successful placements on conveyor.', ['api', 'interface', 'method', 'name', 'version'])
ovms_placement_fail = Counter('ovms_placement_fail', 'Number of failed placements on conveyor.', ['api', 'interface', 'method', 'name', 'version'])
ovms_request_time_us = Histogram('ovms_request_time_us', 'Processing time of requests to a model or a DAG.', ['interface', 'name', 'version'])
ovms_inference_time_us = Histogram('ovms_inference_time_us', 'Inference execution time in the OpenVINO backend.', ['name', 'version'])
ovms_wait_for_infer_req_time_us = Histogram('ovms_wait_for_infer_req_time_us', 'Request waiting time in the scheduling queue.', ['name', 'version'])
#ovms_avg_placement_success = Gauge('ovms_avg_placement_success', 'Average percentage of successful placement on conveyor.', ['name', 'version'])
#ovms_avg_request_success = Gauge('ovms_avg_request_success', 'Average percentage of model inference through model.', ['name', 'version'])

# Fixing these values for validation
name = 'OpenVINO_Anomalib_model'
version = '1'
api = 'KServe'
method = 'ModelInfer'
interface = 'gRPC'

# Fix single thread, we can adapt later
ovms_streams.labels(name, version).set(1)
ovms_current_requests.labels(name, version).set(1)

# Fix sleep time 3-7s between model infer
def random_sleep():
    return random.randint(3, 7)

# Fix 85-95% chance of successful inference
def success():
    if random.randint(0,100) < random.randint(85,95):
        return True
    return False

# Fix 10-30% chance of abnormal items
def abnormal():
    if random.randint(0,100) < random.randint(10,30):
        return True
    return False

# Fix 1-10s processing time
def proc_time():
    return random.random() * 10

# Generate average success rates and return float
def calc_avg(success, total):
    try:
        avg = (success / total) * 100
        return round(avg, 3)
    except:
        return 0.00

class random_data(Thread):
     def run(self):
         while True:
                if success():
                    ovms_requests_success.labels(api, interface, method, name, version).inc()
                else:
                    ovms_requests_fail.labels(api, interface, method, name, version).inc()
                if abnormal():
                    ovms_placement_fail.labels(api, interface, method, name, version).inc()
                else:
                    ovms_placement_success.labels(api, interface, method, name, version).inc()
                ovms_wait_for_infer_req_time_us.labels(name, version).observe(proc_time())
                ovms_inference_time_us.labels(name, version).observe(proc_time())
                ovms_request_time_us.labels(interface, name, version).observe(proc_time())
                time.sleep(random_sleep())

if __name__ == "__main__":
    start_http_server(8000)
    random_data = random_data()
    random_data.start()

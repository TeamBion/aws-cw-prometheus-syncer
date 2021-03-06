"""Prometheus exporter of Cloudwatch Logs main.py """
import os
import time
import logging
from prometheus_client import start_http_server, Gauge
from insights_queries.parsers import Parser
from insights_queries.query import QueryRunner

class Metrics:
    """Class of metric class"""

    def __init__(self, log_group_name, metric_prefix, region="eu-west-1",time_period=5):
        self.time_period = time_period
        self.metric_values = Gauge("{}_metric".format(metric_prefix), "Metrics", ["metric_type"])
        self.query_obj = QueryRunner(region=region)
        self.log_group_name = "{}".format(log_group_name)
        self.parser = Parser()
        self.query_map = self.parser.parse_query_list()

    def run_metrics_loop(self):
        """Metric query runner loop"""
        while True:
            self.fetch()
            time.sleep(self.time_period)

    def fetch(self):
        """Calls the functions which is responsible to run query on CW Insights"""
        metric_map = {}

        query_map = self.query_map
        for query in query_map:
            logging.info(query)
            data = self.query_obj.executeQuery(query_map[query], 
                query,logGroup="{}".format(self.log_group_name))

            logging.warning(data)
            metric_map[query] = data[query]

        for metric in metric_map.items():

            if metric[1] != 0.0 :
                logging.warning("Metric value debug {}".format(metric[0]))
                logging.warning("Metric value {}".format(metric_map[metric[0]]))
                logging.warning("Metric or Message has to produced by this tool")

            else:
                logging.warning("Nothing to produce as a metric {}".format(metric))

            self.metric_values.labels(metric_type=metric[0]).set(metric_map[metric[0]])

def main():
    """Prometheus exporter main function"""

    logging.info("Exporter started")
    
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))
    log_group_name=os.environ.get("LOG_GROUP_NAME" ,"/aws/eks/test-cluster/cluster") ## 
    region=os.environ.get("AWS_DEFAULT_REGION", "eu-west-1")
    interval_time_period=os.environ.get("INTERVAL_TIME_PERIOD", 10)
    metric_prefix = os.environ.get("METRIC_PREFIX")

    app_metrics = Metrics(
        time_period = int(interval_time_period),
        region = region,
        log_group_name = log_group_name,
        metric_prefix = metric_prefix
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
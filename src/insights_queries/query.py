import boto3
import logging
import time
from datetime import datetime, timedelta

class QueryRunner(object):
    def __init__(self, region="eu-central-1"):
        self.client = boto3.client("logs", region)

    def executeQuery(self, query, queryKey, logGroup):
        start_query_response = self.client.start_query(
            logGroupName=logGroup,
            startTime=int((datetime.today() - timedelta(minutes=5)).timestamp()),
            endTime=int(datetime.now().timestamp()),
            queryString=query,
        )
        
        queryId = start_query_response['queryId']
        response = None
        logging.warning("Query Name is => {}".format(queryKey))

        while response == None or response['status'] == 'Running':
            logging.warning('Waiting for query to complete ...')
            time.sleep(1)
            response = self.client.get_query_results(
                queryId=queryId
            )
            matchedRecordCount = response["statistics"]["recordsMatched"]

        logging.warning("Query Execution Completed")
        query_metric_response = {queryKey: matchedRecordCount}

        return query_metric_response
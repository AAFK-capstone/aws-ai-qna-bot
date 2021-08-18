import boto3
import botocore
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

kendra = boto3.client('kendra')

''' function to get id of data source by its name
'''
def find_id_by_datasource_name(indexId, datasourceName):
    try:
        datasourceList = kendra.list_data_sources(IndexId = indexId)['SummaryItems']
    except:
        logger.error('Error retrieving list of data sources')
        raise
    else:
        logger.info("datasourceList: {}".format(datasourceList))
        datasourceId = [ds['Id'] for ds in datasourceList if ds['Name'] == datasourceName]
    if len(datasourceId) == 0:
        raise Exception("Invalid Data source name! create the data source before sync.")
    else:
        return datasourceId[0]

''' function to sync documents items from bucket to kendra data source
 '''
def start_kendra_sync(bucketname, key, kendraIndexId, kendraDataSourceId):
    logger.info('starting sync job for documents in {}/{}'.format(bucketname, key))
    try:
        response = kendra.start_data_source_sync_job(
            Id=kendraDataSourceId,
            IndexId=kendraIndexId
        )
    except Exception as e:
        logger.error('Sync job failed: {}'.format(e))
    else:
        logger.info(response)
        return response['ExecutionId']

def index_documents(settings):
    bucketname = settings['DOCUMENT_BUCKETNAME']
    key = settings['DOCUMENT_PREFIX']
    kendraIndexId = settings['KENDRA_WEB_PAGE_INDEX']
    kendraDatasourceName = settings['KENDRA_CASE_STUDY_DATA_SOURCE_NAME']
    kendraDataSourceId = find_id_by_datasource_name(kendraIndexId, kendraDatasourceName)
    executionString = start_kendra_sync(bucketname, key, kendraIndexId, kendraDataSourceId)
    return executionString
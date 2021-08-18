import logging
import os
import json
from lib.case_study_scraper import get_case_study
from lib.upload_to_s3 import upload_json_and_metadata
from lib.upload_to_s3 import check_file_exists_in_s3
from lib.upload_to_s3 import upload_file_to_s3
from lib.upload_to_s3 import download_file_from_s3
from lib.kendra_sync import index_documents
from lib.get_settings import get_all_settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # proccess function arguments
    requestBody = event
    alias = requestBody['alias']
    max_item = requestBody['max_item']
    metadata_url = requestBody['metadata_url']
    if 'slice' in requestBody and len(requestBody['slice'] == 2):
        slice = requestBody['slice']
    else:
        slice = None
    if 'forceCsvScrapper' in requestBody:
        forceCsvScrapper = requestBody['forceCsvScrapper']
        if isinstance(requestBody['forceCsvScrapper'], str) and requestBody['forceCsvScrapper'].lower() == "true":
            forceCsvScrapper = True
    else:
        forceCsvScrapper = False
    uploadSuccess = False

    # get settings
    settings = get_all_settings()
    
    # get csv file
    get_csv_file(settings, forceCsvScrapper, alias, metadata_url)
    
    # process file and store in tmp folder
    localfile = '/tmp/' + alias + '.csv'
    res = os.path.isfile(localfile)
    executionString = ""
    if res:
        uploadSuccess = upload_json_and_metadata(settings, localfile, max_item, ' ; ', slice)
        if uploadSuccess:
            executionString = index_documents(settings)
    return {
        'statusCode': 200,
        'body': executionString
    }
    
''' function get the csv file with the metadata
it checks s3 to see if the file is available, if not available, it will call a scraper function
otherwise forceCsvScrapper=True, it will also run the scraper
'''
def get_csv_file(settings, forceCsvScrapper, alias, metadata_url):
    bucketname = settings['DOCUMENT_BUCKETNAME']
    csvPrefix = settings['CASE_STUDY_CSV_PREFIX']
    objectKey = csvPrefix + '/' + alias + '.csv'
    localFilename = '/tmp/' + alias + '.csv'
    fileExists = check_file_exists_in_s3(bucketname, objectKey)
    if not fileExists or forceCsvScrapper:
        logger.info('start scraping metadata url: {}'.format(metadata_url))
        get_case_study(localFilename, metadata_url)
        upload_file_to_s3(bucketname, localFilename, objectKey)
    else:
        download_file_from_s3(bucketname, objectKey, localFilename)
    return True
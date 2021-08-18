import logging
import boto3
import botocore
import pandas as pd
import requests
import json
from botocore.retries import bucket
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
default_blog_url = 'https://aws.amazon.com/api/dirs/items/search?item.directoryId=blog-posts&sort_order=desc&size=2000&item.locale=en_US'

''' function to download from s3
'''
def download_file_from_s3(bucketname, objectKey, localFile):
    try:
        s3.Object(bucketname, objectKey).download_file(localFile)
    except:
        logger.error('File download for {}/{} failed!'.format(bucketname, objectKey))
        return False
    else:
        return True


''' function to upload local file to s3
returns the success/ failure of the upload
'''
def upload_file_to_s3(bucketname, localFile, s3Filename):
    try: 
        s3.Bucket(bucketname).upload_file(localFile, s3Filename)
    except Exception as e:
        logger.error('Uploading file to S3 failed for file: {}'.format(s3Filename))
        logger.error(e)
        return False
    else: 
        return True

''' function to check if a file exists in s3 bucket
'''
def check_file_exists_in_s3(bucketname, objectKey):
    try:
        s3.Object(bucketname, objectKey).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":  
            # file does not exist  
            return False
        else:
            raise
    else:
        return True

''' function to generate metadata files, wrapper function that reformats and logs
'''
def generate_json_metadata(max_blog, filename, bucketname, prefix, tag_delimiter=' ; ', slice=None):
    uploadCount = {'total' : 0, 'success' : 0}
    uploadSuccess = True
    tagDataframe = pd.read_csv(filename, delimiter=',')
    if slice is not None:
        if slice[1] < tagDataframe.shape[0]:
            tagDataframe = tagDataframe.loc[slice[0]: slice[1]]
        else:
            tagDataframe = tagDataframe.loc[slice[0]:]
            slice[1] = tagDataframe.shape[0]
    required_tags = ['url', 'title', 'contentType', 'id']
    # iterate through csv rows
    for index, row in tagDataframe.iterrows():
        uploadSuccess = generate_metadata_from_row(row, required_tags, tag_delimiter, bucketname, prefix)
        # for logging purposes
        if uploadSuccess:
            uploadCount['success'] += 1
        uploadCount['total'] += 1
        # if successful uploads hits max count end this, else continue until max
        if uploadCount['success'] >= max_blog:
            uploadSuccess = True
            break
    logger.info('Exiting uploader. Total count {} of which {} were successful'.format(uploadCount['total'], uploadCount['success']))
    if slice is not None:
        logger.info('Data from row {} to row {}'.format(slice[0], slice[1]))
    return uploadSuccess

''' generate metadata and call upload to s3
csv files have to include: url, title, content-type, id
the rest of the attributes are optional will be added if it is there
'''
def generate_metadata_from_row(row, required_tags, tag_delimiter, bucketname, prefix):
    metadata = dict()
    customAttributes = dict()    
    # define required and custom attributes
    metadata['Title'] = row['title']
    metadata['ContentType'] = "HTML"
    ## append the custom attributes such as tech use case, industry, location, etc
    for tagKey, tagValue in row.iteritems():
        logger.info('key/value = {}:{}'.format(tagKey, tagValue))
        if tagKey not in required_tags and isinstance(tagValue, str):
            tagValueArray = tagValue.split(tag_delimiter)
            if len(tagValueArray) > 10: #kendra can't deal with more than 4
                tagValueArray = tagValueArray[:10]
            customAttributes[tagKey] = tagValueArray
    customAttributes['_source_uri'] = row['url']
    customAttributes['_category'] = row['contentType'] # 'customer story'
    customAttributes['item_name'] = row['id']
    metadata['Attributes'] = customAttributes
    uploadSuccess = upload_metatdata_and_html_to_s3(bucketname, prefix, metadata)
    return uploadSuccess



''' upload metadata and html file to s3
NOTE url has to be in metadata['Attributes']['_source_uri']
metadata also has to contain metadata['id'] which will be the name the file will be saved as
'''
def upload_metatdata_and_html_to_s3(bucketname, prefix, metadata):
    htmlFilename = prefix + '/' + metadata['Attributes']['item_name'] + '.html'
    metadataFilename = htmlFilename + '.metadata.json'
    localFilename = {'HTML':'/tmp/page.html', 'metadata': '/tmp/metadata.json'}

    # check and upload html file
    htmlFileExists = check_file_exists_in_s3(bucketname, htmlFilename)
    uploadSuccess = False
    if not htmlFileExists:
        url = metadata['Attributes']['_source_uri']
        downloadSuccess = send_HTTP_request_and_save_file(url, localFilename['HTML'])
        if downloadSuccess:
            uploadSuccess = upload_file_to_s3(bucketname, localFilename['HTML'], htmlFilename) or uploadSuccess

    # check and upload metadata file
    metadataFileExists = check_file_exists_in_s3(bucketname, metadataFilename)
    if not metadataFileExists:
        try: 
            with open(localFilename['metadata'], 'w') as json_file:
                json.dump(metadata, json_file)
        except:
            raise
        else:
            uploadSuccess = upload_file_to_s3(bucketname, localFilename['metadata'], metadataFilename) or uploadSuccess
    return uploadSuccess

''' function to send http request and save as local file
'''
def send_HTTP_request_and_save_file(url, localFilename):
    try:
        r = requests.get(url)
    except Exception as e:
        logger.error('Error retrieving HTML file with the URL {}'.format(url))
        logger.error(e)
        return False
    else:
        try: 
            with open(localFilename, mode='wb') as htmlfile:
                htmlfile.write(r.content)
        except Exception as e:
            logger.error('Error saving HTML file from URL {} to local tmp folder'.format(url))
            logger.error(e)
        else:
            return True

''' function to call everything else
'''
def upload_json_and_metadata(settings, csvFileName, max_item, delimiter, slice): 
    bucketname = settings['DOCUMENT_BUCKETNAME']
    prefix = settings['DOCUMENT_PREFIX']
    # alias and metadata_url to be defined in lambda request - if same alias, won't scrap for metadata, but will perform uploads because of max upload rate
    uploadSuccess = generate_json_metadata(max_item, csvFileName, bucketname, prefix, tag_delimiter=delimiter, slice=slice)
    return uploadSuccess

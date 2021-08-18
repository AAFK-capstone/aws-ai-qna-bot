import boto3
import botocore
import os
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ssm = boto3.client('ssm')

def is_json(string):
    try:
        json.loads(string)
    except ValueError as e:
        return False
    else:
        return True

def str2bool(old_settings):
    new_settings = {k: convert_string_to_bool(v) for k, v in old_settings.items()}
    return new_settings

def convert_string_to_bool(setting):
    if isinstance(setting, str):
        formattedStr = setting.strip('\"').lower()
        if formattedStr == "true":
            setting = True
        elif formattedStr == "false":
            setting = False
    return setting

''' Function to get a set of parameters from QnABot settings from Parameter Store by specifying the param_name
 helper function used for `get_settings`
 @param param_name
 @returns {*}
'''
def get_parameters(param_name):
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    settings = response['Parameter']['Value']
    if is_json(settings):
        settings = json.loads(response['Parameter']['Value'])
        settings = str2bool(settings)
    return settings


''' Function to retrieve all QnABot settings using default and custom settings defined in the environment variables
 DEFAULT_SETTINGS_PARAM and CUSTOM_SETTINGS_PARAM
 helper function used for `performSync`
 @returns {*}
'''
def get_all_settings():
    default_settings_param = os.environ['DEFAULT_SETTINGS_PARAM']
    custom_settings_param = os.environ['CUSTOM_SETTINGS_PARAM']

    logger.info("Getting Default QnABot settings from SSM Parameter Store: {}".format(default_settings_param))
    default_settings = get_parameters(default_settings_param)

    logger.info("Getting Custom QnABot settings from SSM Parameter Store: {}".format(custom_settings_param))
    custom_settings = get_parameters(custom_settings_param)

    logger.info("Getting Local Environment settings: ")
    local_settings = os.environ

    settings = {**default_settings,  **custom_settings, **local_settings}
    return settings

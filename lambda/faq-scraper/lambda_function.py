import os
from bs4 import BeautifulSoup
import requests
import csv
import boto3
import lxml
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Method retrieves all FAQ urls
def retrieve_faq_urls(): 
    #URL to page that contains all URLs
    url = "https://aws.amazon.com/faqs/"
    #Retrieve HTML content
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "html.parser")
    faqURL = []

    for r in soup.find_all('div', {"class:", "six columns"}):
        for a in r.find_all('a'):
            raw = str(a.get('href')).strip()
            
            if(raw.startswith("/")):
                faqURL.append('https://aws.amazon.com'+raw)
                #print(raw)
            else:

                if(raw.startswith("https")):
                    faqURL.append(raw)
    return faqURL
    
def retrieve_raw_text(url):
    html_content = requests.get(url).text
    #print(html_content)

    soup = BeautifulSoup(html_content, "html.parser")

    rs = soup.find_all("div", {"class": "lb-txt-16"})
    raw = []
    for r in rs:
        raw.append(r.get_text().strip())

    return raw

def text_to_faq(raw,url):
    faq = [['Question', 'Answer']]

    #iterate through each chunk 
    for line in raw:
        #split chunk up based on \n -> will get a segment of Q&As
        split = line.split('\n')

        for lineNo in range(len(split)):
            currLine = split[lineNo].strip()
            if currLine.startswith("Q:"):
                question = currLine
                nextQline = False
                answer = ""
                #Collect next few lines as answers until next Q: is found
                while not nextQline and lineNo+1 < len(split):
                    if  (split[lineNo+1]).strip().startswith("Q:"):
                        #print("answer complete")
                        nextQline = True
                    else:
                        lineNo = lineNo+1 
                        answer += split[lineNo].strip()
                #print(answer)
                faq.append([question[3:], answer,url])
    return faq

def fix_missing(faq):
    #Iterate through list to check for missing values
    for row in faq:
            #If answer is missing
            if not row[1]:
                    #split question based on the assumption that a question ends with "?"
                    split = row[0].split("?")
                    #Replace original question & answer with correct values
                    row[0] = split[0].strip()+"?"
                    row[1] = split[1].strip()

    return faq



''' function to upload local file to s3
returns the success/ failure of the upload
'''
def upload_file_to_s3(bucketname, localFile, s3Filename):
    s3 = boto3.resource('s3')
    try: 
        s3.Bucket(bucketname).upload_file(localFile, s3Filename)
    except Exception as e:
        logger.error('Uploading file to S3 failed for file: {}', s3Filename)
        logger.error(e)
        return False
    else: 
        return True

def export_to_csv(filename,faq):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(faq)
    print(filename + " complete!!")

def lambda_handler(event, context):

    url = "https://aws.amazon.com/faqs/"

    faqURL = retrieve_faq_urls()
    uploadSuccess = False

    #failedURL = []
    failc = 0
    for url in faqURL:
        try:
            text = retrieve_raw_text(url)
            faq = text_to_faq(text,url)
            if len(faq) > 1: 
                faq = fix_missing(faq)
                name = "/tmp/"+url.split('/')[3]+".csv"
                
                export_to_csv(name,faq)
                res = os.path.isfile(name)
                if res:
                    uploadSuccess = upload_file_to_s3("faq-lambda-test", name, name)
        except Exception:
            print("**********FAAILED: "+ url)
            #failedURL.append(url) 
            raise
            failc = failc+1
            
    return {
        'statusCode': 200,
        'body': uploadSuccess
    }
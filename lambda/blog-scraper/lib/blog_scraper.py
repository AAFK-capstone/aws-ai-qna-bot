import csv
import json
import requests

#function definition
def get_blog(localfilename, url):
    link_list = []
    item_list = json.loads(requests.get(url).text)['items']
    for item in item_list:
        # print(item['item']['additionalFields'].keys())
        id = item['item']['id'].replace('#', '-') # s3 object names can only comprise alphanumeric chars, hyphens and dots
        title = item['item']['additionalFields']['title']
        url = item['item']['additionalFields']['link']
        contentType = item ['item']['additionalFields']['contentType']
        link_map = {'id': id, 'title': title, 'link': url, 'contentType' : contentType}
        tagDict = get_tags_for_item(item['tags'])
        # .update is to combine the dictionary from one to another
        link_map.update(tagDict)
        link_list.append(link_map)

    with open(localfilename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'title', 'url', 'contentType', 'use-case', 'product', 'tech-category', 'customer-segment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in link_list:
            for keyname in fieldnames:
                if keyname not in link:
                    link[keyname] = ''
            writer.writerow({'id': link['id'], 'url': link['link'], 'title': link['title'],'contentType': link['contentType'], 'use-case': link['use-case'], 'product': link['product'], 'tech-category': link['tech-category'], 'customer-segment': link['customer-segment']})

def get_tags_for_item(tagList):
    tagMap = dict() # a dictionary to store results
    for tagEntry in tagList:
        # get the key here
        key = (tagEntry['tagNamespaceId']).split('#')[1]
        # get the values here
        ## do some cleaning for html tags
        value = tagEntry['description'].strip()
        value = value.replace("\u003cp\u003e", '').replace("\u003c/p\u003e", '')
        if key in tagMap:
            # if there is already an entry, it's going to combine with the existing entry
            value = tagMap[key] + " ; " + value
        # save the value to tagMap
        tagMap[key] = value
    # return dictionary
    return tagMap

if __name__ == '__main__':
    ## don't run this if entrypoint is not this file
    get_blog(
        '../../kendra/blogcsvFile.csv',
        'https://aws.amazon.com/api/dirs/items/search?item.directoryId=blog-posts&sort_order=desc&size=2000&item.locale=en_US'   
    )

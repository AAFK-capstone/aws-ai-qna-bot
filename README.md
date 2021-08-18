# A Question and Answer Bot Using Amazon Lex and Amazon Alexa

> Build a chat bot to answer questions.

## Overview

This repository is a clone of the QnABot, with some features implemented implemented by the author for his own projects. This QnABot is still in beta stage and should only be used after being carefully vetted through.

The original QnABot can be found here (https://github.com/aws-samples/aws-ai-qna-bot); Please refer to the original project for the project features implemented by the QnA bot team. 

## New features
This repository contains a variant of the QnABot. Additional features implemented include changes to the bot when Kendra FAQ answers are found and tweaks to improve dialog flows. The following behavior can be configured:
- Show the source link of the FAQ answer.
- Allow chatbot to continue processing Kendra search results even when FAQ answer is obtained.
- Show a user defined string when AWS Translate is used.
- Allow specialty bot to fallback to mainbot to look for answers or search results when it is unable to answer.
- Allow specialty bot to autoexit the specialty bot when it cannot find an answer.

**The following is the latest feature list version 1.0.1** 
- Added additional lambda functions for webscraping metadata. This feature may not be very useful to users as it is configured to suit certain APIs. Users' may edit this to suit their own webscraping/indexing needs.

**The following is the latest feature list for the original QnABot as of the day of clone** 
- Support for Lex V2 Elicit response bots
- Config import/export
- LexV2 Support with voice interaction in multiple languages.
- Improved Kendra integration and Kibana dashboards. Additional settings to filter Kendra responses based on confidence levels
- Kendra Web Crawler, Comprehend PII Detection, Translate Custom Terminology, Increased deployment regions
For more information, please refer to the original chatbot.

## Prerequisites

- Run Linux. (tested on Amazon Linux)
- Install npm >7.10.0 and node >12.15.1. ([instructions](https://nodejs.org/en/download/))
- Clone this repo.
- Set up an AWS account. ([instructions](https://AWS.amazon.com/free/?sc_channel=PS&sc_campaign=acquisition_US&sc_publisher=google&sc_medium=cloud_computing_b&sc_content=AWS_account_bmm_control_q32016&sc_detail=%2BAWS%20%2Baccount&sc_category=cloud_computing&sc_segment=102882724242&sc_matchtype=b&sc_country=US&s_kwcid=AL!4422!3!102882724242!b!!g!!%2BAWS%20%2Baccount&ef_id=WS3s1AAAAJur-Oj2:20170825145941:s))
- Configure AWS CLI and a local credentials file. ([instructions](http://docs.AWS.amazon.com/cli/latest/userguide/cli-chap-welcome.html))  

## Getting Started

To get started on this variation of the QnABot, you will have to build a version yourself. Alternatively, if you do not require the specific features here, you can use the original QnABot, which can be launched with pre-configured CloudFormation Templates, found in https://github.com/aws-samples/aws-ai-qna-bot. 

To build the QnABot:

### Clone the git repo and build a version

First, install all prerequisites:

```shell
npm install 
```

Next, set up your configuration file:

```shell
npm run config
```

now edit config.json with you information.

| param | description |
|-------|-------------|
|region | the AWS region to launch stacks in |
|profile| the AWS credential profile to use |
|namespace| a logical name space to run your templates in such as dev, test and/or prod |
|devEmail(required) | the email to use when creating admin users in automated stack launches |

Next, use the following command to launch a CloudFormation template to create the S3 bucket to be used for lambda code and CloudFormation templates. Wait for this template to complete (you can watch progress from the command line or [AWS CloudFormation console](https://console.AWS.amazon.com/cloudformation/home))  

```shell
npm run bootstrap
```

Finally, use the following command to launch template to deploy the QnA bot in your AWS account. When the stack has completed you will be able to log into the Designer UI (The URL is an output of the template). A temporary password to the email in your config.json:

```shell
npm run up
```

If you have an existing stack you can run the following to update your stack:

```shell
npm run update
```

#### Designer UI Compatibility

Currently the only browsers supported are:  

- Chrome  
- FireFox  
We are currently working on adding Microsoft Edge support.  

## Built With

- [Vue](https://vuejs.org/)
- [Webpack](https://webpack.github.io/)

## License

See the [LICENSE.md](LICENSE.md) file for details


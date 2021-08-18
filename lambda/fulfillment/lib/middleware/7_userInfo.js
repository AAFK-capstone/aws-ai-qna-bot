var Promise=require('bluebird')
var lex=require('./lex')
var alexa=require('./alexa')
var _=require('lodash')
var util=require('./util')
var AWS=require('aws-sdk');

function getDistinctValues(list,objectId,sortField){
    var dt = new Date();

    var distinctItems = [...new Set(list.map(item => item[objectId]))];
    var sortedItems = _.cloneDeep(list).sort((a,b) => {
        if(a[sortField] == b[sortField]){
            return 0;
        }
        return a["sortField"] < b["sortField"] ? 1 : -1
    });
    distinctItems = distinctItems.map(id => sortedItems.filter( item => item[objectId] == id ).reverse()[0])
    return distinctItems
}
async function update_userInfo(res) {
    // setting to allow session attributes to be logged in DynamoDB
    let logSessionAttributes =  _.get(res, "_settings.LOG_CUSTOM_SESSION_ATTRIBUTES", true);
    let startingPhrase = _.get(res, "_settings.LOG_CUSTOM_SESSION_ATTRIBUTES_PREFIX", "Customer");
    var sessionAttributes = _.get(res, "session", {});
    var topics = _.get(res,"_userInfo.recentTopics",[])
    var distinctTopics= getDistinctValues(topics,"topic").slice(0,10)
    _.set(res,"_userInfo.recentTopics",distinctTopics)
    console.log(res._userInfo)
    var userId = _.get(res,"_userInfo.UserName") && _.get(res,"_userInfo.isVerifiedIdentity") == "true" ? _.get(res,"_userInfo.UserName") : _.get(res,"_userInfo.UserId");
    _.set(res,"_userInfo.UserId",userId)
    if (logSessionAttributes && sessionAttributes) {
        const customSessionAttributes = filter_session_attr(sessionAttributes, startingPhrase);
        if (customSessionAttributes) {
            _.set(res, "_userInfo.CustomSessionAttr", customSessionAttributes);
        }
    }
    var usersTable = process.env.DYNAMODB_USERSTABLE;
    var docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
    var params = {
        TableName: usersTable,
        Item: res._userInfo,
    };
    console.log("Saving response user info to DynamoDB: ", params);
    var ddbResponse={}
    try {
        ddbResponse = await docClient.put(params).promise();
    }catch(e){
        console.log("ERROR: DDB Exception caught - can't save userInfo: ", e)
    }
    console.log("DDB Response: ", ddbResponse);
    return ddbResponse;
}
function filter_session_attr(sessionAttributes, startingPhrase) {
    // these session attributes are for internal use only, forbid if starting phrase contains them
    const forbiddenPhrases = ["connect", "qnabot", "user"];
    let forbidden = false;
    for (let phrase in forbiddenPhrases) {
        forbidden = (startingPhrase.startsWith(phrase)) || (phrase.startsWith(startingPhrase));
    }
    var customSessionAttributes = {};
    if (!forbidden) {
        Object.keys(sessionAttributes).forEach(function (key) {
            if (key.startsWith(startingPhrase)) {
                customSessionAttributes[key] = sessionAttributes[key];
            }
        });
    }
    console.log("custom session attributes: ", customSessionAttributes);
    return customSessionAttributes;
}

module.exports=async function userInfo(req,res){
    console.log("Entering userInfo Middleware")

    await update_userInfo(res);
    return {req,res}
}


/*
Copyright 2017-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License"). You may not use this file
except in compliance with the License. A copy of the License is located at

http://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the
License for the specific language governing permissions and limitations under the License.
*/

const Promise=require('bluebird')
const AWS = require('./aws.js');
const myCredentials = new AWS.EnvironmentCredentials('AWS');
const _=require('lodash')

module.exports=_.memoize(function(address){
    return require('elasticsearch').Client({
        requestTimeout:10*1000,
        pingTimeout:10*1000,
        hosts:process.env.ADDRESS,
        connectionClass: require('http-aws-es'),
        defer: function () {
            return Promise.defer();
        },
        amazonES: {
            region: process.env.AWS_REGION,
            credentials: myCredentials
        }
    })
})

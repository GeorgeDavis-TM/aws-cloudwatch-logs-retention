from distutils.command.config import config
import os
import json
import boto3

def getLogGroupsDict(logsClient):

    describeLogGroupsResponse = logsClient.describe_log_groups()

    logGroupsDict = {}

    for logGroup in describeLogGroupsResponse["logGroups"]:

        logGroupsDict.update({logGroup["logGroupName"]:logGroup["arn"]})

    return logGroupsDict

def getRetentionPolicyDays(configDict, logGroupName):

    for logGroupType in configDict["logGroupRetentionConfig"].keys():

        if logGroupType in logGroupName:
            return configDict["logGroupRetentionConfig"][logGroupType]
        
    return configDict["default"]

def setLogGroupRetentionPolicy(logsClient, logGroupName, retentionPolicyDays):

    putLogGroupRetentionPolicyResponse = logsClient.put_retention_policy(
        logGroupName=logGroupName,
        retentionInDays=retentionPolicyDays
    )

    print(str(putLogGroupRetentionPolicyResponse))

def main(event, context):

    regionList = str(os.environ.get("regionList"))
    exceptionLogGroups = str(os.environ.get("exceptionLogGroups"))

    f = open('config.json', 'r')
    configDict = json.loads(f.read())
    f.close()

    if regionList[-1] == ",":
        regionList = regionList[:-1].replace(" ", "").split(",")
    else:
        regionList = regionList.replace(" ", "").split(",")

    if exceptionLogGroups[-1] == ",":
        exceptionLogGroups = exceptionLogGroups[:-1].replace(" ", "").split(",")
    else:
        exceptionLogGroups = exceptionLogGroups.replace(" ", "").split(",")

    for regionName in regionList:

        print("Starting in Region ", str(regionName), "...")

        logsClient = boto3.client('logs', region_name=regionName)

        logGroupsDict = getLogGroupsDict(logsClient)

        for logGroupName in logGroupsDict.keys():

            retentionPolicyDays = getRetentionPolicyDays(configDict, logGroupName)

            setLogGroupRetentionPolicy(logsClient, logGroupName, retentionPolicyDays)

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}

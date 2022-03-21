# aws-cloudwatch-logs-retention
Enforce CloudWatch Log Retention Policies in AWS Regions as a Cost optimization measure

## Usage

### Deployment

In order to deploy the example, you need to run the following command:

```
$ serverless deploy -s dev
```

After running deploy, you should see output similar to:

```bash
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
........
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service aws-python.zip file to S3 (711.23 KB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
.................................
Serverless: Stack update finished...
Service Information
service: aws-python
stage: dev
region: us-east-1
stack: aws-python-dev
resources: 6
functions:
  api: aws-python-dev-hello
layers:
  None
```

After successful deployment, you can see the stack created on AWS CloudFormation.

The script is triggered on the 1st of every month, at 2300hrs UTC, as configured in the serverless.yml file before deployment, under `.functions.main.events.schedule.rate`.

## Configuration

All configurable options are found in the serverless.yml file under `.custom` and under `config.json` file.

### serverless.yml

| Fields | Description | Required? |
|--------| ----------- | --------- |
| `awscli_profile` | AWS CLI profile to use to deploy the Serverless CloudFormation stack | Yes |
| `aws_region` | AWS Region to deploy the CloudFormation stack to | Yes |
| `regionList` | AWS Regions to enforce AWS CloudWatch Log groups to use this log retention policy value | Yes |
| `exceptionLogGroups` | Exceptions for specific log groups | Yes |

### config.json

```
{
    "default": <catch-all-default-number-of-days>,
    "logGroupRetentionConfig": {
        "/aws/lambda": <number-of-days-for-lambda-function-logs>,
        "/aws/apigateway": <number-of-days-for-api-gateway-logs>,         
        "/aws/<aws-service>": <number-of-days-for-aws-service-specific-logs>,
        "/aws/...": <number-of-days-for-...-logs>  
    }
}
```

## TODO
- [ ] Implement code for `exceptionLogGroups`
- [ ] Better input handling for empty strings from `os.environ.get` so string manipulation tasks don't fail
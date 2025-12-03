# aws-cost-optimization-ebs-cleanup

# Overview
1. **AWS Lambda** (Python 3.10+)
   Runs cleanup logic using Boto3.
2. **CloudWatch EventBridge Rule**
   Schedules the Lambda (e.g., daily at midnight).
3. **IAM Role for Lambda**
   Permissions to list and delete:
    - EBS volumes
    - Snapshots
4. **Python/Boto3 Script**
    - Find volumes in available state
    - Delete them
    - Optionally delete snapshots older than X days
    - Log deleted resources

  # 1. IAM Role Required for Lambda
  Attach this policy (or equivalent managed permissions):
  
  **IAM Permissions**
  - `ec2:DescribeVolumes`
  - `ec2:DeleteVolume`
  - `ec2:DescribeSnapshots`
  - `ec2:DeleteSnapshot`

 # 2. Schedule the Lambda using EventBridge
 Create a rule:

- Name: `ebs-cleanup-schedule`
- Schedule expression: `rate(1 day)` or `cron(0 0 * * ? *)`
- Target → your Lambda function

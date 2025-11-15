# 🚨 Real-Time Threat Detection & Alerting : AWS Security Project 

# **Introduction**

# In this project, we will create a cloud security workflow(pipeline) that automatically detects threats using Amazon GuardDuty and notifies you immediately using Amazon SNS. This project is ideal for beginners who want to learn how AWS security services work together.

**TECH STACK**  
The project uses the following AWS services:

* [**AWS CloudTrail**](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) – logs all API activity 

* [**Amazon GuardDuty**](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html) – detects threats using ML and threat intelligence

* [**Amazon EventBridge**](https://docs.aws.amazon.com/eventbridge/) – triggers automated responses

* [**AWS Lambda**](https://docs.aws.amazon.com/eventbridge/) – formats alert data

* [**Amazon SNS**](https://docs.aws.amazon.com/sns/) – sends email/SMS alerts to the user

**Steps** 

Following are the steps involved

**Step 1: Enable CloudTrail**

CloudTrail records all your AWS API calls and user activity in your AWS account. GuardDuty later analyzes these logs to identify suspicious behavior.

**Steps:**

1. Open the CloudTrail console.  
2. If CloudTrail is not already active, click “Create trail”.  
3. Name the trail like a management-event.  
4. AWS will automatically choose a S3 bucket for storing logs.  
5. Create the trail.

Once enabled, CloudTrail begins logging all API activity made by users, roles, and AWS services.

### **Step 2: Enable Amazon GuardDuty**

GuardDuty analyzes CloudTrail logs, DNS logs, VPC Flow Logs, and other telemetry to detect suspicious or malicious activity.

**Steps:**

1. Open the GuardDuty console.  
2. Click “Enable GuardDuty”.  
3. Wait while the service starts processing account activity.

After activation, GuardDuty monitors your AWS account for threats such as account compromise, EC2 attacks, port scans, unauthorized access patterns, malware traffic, and more.

### **Step 3: Create an SNS Topic for Notifications**

SNS is used to send alerts to your email whenever GuardDuty detects a threat.

**Steps:**

1. Open Amazon SNS → left navigation panel → Topics → Create topic.  
2. Choose type "Standard".  
3. Enter topic name like: `GuardDuty-Threat-Alerts`.  
4. Create the topic.  
5. Create a subscription:  
   * Protocol: Email  
   * Endpoint: your email address  
6. Confirm subscription by clicking the link sent to your email. Or you can directly right click on(Confirm subscription) in mail which you got and copy that and paste it in confirm subscriptions. 

SNS is now ready for sending alert messages.

### **Step 4: Create a Lambda Function to Process GuardDuty Findings**

This Lambda function receives GuardDuty event data from EventBridge, extracts important details, and sends a readable alert to SNS.

#### **Create IAM Role for Lambda**

1. Open IAM → Create role.  
2. Trusted entity: AWS service.  
3. Use case: Lambda.  
4. Attach policy: `AWSLambdaBasicExecutionRole`  
   (This allows writing logs to CloudWatch.)  
5. Name the role: `GuardDuty-Lambda-Role`.

#### **Create the Lambda Function**

1. Open the Lambda console.  
2. Create a new function.  
3. Choose:  
   * Name: `GuardDuty-Automated-Response`  
   * Runtime: Python 3.13  
   * Architecture: x86\_64  
   * Permissions: "Use existing role" → select the IAM role created above  
4. Create the function.

Paste the Python code into the function (provided Lambda\_Code.py).

#### **Add Environment Variable**

Key: `SNS_TOPIC_ARN`  
Value: ARN of the SNS topic created earlier.

#### **Allow Lambda to Publish to SNS**

1. Go to IAM → Roles →`GuardDuty-Lambda-Role`.  
2. Add an inline policy:

`{`  
  `"Version": "2012-10-17",`  
  `"Statement": [`  
    `{`  
      `"Effect": "Allow",`  
      `"Action": "sns:Publish",`  
      `"Resource": "arn:aws:sns:your-region:your-account-id:your-topic-name"`  
    `}`  
  `]`  
`}`

Replace the placeholders with your actual values.

This grants Lambda permission to publish alerts.

### **Step 5: Create an EventBridge Rule**

EventBridge listens for new GuardDuty findings and triggers your Lambda function automatically.

Steps:

1. Open EventBridge → Rules → Create rule.  
2. Name: `GuardDuty-EC2-Threat-Rule`.  
3. Event bus: default.  
4. Rule type: "Rule with event pattern".  
5. Event source: AWS services → GuardDuty.  
6. Event type: GuardDuty Finding.  
7. Use this event pattern:

`{`  
  `"source": ["aws.guardduty"],`  
  `"detail-type": ["GuardDuty Finding"],`  
  `"detail": {`  
    `"type": ["Trojan:EC2/BlackholeTraffic"]`  
  `}`  
`}`

8. Target:

   * Type: AWS service  
   * Service: Lambda  
   * Function: GuardDuty-Automated-Response  
9. Create the rule.

### **Testing the Setup**

Use AWS CLI to generate a sample GuardDuty finding.

**Steps:**

1. Find your GuardDuty detector ID in `Settings` (GuardDuty console).  
2. Run:

`aws guardduty create-sample-findings \`  
`--detector-id YOUR_DETECTOR_ID \`  
`--finding-types "Trojan:EC2/BlackholeTraffic"`

This generates a simulated threat.

### **Verification**

**1\. Check your email.**  
 SNS will send an alert containing important details about the threat.

**2\. Check GuardDuty console.**  
 The sample finding will appear in the findings list.

### **Cleanup**

**To avoid charges:**

* Delete SNS topic  
* Delete Lambda function  
* Delete EventBridge rule  
* Disable GuardDuty (optional)  
* Delete CloudTrail trail (optional)


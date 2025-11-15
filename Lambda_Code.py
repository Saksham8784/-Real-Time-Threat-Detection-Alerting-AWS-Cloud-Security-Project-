import boto3
import json
import os
from datetime import datetime

sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        detail = event["detail"]
        instance_id = detail["resource"]["instanceDetails"]["instanceId"]
        public_ip = detail["resource"]["instanceDetails"]["networkInterfaces"][0]["publicIp"]
        finding_type = detail["type"]
        region = detail["region"]
        description = detail["description"]
        time = detail["service"]["eventFirstSeen"]
        profile = detail["resource"]["instanceDetails"]["iamInstanceProfile"]["arn"]
        remote_ip = detail["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["ipAddressV4"]
        remote_port = detail["service"]["action"]["networkConnectionAction"]["remotePortDetails"]["port"]
        
        readable_message = f"""
🚨 GuardDuty Alert: Trojan Activity Detected

🔍 Type: {finding_type}
💡 Description: {description}

🖥 Instance ID: {instance_id}
🔐 Instance Profile: {profile}
🌐 Public IP: {public_ip}
➡️ Remote IP: {remote_ip}:{remote_port}
📍 Region: {region}
🕒 Time: {datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d %H:%M:%S')} UTC

🧠 Recommendation:
Isolate or stop the EC2 instance and investigate for malware or unauthorized traffic.

📘 Learn more: https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html
"""

        sns.publish(
            TopicArn=os.environ["SNS_TOPIC_ARN"],
            Subject="🚨 GuardDuty Alert: EC2 Threat Detected",
            Message=readable_message
        )

        return {
            'statusCode': 200,
            'body': f"Formatted alert sent to SNS topic for instance {instance_id}"
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': f"Error processing event: {str(e)}"
        }
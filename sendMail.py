import json
import boto3
import os

# Initialize the SNS client
sns_client = boto3.client('sns')

# Replace with your SNS Topic ARN

def lambda_handler(event, context):
    try:
        # Parse incoming payload from EventBridge Scheduler
        email = event.get("email")
        details = event.get("details")
        due_date = event.get("due_date")
        name = event.get("name")
        title = event.get("title")
        additional_notes = event.get("additional_notes")
        
        sns_topic_arn = event.get("sns_topic_arn")
        #sns_topic_arn = "arn:aws:sns:af-south-1:590184089259:task-notifications-a3109d06-a59e-4a6e-9b76-28ec0e1287e1"

        email_body = f"""
        Hello {name},

        You have a new task scheduled. Here are the details:

        📝 Task Title: {title}
        📅 Due Date: {due_date}
        📖 Details: {details}

        {"🗒 Additional Notes: " + additional_notes if additional_notes else ""}

        📌 Please ensure that you complete this task on time.

        Best Regards,  
        Your Task Management Team  
        (This is an automated message. Please do not reply.)
        """


        # Publish the message to SNS Topic
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=email_body,
            Subject="New Task Notification",
            MessageAttributes={
                "email": {
                    "DataType": "String",
                    "StringValue": email
                }
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Email sent successfully via SNS",
                "sns_message_id": response["MessageId"]
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

import json
import boto3
import datetime
import uuid
import logging

# Initialize SNS and EventBridge clients
sns = boto3.client('sns')
eventbridge = boto3.client('events')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('theServerlessPlanner')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def convert_to_cron(iso_date):
    dt = datetime.datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
    # AWS Scheduler cron format: "cron(Min Hour Day Month ? Year)"
    cron_expression = f"cron({dt.minute} {dt.hour} {dt.day} {dt.month} ? {dt.year})"
    return cron_expression

def create_sns_topic():
    """
    Create a new SNS topic dynamically and return the ARN of the created topic.
    """
    try:
        response = sns.create_topic(Name=f'task-notifications-{str(uuid.uuid4())}')
        return response['TopicArn']
    except Exception as e:
        print(f"Error creating SNS topic: {str(e)}")
        raise

def subscribe_to_sns_topic(email, sns_topic_arn):
    """
    Subscribe the provided email to the SNS topic and send a confirmation.
    """
    try:
        response = sns.subscribe(
            TopicArn=sns_topic_arn,
            Protocol='email',
            Endpoint=email
        )
        return response['SubscriptionArn']
    except Exception as e:
        print(f"Error subscribing to SNS topic: {str(e)}")
        raise


def create_eventbridge_schedule(due_date, sns_topic_arn, email,name, title,
        details, additional_notes):

    client = boto3.client('scheduler')
    lambda_arn = "arn:aws:lambda:af-south-1:590184089259:function:SendMailforPlan"
    
    schedule_name = f"task-reminder-{email.replace('@', '-').replace('.', '-')}-schedule"
    schedule_expression = convert_to_cron(due_date)
    role_arn = "arn:aws:iam::590184089259:role/service-role/Amazon_EventBridge_Scheduler_SNS_46046a94c3"  # Replace with your IAM Role ARN
    schedule_timezone = 'Africa/Lagos'
    flexible_time_window = {'Mode': 'OFF'}
    input_payload = json.dumps({'email': email, 'due_date':due_date, 
                        'name':name, 'title':title,'details':details,
                        'additional_notes':additional_notes,
                        'sns_topic_arn':sns_topic_arn})
    
    try:
        response = client.create_schedule(
            Name=schedule_name,
            ScheduleExpression=schedule_expression,
            ScheduleExpressionTimezone=schedule_timezone,
            FlexibleTimeWindow=flexible_time_window,
            State='ENABLED',  # Ensures the schedule is active
            Target={
                'Arn': lambda_arn,
                'RoleArn': role_arn,
                'Input': input_payload
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Schedule created successfully',
            'schedule_arn': response['ScheduleArn'],
            'sns_topic_arn': sns_topic_arn
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def store_data_in_dynamodb(email, title, name, details, due_date, additional_notes, created_at):
    table = dynamodb.Table("theServerlessPlannerRecords")

    """
    Store data in DynamoDB.
    """
    response = table.put_item(
        Item={
            'email': email,  # Partition Key
            'title': title,  # Sort Key (optional, but recommended for better querying)
            'name': name,
            'details': details,
            'dueDate': due_date,
            'additionalNotes': additional_notes,
            'createdAt': created_at
            }
    )

def lambda_handler(event, context):
    try:

        # Log the full incoming event for debugging
        logger.info("Incoming Event: %s", json.dumps(event, indent=2))
        # Parse incoming data from API Gateway
        body = event['body']
        #body = json.loads(event['body'])

        name = body.get('name')
        email = body.get('email')
        title = body.get('title')
        details = body.get('details')
        due_date = body.get('dueDate')
        additional_notes = body.get('additionalNotes', '')
        created_at = datetime.datetime.utcnow().isoformat()

        # Validate required fields
        if not name or not email or not title or not details or not due_date:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        # Log parsed data
        logger.info(f"Parsed Data - Name: {name}, Email: {email}, Title: {title}, DueDate: {due_date}")

        # Create an SNS topic dynamically
        sns_topic_arn = create_sns_topic()
        subscription_arn = subscribe_to_sns_topic(email, sns_topic_arn)

        # Create EventBridge rule to trigger the SNS notification at the specified due date
        create_eventbridge_schedule(due_date, sns_topic_arn, email, name, title,
        details, additional_notes)

        #Store the Data in DynamoDB
        store_data_in_dynamodb(email, title, name, details, due_date, additional_notes, created_at)
       

        # Send the confirmation email to the user
        

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Task scheduled and notification will be sent. Please check your email to confirm your subscription.'})
        }

    except Exception as e:
        logger.error("Error processing request: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

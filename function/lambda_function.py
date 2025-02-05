import boto3
from sns import SNS


TOPIC_ARN = 'arn:aws:sns:us-east-1:886436967044:Coffein-UploadsNotificationTopic'

def lambda_handler(event, context):
    sns_instance = SNS(topic_arn=TOPIC_ARN)
    messages = event.get("Records", [])
    outcome_msg = "\n\n".join([message.get("body","Body_not_found") for message in messages])
    if outcome_msg:
        sns_instance.topic.publish(
            Message=outcome_msg,
            Subject='Uploads images'
        )
    return {'statusCode': 200,"body": "Successful!", "notification": outcome_msg}







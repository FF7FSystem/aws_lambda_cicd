import boto3

class SQS:
    """
    Amazon SQS Service via python sdk (boto)
    """

    def __init__(self, queue_url: str) -> None:
        self.client = boto3.client('sqs', region_name='us-east-1')
        resource = boto3.resource('sqs', region_name='us-east-1')
        self.queue = resource.Queue(queue_url)

    def send_message(self, message: str):
        self.queue.send_message(MessageBody=message)

    def get_messages_end_clear_queue(self) -> list:
        # bached - ? no thanks
        outcome = []
        # too easy, need more checking (that a file was deleted or added to outcome)
        while int(self.queue.attributes['ApproximateNumberOfMessages']):
            for message in self.queue.receive_messages():
                outcome.append(message)
                message.delete()
            self.queue.reload()
        return outcome
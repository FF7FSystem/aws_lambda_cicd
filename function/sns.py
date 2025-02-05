import boto3

class SNS:
    """
    Amazon SNS Service via python sdk (boto)
    """

    def __init__(self, topic_arn: str, protocol: str = 'email') -> None:
        self.client = boto3.client('sns', region_name='us-east-1')
        resource = boto3.resource('sns', region_name='us-east-1')
        self.topic = resource.Topic(topic_arn)
        self.topic_arn = topic_arn
        self.protocol = protocol

    def get_subscriptions(self) -> list:
        return list(self.topic.subscriptions.all())

    def subscribe(self, email: str) -> str:
        return self.topic.subscribe(Endpoint=email, Protocol=self.protocol, ReturnSubscriptionArn=True)

    def unsubscribe(self, arn: str) -> None:
        self.client.unsubscribe(SubscriptionArn=arn)

    def get_subscription_arn_by_email(self, email: str) -> None | str:
        for subscription in self.topic.subscriptions.all():
            # use pydantic model here !
            if 'PendingConfirmation' == getattr(subscription, "arn", "PendingConfirmation"):
                continue
            subscription_attr = getattr(subscription, "attributes", {})
            subscription_email = subscription_attr.get('Endpoint', None)
            subscription_arn = subscription_attr.get('SubscriptionArn', None)
            if email == subscription_email and subscription_arn:
                return subscription_arn

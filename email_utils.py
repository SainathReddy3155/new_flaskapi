import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
load_dotenv()


SENDER = "sainathreddy.unf12@gmail.com"

def send_registration_email(recipient_email: str, username: str) -> bool:
    print("recipient_email : ",recipient_email)
    print("username",username)
    subject = "Welcome to Our App!"
    body_text = f"Hi {username},\n\nThank you for registering successfully!"
    body_html = f"""
    <html>
    <head></head>
    <body>
      <h1>Welcome, {username}!</h1>
      <p>You have successfully registered.</p>
    </body>
    </html>
    """

    client = boto3.client(
    "ses",
    region_name=os.getenv("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


    try:
        response = client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [recipient_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {"Data": body_text},
                    "Html": {"Data": body_html}
                },
            },
        )
        return True
    except ClientError as e:
        print(f"Failed to send email: {e.response['Error']['Message']}")
        return False

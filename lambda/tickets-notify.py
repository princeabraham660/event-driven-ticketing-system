import json
import boto3

ses = boto3.client("ses", region_name="eu-north-1")

SENDER_EMAIL = "YOUR_VERIFIED_EMAIL"


def lambda_handler(event, context):

    detail = event.get("detail", {})

    ticket_id = detail.get("ticketid")
    title = detail.get("title")
    description = detail.get("description")
    priority = detail.get("priority")
    requester_email = detail.get("email")

    subject = f"New Ticket Created - {priority} Priority"

    body = f"""
A new support ticket has been created.

Ticket ID: {ticket_id}
Title: {title}
Description: {description}
Priority: {priority}

Requester Email: {requester_email}
"""

    response = ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            "ToAddresses": [
                SENDER_EMAIL
            ]
        },
        Message={
            "Subject": {
                "Data": subject
            },
            "Body": {
                "Text": {
                    "Data": body
                }
            }
        }
    )

    print("Email sent successfully")
    print("SES Message ID:", response["MessageId"])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Notification email sent successfully"
        })
    }

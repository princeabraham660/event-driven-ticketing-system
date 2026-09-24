import json
import boto3

ses = boto3.client("ses", region_name="eu-north-1")

SENDER_EMAIL = "YOUR_VERIFIED_EMAIL"


def lambda_handler(event, context):

    detail = event.get("detail", {})

    ticket_id = detail.get("ticketid")
    title = detail.get("title")
    status = detail.get("status")
    requester_email = detail.get("email")

    subject = f"Ticket Status Updated - {status}"

    body = f"""
Your support ticket has been updated.

Ticket ID: {ticket_id}
Title: {title}
New Status: {status}

Thank you.
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

    print("Status notification email sent successfully")
    print("SES Message ID:", response["MessageId"])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Status notification sent"
        })
    }

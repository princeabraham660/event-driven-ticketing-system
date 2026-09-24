import json


def lambda_handler(event, context):

    print("SQS message received")

    for record in event.get("Records", []):

        message_body = record.get("body")

        print("Message body:")
        print(message_body)

        try:
            ticket_event = json.loads(message_body)

            print("Ticket event processed:")
            print(json.dumps(ticket_event, indent=2))

        except Exception as e:
            print("Error processing message:", str(e))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "SQS messages processed successfully"
        })
    }

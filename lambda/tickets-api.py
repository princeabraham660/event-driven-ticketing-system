import json
import boto3
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
table = dynamodb.Table("Tickets")

events = boto3.client("events", region_name="eu-north-1")


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    method = event.get("requestContext", {}).get("http", {}).get("method")

    # CREATE TICKET
    if method == "POST":

        body = json.loads(event.get("body", "{}"))

        ticket_id = str(uuid.uuid4())

        ticket = {
            "ticketid": ticket_id,
            "string": "ticket",
            "title": body.get("title"),
            "description": body.get("description"),
            "priority": body.get("priority"),
            "email": body.get("email"),
            "status": "Open",
            "createdAt": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=ticket)

        # Publish TicketCreated event
        events.put_events(
            Entries=[
                {
                    "EventBusName": "ticket-events",
                    "Source": "ticketing.system",
                    "DetailType": "TicketCreated",
                    "Detail": json.dumps(ticket)
                }
            ]
        )

        return response(201, {
            "message": "Ticket created successfully",
            "ticket": ticket
        })

    # LIST TICKETS
    if method == "GET":

        result = table.scan()

        return response(200, {
            "tickets": result.get("Items", [])
        })

    # UPDATE TICKET STATUS
    if method == "PATCH":

        ticket_id = event.get("pathParameters", {}).get("ticketid")

        body = json.loads(event.get("body", "{}"))
        new_status = body.get("status")

        allowed_statuses = [
            "Open",
            "In Progress",
            "Resolved",
            "Closed"
        ]

        if new_status not in allowed_statuses:
            return response(400, {
                "message": "Invalid status"
            })

        result = table.update_item(
            Key={
                "ticketid": ticket_id,
                "string": "ticket"
            },
            UpdateExpression="SET #s = :status",
            ExpressionAttributeNames={
                "#s": "status"
            },
            ExpressionAttributeValues={
                ":status": new_status
            },
            ReturnValues="ALL_NEW"
        )

        updated_ticket = result.get("Attributes")

        # Publish TicketStatusChanged event
        events.put_events(
            Entries=[
                {
                    "EventBusName": "ticket-events",
                    "Source": "ticketing.system",
                    "DetailType": "TicketStatusChanged",
                    "Detail": json.dumps(updated_ticket)
                }
            ]
        )

        return response(200, {
            "message": "Ticket status updated successfully",
            "ticket": updated_ticket
        })

    return response(400, {
        "message": "Unsupported method"
    })

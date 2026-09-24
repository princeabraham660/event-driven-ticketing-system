# Event-Driven Ticketing System
AWS Event-Driven Ticketing System using S3, API Gateway, Lambda, DynamoDB, EventBridge, SQS, SES, CloudWatch, and IAM.
An AWS-based serverless ticketing system that uses event-driven architecture to create, manage, and process support tickets.

## Project Overview

The system allows users to:

- Create support tickets
- Set ticket priority
- View tickets
- Update ticket status
- Receive ticket notifications
- Escalate high-priority tickets
- Process ticket events asynchronously

## AWS Services Used

- Amazon S3 – Hosts the frontend
- Amazon API Gateway – Provides REST API endpoints
- AWS Lambda – Handles backend logic and event processing
- Amazon DynamoDB – Stores ticket information
- Amazon EventBridge – Routes ticket events
- Amazon SQS – Provides asynchronous message processing
- Amazon SES – Sends email notifications
- Amazon CloudWatch – Provides logging and monitoring
- AWS IAM – Manages permissions and access

## Event Flow

1. User creates a ticket through the S3-hosted website.
2. API Gateway receives the request.
3. Lambda processes the request.
4. Ticket information is stored in DynamoDB.
5. Lambda publishes a `TicketCreated` event to EventBridge.
6. EventBridge routes the event to different consumers.
7. Notification and escalation Lambda functions send emails using SES.
8. The ticket event can also be sent to SQS for asynchronous processing.
9. When the ticket status changes, a `TicketStatusChanged` event is published.
10. The status notification Lambda sends an email.

## Ticket Status

Tickets can have the following statuses:

- Open
- In Progress
- Resolved
- Closed

## Priority Levels

- Low
- Medium
- High

High-priority tickets trigger an escalation notification.

## Project Structure

```text
event-driven-ticketing-system/
│
├── index.html
│
├── lambda/
│   ├── tickets-api.py
│   ├── tickets-notify.py
│   ├── ticket-escalation.py
│   ├── ticket-status-notify.py
│   └── ticket-queue-processor.py
│
└── architecture.png

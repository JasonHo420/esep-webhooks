import json
import os
import requests

def lambda_handler(event, context):
    # Log the received event for debugging
    context.logger.info(f"Event received: {json.dumps(event)}")
    
    # Parse the event body (assuming it's JSON from GitHub Webhook)
    try:
        body = json.loads(event['body'])  # GitHub webhook payload is usually in 'body'
        
        # Extract the 'html_url' from the issue object
        issue_url = body['issue']['html_url']
        print(f"Issue Created: {issue_url}")
        
        # Prepare the payload for Slack message
        payload = {
            "text": f"Issue Created: {issue_url}"
        }
        
        # Get the Slack webhook URL from environment variables
        slack_url = os.getenv("SLACK_URL")
        
        # Send the POST request to Slack
        response = requests.post(slack_url, json=payload)
        
        # Log the response from Slack for debugging
        print(f"Slack response status: {response.status_code}")
        
        # Return the response from Slack (or any other necessary info)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Message sent to Slack', 'slack_response': response.text})
        }

    except KeyError as e:
        # Handle missing keys in the event or body
        print(f"Error extracting data: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Error processing the webhook event'})
        }
    except json.JSONDecodeError:
        # Handle invalid JSON in the event body
        print("Invalid JSON received.")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in the webhook payload'})
        }




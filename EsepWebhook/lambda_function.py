import json
import os
import requests

def lambda_handler(event, context):
    # Log the received event for debugging
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract the GitHub issue payload from the event
        issue_data = event.get("issue")
        
        # Check if issue data exists and retrieve the html_url
        if issue_data and "html_url" in issue_data:
            issue_url = issue_data["html_url"]
            print(f"Issue URL: {issue_url}")
            
            # Prepare the payload for the Slack message
            payload = {
                "text": f"Issue Created: {issue_url}"
            }
            
            # Get the Slack webhook URL from environment variables
            slack_url = os.getenv("SLACK_URL")
            
            # Send the payload to the Slack webhook URL
            response = requests.post(slack_url, json=payload)
            
            # Log the response for debugging
            print(f"Slack response status: {response.status_code}")
            print(f"Slack response text: {response.text}")
            
            # Return success message and response data
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Message sent to Slack successfully',
                    'slack_response': response.text
                })
            }
        else:
            # If no issue data is found, return an error message
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No issue data found in the webhook payload'
                })
            }
            
    except Exception as e:
        # Handle any exceptions that occur
        print(f"Error processing the event: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }





import json
import boto3
import uuid

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    # TODO implement
    transaction_id = str(uuid.uuid1())
    
    print(event)
    
    if event['httpMethod'] != 'POST':
        return {
            "statusCode": 405,
            "body": json.dumps('Method is not allowed')
        }
    
    body = json.loads(event['body'])
    
    input = {
        "user_id": body['user_id'],
        "transaction_type": body['transaction_type'],
        "ticker": body['ticker'],
        "quantity": body['quantity'],
        "money_amount": body['price'] * body['quantity']
    }
    
    response = client.start_execution(
        stateMachineArn="arn:aws:states:us-east-1:593444383578:stateMachine:StockTransaction",
        name=transaction_id,
        input=json.dumps(input)
    )
    
    print(response)
    
    return {
        "statusCode": 200,
        "body": json.dumps('Stock transaction is successfully done')
    }

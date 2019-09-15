# Reacts to pipeline stack deployment status changes and notifies the integration


import boto3
import re


def extract_variables(message):
    variables = {}

    for line in message.lines:
        # FIXME: compile regex

        match = re.search(
        )

        variable = match[1]
        value = match[2]

        variables[variable] = value

    return variables


def notify_integration():
    return


def process_message(message):
    variables = extract_variables(
        message,
    )

    # Available variables:
    # StackId
    # Timestamp
    # EventId
    # LogicalResourceId
    # Namespace
    # PhysicalResourceId
    # PrincipalId
    # ResourceProperties
    # ResourceStatus
    # ResourceStatusReason
    # ResourceType
    # StackName
    # ClientRequestToken

    stack_name = variables['StackName']
    logical_resource_id = variables['LogicalResourceId']
    resource_type = variables['ResourceType']

    message_relates_to_stack_itself = stack_name == logical_resource_id and resource_type == 'AWS::CloudFormation::Stack'

    if message_relates_to_stack_itself:
        resource_status = variables['ResourceStatus']

        notify_integration(
          stack,
          resource_status,
        )

    return


def main(records):
    for record in records:
        obj = record['Sns']
        subject = obj['Subject']

        if subject == 'AWS CloudFormation Notification':
            message = obj['Message']
            process_message(message)
        else:
            # forged message!

            # TODO: Submit metric to CloudWatch (about forged messages)

    return


def handler(event, context):
    records = event['Records']

    main(records)

    response = {
    }

    return response

# Reacts to pipeline stack deployment status changes and notifies the integration


import boto3
import re


variable_value_pattern = re.compile(
    '^([^=]+)=(.*)$',
)


def extract_variables(message):
    variables = {}

    for line in message.lines:
        match = variable_value_pattern.search(
            line,
        )

        variable = match[1]
        value = match[2]

        variables[variable] = value

    return variables


def trigger_pipeline():
    codepipeline = foreign_session.client(
        'codepipeline',
    )

    pipeline_name = stack_outputs['Pipeline']

    codepipeline.start_pipeline_execution(
        PipelineName=pipeline_name,
    )

    return


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

        if resource_status == 'CREATE_COMPLETE':
            status = 'CREATED'

            # When the stack is created, the pipeline will run automatically,
            # so it's not necessary to trigger it manually.
        elif resource_status == 'UPDATE_COMPLETE':
            # Manual pipeline triggers are necessary after stack updates.

            trigger_pipeline(
            )

            status = 'UPDATED'
        else:
            status = 'FAILED'

        notify_integration(
          stack,
          status,
        )

    return


def process_record(record):
    obj = record['Sns']
    subject = obj['Subject']

    if subject == 'AWS CloudFormation Notification':
        message = obj['Message']
        process_message(
            message,
        )
    else:
        # forged message!

        # TODO: Submit metric to CloudWatch (about forged messages)

    return


def process_records(records):
    for record in records:
        process_record(
            record,
        )

    return


def handler(event, context):
    records = event['Records']

    record = records[0]

    process_record(
        record,
    )
    #main(records)

    response = {
    }

    return response

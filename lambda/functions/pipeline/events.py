# Reacts to pipeline status changes and notifies GitHub


import boto3


def notify_integration():
    return


def process_event(event):
    must_notify_integration = gate_reached or pipeline_finished

    if must_notify_integration:
        notify_integration(
        )

    return


def handler(event, context):
    records = event['Records']

    for record in records:
        event = record['events']

        process_event(
            event,
        )

    response = {
    }

    return response

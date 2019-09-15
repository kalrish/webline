import boto3


def assume_role(role_arn):
    sts = boto3.client(
        'sts',
    )

    session_name = 'pipeduct-pipeline-deploy'

    response = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
    )

    credentials = response['Credentials']

    return credentials


def create_session(credentials):
    access_key_id = credentials['AccessKeyId']
    secret_access_key = credentials['SecretAccessKey']
    session_token = credentials['SessionToken']

    session = boto3.session.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )

    return session


def create_session_from_role(role_arn):
    credentials = assume_role(
        role_arn,
    )

    session = create_session(
        credentials,
    )

    return session


def get_stack_status(branch, repository, session):
    client = session.client(
        'cloudformation',
    )

    try:
        response = client.describe_stacks(
        )
    except AmazonCloudFormationException:
        return_value = False
    else:
        stack_status = response['Stacks'][0]['StackStatus']

        return_value = stack_status

    return return_value


def deploy_stack(bucket, cloudformation_role, topic_arn):
client = boto3.client(
    'cloudformation',
)

stack_name = f'pipeduct-{owner}-{repository}-{branch}'
template_url = f'https://{bucket}.s3.amazonaws.com/v1/cfn/pipeline.yaml'

response = client.create_change_set(
    stack_name=stack_name,
    template_url=template_url,
    parameters=[
        {
            parameter_key='WebpipeBucket',
            parameter_value=bucket,
        },
        {
            parameter_key='Branch',
            parameter_value=branch,
        },
        {
            parameter_key='SourceProvider',
            parameter_value='github',
        },
    ],
    capabilities=[
        'CAPABILITY_IAM',
    ],
    role_arn=cloudformation_role,
    notification_arns=[
        topic_arn,
    ],
    tags=[
        {
            key='GitHub-Owner',
            value=owner,
        },
        {
            key='GitHub-Repo',
            value=repo,
        },
    ],
)

response = client.execute_change_set(
)

return


def enqueue_stack_update():
return


def main(config):
app_role = config['app_role']
cloudformation_role = config['cloudformation_role']

foreign_session = create_session_from_role(
    app_role,
)

stack_status = get_stack_status(
    branch=branch,
    repository=repository,
    session=foreign_session,
)

status = None

if stack_status:
    # The stack exists

    stack_must_be_recreated = stack_status == 'CREATE_FAILED' or stack_status == 'DELETE_COMPLETE'
    stack_may_be_updated = stack_status == 'CREATE_COMPLETE' or stack_status == 'UPDATE_COMPLETE'

    if stack_must_be_recreated:
        delete_stack(
        )

        enqueue_stack_update(
            config,
        )

        status = 'RECREATING'
    elif stack_may_be_updated:
        deploy_stack(
            branch=branch,
            bucket=webpipe_bucket,
            owner=owner,
            repository=repository,
            role=pipeline_stack_deployment_role,
            sns_arn=pipeline_stack_notification_topic,
        )

        status = 'UPDATING'
    else:
        # somebody was nasty and pushed too quick
        # so the stack is still being updated (or created)
        # we can only wait until the operation is complete
        # then issue an update / create a changeset

        assert(
            stack_status == 'CREATE_IN_PROGRESS' or stack_status == 'UPDATE_IN_PROGRESS',
        )

        enqueue_stack_update(
                config,
            )

            status = 'QUEUED'

    else:
        # The stack doesn't exist

        status = 'CREATING'

    trigger_pipeline(
    )

    return status


def handler(events, context):
    config = events['Records'][0]

    status = main(
        config,
    )

    return status

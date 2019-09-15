import boto3


def pipeline_deployed(branch, repository):
  client = Aws::CloudFormation::Client.new()

  response = {}

  pipeline_stack_exists = false

  return pipeline_stack_exists


def deploy_pipeline(bucket, role, sns_arn):
    client = boto3.client(
        'cloudformation',
    )

    response = client.create_change_set(
        stack_name: "webpipe-pipeline-#{owner}-#{repository}-#{branch}",
        template_url: "https://#{bucket}.s3.amazonaws.com/v1/cfn/pipeline.yaml",
        parameters: [
            {
                parameter_key: 'WebpipeBucket',
                parameter_value: bucket,
            },
            {
                parameter_key: 'Branch',
                parameter_value: branch,
            },
            {
                parameter_key: 'SourceProvider',
                parameter_value: 'github',
            },
        ],
        capabilities: [
            'CAPABILITY_IAM',
        ],
        role_arn: role,
        notification_arns: [
            sns_arn,
        ],
        tags: [
            {
                key: 'GitHub-Owner',
                value: owner,
            },
            {
                key: 'GitHub-Repo',
                value: repo,
            },
        ],
    )

    response = client.execute_change_set(
    )

    return


def main():
    role = get_customer_role_from_repo_branch()

    assume_role(role)

    pipeline_deployed = pipeline_deployed(
        branch=branch,
        repository=repository,
    )

    if not pipeline_deployed:
        deploy_pipeline(
            branch=branch,
            bucket=webpipe_bucket,
            owner=owner,
            repository=repository,
            role=pipeline_stack_deployment_role,
            sns_arn=pipeline_stack_notification_topic,
        )

    trigger_pipeline(
    )

    return


def handler():
    return

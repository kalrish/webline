# Manages pipelines on behalf of integrations


require 'aws-sdk-cloudformation'
require 'yaml'


def assume_role(role_arn)
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
end


def create_session(credentials)
  access_key_id = credentials['AccessKeyId']
  secret_access_key = credentials['SecretAccessKey']
  session_token = credentials['SessionToken']

  session = boto3.session.Session(
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token,
  )

  return session
end


def create_session_from_role(role_arn)
    credentials = assume_role(
        role_arn,
    )

    session = create_session(
        credentials,
    )

    return session
end


def get_stack_status(branch, repository, session)
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
end


def enqueue_stack_update()
end


def main(parameters)
  # Raw YAML
  config_data = parameters['config']

  config = YAML.safe_load(
    config_data,
  )

  app_role = config['app_role']
  cloudformation_role = config['cloudformation_role']

  foreign_session = create_session_from_role(
    app_role,
  )

  cloudformation = foreign_session.client(
    'cloudformation',
  )

  action = parameters['action']

  stack_name_suffix = config['stack']['name_suffix']

  stack_name = "pipeduct-#{owner}-#{repository}-#{identifier_from_integration}"

  status = None

  begin
    if action == 'create':
      template_url = f'https://{bucket}.s3.amazonaws.com/v1/cfn/pipeline.yaml'

      begin
        cloudformation.validate_template(
          TemplateURL=template_url,
        )
      rescue ClientError
        status = 'INVALID'
      else:
        parameters = {
          'StackName': stack_name,
          'TemplateURL': template_url,
          'Parameters': [
            {
              'ParameterKey': 'WebpipeBucket',
              'ParameterValue': bucket,
            },
            {
              'ParameterKey': 'Branch',
              'ParameterValue': branch,
            },
            {
              'ParameterKey': 'SourceProvider',
              'ParameterValue': 'github',
            },
          ],
          'Capabilities': [
            'CAPABILITY_IAM',
          ],
          'RoleARN': cloudformation_role,
          'NotificationARNs': [
            topic_arn,
          ],
          'OnFailure': 'DELETE',
          'Tags': [
            {
              'Key': 'GitHub-Owner',
              'Value': owner,
            },
            {
              'Key': 'GitHub-Repo',
              'Value': repo,
            },
          ],
        }

        # FIXME: handle CREATE_FAILED ?

        try:
            cloudformation.create_stack(
                **parameters,
            )
        except cloudformation.exceptions.AlreadyExists:
            try:
                cloudformation.update_stack(
                    **parameters,
                )
            except UpdateInProgress:
                enqueue_stack_update(
                )

                status = 'PENDING'
            else:
                status = 'UPDATING'
        else:
            status = 'CREATING'
    else
      assert(
          action == 'delete',
      )

      begin
        cloudformation.delete_stack(
            StackName=stack_name,
        )
      rescue ClientError
        status = 'Couldn"t delete'
      else
        status = 'DELETING'
      end
  rescue cloudformation.exceptions.AccessDeniedException
    status = 'DENIED'
  rescue botocore.exceptions.ClientError as e
    status = 'FAILED'

    error_code = e.response['Error']['Code']
    error_message = e.response['Error']['Message']
    request_id = e.response['ResponseMetadata']['RequestId']

    extra_status = {
      'code': error_code,
      'message': error_message,
      'request_id': request_id,
    }
  end

  response = {
    'status': status,
    'extra': extra_status,
  }

  return response
end


def handler(event, context)
  status = main(
    event,
  )

  return status
end

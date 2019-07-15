webLine: AWS-based website deployment system
================================================================================

webLine


Features
--------------------------------------------------------------------------------

 -  Listen to GitHub
 -  Branch deployments for preview & testing


Installation
--------------------------------------------------------------------------------

 -  AWS account
 -  AWS SAM CLI
 
    -  Lambda function
    -  API gateway
    -  CloudFormation stack template (cfn/pipeline/template.yaml) (or embedded in the Lambda function?)


Architecture
--------------------------------------------------------------------------------

Three CloudFormation stacks:

 -  `www-me-github`
 -  ``


DNS hierarchy
--------------------------------------------------------------------------------

 -  Root: `www.djsp.eu`.
 -  Personal website: `me.www.djsp.eu`.
 -  Blog: `blog.www.djsp.eu`.
 -  Flaschenpost: `flaschenpost.www.djsp.eu`.

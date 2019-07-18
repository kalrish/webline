webLine: AWS-based website deployment system
================================================================================

webLine is a website build and deployment solution based on AWS.


Overview
--------------------------------------------------------------------------------

webLine is the core of a CI/CD solution for websites. Thus, by itself, webLine is useless. Instead, an integration for your website's code repository must handle.


Installation
--------------------------------------------------------------------------------

To install webLine, you will need:

 -  an AWS account
 -  [GNU make](https://www.gnu.org/software/make/) >= 3.82
 -  a shell (for instance, [Bash](https://www.gnu.org/software/bash/) or [DASH](http://gondor.apana.org.au/~herbert/dash/))
 -  the [AWS CLI](https://aws.amazon.com/cli/)

If you meet the above requirements:

 1.  Create the webLine bucket.

     You can use the [CloudFormation stack template](cfn/bucket.yaml) provided.

 2.  Build the artifacts.

 3.  Upload artifacts to the webLine bucket.

     Once you have built all the artifacts, upload them to the webLine bucket

set -e


aws cloudformation deploy \
	--stack-name webline \
	--template-file cfn/bootstrap.yaml \
	#

bucket="$(
	aws \
		--query 'Stacks[0].Outputs[OutputKey==Bucket].OutputValue' \
		--output text \
		cloudformation describe-stacks \
		--stack-name webline \
		#
)"

aws s3 cp \
	--no-progress \
	--recursive \
	--exclude bootstrap.yaml \
	cfn \
	"s3://${bucket}/cfn/" \
	#

make buildspecs

aws s3 cp \
	--no-progress \
	buildspecs.zip \
	"s3://${bucket}/v1/buildspecs.zip" \
	#

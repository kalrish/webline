set -e


aws cloudformation deploy \
	--stack-name webline \
	--template-file cfn/bucket.yaml \
	--no-fail-on-empty-changeset \
	#

bucket="$(
	aws \
		--query 'Stacks[0].Outputs[?OutputKey==`Bucket`].OutputValue' \
		--output text \
		cloudformation describe-stacks \
		--stack-name webline \
		#
)"

aws s3 cp \
	--no-progress \
	--recursive \
	--exclude bucket.yaml \
	cfn \
	"s3://${bucket}/v1/cfn/" \
	#

make buildspecs

aws s3 cp \
	--no-progress \
	buildspecs.zip \
	"s3://${bucket}/v1/buildspecs.zip" \
	#

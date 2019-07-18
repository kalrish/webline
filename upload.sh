set -e

webline_bucket="$1"

aws s3 cp \
	--no-progress \
	--recursive \
	--exclude bucket.yaml \
	cfn \
	"s3://${webline_bucket}/v1/cfn/" \
	#

aws s3 cp \
	--no-progress \
	buildspecs.zip \
	"s3://${webline_bucket}/v1/buildspecs.zip" \
	#

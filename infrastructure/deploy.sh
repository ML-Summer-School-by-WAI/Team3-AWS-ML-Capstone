
AWS_REGION="ap-southeast-1" 
AWS_ACCOUNT_ID=
IMAGE_NAME=
LAMBDA_FUNCTION_NAME=
MODEL_BUCKET=
MODEL_KEY="models/model.joblib"

echo "Starting deployment script..."

echo "Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com


echo "Building Docker image..."
docker build -t $IMAGE_NAME .


echo "Tagging image for ECR..."
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_NAME:latest"
docker tag $IMAGE_NAME:latest $ECR_URI


echo "Pushing image to ECR..."
docker push $ECR_URI

echo "Updating Lambda function..."
aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION_NAME \
    --image-uri $ECR_URI \
    --region $AWS_REGION

aws lambda update-function-configuration \
    --function-name $LAMBDA_FUNCTION_NAME \
    --environment "Variables={MODEL_BUCKET=${MODEL_BUCKET},MODEL_KEY=${MODEL_KEY}}" \
    --region $AWS_REGION

echo "Deployment complete!"
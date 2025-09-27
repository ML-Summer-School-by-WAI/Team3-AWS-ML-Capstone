# docs/ARCHITECTURE.md

## AWS Architecture for the ML Pipeline

This document outlines the architecture of the end-to-end machine learning system deployed on AWS. The system is designed to be event-driven, serverless, and cost-effective, leveraging the AWS Free Tier.

### Component Descriptions

1.  **Amazon S3 (Simple Storage Service)**
    * **Purpose**: Serves as the central data lake for the project.
    * **Structure**: A single bucket (`project-bucket`) is used with three main prefixes (folders):
        * `/raw`: For storing raw, unprocessed datasets (e.g., `titanic.csv`).
        * `/processed`: For storing cleaned, validated, and feature-engineered data ready for training.
        * `/models`: For storing serialized, trained machine learning model artifacts (e.g., `model.joblib`).

2.  **AWS Lambda**
    * Two distinct Lambda functions power the pipeline:
    * **Data Validation Lambda**:
        * **Trigger**: S3 `PutObject` events in the `/raw` directory.
        * **Function**: Reads the newly uploaded raw data, validates its schema, checks for nulls and ranges, performs preprocessing, and saves the cleaned data to the `/processed` directory.
    * **Inference Lambda**:
        * **Trigger**: API Gateway HTTP requests.
        * **Function**: Deployed as a Docker container. It loads the trained model from S3, processes the incoming request data, and returns a real-time prediction.

3.  **Amazon API Gateway**
    * **Purpose**: Provides a public, serverless HTTP endpoint for the ML model.
    * **Function**: It receives `POST` requests with passenger data, triggers the Inference Lambda, and returns the model's prediction in the HTTP response.

4.  **Amazon ECR (Elastic Container Registry)**
    * **Purpose**: A managed Docker container registry.
    * **Function**: It stores the Docker image for our Inference Lambda, which contains all the necessary dependencies (pandas, scikit-learn) and the `predict.py` script.

5.  **Amazon CloudWatch**
    * **Purpose**: Provides monitoring and logging for all AWS services.
    * **Function**: It automatically captures logs from both Lambda functions, which is essential for debugging. It also monitors metrics like invocation count and duration.

### Workflow

1.  A user uploads a raw CSV file to the `s3://project-bucket/raw/` directory.
2.  The S3 event triggers the **Data Validation Lambda**.
3.  This Lambda validates and processes the data, saving the clean version to `s3://project-bucket/processed/`.
4.  A developer runs the `train.py` script, which loads the processed data, trains a model, and saves the artifact to `s3://project-bucket/models/`.
5.  The **Inference Lambda**'s container image is built and pushed to **ECR**.
6.  A client sends a `POST` request with new data to the **API Gateway** endpoint.
7.  API Gateway triggers the **Inference Lambda**, which loads the model from S3 and returns a prediction.
8.  All operations are logged and monitored by **CloudWatch**.
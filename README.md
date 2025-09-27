## Project Idea: Titanic Survival Prediction

The project will focus on building a machine learning system that **predicts whether a passenger survived the Titanic disaster based on their personal and travel details**, such as age, sex,  ticket class and so on. This aligns with the classic "Titanic" dataset. The system will be deployed on AWS using free-tier services, creating an end-to-end pipeline from data ingestion to a live prediction endpoint.

### Project Details

Here are the specific details for this project, following the submission template outlined in the document.

#### Team Info

- **Team Name:** TEAM 3

- **Team Leader:** Zwe Yaung Ni Tun

- **Members:** Kaung Khant Paing and Myint Myat Aung

- **GitHub Repo:**

- **Demo Video:**  

## Executive Summary

**Dataset used:** Titanic Survival

**Task type:** Binary classification

**Deployed model versions:** v1.0 - Logistic Regression

**Endpoint:** ``

**System Description:** This project implements a serverless machine learning pipeline on AWS to predict **passenger survival on the Titanic**. The system ingests raw passenger data into an S3 bucket, which triggers a Lambda function to validate, clean, and preprocess the data.

A Dockerized machine learning environment is used to train a logistic regression model. The resulting container image is stored in Amazon ECR and deployed as a Lambda function, which serves as the inference endpoint. An API Gateway provides public access to the prediction model. The entire system is designed to operate within the AWS Free Tier and emphasizes security and reproducibility.

### IAM Security Plan

| Role      | Users      | Permissions/Policies     |
|---------------|---------------|---------------|
| Team Leader | Zwe Yaung Ni Tun | `AdministratorAccess` to provide full control over all project resources. |
| Members | Kaung Khannt Paing, Myint Myat Aung | `AWSLambda_FullAccess`, `AmazonS3ReadOnlyAccess`, `CloudWatchLogsFullAccess` to allow for function deployment, data access, and log monitoring without granting excessive permissions. |
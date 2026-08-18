# Student Performance Prediction

End-to-end Data Science and Machine Learning project for predicting student math scores using a Flask web application and AWS Elastic Beanstalk.

## Project Workflow

```text
Data Ingestion
      ↓
Data Transformation
      ↓
Model Training
      ↓
Model Evaluation
      ↓
Prediction Pipeline
      ↓
Flask Web App
      ↓
GitHub
      ↓
AWS Elastic Beanstalk
```

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- CatBoost
- Flask
- HTML/CSS
- Git & GitHub
- GitHub Actions
- AWS Elastic Beanstalk
- AWS S3
- AWS IAM
- AWS CodePipeline

## Project Structure

```text
├── .ebextensions/
│   └── python.config
├── artifacts/
├── notebooks/
├── src/
│   ├── components/
│   ├── pipeline/
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
├── templates/
│   ├── index.html
│   └── home.html
├── app.py
├── requirements.txt
├── setup.py
└── README.md
```

## Run Locally

### 1. Clone Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd End-To-End-DS-Project-Implementation-With-Deployment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app.py
```

Application:

```text
http://127.0.0.1:5000
```

## AWS Elastic Beanstalk Deployment

### Configuration

Create:

```text
.ebextensions/python.config
```

```yaml
option_settings:
  "aws:elasticbeanstalk:container:python":
    WSGIPath: app:app
```

`app:app` means:

```text
app.py → Flask object named app
```

### Elastic Beanstalk Settings

```text
Application: StudentPerformance
Environment: StudentPerformance-env
Region: us-east-1
```

The deployment package should contain:

```text
app.py
requirements.txt
.ebextensions/
src/
templates/
```

## GitHub Actions Deployment

Add these repository secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Workflow file:

```text
.github/workflows/deploy.yml
```

```yaml
name: Deploy to AWS Elastic Beanstalk

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Create deployment package
        run: |
          zip -r deployment.zip . \
            -x ".git/*" ".github/*" "venv/*"

      - name: Deploy to Elastic Beanstalk
        uses: einaregilsson/beanstalk-deploy@v22
        with:
          aws_access_key: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          application_name: StudentPerformance
          environment_name: StudentPerformance-env
          version_label: ${{ github.sha }}
          region: us-east-1
          deployment_package: deployment.zip
```

### Deployment Flow

```text
git push
   ↓
GitHub Actions
   ↓
AWS Credentials
   ↓
Create deployment.zip
   ↓
S3
   ↓
Elastic Beanstalk
   ↓
StudentPerformance-env
```

## AWS CodePipeline

Alternative CI/CD flow:

```text
GitHub
   ↓
AWS CodePipeline
   ↓
Source
   ↓
Elastic Beanstalk
   ↓
StudentPerformance-env
```

### Create Pipeline

1. Open **AWS CodePipeline**.
2. Click **Create pipeline**.
3. Pipeline name:

```text
StudentPerformancePipeline
```

4. Source provider:

```text
GitHub (via GitHub App)
```

5. Select the repository and `main` branch.
6. Skip the Build stage if no build step is required.
7. Deploy provider:

```text
AWS Elastic Beanstalk
```

8. Select:

```text
Application: StudentPerformance
Environment: StudentPerformance-env
```

9. Create the pipeline.

After setup:

```text
git push
   ↓
GitHub
   ↓
CodePipeline
   ↓
Elastic Beanstalk
```

## Security

Never commit AWS credentials.

Do not add credentials to:

```text
.env
README.md
workflow YAML
source code
```

Use **GitHub Repository Secrets** for GitHub Actions.

For AWS CodePipeline, use the AWS-managed service roles.

## Important

Use **either GitHub Actions or AWS CodePipeline** as the automatic deployment method for `main` to avoid duplicate deployments.

## License

This project is for educational and demonstration purposes.

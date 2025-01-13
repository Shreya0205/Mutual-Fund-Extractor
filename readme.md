# Mutual Fund Management System

A Django-based API for managing mutual fund families and their associated schemes. 
The system allows users to register mutual fund families, retrieve a list of available mutual fund schemes.

## Features

- **User Authentication**: JWT-based authentication is used to register/login using email and password.
- **Register Mutual Fund Family**: Allows users to register a new mutual fund family.
- **List Mutual Fund Families**: Lists all registered mutual fund families.
- **Fetch Mutual Fund Schemes**: Fetches the schemes associated with a registered mutual fund family, including details like scheme name, category, and net asset value.
- **Track Schemes hourly**: Cron job to update NAV value of all schemes for registered mutual fund hourly.



## Requirements

- Python 
- Django 
- Django REST Framework
- APScheduler (for scheduling tasks)
- RapidAPIClient for fetching mutual fund schemes (mocked in tests)

## Instructions
- Create account and get rapid api key from https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav

## Database table used
### 1. MutualFundFamily 
To store registered mutual fund.
Columns are:
- mutual_fund_family 
- created_at 

### 2. MutualFundScheme
To store open-ended schemes of all registered mutual fund family. All the fields returned as response of rapid api is stored into DB.
Columns are:
- created_at 
- updated_at 
- scheme_code 
- scheme_name 
- net_asset_value 
- scheme_type 
- scheme_category 
- mutual_fund_family (FK to MutualFundFamily)
- isin_growth 
- isin_reinvestment 
- date 

### 3. MasterUser
To store registered users. It is an extension of AbstractUser class of Django.

## Prerequisites
- Python (3.6 or higher)
- Git 


## Setup
### 1. Clone the repository

```bash
git clone https://github.com/Shreya0205/Mutual-Fund-Extractor.git
cd Mutual-Fund-Extractor
```

### 2. Create a virtual environment (optional but recommended)
```bash
python3 -m venv <env_name> 
source <env_name>/bin/activate  # On Windows use .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running and Testing application

### 1. Change directory
```bash
cd mutual_fund
```

### 1. Create env file
- create .env file with vim .env
- add
```bash
RAPID_API_BASE_URL=https://latest-mutual-fund-nav.p.rapidapi.com/latest
RAPID_API_TOKEN=<rapid_api_key>
RAPID_API_HOST=latest-mutual-fund-nav.p.rapidapi.com
```
- replace rapid api key with your key

### 2. Apply database migrations
```bash
python manage.py migrate
```

### 2. Run the testcases
```bash
python manage.py test
```

### 3. Run the development server
```bash
python manage.py runserver 0:7000
```

## Accessing application
Running server will give the port on which it is running.

## API Endpoints

### Register User
- Endpoint: /users/register
- Method: POST
- Description: Register a user and return JWT refresh and access token
- Body:
```bash
{
    "email": "email@gmail.com",
    "password": "password"
}
```
- Curl Request:
```bash
curl --location 'http://127.0.0.1:7000/users/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "shreya",
    "email": "email@gmail.com",
    "password": "password"
}'
```
- Response:
  - 201 Created on successful registration. 
  - 400 Bad Request if user already present, or field is missing.


### Login User
- Endpoint: /users/login
- Method: POST
- Description: Used for login a user and return JWT token
- Body:
```bash
{
    "email": "email@gmail.com",
    "password": "password"
}
```
- Curl Request:
```bash
curl --location 'http://127.0.0.1:7000/users/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "email@gmail.com",
    "password": "password"
}'
```
- Response:
  - 200 Created on successful login
  ```bash
  {
    "refresh": "xxxx"
    "access": "xxxx"
  }
  ```
  - 401 Invalid credentials, when user is not registered.

### Register a mutual fund family
- Endpoint: /funds/mutual-fund-families
- Method: POST
- Description: Register a mutual fund open-ended scheme family
- Authorization: Use access token from login API as bearer token (Authorization tab) in Postman
- PLEASE NOTE: 
- Body:
```bash
{
    "mutual_fund_family": "HDFC Mutual Fund"
}
```
- Curl Request:
```bash
curl --location 'http://127.0.0.1:7000/funds/mutual-fund-families/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer xxxx' \
--data '{
    "mutual_fund_family": "HDFC Mutual Fund"
}'
```
- Response:
  - 201 Created on successful registration of mutual fund. 
  - 400 Bad Request if mutual fund family is already registered.
  - 401 Unauthorised when access token is not provided
  - 404 when no open ended scheme found for the family. Mutual fund family will not be registered.


### List all mutual fund family
- Endpoint: /funds/mutual-fund-families
- Method: GET
- Description: List registered mutual fund families
- Authorization: Use access token from login API as bearer token (Authorization tab) in Postman
- Curl Request:
```bash
curl --location 'http://localhost:7000/funds/mutual-fund-families/' \
--header 'Authorization: Bearer xxxx' \
```
- Response:
  - 200 list of all families 
  ```bash
      [
        {
          "id": 1,
          "mutual_fund_family": "HDFC Mutual Fund",
          "created_at": "2025-01-11T12:17:45.617624Z"
        }
      ]
  ```
  - 401 Unauthorised when access token is not provided

### List all mutual fund open ended scheme for a family
- Endpoint: /funds/mutual-fund-families
- Method: GET
- Description: 
  - List of all open ended scheme for given family
  - The API result will keep on updating every hour with the help of schedular task which runs every hour which fetches latest data of open-ended schemes of registered mutual fund from rapidAPI.
- Authorization: Use access token from login API as bearer token (Authorization tab) in Postman
- Query params:
```bash
mutual_fund_family=HDFC Mutual Fund
```
- Curl Request:
```bash
curl --location 'http://localhost:7000/funds/mutual-fund-families/schemes/?mutual_fund_family=HDFC%20Mutual%20Fund' \
--header 'Authorization: Bearer xxxx' \
```
- Response:
  - 200 list of mutual fund schemes.
  ```bash
  [
    {
        "created_at": "2025-01-12T10:00:14.118030Z",
        "updated_at": "2025-01-12T10:00:14.118036Z",
        "scheme_code": "128628",
        "scheme_name": "HDFC Banking and PSU Debt Fund - Growth Option",
        "net_asset_value": 22.0467,
        "scheme_type": "Open Ended Schemes",
        "scheme_category": "Debt Scheme - Banking and PSU Fund",
        "date": "2025-01-10",
        "isin_growth": "INF179KA1JC4",
        "isin_reinvestment": "-"
    },
  ]
  ```
  - 401 Unauthorised when access token is not provided
  - 404 Mutual Fund family not registered

## Cron Job for Periodic Updates

### Overview
In this project, APScheduler is used to manage periodic tasks, specifically for updating mutual fund schemes. The task is scheduled to run every hour after the application is started.

### How It Works
- Scheduled Task: The Cron job is set up to trigger a script at specific time intervals (e.g., every hour when the app is running) to execute the update_mutual_fund_schemes function.
- Fetching Data: The function fetches the latest mutual fund scheme data from rapid API using the MutualFundService.fetch_open_ended_schemes_for_family() method.
- Saving to Database: If the data is successfully retrieved, it is saved to the database using the MutualFundService.save_schemes_to_db() method.
- Logging: Detailed logs are maintained for every successful update or failure in mutual_fund/logs/scheduler_logs.log, which can be monitored to ensure the system is working as expected.
- Example logs:
  ```bash
    DEBUG 2025-01-12 19:25:47,369 base Next wakeup is due at 2025-01-12 19:25:47.533384+00:00 (in 0.164351 seconds)
    DEBUG 2025-01-12 19:25:47,537 base Looking for jobs to run
    INFO 2025-01-12 19:25:47,540 base Running job "update_mutual_fund_schemes (trigger: interval[1:00:00], next run at: 2025-01-12 19:25:47 UTC)" (scheduled at 2025-01-12 19:25:47.533384+00:00)
    DEBUG 2025-01-12 19:25:47,540 base Next wakeup is due at 2025-01-12 20:25:47.533384+00:00 (in 3599.992479 seconds)
    INFO 2025-01-12 19:25:48,291 base Job "update_mutual_fund_schemes (trigger: interval[1:00:00], next run at: 2025-01-12 20:25:47 UTC)" executed successfully
    INFO 2025-01-12 19:25:48,454 base Job "update_mutual_fund_schemes (trigger: interval[1:00:00], next run at: 2025-01-12 20:25:47 UTC)" executed successfully
  ```

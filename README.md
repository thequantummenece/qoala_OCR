# Thai ID OCR

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Advanced Features](#advanced-features)
- [Hosting](#hosting)
- [License](#license)

## About

[Qoala_OCR] is a web application designed to analyze Thai ID cards using Optical Character Recognition (OCR). The app integrates with the Google Vision API for OCR processing, extracts relevant data, and stores the results in a chosen database. Additionally, it provides a user-friendly interface for uploading ID card images, displaying OCR data, and managing records.

## Features

- Optical Character Recognition (OCR) processing of Thai ID cards.
- Data extraction and structuring for key information such as ID number, name, last name, date of birth, date of issue, and date of expiry.
- User interface for uploading Thai ID card images in various formats.
- CRUD API endpoints for creating, updating, retrieving, and deleting OCR records.
- Integration with a chosen database for storing OCR data.
- Error handling for unreadable or unclear ID cards.
- Unit test cases, code comments, and sample JSON output.
- Advanced features such as filtering OCR data and handling soft deletes.

## Tech Stack

- **Programming Language:** [PYTHON]
- **Web Framework:** [Flask]
- **OCR Solution:** [Google Vision API]
- **Database:** [Mysql | supabase]
- **Hosting:** [Render]
- **Project URL** <a href = "https://aabsurdymakesqoalaproject.onrender.com">[https://aabsurdymakesqoalaproject.onrender.com]</a>

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/thequantummenece/qoala_OCR.git
cd qoala_OCR
```

2.Install dependencies: 
```bash
alembic==1.13.1
annotated-types==0.6.0
anyio==4.2.0
blinker==1.7.0
cachetools==5.3.2
certifi==2023.11.17
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
deprecation==2.1.0
Flask==3.0.0
Flask-Migrate==4.0.5
Flask-SQLAlchemy==3.1.1
google-api-core==2.15.0
google-auth==2.25.2
google-cloud-vision==3.5.0
googleapis-common-protos==1.62.0
gotrue==2.1.0
greenlet==3.0.3
grpcio==1.60.0
grpcio-status==1.60.0
h11==0.14.0
httpcore==0.17.3
httpx==0.24.1
idna==3.6
itsdangerous==2.1.2
Jinja2==3.1.2
Mako==1.3.0
MarkupSafe==2.1.3
mysql-connector-python==8.2.0
packaging==23.2
postgrest==0.13.0
proto-plus==1.23.0
protobuf==4.21.12
pyasn1==0.5.1
pyasn1-modules==0.3.0
pydantic==2.5.3
pydantic_core==2.14.6
python-dateutil==2.8.2
realtime==1.0.2
requests==2.31.0
rsa==4.9
six==1.16.0
sniffio==1.3.0
SQLAlchemy==2.0.23
storage3==0.7.0
StrEnum==0.4.15
supabase==2.3.0
supafunc==0.3.1
typing_extensions==4.9.0
urllib3==2.1.0
websockets==11.0.3
Werkzeug==3.0.1
gunicorn==21.2.0
```


3.Run the application: 
```bash
flask --app app run
```

## Usage
1.Open the application in your web browser.

2.Upload a Thai ID card image using the provided interface.

3.View the OCR data, including key information extracted from the ID card.

4.Explore CRUD functionalities via the API endpoints.

## Api Endpoints

1. Create a New OCR Record: /api/create
1. Update Existing OCR Data: /api/update/:id
1. Retrieve and Display OCR Data: /api/ocr-data
1. Delete OCR Records: /api/delete/:id

## Advanced Features
- Error Handling: The application handles unreadable or unclear ID cards gracefully, providing meaningful error messages.

- Unit Test Cases: The code includes unit test cases to ensure the reliability of the application.

- Code Comments: The code is well-documented with comments for improved readability.

## Hosting
The application is hosted on render (<a href = "https://aabsurdymakesqoalaproject.onrender.com"> https://aabsurdymakesqoalaproject.onrender.com </a> ).

## License
This project is licensed under the MIT License.



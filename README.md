# Thai ID OCR

![Project Logo](link-to-your-logo.png)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Advanced Features](#advanced-features)
- [Hosting](#hosting)
- [Contributing](#contributing)
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

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/thequantummenece/qoala_OCR.git
cd qoala_OCR

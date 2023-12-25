from flask import Flask, render_template, request, jsonify
import os
import re
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from supabase import create_client
from datetime import datetime

app = Flask(__name__)

# Configure Supabase
SUPABASE_URL = 'https://cborceqktamiafwiaodn.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNib3JjZXFrdGFtaWFmd2lhb2RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM1MjM2NjgsImV4cCI6MjAxOTA5OTY2OH0.qojQGVJdvAAEVBEB5nYiMaGgXWDMeHaJPCWeSFp-U7I'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Ensure the Supabase table exists
OCR_RECORDS_TABLE = 'ocr_records'
supabase.table(OCR_RECORDS_TABLE).upsert([
    {'id': 1, 'identification_number': '', 'name': '', 'last_name': '', 'date_of_birth': '',
     'date_of_issue': '', 'date_of_expiry': '', 'timestamp': '', 'status': '', 'error_message': ''}
])


@app.route('/',methods = ['GET','POST'])
def home():
    return render_template('index.html')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "qoala-409117-a9532ba30b5d.json"

def process_image(file_path):
    client = vision_v1.ImageAnnotatorClient()

    with open(file_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    try:
        response = client.text_detection(image=image)
        if response.text_annotations:
            return response.text_annotations[0].description
        else:
            return None
    except Exception as e:
        return None

UPLOAD_FOLDER = 'C:/Users/aades/PycharmProjects/qoala/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET','POST'])
def upload_image():
    # print("hello world",flush=True)
    if 'file' not in request.files:
        return jsonify({"status": "failure", "message": "No file provided"})
    file = request.files['file']

    # print(file)
    if file.filename == '':
        return jsonify({"status": "failure", "message": "No file selected"})

    if file:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # print(file_path)
        file.save(file_path)

        ocr_result = process_image(file_path)
        # print(ocr_result)

        if ocr_result:

            # Define regular expressions
            id_number_regex = re.compile(r"(\d\s\d{4}\s\d{5}\s\d{2}\s\d)")
            name_regex = re.compile(r"Name (.+)")
            last_name_regex = re.compile(r"Last name (.+)")
            dob_regex = re.compile(r"Date of Birth (\d{1,2} [A-Za-z]+\. \d{4})")
            issue_date_regex = re.compile(r"(\d{1,2} [A-Za-z]+\. \d{4})[\n\s]+Date of Issue")
            expiry_date_regex = re.compile(r"(\d{1,2} [A-Za-z]+\. \d{4})[\n\s]+Date of Expiry")

            # Extract information using regular expressions with null checks
            id_number_match = id_number_regex.search(ocr_result)
            name_match = name_regex.search(ocr_result)
            last_name_match = last_name_regex.search(ocr_result)
            dob_match = dob_regex.search(ocr_result)
            issue_date_match = issue_date_regex.search(ocr_result)
            expiry_date_match = expiry_date_regex.search(ocr_result)

            # Define matches
            matches = [
                id_number_match,
                name_match,
                last_name_match,
                dob_match,
                issue_date_match,
                expiry_date_match,
            ]

            # Count the non-null matches
            non_null_matches = [match for match in matches if match is not None]

            # Calculate the percentage
            percentage_success = (len(non_null_matches) / len(matches)) * 100

            # Return extracted information
            OCR_parsed = {
                "identification_number": id_number_match.group(1) if id_number_match else "Not found",
                "name": name_match.group(1) if name_match else "Not found",
                "last_name": last_name_match.group(1) if last_name_match else "Not found",
                "date-of-birth": dob_match.group(1) if dob_match else "Not found",
                "date-of-issue": issue_date_match.group(1) if issue_date_match else "Not found",
                "date-of-expiry": expiry_date_match.group(1) if expiry_date_match else "Not found",
                "percentageSuccess": percentage_success,
                "rawData": ocr_result
            }

            OCR_parsed_refactored ={
                "identification_number": id_number_match.group(1) if id_number_match else "Not found",
                "name": name_match.group(1) if name_match else "Not found",
                "last_name": last_name_match.group(1) if last_name_match else "Not found",
                "date-of-birth": dob_match.group(1) if dob_match else "Not found",
                "date-of-issue": issue_date_match.group(1) if issue_date_match else "Not found",
                "date-of-expiry": expiry_date_match.group(1) if expiry_date_match else "Not found",
            }

            # print(OCR_parsed)


            identification_number = OCR_parsed["identification_number"]
            name = OCR_parsed["name"]
            last_name = OCR_parsed["last_name"]
            date_of_birth = OCR_parsed["date-of-birth"]
            date_of_issue = OCR_parsed["date-of-issue"]
            date_of_expiry = OCR_parsed["date-of-expiry"]

            # Insert the record into the Supabase table
            success, error_message = insert_record_into_supabase(
                identification_number, name, last_name, date_of_birth,
                date_of_issue, date_of_expiry, "success"
            )
            if success:
                return render_template('success.html', data=OCR_parsed_refactored)
            else:
                return jsonify(
                    {"status": "failure", "message": f"Failed to insert record into Supabase: {error_message}"})
        else:
            return jsonify({"status": "failure", "message": "Unable to extract text from the image"})

def insert_record_into_supabase(identification_number, name, last_name, date_of_birth,
                                date_of_issue, date_of_expiry, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        'identification_number': identification_number,
        'name': name,
        'last_name': last_name,
        'date_of_birth': date_of_birth,
        'date_of_issue': date_of_issue,
        'date_of_expiry': date_of_expiry,
        'timestamp': timestamp,
        'status': status,
        'error_message': '',
    }
    try:
        data,count = supabase.table(OCR_RECORDS_TABLE).insert(data).execute()
        return True, None
    except Exception as error:
        return False,str(error)


# Add a new route for the success page
@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


@app.route('/ocr-data', methods=['GET'])
def get_ocr_data():
    response = supabase.table(OCR_RECORDS_TABLE).select("*").execute()
    ocr_records = response.data if response.data else []

    result = []
    for record in ocr_records:
        result.append({
            "identification_number": record.get('identification_number', ''),
            "name": record.get('name', ''),
            "last_name": record.get('last_name', ''),
            "date_of_birth": record.get('date_of_birth', ''),
            "date_of_issue": record.get('date_of_issue', ''),
            "date_of_expiry": record.get('date_of_expiry', ''),
            "timestamp": record.get('timestamp', ''),
            "status": record.get('status', ''),
            "error_message": record.get('error_message', '')
        })

    return jsonify(result)

@app.route('/update-ocr/<int:id>', methods=['PUT'])
def update_ocr_data(id):
    # Assume you have a JSON payload with updated data in the request
    updated_data = request.json

    response, error = supabase.table(OCR_RECORDS_TABLE).update(updated_data).eq("id",id).execute()
    if error:
        return jsonify({"status": "failure", "message": f"Failed to update record in Supabase: {error}"})
    else:
        return jsonify({"status": "success", "message": f"OCR record {id} updated successfully"})

@app.route('/delete-ocr/<int:id>', methods=['DELETE'])
def delete_ocr_data(id):
    response, error = supabase.table(OCR_RECORDS_TABLE).delete().eq("id",id).execute()
    if error:
        return jsonify({"status": "failure", "message": f"Failed to delete record in Supabase: {error}"})
    else:
        return jsonify({"status": "success", "message": f"OCR record {id} deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)

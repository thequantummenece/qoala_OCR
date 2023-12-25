from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os,io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:(Aady24)@localhost/qoala_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class OCRRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identification_number = db.Column(db.String(20))
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(10))
    date_of_issue = db.Column(db.String(10))
    date_of_expiry = db.Column(db.String(10))
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    status = db.Column(db.String(10))
    error_message = db.Column(db.String(255))

with app.app_context():
    db.create_all()

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
    print("hello world",flush=True)
    if 'file' not in request.files:
        return jsonify({"status": "failure", "message": "No file provided"})
    file = request.files['file']

    print(file)
    if file.filename == '':
        return jsonify({"status": "failure", "message": "No file selected"})

    if file:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(file_path)
        file.save(file_path)

        ocr_result = process_image(file_path)

        if ocr_result:
            identification_number = "123456789"
            name = "John"
            last_name = "Doe"
            date_of_birth = "01/01/1990"
            date_of_issue = "01/01/2022"
            date_of_expiry = "01/01/2030"

            new_record = OCRRecord(
                identification_number=identification_number,
                name=name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                date_of_issue=date_of_issue,
                date_of_expiry=date_of_expiry,
                status="success"
            )

            db.session.add(new_record)
            db.session.commit()

            return jsonify({"status": "success", "message": "OCR processed successfully"})
        else:
            return jsonify({"status": "failure", "message": "Unable to extract text from the image"})

@app.route('/ocr-data', methods=['GET'])
def get_ocr_data():
    ocr_records = OCRRecord.query.all()
    result = []

    for record in ocr_records:
        result.append({
            "identification_number": record.identification_number,
            "name": record.name,
            "last_name": record.last_name,
            "date_of_birth": record.date_of_birth,
            "date_of_issue": record.date_of_issue,
            "date_of_expiry": record.date_of_expiry,
            "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": record.status,
            "error_message": record.error_message
        })

    return jsonify(result)

@app.route('/update-ocr/<int:id>', methods=['PUT'])
def update_ocr_data(id):
    record = OCRRecord.query.get(id)

    if record:
        db.session.commit()

        return jsonify({"status": "success", "message": f"OCR record {id} updated successfully"})
    else:
        return jsonify({"status": "failure", "message": f"OCR record {id} not found"})

@app.route('/delete-ocr/<int:id>', methods=['DELETE'])
def delete_ocr_data(id):
    record = OCRRecord.query.get(id)

    if record:
        record.status = "deleted"
        db.session.commit()

        return jsonify({"status": "success", "message": f"OCR record {id} deleted successfully"})
    else:
        return jsonify({"status": "failure", "message": f"OCR record {id} not found"})

if __name__ == '__main__':
    app.run(debug=True)

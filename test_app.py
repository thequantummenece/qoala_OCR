import unittest
from app import app, db, OCRRecord, process_image

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        # Create the application context
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop all tables at the end of the test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_upload_image(self):
        # Mock image upload (replace with your image path)
        image_path = 'sample.jpg'

        # Use Flask test client to simulate file upload
        response = self.app.post('/upload', data={'file': (open(image_path, 'rb'), 'sample.jpg')})
        data = response.get_json()

        # Check if the response contains the expected keys
        self.assertIn('status', data)
        self.assertIn('message', data)

        # Check if the status is success
        self.assertEqual(data['status'], 'success')

        # Check if the OCR record is added to the database
        with app.app_context():
            ocr_record = OCRRecord.query.first()
            self.assertIsNotNone(ocr_record)
            self.assertEqual(ocr_record.status, 'success')

if __name__ == '__main__':
    unittest.main()

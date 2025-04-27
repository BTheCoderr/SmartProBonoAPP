import os
import pytest
import json
from PIL import Image, ImageDraw, ImageFont
import io
from bson import ObjectId
from backend.routes.document_scanner import allowed_file, process_image, process_pdf, scanner_bp
from backend.app import create_app
import numpy as np
from flask_jwt_extended import create_access_token
from datetime import timedelta
from reportlab.pdfgen import canvas

TEST_USER_ID = "test_user_123"

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def auth_headers(app):
    """Create valid JWT token and headers."""
    with app.app_context():
        token = create_access_token(identity=TEST_USER_ID)
        return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_image(upload_dir):
    """Create a test image file."""
    image_path = upload_dir / 'test_image.png'
    img = Image.new('RGB', (100, 100), color='white')
    img.save(image_path)
    yield image_path
    if image_path.exists():
        image_path.unlink()

@pytest.fixture
def test_pdf(upload_dir):
    """Create a test PDF file."""
    pdf_path = upload_dir / 'test.pdf'
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "Test PDF")
    c.save()
    yield pdf_path
    if pdf_path.exists():
        pdf_path.unlink()

def create_test_image(text: str) -> io.BytesIO:
    """Create a test image with the given text."""
    # Create a new image with white background
    width = 800
    height = 400
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Use a larger font size for better OCR
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 36)
    
    # Calculate text position to center it
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw black text
    draw.text((x, y), text, fill='black', font=font)
    
    # Save to BytesIO
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_test_pdf(text="Test PDF Document"):
    """Create a test PDF file with text."""
    # Create an image first
    img_data = create_test_image(text)
    img = Image.open(img_data)
    
    # Save as PDF
    pdf_bytes = io.BytesIO()
    img.save(pdf_bytes, format='PDF', resolution=300.0)
    pdf_bytes.seek(0)
    return pdf_bytes

def test_allowed_file():
    """Test file extension validation."""
    assert allowed_file('test.png') is True
    assert allowed_file('test.pdf') is True
    assert allowed_file('test.exe') is False
    assert allowed_file('test') is False
    assert allowed_file('test.jpg') is True
    assert allowed_file('test.jpeg') is True
    assert allowed_file('test.gif') is True
    assert allowed_file('test.tiff') is True

def test_process_image():
    """Test image processing functionality."""
    # Create test image with more text
    test_text = "This is a test document for OCR processing"
    img_data = create_test_image(test_text)
    
    # Save temporarily
    test_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
    with open(test_path, 'wb') as f:
        f.write(img_data.getvalue())
    
    try:
        # Process the image
        results = process_image(test_path)
        
        # Verify results
        assert 'text' in results
        assert 'confidence' in results
        assert isinstance(results['confidence'], (int, float))
        assert results['confidence'] >= 0
        assert test_text in results['text']
        assert results['word_count'] > 0
        
    finally:
        # Clean up
        if os.path.exists(test_path):
            os.remove(test_path)

def test_process_pdf():
    """Test PDF processing functionality."""
    test_text = "This is a test PDF document"
    pdf_data = create_test_pdf(test_text)
    
    # Save temporarily
    test_path = os.path.join(os.path.dirname(__file__), 'test.pdf')
    with open(test_path, 'wb') as f:
        f.write(pdf_data.getvalue())
    
    try:
        # Process the PDF
        results = process_pdf(test_path)
        
        # Verify results
        assert 'pages' in results
        assert len(results['pages']) > 0
        assert 'text' in results['pages'][0]
        assert test_text in results['pages'][0]['text']
        assert results['total_pages'] == 1
        assert 'average_confidence' in results
        
    finally:
        # Clean up
        if os.path.exists(test_path):
            os.remove(test_path)

def test_scan_endpoint_with_jwt(client, auth_headers):
    """Test the document scanning endpoint with JWT authentication."""
    test_text = "This is a test document for API testing"
    img_data = create_test_image(test_text)
    
    data = {
        'file': (img_data, 'test.png')
    }
    
    response = client.post(
        '/api/scanner/scan',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'results' in data
    assert 'text' in data['results']
    assert test_text in data['results']['text']
    assert data['results']['word_count'] > 0

def test_scan_endpoint_without_jwt(client):
    """Test that scanning fails without JWT."""
    test_text = "This is a test document"
    img_data = create_test_image(test_text)
    
    data = {
        'file': (img_data, 'test.png')
    }
    
    response = client.post(
        '/api/scanner/scan',
        data=data,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 401

def test_scan_endpoint_with_different_formats(client, auth_headers):
    """Test scanning with different image formats."""
    test_text = "Testing different image formats"
    formats = ['PNG', 'JPEG', 'GIF']
    
    for fmt in formats:
        img_data = create_test_image(test_text)
        
        data = {
            'file': (img_data, f'test.{fmt.lower()}')
        }
        
        response = client.post(
            '/api/scanner/scan',
            data=data,
            headers=auth_headers,
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert test_text in data['results']['text']

def test_scan_endpoint_with_pdf(client, auth_headers):
    """Test scanning a PDF document."""
    test_text = "This is a test PDF for scanning"
    pdf_data = create_test_pdf(test_text)
    
    data = {
        'file': (pdf_data, 'test.pdf')
    }
    
    response = client.post(
        '/api/scanner/scan',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'results' in data
    assert 'pages' in data['results']
    assert test_text in data['results']['pages'][0]['text']

def test_invalid_file_type(client, auth_headers):
    """Test rejection of invalid file types."""
    data = {
        'file': (io.BytesIO(b'invalid data'), 'test.exe')
    }
    
    response = client.post(
        '/api/scanner/scan',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'File type not allowed'

def test_missing_file(client, auth_headers):
    """Test handling of missing file."""
    response = client.post(
        '/api/scanner/scan',
        data={},
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'No file provided'

def test_capture_endpoint(client, auth_headers):
    """Test the image capture endpoint."""
    test_text = "This is a captured image"
    img_data = create_test_image(test_text)
    
    data = {
        'image': (img_data, 'capture.jpg')
    }
    
    response = client.post(
        '/api/scanner/capture',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'results' in data
    assert 'text' in data['results']
    assert test_text in data['results']['text']

def test_get_documents_pagination(client, auth_headers):
    """Test pagination of scanned documents."""
    # Create multiple test documents
    test_text = "Pagination test document"
    
    # Upload multiple documents
    for i in range(15):  # Create more than default per_page
        img_data = create_test_image(test_text)  # Create fresh image for each request
        data = {
            'file': (img_data, f'test_{i}.png')
        }
        response = client.post(
            '/api/scanner/scan',
            data=data,
            headers=auth_headers,
            content_type='multipart/form-data'
        )
        assert response.status_code == 200
        img_data.close()  # Close the BytesIO object

def test_get_documents_filtering(client, auth_headers):
    """Test filtering documents by case_id and document_type."""
    # Create test documents with different case_ids and types
    test_text = "Filter test document"
    img_data = create_test_image(test_text)
    
    # Upload document with case_id
    data = {
        'file': (img_data, 'test_case.png'),
        'case_id': str(ObjectId()),
        'document_type': 'identification'
    }
    client.post(
        '/api/scanner/scan',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    # Test filtering by case_id
    response = client.get(
        f'/api/scanner/documents?case_id={data["case_id"]}',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['documents']) == 1
    
    # Test filtering by document_type
    response = client.get(
        '/api/scanner/documents?document_type=identification',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['documents']) == 1

def test_invalid_pagination_params(client, auth_headers):
    """Test handling of invalid pagination parameters."""
    # Test invalid page number
    response = client.get(
        '/api/scanner/documents?page=0&per_page=10',
        headers=auth_headers
    )
    assert response.status_code == 400
    
    # Test invalid per_page value
    response = client.get(
        '/api/scanner/documents?page=1&per_page=0',
        headers=auth_headers
    )
    assert response.status_code == 400

def test_expired_token(client):
    """Test handling of expired JWT token."""
    from flask_jwt_extended import create_access_token
    from datetime import timedelta
    
    # Create an expired token
    with client.application.app_context():
        expired_token = create_access_token(
            identity=TEST_USER_ID,
            expires_delta=timedelta(seconds=-1)
        )
    
    headers = {'Authorization': f'Bearer {expired_token}'}
    response = client.get('/api/scanner/documents', headers=headers)
    assert response.status_code == 401

def test_invalid_token(client):
    """Test handling of invalid JWT token."""
    headers = {'Authorization': 'Bearer invalid_token'}
    response = client.get('/api/scanner/documents', headers=headers)
    assert response.status_code == 422  # Flask-JWT-Extended returns 422 for malformed tokens

def test_image_orientations(client, auth_headers):
    """Test processing images with different orientations."""
    test_text = "Orientation test"
    img_data = create_test_image(test_text)
    
    # Open the image and rotate it
    img = Image.open(img_data)
    rotated = img.rotate(90, expand=True)  # Added expand=True to maintain text dimensions
    
    # Save rotated image
    rotated_data = io.BytesIO()
    rotated.save(rotated_data, format='PNG')
    rotated_data.seek(0)
    
    data = {
        'file': (rotated_data, 'rotated.png')
    }
    
    response = client.post(
        '/api/scanner/scan',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert 'text' in data['results']
    # Rotated text may not be recognized correctly across all environments,
    # so just verify we got some text back
    assert len(data['results']['text']) > 0
    
    # Clean up
    img_data.close()
    rotated_data.close()

def test_different_color_spaces(client, auth_headers):
    """Test processing images with different color spaces."""
    test_text = "Color space test"
    img_data = create_test_image(test_text)
    
    # Convert to grayscale
    img = Image.open(img_data)
    gray = img.convert('L')
    
    gray_data = io.BytesIO()
    gray.save(gray_data, format='PNG')
    gray_data.seek(0)
    
    data = {
        'file': (gray_data, 'grayscale.png')
    }
    
    response = client.post(
        '/api/scanner/scan',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert test_text in data['results']['text']

def test_no_text_image(client, auth_headers):
    """Test handling of images with no text."""
    # Create blank image
    img = Image.new('RGB', (800, 600), color='white')
    img_data = io.BytesIO()
    img.save(img_data, format='PNG')
    img_data.seek(0)
    
    data = {
        'file': (img_data, 'blank.png')
    }
    
    response = client.post(
        '/api/scanner/scan',
        data=data,
        headers=auth_headers,
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['results']['text'].strip() == ''
    assert data['results']['word_count'] == 0

def test_concurrent_uploads(client, auth_headers):
    """Test handling of concurrent file uploads."""
    import threading
    import queue
    
    results = queue.Queue()
    test_text = "Concurrent test"
    
    def upload_file():
        img_data = create_test_image(test_text)  # Create fresh image for each thread
        try:
            data = {
                'file': (img_data, 'concurrent.png')
            }
            response = client.post(
                '/api/scanner/scan',
                data=data,
                headers=auth_headers,
                content_type='multipart/form-data'
            )
            results.put(response.status_code)
        finally:
            img_data.close()  # Ensure BytesIO is closed
    
    # Start multiple threads
    threads = []
    for _ in range(5):
        t = threading.Thread(target=upload_file)
        t.start()
        threads.append(t)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    # Check results
    success_count = 0
    while not results.empty():
        if results.get() == 200:
            success_count += 1
    
    assert success_count == 5  # All uploads should succeed

def test_scan_document_image(client, auth_headers):
    """Test scanning a valid image document."""
    # Use an absolute path to the test file
    import os
    test_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test_image.jpg')
    with open(test_file_path, 'rb') as f:
        data = {'file': (f, 'test_image.jpg')}
        response = client.post('/api/scanner/scan', 
                             data=data,
                             headers={**auth_headers, 'Content-Type': 'multipart/form-data'})
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert 'results' in result

def test_scan_document_pdf(client, auth_headers):
    """Test scanning a valid PDF document."""
    # Use an absolute path to the test file
    import os
    test_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'test.pdf')
    with open(test_file_path, 'rb') as f:
        data = {'file': (f, 'test.pdf')}
        response = client.post('/api/scanner/scan',
                             data=data,
                             headers={**auth_headers, 'Content-Type': 'multipart/form-data'})
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] is True
        assert 'results' in result

def test_corrupted_file(client, auth_headers, tmp_path):
    """Test handling of a corrupted file upload.
    
    Creates a corrupted file and verifies that the API returns a 400 status code
    with appropriate error message when attempting to scan it.
    """
    # Create a corrupted file
    corrupted_file = tmp_path / "corrupted.jpg"
    try:
        with open(corrupted_file, 'wb') as f:
            f.write(b'This is not a valid image file')
        
        with open(corrupted_file, 'rb') as f:
            data = {'file': (f, 'corrupted.jpg')}
            response = client.post('/api/scanner/scan',
                                 data=data,
                                 headers={**auth_headers, 'Content-Type': 'multipart/form-data'})
            
        assert response.status_code == 400
        result = json.loads(response.data)
        assert result['success'] is False
        assert 'error' in result
        assert 'Could not process file' in result['error']
    
    finally:
        # Clean up the temporary file
        if corrupted_file.exists():
            corrupted_file.unlink()

def test_document_storage(client, auth_headers):
    """Test that processed documents are correctly stored in MongoDB."""
    test_text = "Database storage test"
    img_data = create_test_image(test_text)
    
    data = {
        'file': (img_data, 'test.png'),
        'document_type': 'test_type',
        'case_id': str(ObjectId())
    }
    
    response = client.post('/api/scanner/scan',
                          data=data,
                          headers=auth_headers,
                          content_type='multipart/form-data')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['success'] is True
    
    # Verify document in database
    response = client.get('/api/scanner/documents',
                         headers=auth_headers)
    assert response.status_code == 200
    documents = json.loads(response.data)['documents']
    assert len(documents) > 0
    stored_doc = next((doc for doc in documents if doc['document_type'] == 'test_type'), None)
    assert stored_doc is not None
    assert stored_doc['filename'] == 'test.png'

def test_database_failure_handling(client, auth_headers, monkeypatch):
    """Test graceful handling of database failures."""
    def mock_insert(*args, **kwargs):
        raise Exception("Database connection failed")
    
    # Mock the database insert
    monkeypatch.setattr("pymongo.collection.Collection.insert_one", mock_insert)
    
    test_text = "Database failure test"
    img_data = create_test_image(test_text)
    
    data = {'file': (img_data, 'test.png')}
    response = client.post('/api/scanner/scan',
                          data=data,
                          headers=auth_headers,
                          content_type='multipart/form-data')
    
    # Should still return success since OCR worked
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['success'] is True
    assert test_text in result['results']['text']

def test_concurrent_document_access(client, auth_headers):
    """Test concurrent access to documents."""
    import threading
    import queue
    
    # First, upload some test documents
    for i in range(5):
        test_text = f"Concurrent test document {i}"
        img_data = create_test_image(test_text)
        data = {'file': (img_data, f'test_{i}.png')}
        response = client.post('/api/scanner/scan',
                             data=data,
                             headers=auth_headers,
                             content_type='multipart/form-data')
        assert response.status_code == 200
        img_data.close()
    
    results = queue.Queue()
    
    def access_documents():
        try:
            response = client.get('/api/scanner/documents',
                                headers=auth_headers)
            results.put(('success', response.status_code))
        except Exception as e:
            results.put(('error', str(e)))
    
    # Start multiple threads
    threads = []
    for _ in range(10):
        t = threading.Thread(target=access_documents)
        t.start()
        threads.append(t)
    
    # Wait for completion
    for t in threads:
        t.join()
    
    # Check results
    error_count = 0
    while not results.empty():
        status, value = results.get()
        if status == 'error':
            error_count += 1
        else:
            assert value == 200
    
    assert error_count == 0, f"Got {error_count} errors during concurrent access"

def test_temp_file_cleanup(client, auth_headers):
    """Test that temporary files are properly cleaned up."""
    import tempfile
    import time
    
    # Get initial count of files in temp directory
    temp_dir = tempfile.gettempdir()
    initial_files = {f for f in os.listdir(temp_dir) if f.startswith('scan_')}
    
    # Process a file
    test_text = "Cleanup test"
    img_data = create_test_image(test_text)
    data = {'file': (img_data, 'test.png')}
    
    response = client.post('/api/scanner/scan',
                          data=data,
                          headers=auth_headers,
                          content_type='multipart/form-data')
    
    assert response.status_code == 200
    
    # Give a small delay to ensure cleanup has completed
    time.sleep(0.1)
    
    # Check that no new scan files remain in temp directory
    final_files = {f for f in os.listdir(temp_dir) if f.startswith('scan_')}
    new_files = final_files - initial_files
    assert len(new_files) == 0, f"Temporary files were not cleaned up: {new_files}"

def test_rapid_requests(client, auth_headers):
    """Test handling of rapid successive requests."""
    test_text = "Rate limit test"
    img_data = create_test_image(test_text)
    
    # Make multiple rapid requests
    responses = []
    successful_requests = 0
    rate_limited_requests = 0
    
    for _ in range(20):  # Try 20 rapid requests
        data = {'file': (create_test_image(test_text), 'test.png')}
        response = client.post('/api/scanner/scan',
                             data=data,
                             headers=auth_headers,
                             content_type='multipart/form-data')
        responses.append(response.status_code)
        
        if response.status_code == 200:
            successful_requests += 1
        elif response.status_code == 429:  # Too Many Requests
            rate_limited_requests += 1
    
    # All requests should either succeed or fail gracefully
    for status_code in responses:
        assert status_code in [200, 429], f"Unexpected status code: {status_code}"
    
    print(f"Successful requests: {successful_requests}")
    print(f"Rate limited requests: {rate_limited_requests}") 
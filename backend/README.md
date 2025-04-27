## OCR Document Scanning

The API now supports document scanning and OCR (Optical Character Recognition) via the following endpoint:

### Scan Document

```
POST /api/documents/scan
```

**Description**: Process an uploaded document image using OCR to extract text and structured data.

**Request**:
- Content-Type: `multipart/form-data`
- Body:
  - `file`: The image file to scan (required)
  - `documentType`: Type of document to process (optional, default: 'general')
    - Options: 'general', 'identification', 'immigration', 'legal'
  - `userId`: Optional user ID to associate with the document

**Response**:
```json
{
  "success": true,
  "extractedText": "Full text extracted from the document...",
  "extractedData": {
    "field1": "value1",
    "field2": "value2",
    ...
  },
  "fileUrl": "https://example.com/path/to/file.jpg",
  "fileId": "unique-file-id",
  "publicId": "cloudinary-public-id",
  "timestamp": "2023-01-01T12:00:00.000Z",
  "documentType": "general"
}
```

**Error Response**:
```json
{
  "error": "Error message"
}
```

## Setup OCR

To use the document scanning functionality, you need to install Tesseract OCR on your system:

1. Run the installation script:
   ```
   cd backend
   chmod +x scripts/install_tesseract.sh
   ./scripts/install_tesseract.sh
   ```

2. Test the OCR service:
   ```
   python scripts/test_ocr.py /path/to/test/image.jpg
   ```

3. If needed, update the Tesseract path in `backend/services/ocr_service.py` 
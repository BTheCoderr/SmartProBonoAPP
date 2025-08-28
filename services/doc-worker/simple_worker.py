import os
import json
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import base64
import io
import fitz  # PyMuPDF for PDF processing
import pytesseract
from PIL import Image
import cv2
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

# Database configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "smartprobono_db")
DB_USER = os.environ.get("DB_USER", "baheemferrell")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")

# AI configuration
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def extract_text_from_pdf(pdf_data: bytes) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Try to extract text directly first
            page_text = page.get_text()
            
            if page_text.strip():
                text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            else:
                # If no text found, try OCR
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Convert to grayscale for better OCR
                img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
                
                # OCR the image
                ocr_text = pytesseract.image_to_string(img_gray)
                if ocr_text.strip():
                    text += f"\n--- Page {page_num + 1} (OCR) ---\n{ocr_text}\n"
        
        pdf_document.close()
        return text.strip()
        
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    """Split text into overlapping chunks for better context"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundaries
        if end < len(text):
            # Look for sentence endings
            for i in range(end, max(start, end - 200), -1):
                if text[i] in '.!?':
                    end = i + 1
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks

def generate_embeddings(text: str) -> list:
    """Generate embeddings using sentence-transformers"""
    try:
        # Initialize the model (this will download on first use)
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embedding = model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Return a placeholder embedding
        return [0.0] * 384

app = FastAPI(title="SmartProBono Document AI Worker")

class ProcessBody(BaseModel):
    document_id: str
    language: str | None = "eng"

class AskBody(BaseModel):
    document_id: str
    question: str

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Worker is running"}

@app.post("/process")
def process_doc(body: ProcessBody):
    """Process a document: extract text, chunk it, and generate embeddings"""
    try:
        # Get document from database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get document info
        cursor.execute(
            "SELECT * FROM documents WHERE id = %s",
            (body.document_id,)
        )
        document = cursor.fetchone()
        
        if not document:
            raise HTTPException(404, "Document not found")
        
        # Get the actual text from the document
        # Read the file and extract text
        with open(document['storage_path'], 'rb') as f:
            file_content = f.read()
        
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(file_content)
        
        if not extracted_text:
            raise HTTPException(400, "Could not extract text from document")
        
        # Chunk the text
        chunks = chunk_text(extracted_text, chunk_size=1000, overlap=200)
        
        # Store chunks and generate embeddings
        for i, chunk_text in enumerate(chunks):
            cursor.execute(
                "INSERT INTO doc_chunks (document_id, chunk_index, text) VALUES (%s, %s, %s) RETURNING id",
                (body.document_id, i, chunk_text)
            )
            chunk_id = cursor.fetchone()['id']
            
            # Generate real embeddings
            embedding = generate_embeddings(chunk_text)
            
            cursor.execute(
                "INSERT INTO doc_embeddings (chunk_id, embedding) VALUES (%s, %s)",
                (chunk_id, json.dumps(embedding))
            )
        
        # Update document status
        cursor.execute(
            "UPDATE documents SET status = 'processed' WHERE id = %s",
            (body.document_id,)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "ok": True, 
            "chunks": len(chunks), 
            "message": "Document processed successfully",
            "document_id": body.document_id
        }
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...), user_id: str = None, title: str = None):
    """Upload and process a document"""
    try:
        if not file.filename.lower().endswith(('.pdf', '.txt', '.doc', '.docx')):
            raise HTTPException(400, "Only PDF, TXT, DOC, and DOCX files are supported")
        
        # Read file content
        file_content = await file.read()
        
        # Generate document ID
        import uuid
        document_id = str(uuid.uuid4())
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_content)
        elif file.filename.lower().endswith('.txt'):
            extracted_text = file_content.decode('utf-8')
        else:
            # For other formats, try to extract text (placeholder for now)
            extracted_text = file_content.decode('utf-8', errors='ignore')
        
        if not extracted_text:
            raise HTTPException(400, "Could not extract text from document")
        
        # Store file temporarily (in production, use proper storage)
        temp_path = f"/tmp/{document_id}_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(file_content)
        
        # Create document record in database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            """
            INSERT INTO documents (id, user_id, title, storage_path, status, language)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (document_id, user_id or 'anonymous', title or file.filename, temp_path, 'uploaded', 'eng')
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "ok": True,
            "document_id": document_id,
            "path": temp_path,
            "message": "Document uploaded and text extracted successfully",
            "text_length": len(extracted_text),
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.post("/ask")
def ask_doc(body: AskBody):
    """Ask a question about a document using AI generation"""
    try:
        # Get document chunks from database
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get document chunks
        cursor.execute(
            """
            SELECT dc.chunk_index, dc.text, de.embedding
            FROM doc_chunks dc
            LEFT JOIN doc_embeddings de ON dc.id = de.chunk_id
            WHERE dc.document_id = %s
            ORDER BY dc.chunk_index
            """,
            (body.document_id,)
        )
        chunks = cursor.fetchall()
        
        if not chunks:
            raise HTTPException(404, "No chunks found for this document")
        
        # Use Ollama for real AI responses
        try:
            # Prepare context from relevant chunks
            chunk_texts = [chunk['text'] for chunk in chunks]
            context = "\n\n".join(chunk_texts[:3])  # Use first 3 chunks for context
            
            # Create prompt for Ollama
            prompt = f"""You are a helpful AI assistant analyzing a legal document. 

Document Context:
{context}

Question: {body.question}

Please provide a clear, helpful answer based on the document content. If the document doesn't contain enough information to answer the question, say so. Be concise but thorough.

Answer:"""
            
            # Call Ollama
            ollama_response = requests.post(
                f"{OLLAMA_BASE}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                },
                timeout=30
            )
            
            if ollama_response.status_code == 200:
                ai_response = ollama_response.json()
                answer = ai_response.get('response', 'Sorry, I could not generate a response.')
            else:
                # Fallback if Ollama fails
                answer = f"Based on the document content, here's what I found: {context[:300]}...\n\nYour question was: '{body.question}'\n\nI'm having trouble connecting to the AI service, but here's the relevant document content."
                
        except Exception as e:
            print(f"Ollama error: {e}")
            # Fallback response
            chunk_texts = [chunk['text'] for chunk in chunks]
            combined_text = " ".join(chunk_texts)
            answer = f"Based on the document content: {combined_text[:300]}...\n\nYour question was: '{body.question}'\n\nI'm having trouble connecting to the AI service, but here's the relevant document content."
        
        # Return source information
        sources = [chunk['chunk_index'] for chunk in chunks]
        
        cursor.close()
        conn.close()
        
        return {
            "answer": answer,
            "sources": sources,
            "chunks_used": len(chunks)
        }
    except Exception as e:
        raise HTTPException(500, f"Question failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

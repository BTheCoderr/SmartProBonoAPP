# Ultra-minimal FastAPI requirements for SmartProBono
# Only the essential packages needed for the basic FastAPI app

# Core FastAPI dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-dotenv==1.0.1
requests==2.31.0
gunicorn==21.2.0

# Note: pydantic and pydantic-core are often installed as dependencies of fastapi
# and compatible versions for Python 3.13 are expected to be resolved by pip.
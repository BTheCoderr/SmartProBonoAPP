from setuptools import setup, find_packages

setup(
    name="smartprobono",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-jwt-extended',
        'flask-mail',
        'flask-socketio',
        'pymongo',
        'pytest',
        'pytest-cov',
        'python-dotenv',
        'requests',
        'pillow',
        'pytesseract',
        'pdf2image',
        'opencv-python',
        'reportlab',
        'bson',
    ],
    python_requires='>=3.9',
) 
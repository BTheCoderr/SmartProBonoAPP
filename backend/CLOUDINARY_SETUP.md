# Cloudinary Setup Instructions

To test the file upload functionality, you need valid Cloudinary credentials:

## Step 1: Create a Cloudinary Account

If you don't have one already, sign up for a free Cloudinary account at [https://cloudinary.com/users/register/free](https://cloudinary.com/users/register/free).

## Step 2: Get Your Credentials

1. Log in to your Cloudinary account
2. Go to the Dashboard
3. Look for your account details in the top-right section
4. You'll need:
   - Cloud Name
   - API Key
   - API Secret

## Step 3: Add Credentials to Your .env File

Edit the `.env` file in your backend directory and add the following with your actual credentials:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Step 4: Test Your Configuration

Run the setup script to verify your credentials work:

```bash
python scripts/setup_cloudinary.py --test-only
```

If successful, you should see a message that the configuration was tested successfully.

## Step 5: Set Up Cloudinary Resources

Run the setup script without the `--test-only` flag to create the necessary folders and upload presets:

```bash
python scripts/setup_cloudinary.py
```

This will create:
- Folder structure for different document types
- Upload presets for each document category

## Step 6: Test File Uploads

After setting up the Cloudinary resources, you can test file uploads through the DocumentsPage in the frontend application. 
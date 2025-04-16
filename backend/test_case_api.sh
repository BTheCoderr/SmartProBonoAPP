#!/bin/bash
# Simple test script for case API endpoints

API_URL="http://localhost:5002"

echo "Testing Case API endpoints..."
echo "-----------------------------"

# 1. Get all cases
echo "1. GET /api/cases"
curl -s -X GET "${API_URL}/api/cases"
echo -e "\n"

# 2. Create a new case
echo -e "2. POST /api/cases (Create new case)"
NEW_CASE=$(curl -s -X POST "${API_URL}/api/cases" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Eviction Case",
    "type": "housing",
    "status": "new",
    "priority": "high",
    "description": "This is a test case created via API",
    "client": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "555-123-4567"
    }
  }')

echo "$NEW_CASE"
echo -e "\n"

# Extract case ID from response using grep
CASE_ID=$(echo "$NEW_CASE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Extracted Case ID: $CASE_ID"

# 3. Get case by ID
echo -e "\n3. GET /api/cases/${CASE_ID}"
curl -s -X GET "${API_URL}/api/cases/${CASE_ID}"
echo -e "\n"

# 4. Add timeline event
echo -e "\n4. POST /api/cases/${CASE_ID}/timeline"
curl -s -X POST "${API_URL}/api/cases/${CASE_ID}/timeline" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "note",
    "description": "Called client to discuss case details"
  }'
echo -e "\n"

# 5. Add next step
echo -e "\n5. POST /api/cases/${CASE_ID}/next-steps"
curl -s -X POST "${API_URL}/api/cases/${CASE_ID}/next-steps" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "File response with court",
    "dueDate": "2024-08-01T09:00:00Z",
    "assignedTo": "attorney"
  }'
echo -e "\n"

# 6. Get all cases again to see the updated list
echo -e "\n6. GET /api/cases (after changes)"
curl -s -X GET "${API_URL}/api/cases"
echo -e "\n"

echo -e "\nAPI test completed!" 
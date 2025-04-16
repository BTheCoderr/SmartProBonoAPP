#!/bin/bash

# Execute Initial Issues Setup
# This script helps execute the steps outlined in initial_issues.md

echo "===== SmartProBono Initial Issues Setup ====="
echo ""
echo "This script will guide you through setting up initial issues for SmartProBono."
echo "Please follow the prompts and instructions carefully."
echo ""

# Step 1: Setting Up Issue Labels
echo "Step 1: Setting Up Issue Labels"
echo "----------------------------"
echo "Please create the following labels in your GitHub repository:"
echo ""
echo "1. good first issue - Beginner-friendly issues for first-time contributors"
echo "2. help wanted - Issues where we're actively seeking community help"
echo "3. documentation - Documentation-related issues"
echo "4. bug - Something isn't working as expected"
echo "5. enhancement - New feature or improvement"
echo "6. frontend - Frontend-related issues"
echo "7. backend - Backend-related issues"
echo "8. legal-content - Legal content-related issues"
echo "9. ui/ux - User interface and experience issues"
echo "10. accessibility - Accessibility-related issues"
echo ""
read -p "Have you created all the labels? (y/n): " labels_created
if [[ $labels_created != "y" ]]; then
  echo "Please create the labels before continuing."
  exit 1
fi

# Step 2: Creating Good First Issues
echo ""
echo "Step 2: Creating Good First Issues"
echo "-------------------------------"
echo "Please create the following 10 beginner-friendly issues:"
echo ""
echo "1. Documentation Improvements: Improve installation instructions in README"
echo "2. Frontend Enhancement: Add loading indicators to document generation form"
echo "3. Bug Fix: Fix mobile responsive layout on homepage"
echo "4. Accessibility Improvement: Add ARIA labels to form inputs"
echo "5. Backend Test Coverage: Add unit tests for user authentication"
echo "6. Documentation Translation: Translate README to Spanish"
echo "7. Legal Content Review: Review and improve eviction notice template"
echo "8. UI Component: Create a reusable button component"
echo "9. Performance Optimization: Optimize images on the landing page"
echo "10. DevOps Improvement: Add GitHub Actions workflow for linting"
echo ""
echo "Use the detailed descriptions provided in initial_issues.md for each issue."
echo ""
read -p "Have you created all the issues? (y/n): " issues_created
if [[ $issues_created != "y" ]]; then
  echo "Please create the issues before continuing."
  exit 1
fi

# Step 3: Setting Up Project Board
echo ""
echo "Step 3: Setting Up Project Board"
echo "-----------------------------"
echo "Please create a 'New Contributors' project board with the following columns:"
echo ""
echo "1. Available - Issues ready for new contributors"
echo "2. Claimed - Issues someone is working on"
echo "3. In Review - PRs under review"
echo "4. Completed - Merged contributions"
echo ""
echo "Add all the 'good first issues' to the 'Available' column."
echo ""
read -p "Have you set up the project board? (y/n): " board_setup
if [[ $board_setup != "y" ]]; then
  echo "Please set up the project board before continuing."
  exit 1
fi

# Step 4: Supporting New Contributors
echo ""
echo "Step 4: Supporting New Contributors"
echo "--------------------------------"
echo "Remember to follow these guidelines when new contributors express interest:"
echo ""
echo "1. Respond promptly and welcomingly"
echo "2. Provide additional guidance if needed"
echo "3. Offer to pair program or provide mentorship"
echo "4. Be patient and constructive in feedback"
echo "5. Celebrate their contributions"
echo ""
read -p "Do you understand how to support new contributors? (y/n): " support_understood
if [[ $support_understood != "y" ]]; then
  echo "Please review the guidelines for supporting new contributors."
  exit 1
fi

# Step 5: Regular Maintenance
echo ""
echo "Step 5: Regular Maintenance"
echo "------------------------"
echo "Remember to regularly review and replenish good first issues:"
echo ""
echo "1. Aim to always have 5-10 open good first issues"
echo "2. Vary the types of issues (frontend, backend, docs, etc.)"
echo "3. Adjust difficulty levels based on community feedback"
echo "4. Thank and recognize contributors who complete these issues"
echo ""
read -p "Do you understand the maintenance process for good first issues? (y/n): " maintenance_understood
if [[ $maintenance_understood != "y" ]]; then
  echo "Please review the maintenance guidelines for good first issues."
  exit 1
fi

echo ""
echo "===== Initial Issues Setup Complete! ====="
echo "Your SmartProBono repository now has beginner-friendly issues to attract new contributors."
echo "Next steps: Publish launch announcements"
echo "" 
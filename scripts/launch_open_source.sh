#!/bin/bash

# SmartProBono Open Source Launch
# This script executes all the steps needed to launch SmartProBono as an open-source project

echo "===== SmartProBono Open Source Launch ====="
echo ""
echo "This script will guide you through the complete process of launching SmartProBono as an open-source project."
echo "Please follow the prompts and instructions carefully."
echo ""

# Make all scripts executable
chmod +x execute_github_org_setup.sh
chmod +x execute_community_platforms_setup.sh
chmod +x execute_initial_issues_setup.sh
chmod +x execute_launch_announcements.sh
chmod +x execute_monitor_and_engage.sh

# Step 1: GitHub Organization Setup
echo "Step 1: GitHub Organization Setup"
echo "==============================="
./execute_github_org_setup.sh
if [ $? -ne 0 ]; then
  echo "GitHub Organization Setup failed. Please fix the issues and try again."
  exit 1
fi

# Step 2: Community Platforms Setup
echo ""
echo "Step 2: Community Platforms Setup"
echo "=============================="
./execute_community_platforms_setup.sh
if [ $? -ne 0 ]; then
  echo "Community Platforms Setup failed. Please fix the issues and try again."
  exit 1
fi

# Step 3: Initial Issues Setup
echo ""
echo "Step 3: Initial Issues Setup"
echo "========================="
./execute_initial_issues_setup.sh
if [ $? -ne 0 ]; then
  echo "Initial Issues Setup failed. Please fix the issues and try again."
  exit 1
fi

# Step 4: Launch Announcements
echo ""
echo "Step 4: Launch Announcements"
echo "=========================="
./execute_launch_announcements.sh
if [ $? -ne 0 ]; then
  echo "Launch Announcements failed. Please fix the issues and try again."
  exit 1
fi

# Step 5: Monitor and Engage
echo ""
echo "Step 5: Monitor and Engage"
echo "========================"
./execute_monitor_and_engage.sh
if [ $? -ne 0 ]; then
  echo "Monitor and Engage Setup failed. Please fix the issues and try again."
  exit 1
fi

echo ""
echo "===== SmartProBono Open Source Launch Complete! ====="
echo "Congratulations! You have successfully launched SmartProBono as an open-source project."
echo "Continue to monitor and engage with your community to build a thriving ecosystem around your project."
echo ""
echo "Remember to regularly review and update your:"
echo "- Documentation"
echo "- Good first issues"
echo "- Roadmap"
echo "- Community engagement activities"
echo ""
echo "Thank you for contributing to the open-source community and improving access to legal assistance!"
echo "" 
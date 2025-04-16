#!/bin/bash

# Execute GitHub Organization Setup
# This script helps execute the steps outlined in github_org_setup.md

echo "===== SmartProBono GitHub Organization Setup ====="
echo ""
echo "This script will guide you through setting up the GitHub organization for SmartProBono."
echo "Please follow the prompts and instructions carefully."
echo ""

# Step 1: Create GitHub Organization
echo "Step 1: Create GitHub Organization"
echo "--------------------------------"
echo "Please go to https://github.com/organizations/plan"
echo "Select the Free plan"
echo "Name the organization 'SmartProBono'"
echo "Use admin@smartprobono.org as the contact email (or your preferred email)"
echo "Select 'My personal account' for the organization owner"
echo "Complete the verification process"
echo ""
read -p "Have you created the GitHub organization? (y/n): " org_created
if [[ $org_created != "y" ]]; then
  echo "Please create the GitHub organization before continuing."
  exit 1
fi

# Step 2: Set up Teams
echo ""
echo "Step 2: Set up Teams"
echo "-------------------"
echo "Please create the following teams in your organization:"
echo ""
echo "Core Teams:"
echo "1. Core Team (Maintainers) - Admin permission"
echo "2. Board - Admin permission"
echo ""
echo "Development Teams:"
echo "3. Frontend Team - Write permission"
echo "4. Backend Team - Write permission"
echo "5. DevOps Team - Write permission"
echo ""
echo "Specialized Teams:"
echo "6. Legal Team - Write permission"
echo "7. Security Team - Write permission"
echo "8. Docs Team - Write permission"
echo "9. Community Team - Write permission"
echo ""
read -p "Have you set up all the teams? (y/n): " teams_setup
if [[ $teams_setup != "y" ]]; then
  echo "Please set up the teams before continuing."
  exit 1
fi

# Step 3: Repository Transfer
echo ""
echo "Step 3: Repository Transfer"
echo "-------------------------"
echo "To transfer the repository from your personal account to the organization:"
echo "1. Go to your repository settings"
echo "2. Scroll down to the 'Danger Zone'"
echo "3. Click 'Transfer ownership'"
echo "4. Select the 'SmartProBono' organization"
echo "5. Confirm the transfer"
echo ""
read -p "Have you transferred the repository? (y/n): " repo_transferred
if [[ $repo_transferred != "y" ]]; then
  echo "Please transfer the repository before continuing."
  exit 1
fi

# Step 4: Post-Transfer Setup
echo ""
echo "Step 4: Post-Transfer Setup"
echo "-------------------------"
echo "After transferring the repository, please:"
echo "1. Update repository settings:"
echo "   - Enable Discussions"
echo "   - Enable Sponsorships"
echo "   - Set up branch protection rules for 'main'"
echo "   - Enable vulnerability alerts"
echo ""
echo "2. Create project boards:"
echo "   - Development Roadmap"
echo "   - Bug Tracking"
echo "   - Feature Requests"
echo "   - Community Engagement"
echo ""
echo "3. Set up repository secrets for CI/CD:"
echo "   - OPENAI_API_KEY"
echo "   - Deployment credentials"
echo ""
echo "4. Create initial labels:"
echo "   - good first issue"
echo "   - help wanted"
echo "   - bug"
echo "   - enhancement"
echo "   - documentation"
echo "   - legal-review"
echo ""
read -p "Have you completed the post-transfer setup? (y/n): " post_setup
if [[ $post_setup != "y" ]]; then
  echo "Please complete the post-transfer setup before continuing."
  exit 1
fi

# Step 5: GitHub Apps Integration
echo ""
echo "Step 5: GitHub Apps Integration"
echo "-----------------------------"
echo "Enable the following GitHub apps:"
echo "1. Welcome Bot"
echo "2. Stale Bot"
echo "3. CodeCov"
echo "4. Dependabot"
echo "5. GitHub Actions"
echo ""
read -p "Have you integrated the GitHub apps? (y/n): " apps_integrated
if [[ $apps_integrated != "y" ]]; then
  echo "Please integrate the GitHub apps before continuing."
  exit 1
fi

echo ""
echo "===== GitHub Organization Setup Complete! ====="
echo "Your SmartProBono GitHub organization is now set up and ready for community contributions."
echo "Next steps: Set up community platforms (Discord, Discourse, social media)"
echo "" 
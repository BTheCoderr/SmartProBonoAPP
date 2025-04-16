#!/bin/bash

# Execute Community Platforms Setup
# This script helps execute the steps outlined in community_platforms_setup.md

echo "===== SmartProBono Community Platforms Setup ====="
echo ""
echo "This script will guide you through setting up the community platforms for SmartProBono."
echo "Please follow the prompts and instructions carefully."
echo ""

# Step 1: Discord Server Setup
echo "Step 1: Discord Server Setup"
echo "--------------------------"
echo "Please follow these steps to create a Discord server:"
echo ""
echo "1. Create a Discord Server:"
echo "   - Open Discord and click the '+' icon on the left sidebar"
echo "   - Select 'Create My Own'"
echo "   - Choose 'For a club or community'"
echo "   - Name the server 'SmartProBono'"
echo "   - Upload the SmartProBono logo as the server icon"
echo ""
echo "2. Set Up Channels:"
echo "   - Create the categories and channels as outlined in community_platforms_setup.md"
echo ""
echo "3. Set Up Roles:"
echo "   - Create the roles as outlined in community_platforms_setup.md"
echo ""
echo "4. Set Up Permissions:"
echo "   - Configure appropriate permissions for each role and channel"
echo ""
echo "5. Set Up Bots:"
echo "   - Add the recommended bots (MEE6/Dyno, GitHub, Welcome-bot, Carl-bot, TicketTool)"
echo ""
echo "6. Create Server Invite:"
echo "   - Create a permanent invite link to share in documentation and social media"
echo ""
read -p "Have you set up the Discord server? (y/n): " discord_setup
if [[ $discord_setup != "y" ]]; then
  echo "Please set up the Discord server before continuing."
  exit 1
fi

# Step 2: Discourse Forum Setup
echo ""
echo "Step 2: Discourse Forum Setup"
echo "---------------------------"
echo "Please follow these steps to set up a Discourse forum:"
echo ""
echo "1. Choose Hosting Option:"
echo "   - Self-hosted or Discourse.org hosting (recommended)"
echo ""
echo "2. Domain Setup:"
echo "   - Register forum.smartprobono.org or a similar domain"
echo "   - Configure DNS settings to point to your Discourse instance"
echo ""
echo "3. Basic Configuration:"
echo "   - Set the forum name to 'SmartProBono Community'"
echo "   - Upload the SmartProBono logo"
echo "   - Configure email settings for notifications"
echo "   - Set up SSO (Single Sign-On) if desired"
echo ""
echo "4. Create Categories:"
echo "   - Create the categories as outlined in community_platforms_setup.md"
echo ""
echo "5. Set Up User Groups:"
echo "   - Create the user groups as outlined in community_platforms_setup.md"
echo ""
echo "6. Configure Permissions:"
echo "   - Set appropriate permissions for each category and user group"
echo ""
echo "7. Install Plugins:"
echo "   - Install the recommended plugins (discourse-github, discourse-solved, etc.)"
echo ""
read -p "Have you set up the Discourse forum? (y/n): " discourse_setup
if [[ $discourse_setup != "y" ]]; then
  echo "Please set up the Discourse forum before continuing."
  exit 1
fi

# Step 3: Social Media Accounts
echo ""
echo "Step 3: Social Media Accounts"
echo "---------------------------"
echo "Please create the following social media accounts:"
echo ""
echo "1. Twitter/X:"
echo "   - Create a new account with the handle @SmartProBono"
echo "   - Use the SmartProBono logo as the profile picture"
echo "   - Create a compelling bio that mentions 'open-source legal assistance platform'"
echo "   - Add the website URL"
echo ""
echo "2. LinkedIn:"
echo "   - Create a company page named 'SmartProBono'"
echo "   - Add the logo and banner image"
echo "   - Write a detailed 'About' section"
echo "   - Add relevant industry tags (Legal Services, Open Source, Technology)"
echo ""
echo "3. YouTube:"
echo "   - Create a new channel named 'SmartProBono'"
echo "   - Add channel art and logo"
echo "   - Create channel sections (Tutorials, Community Calls, Feature Demos, Legal Tech Talks)"
echo ""
echo "4. Social Media Management:"
echo "   - Consider setting up a social media management tool (Buffer, Hootsuite, or Later)"
echo ""
read -p "Have you created the social media accounts? (y/n): " social_media_setup
if [[ $social_media_setup != "y" ]]; then
  echo "Please create the social media accounts before continuing."
  exit 1
fi

# Step 4: Integration Between Platforms
echo ""
echo "Step 4: Integration Between Platforms"
echo "----------------------------------"
echo "Please set up the following integrations:"
echo ""
echo "1. Add links to all platforms in each platform's description/about section"
echo "2. Set up webhook integrations between GitHub and Discord"
echo "3. Configure GitHub Discussion notifications to Discord"
echo "4. Set up cross-posting between platforms where appropriate"
echo ""
read -p "Have you set up the integrations between platforms? (y/n): " integrations_setup
if [[ $integrations_setup != "y" ]]; then
  echo "Please set up the integrations before continuing."
  exit 1
fi

# Step 5: Content Calendar
echo ""
echo "Step 5: Content Calendar"
echo "----------------------"
echo "Create a content calendar for the first month post-launch:"
echo ""
echo "1. Week 1: Introduction to SmartProBono"
echo "2. Week 2: How to Contribute"
echo "3. Week 3: Feature Highlights"
echo "4. Week 4: Community Spotlight"
echo ""
read -p "Have you created the content calendar? (y/n): " calendar_created
if [[ $calendar_created != "y" ]]; then
  echo "Please create the content calendar before continuing."
  exit 1
fi

echo ""
echo "===== Community Platforms Setup Complete! ====="
echo "Your SmartProBono community platforms are now set up and ready for engagement."
echo "Next steps: Create initial issues and set up the project board"
echo "" 
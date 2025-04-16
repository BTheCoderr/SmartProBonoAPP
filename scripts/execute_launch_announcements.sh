#!/bin/bash

# Execute Launch Announcements
# This script helps execute the steps outlined in launch_announcement.md

echo "===== SmartProBono Launch Announcements ====="
echo ""
echo "This script will guide you through publishing launch announcements for SmartProBono."
echo "Please follow the prompts and instructions carefully."
echo ""

# Step 1: Publish Blog Post
echo "Step 1: Publish Blog Post"
echo "----------------------"
echo "Please publish the blog post announcement using the template in launch_announcement.md:"
echo ""
echo "1. Choose a blogging platform (Medium, Dev.to, your website, etc.)"
echo "2. Copy the blog post template from launch_announcement.md"
echo "3. Customize it with your specific details"
echo "4. Add appropriate images and formatting"
echo "5. Publish the post"
echo "6. Share the link on your social media accounts"
echo ""
read -p "Have you published the blog post? (y/n): " blog_published
if [[ $blog_published != "y" ]]; then
  echo "Please publish the blog post before continuing."
  exit 1
fi

# Step 2: Send Press Release
echo ""
echo "Step 2: Send Press Release"
echo "-----------------------"
echo "Please send the press release using the template in launch_announcement.md:"
echo ""
echo "1. Customize the press release template with your specific details"
echo "2. Create a list of relevant media outlets and journalists"
echo "3. Send the press release to your media contacts"
echo "4. Follow up with key contacts after a few days"
echo ""
read -p "Have you sent the press release? (y/n): " press_release_sent
if [[ $press_release_sent != "y" ]]; then
  echo "Please send the press release before continuing."
  exit 1
fi

# Step 3: Post on Social Media
echo ""
echo "Step 3: Post on Social Media"
echo "-------------------------"
echo "Please post the launch announcements on social media using the templates in launch_announcement.md:"
echo ""
echo "1. Twitter/X:"
echo "   - Post the Twitter thread template"
echo "   - Pin the first tweet to your profile"
echo ""
echo "2. LinkedIn:"
echo "   - Post the LinkedIn announcement template"
echo "   - Tag relevant connections and organizations"
echo ""
echo "3. Facebook/Instagram:"
echo "   - Post the Facebook/Instagram announcement template"
echo "   - Add appropriate hashtags"
echo ""
read -p "Have you posted on social media? (y/n): " social_media_posted
if [[ $social_media_posted != "y" ]]; then
  echo "Please post on social media before continuing."
  exit 1
fi

# Step 4: Send Email Newsletter
echo ""
echo "Step 4: Send Email Newsletter"
echo "--------------------------"
echo "Please send the email newsletter using the template in launch_announcement.md:"
echo ""
echo "1. Set up an email newsletter service if you haven't already"
echo "2. Customize the email newsletter template with your specific details"
echo "3. Create a compelling subject line"
echo "4. Test the email to ensure all links work"
echo "5. Send the newsletter to your subscriber list"
echo ""
read -p "Have you sent the email newsletter? (y/n): " newsletter_sent
if [[ $newsletter_sent != "y" ]]; then
  echo "Please send the email newsletter before continuing."
  exit 1
fi

# Step 5: Send Outreach Emails
echo ""
echo "Step 5: Send Outreach Emails"
echo "-------------------------"
echo "Please send outreach emails to legal tech communities using the template in launch_announcement.md:"
echo ""
echo "1. Create a list of relevant legal tech communities and organizations"
echo "2. Customize the outreach email template for each recipient"
echo "3. Send personalized emails to each community"
echo "4. Track responses and follow up as needed"
echo ""
read -p "Have you sent outreach emails? (y/n): " outreach_emails_sent
if [[ $outreach_emails_sent != "y" ]]; then
  echo "Please send outreach emails before continuing."
  exit 1
fi

echo ""
echo "===== Launch Announcements Complete! ====="
echo "Your SmartProBono launch has been announced across multiple channels."
echo "Next steps: Monitor and engage with the community"
echo "" 
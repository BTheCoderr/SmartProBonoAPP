/**
 * Test script for verifying testimonial styling in SmartProBono
 * 
 * This script uses Puppeteer to visually check the testimonials section
 * on the beta landing page to ensure it's properly styled.
 */

const puppeteer = require('puppeteer');

async function testTestimonialStyling() {
  console.log('Starting testimonial styling test...');
  
  // Launch browser
  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 100,
    defaultViewport: {
      width: 1280,
      height: 800
    }
  });
  
  const page = await browser.newPage();
  
  try {
    // Navigate to the beta landing page
    await page.goto('http://localhost:3002', { waitUntil: 'networkidle2' });
    console.log('Loaded landing page');
    
    // Find all testimonial cards
    const testimonialCards = await page.$$('.testimonial-card');
    console.log(`Found ${testimonialCards.length} testimonial cards`);
    
    // Check if each card has proper styling
    for (let i = 0; i < testimonialCards.length; i++) {
      const card = testimonialCards[i];
      
      // Check if the avatar exists and has proper size
      const avatar = await card.$('.MuiAvatar-root');
      if (avatar) {
        console.log(`✅ Testimonial #${i + 1} has an avatar`);
      } else {
        console.log(`❌ Testimonial #${i + 1} is missing an avatar`);
      }
      
      // Check if the rating is shown
      const rating = await card.$('.MuiRating-root');
      if (rating) {
        console.log(`✅ Testimonial #${i + 1} has a rating`);
      } else {
        console.log(`❌ Testimonial #${i + 1} is missing a rating`);
      }
      
      // Check for text content
      const text = await card.$eval('p', el => el.textContent);
      if (text && text.length > 20) {
        console.log(`✅ Testimonial #${i + 1} has text content: "${text.substring(0, 20)}..."`);
      } else {
        console.log(`❌ Testimonial #${i + 1} has insufficient text content`);
      }
    }
    
    // Also check the partners section
    const partnerSection = await page.$('h6:contains("Trusted By Leading Organizations")');
    if (partnerSection) {
      console.log('✅ Found partners section');
      
      const partnerImages = await page.$$('img[alt="Legal Aid Society"], img[alt="Pro Bono Net"], img[alt="American Bar Association"]');
      console.log(`Found ${partnerImages.length} partner logos`);
      
      if (partnerImages.length === 3) {
        console.log('✅ All partner logos are present');
      } else {
        console.log('❌ Some partner logos are missing');
      }
    } else {
      console.log('❌ Partners section not found');
    }
    
    console.log('Test completed successfully');
  } catch (error) {
    console.error('Test failed:', error);
  } finally {
    await browser.close();
  }
}

// Run the test if executed directly
if (require.main === module) {
  testTestimonialStyling().catch(console.error);
}

module.exports = { testTestimonialStyling }; 
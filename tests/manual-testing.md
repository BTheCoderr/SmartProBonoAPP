# Manual Testing Guide for SmartProBono

This document provides a step-by-step guide for manually testing key features of the SmartProBono application, with a focus on the recently implemented fixes.

## 1. Immigration Form Testing

### Test Immigration Form Dropdown Menus

1. Navigate to `http://localhost:3100/#/immigration`
2. Click on "Get Help" under "Family-Based Immigration"
3. Verify that the form appears and the Immigration Matter Type is pre-filled with "family"
4. Check each dropdown menu to ensure options appear and can be selected:
   - Nationality
   - Current Immigration Status
   - Desired Immigration Service
   - Annual Income Level
   - How did you hear about us?
5. Try selecting different options in each dropdown
6. Fill out other required fields and submit the form
7. Verify the success notification appears

### Test Form Validation

1. Navigate to the Immigration Form
2. Try submitting without filling required fields
3. Verify validation error messages appear
4. Fill out only some required fields and verify partial validation works
5. Complete all fields and verify form submits successfully

## 2. Navigation Testing

### Test Resource Page Navigation

1. Navigate to `http://localhost:3100/#/resources`
2. Click on "Access Documents" buttons
3. Verify that you are redirected to the Documents page
4. Return to Resources page
5. Click on "Learn More" buttons
6. Verify that you are redirected to the appropriate pages (Rights, Procedures, etc.)

### Test Immigration Service Card Actions

1. Navigate to Immigration page
2. Click on each service card's "Get Help" button
3. Verify each opens the form with the correct service type pre-selected
4. Test the "START FREE CONSULTATION" button at the bottom
5. Verify it also opens the intake form

## 3. Authentication Testing

### Test Login and Rate Limiting

1. Navigate to the Login page
2. Enter valid credentials and login
3. Verify successful login
4. Logout and login again several times in quick succession
5. Verify no rate limiting errors occur
6. Check browser console for any API errors

### Test Token Refresh

1. Login to the application
2. Keep the page open for >30 minutes
3. Perform an action requiring authentication
4. Verify the action works without requiring re-login
5. Check browser console to ensure no 429 errors

## 4. Mobile Responsiveness Testing

1. Use browser dev tools to emulate mobile devices (iPhone, Android)
2. Navigate through main pages and verify layout adjusts properly
3. Test the Immigration Form on mobile
4. Verify all dropdowns and form controls are usable on small screens
5. Test form submission on mobile

## 5. Performance Testing

1. Open browser dev tools and navigate to the Network tab
2. Load the Immigration page and monitor network requests
3. Verify no excessive API calls
4. Check for duplicate requests
5. Monitor memory usage in the Performance tab

## Reporting Issues

If any issues are found during testing, please document them with the following information:
- Page/feature where the issue occurred
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Browser and device information 
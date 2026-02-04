# 🔍 DEBUG DATA FLOW - Step by Step Guide

## The Problem
User data (customer name, phone) is not showing on the thank you page.

## How to Debug

### Step 1: Test Data Flow Directly
1. Open browser and go to: `http://localhost:3000/test-data-flow.html`
2. Click "1. Save Test Data" - should show success
3. Click "2. Read Data" - should show the saved data
4. Click "4. Go to Thank You Page" - should display the test data

If this works → The thank you page reading logic is fine.
If this doesn't work → There's a problem with sessionStorage or the page itself.

### Step 2: Test Real Form Submission
1. Clear sessionStorage:
   ```javascript
   sessionStorage.clear();
   location.reload();
   ```

2. Go to a frame detail page (e.g., `http://localhost:3000/frame-detail.html?id=1`)

3. Fill the form:
   - First Name: محمد
   - Last Name: أحمد  
   - Phone: 0555123456

4. Open browser console (F12) BEFORE submitting

5. Submit the form and watch console logs:
   - Look for `=== CAPTURED FORM DATA ===`
   - Look for `=== FINAL VALIDATION BEFORE SAVING ===`
   - Look for `=== SAVING TO SESSION STORAGE ===`
   - Look for `✅ VERIFIED IMMEDIATELY AFTER SAVE`

6. After redirect to thank you page, check console:
   - Look for `=== THANK YOU PAGE - START ===`
   - Look for `=== FINAL VALUES TO DISPLAY ===`

7. Check what's actually in sessionStorage:
   ```javascript
   JSON.parse(sessionStorage.getItem('orderData'))
   ```

### Step 3: Manual Data Check
On the thank you page, run in console:
```javascript
// Check if data exists
const data = sessionStorage.getItem('orderData');
console.log('Raw data:', data);

// Check parsed data
if (data) {
    const parsed = JSON.parse(data);
    console.log('Parsed:', parsed);
    console.log('Customer Name:', parsed.customerName);
    console.log('Phone:', parsed.phone);
    console.log('FirstName:', parsed.firstName);
    console.log('LastName:', parsed.lastName);
}

// Check if elements exist
console.log('Customer name element:', document.getElementById('customer-name'));
console.log('Phone element:', document.getElementById('customer-phone'));

// Try to set manually
const nameEl = document.getElementById('customer-name');
const phoneEl = document.getElementById('customer-phone');
if (nameEl) nameEl.textContent = 'TEST NAME';
if (phoneEl) phoneEl.textContent = 'TEST PHONE';
```

If manual setting works → The display logic is fine, data is the issue.
If manual setting doesn't work → Elements don't exist or there's a CSS/JS issue.

## Common Issues

### Issue 1: Data Not Saved
**Symptoms:** No data in sessionStorage after form submit
**Fix:** Check if form submission is being prevented or if API call is blocking

### Issue 2: Data Saved But Wrong Format
**Symptoms:** Data exists but customerName is "undefined undefined"
**Fix:** Check form field capture - ensure values are captured before API call

### Issue 3: Data Not Read
**Symptoms:** Data exists in sessionStorage but page shows "غير محدد"
**Fix:** Check parsing logic and element selection

### Issue 4: Elements Don't Exist
**Symptoms:** Console shows "element not found"
**Fix:** Check if page HTML structure matches what JS expects

## Quick Test Commands

```javascript
// Save test data directly
sessionStorage.setItem('orderData', JSON.stringify({
    orderId: 'TEST123',
    firstName: 'محمد',
    lastName: 'أحمد',
    customerName: 'محمد أحمد',
    phone: '0555123456',
    frameTitle: 'Test Frame',
    framePrice: '100',
    hasAudio: true
}));

// Reload thank you page
location.reload();

// Or navigate to it
location.href = '/thank-you';
```

## Expected Console Output

When form is submitted:
```
=== CAPTURED FORM DATA ===
First Name: محمد
Last Name: أحمد
Phone: 0555123456
Customer Name: محمد أحمد
=== FINAL VALIDATION BEFORE SAVING ===
=== SAVING TO SESSION STORAGE ===
Customer Name (final): محمد أحمد
Phone (final): 0555123456
✅ Data saved to sessionStorage
✅ VERIFIED IMMEDIATELY AFTER SAVE
  - customerName: محمد أحمد
  - phone: 0555123456
```

When thank you page loads:
```
=== THANK YOU PAGE LOADING ===
=== THANK YOU PAGE - START ===
Try 1 - customerName field: محمد أحمد
Try 2 - firstName: محمد lastName: أحمد
✅ Constructed from firstName + lastName: محمد أحمد
=== FINAL VALUES TO DISPLAY ===
Customer Name: محمد أحمد
Phone: 0555123456
✅ Customer name element updated: محمد أحمد
✅ Phone element updated: 0555123456
```


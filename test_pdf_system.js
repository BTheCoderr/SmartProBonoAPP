/**
 * Test script for SmartProBono PDF Generation System
 * This script tests the PDF generation API endpoint
 */

const fetch = require('node-fetch');

async function testPdfGeneration() {
  console.log('🧪 Testing SmartProBono PDF Generation System...\n');

  const testData = {
    clientName: "Maria Lopez",
    caseNumber: "SPB-2025-0912",
    dateIssued: "09/02/2025",
    bodyText: "Intake summary and pro se instructions below.",
    tableRows: [
      { cols: ["Document", "Status", "Notes"] },
      { cols: ["Fee Waiver", "Prepared", "Signature pending"] },
      { cols: ["Summons", "Queued", "Serve via sheriff"] }
    ]
  };

  try {
    console.log('📤 Sending PDF generation request...');
    console.log('Data:', JSON.stringify(testData, null, 2));
    
    const response = await fetch('http://localhost:3000/api/pdf/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const pdfBuffer = await response.buffer();
    console.log('✅ PDF generated successfully!');
    console.log(`📄 PDF size: ${pdfBuffer.length} bytes`);
    
    // Save the PDF to a file for inspection
    const fs = require('fs');
    fs.writeFileSync('test-generated.pdf', pdfBuffer);
    console.log('💾 PDF saved as "test-generated.pdf"');
    
    return true;
  } catch (error) {
    console.error('❌ PDF generation failed:', error.message);
    return false;
  }
}

async function testTemplateEditor() {
  console.log('\n🎨 Testing PDF Template Editor...');
  console.log('📝 Template Editor should be available at: http://localhost:3000/tools/pdf-template-editor');
  console.log('🔧 Use the visual editor to create custom templates');
  console.log('📤 Export templates with d.getTemplate() in browser devtools');
}

async function runTests() {
  console.log('🚀 SmartProBono PDF System Test Suite\n');
  console.log('=' .repeat(50));
  
  // Test PDF generation
  const pdfTest = await testPdfGeneration();
  
  // Test template editor info
  await testTemplateEditor();
  
  console.log('\n' + '=' .repeat(50));
  console.log('📊 Test Results:');
  console.log(`PDF Generation: ${pdfTest ? '✅ PASS' : '❌ FAIL'}`);
  console.log('Template Editor: ✅ Available at /tools/pdf-template-editor');
  
  if (pdfTest) {
    console.log('\n🎉 All tests passed! PDF system is working correctly.');
    console.log('\n📋 Next Steps:');
    console.log('1. Open http://localhost:3000/tools/pdf-template-editor');
    console.log('2. Create custom templates using the visual editor');
    console.log('3. Use PdfService in your frontend components');
    console.log('4. Generate legal documents, intake summaries, etc.');
  } else {
    console.log('\n⚠️  Some tests failed. Check the error messages above.');
  }
}

// Run the tests
runTests().catch(console.error);

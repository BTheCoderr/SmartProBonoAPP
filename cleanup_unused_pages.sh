#!/bin/bash
# Clean up unused/test pages

echo "🧹 Cleaning up unused/test pages..."
echo ""

# Test/Demo/Beta pages (safe to delete)
TEST_PAGES=(
  "frontend/src/pages/AuthTestPage.js"
  "frontend/src/pages/DocumentAITest.js"
  "frontend/src/pages/LangGraphDemo.js"
  "frontend/src/pages/SaulTestPage.js"
  "frontend/src/pages/ScannerTestPage.js"
  "frontend/src/pages/BetaLandingPage.js"
  "frontend/src/pages/BetaConfirm.js"
  "frontend/src/pages/SignatureDemoPage.js"
)

# Duplicate pages (use alternatives)
DUPLICATES=(
  "frontend/src/pages/AboutUsPage.js"  # Use About.js
  "frontend/src/pages/DocumentScannerPage.js"  # Use DocumentScanPage.js
  "frontend/src/pages/DocumentGenerationPage.js"  # Use PDFGenerator
  "frontend/src/pages/HelpCenterPage.js"  # Use HelpPage.js
  "frontend/src/pages/GlossaryPage.js"  # Use ComprehensiveGlossaryPage.js
  "frontend/src/pages/LegalChat.js"  # Use LegalAIChatPage.js
  "frontend/src/pages/LegalChatPage.js"  # Use LegalAIChatPage.js
  "frontend/src/pages/Home.js"  # Use HomePage.js
  "frontend/src/pages/Documents.js"  # Use DocumentsPage.js
  "frontend/src/pages/Contracts.js"  # Use ContractsPage.js
  "frontend/src/pages/ScanDocument.js"  # Use DocumentScanPage.js
  "frontend/src/pages/LandingPage.js"  # Use HomePage.js
  "frontend/src/pages/KnowYourRightsPage.js"  # Use RightsPage.js
)

# Unused forms (if not using)
UNUSED_FORMS=(
  "frontend/src/pages/EvictionResponseForm.js"
  "frontend/src/pages/FeeWaiverRequestForm.js"
  "frontend/src/pages/SmallClaimsComplaintForm.js"
)

# Unused dashboards
UNUSED_DASHBOARDS=(
  "frontend/src/pages/AdminNotificationDashboard.js"
  "frontend/src/pages/AnalyticsDashboard.js"
  "frontend/src/pages/ImmigrationDashboard.js"
  "frontend/src/pages/TemplatesDashboardPage.js"
)

# Other unused
OTHER_UNUSED=(
  "frontend/src/pages/BusinessModel.js"
  "frontend/src/pages/StartupBusinessModel.js"
  "frontend/src/pages/CaseDetailPage.js"
  "frontend/src/pages/ComplianceScannerPage.js"
  "frontend/src/pages/EducationalContentPage.js"
  "frontend/src/pages/ExpungementPage.js"  # Use ExpungementWizard component
  "frontend/src/pages/FormsIndexPage.js"
  "frontend/src/pages/LegalAnalysis.js"
  "frontend/src/pages/LegalTemplatesPage.js"
  "frontend/src/pages/ModelManagementPage.js"
  "frontend/src/pages/OnboardingPage.js"
  "frontend/src/pages/PolicyGeneratorPage.js"
  "frontend/src/pages/ProceduresPage.js"
  "frontend/src/pages/RiskAssessmentPage.js"
  "frontend/src/pages/SignaturePage.js"
  "frontend/src/pages/SignaturePlacementPage.js"
  "frontend/src/pages/ThankYouPage.js"
)

ALL_TO_DELETE=("${TEST_PAGES[@]}" "${DUPLICATES[@]}" "${UNUSED_FORMS[@]}" "${UNUSED_DASHBOARDS[@]}" "${OTHER_UNUSED[@]}")

DELETED=0
NOT_FOUND=0

for file in "${ALL_TO_DELETE[@]}"; do
  if [ -f "$file" ]; then
    rm "$file"
    echo "❌ Deleted: $file"
    ((DELETED++))
  else
    ((NOT_FOUND++))
  fi
done

echo ""
echo "📊 Summary:"
echo "   Deleted: $DELETED files"
echo "   Not found: $NOT_FOUND files"
echo ""
echo "✅ Cleanup complete!"


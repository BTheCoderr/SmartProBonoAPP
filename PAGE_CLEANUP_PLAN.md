# 📋 Page Cleanup Plan

## 📊 Current Status

- **Total Page Files:** 103
- **Actually Used:** ~44 pages
- **Unused/Test Pages:** 46+ pages
- **Reduction Possible:** ~45% fewer files

---

## ✅ ESSENTIAL PAGES (Keep - 8 pages)

**Core functionality - Required for platform to work:**

1. `HomePage.js` - Landing page
2. `LegalAIChatPage.js` - AI chat (main feature)
3. `DocumentScanPage.js` - Document scanner
4. `DocumentsPage.js` - Document management
5. `LoginPage.js` - User authentication
6. `RegisterPage.js` - User registration
7. `Dashboard.js` / `EnhancedDashboard.js` - User dashboard
8. `NotFoundPage.js` - 404 error page

---

## ⭐ IMPORTANT PAGES (Keep - 12 pages)

**User-facing pages - Important for UX:**

1. `About.js` - About page
2. `Contact.js` - Contact form
3. `Services.js` - Services listing
4. `Resources.js` - Resources page
5. `RightsPage.js` - Know your rights
6. `PrivacyPolicyPage.js` - Legal requirement
7. `TermsOfServicePage.js` - Legal requirement
8. `HelpPage.js` - Help/support
9. `BugReportPage.js` - User feedback
10. `FeatureRequestPage.js` - User feedback
11. `ComprehensiveGlossaryPage.js` - Legal glossary
12. `FAQPage.js` - Frequently asked questions

---

## 🔧 TOOL PAGES (Keep - 6 pages)

**Core legal tools:**

1. `LegalToolsPage.js` - Tools hub
2. `CaseLawPage.js` - Case law research
3. `ExpertHelpPage.js` - Expert help
4. `SafetyCheckPage.js` - Safety checker
5. `DocumentChecklistPage.js` - Document checklist
6. `PDFGenerator.js` - PDF generator (component)

---

## 👥 DASHBOARD PAGES (Keep - 7 pages)

**Role-based dashboards:**

1. `AdminDashboard.js` - Admin panel
2. `LawyerDashboard.js` - Lawyer dashboard
3. `BondsmanDashboard.js` - Bondsman dashboard
4. `ClientPortal.js` - Client portal
5. `VirtualParalegalPage.js` - Virtual paralegal
6. `FormsDashboard.js` - Forms dashboard
7. `ProfilePage.js` - User profile

---

## 📄 OPTIONAL PAGES (Keep for now - 11 pages)

**Nice-to-have, but not critical:**

1. `PartnersPage.js` - Partners page
2. `PressPage.js` - Press/media
3. `CareersPage.js` - Careers
4. `TeamPage.js` - Team page
5. `OurMissionPage.js` - Mission statement
6. `BlogPage.js` - Blog (if using)
7. `StatusPage.js` - System status
8. `SitemapPage.js` - Sitemap
9. `AccessibilityPage.js` - Accessibility info
10. `VolunteerFormPage.js` - Volunteer form
11. `LegalHelpFormPage.js` - Legal help form

---

## ❌ UNUSED/TEST PAGES (Can Delete - 46+ pages)

**Not routed, duplicates, or test pages:**

### Duplicates/Alternatives:
- `AboutUsPage.js` (use `About.js`)
- `DocumentScannerPage.js` (use `DocumentScanPage.js`)
- `DocumentGenerationPage.js` (use PDFGenerator)
- `HelpCenterPage.js` (use `HelpPage.js`)
- `GlossaryPage.js` (use `ComprehensiveGlossaryPage.js`)
- `LegalChat.js` / `LegalChatPage.js` (use `LegalAIChatPage.js`)
- `Home.js` (use `HomePage.js`)
- `Documents.js` (use `DocumentsPage.js`)
- `Contracts.js` (use `ContractsPage.js`)

### Test/Demo Pages:
- `AuthTestPage.js`
- `DocumentAITest.js`
- `LangGraphDemo.js`
- `SaulTestPage.js`
- `ScannerTestPage.js`
- `BetaLandingPage.js`
- `BetaConfirm.js`

### Unused Forms:
- `EvictionResponseForm.js`
- `FeeWaiverRequestForm.js`
- `SmallClaimsComplaintForm.js`
- `ForgotPasswordPage.js` (if not using)
- `ResetPasswordPage.js` (if not using)

### Unused Dashboards:
- `AdminNotificationDashboard.js`
- `AnalyticsDashboard.js`
- `ImmigrationDashboard.js`
- `TemplatesDashboardPage.js`

### Other Unused:
- `BusinessModel.js`
- `StartupBusinessModel.js`
- `CaseDetailPage.js`
- `ComplianceScannerPage.js`
- `EducationalContentPage.js`
- `ExpungementPage.js` (use ExpungementWizard component)
- `FormsIndexPage.js`
- `KnowYourRightsPage.js` (use `RightsPage.js`)
- `LandingPage.js` (use `HomePage.js`)
- `LegalAnalysis.js`
- `LegalTemplatesPage.js`
- `ModelManagementPage.js`
- `OnboardingPage.js`
- `PolicyGeneratorPage.js`
- `ProceduresPage.js`
- `RiskAssessmentPage.js`
- `ScanDocument.js` (use `DocumentScanPage.js`)
- `SignatureDemoPage.js`
- `SignaturePage.js`
- `SignaturePlacementPage.js`
- `ThankYouPage.js`
- `UnauthorizedPage.js` (can keep if using auth)

---

## 🎯 Recommendation

### Keep: ~44 pages
- 8 Essential
- 12 Important
- 6 Tools
- 7 Dashboards
- 11 Optional

### Delete: ~46+ pages
- Duplicates
- Test pages
- Unused forms
- Unused dashboards

### Result:
- **Before:** 103 pages
- **After:** ~44 pages
- **Reduction:** ~57% fewer files

---

## 🚀 Quick Win: Delete Test Pages First

These are safe to delete immediately:
- All `*Test*.js` pages
- All `*Demo*.js` pages
- All `*Beta*.js` pages

This alone removes ~10-15 files!


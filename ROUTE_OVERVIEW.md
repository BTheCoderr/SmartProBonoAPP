# SmartProBono Platform - Complete Route Overview

## 🏠 **Main Application Routes**

### **Home & Core**
- **`/`** - HomePage (Landing page)
- **`/test`** - TestPage (Development testing)
- **`/about`** - About (Company information)
- **`/contact`** - Contact (Contact form)

### **Authentication**
- **`/login`** - LoginPage (User login)
- **`/register`** - RegisterPage (User registration)
- **`/unauthorized`** - UnauthorizedPage (Access denied)

---

## 👥 **Role-Based Dashboards**

### **Client Portal**
- **`/client-portal`** - ClientPortal
  - Case tracking and progress monitoring
  - Document access and management
  - Real-time notifications
  - Client communication tools

### **Lawyer Dashboard**
- **`/lawyer-dashboard`** - LawyerDashboard
  - Case management system
  - Client communication
  - Analytics and reporting
  - Document management

### **Bondsman Dashboard**
- **`/bondsman-dashboard`** - BondsmanDashboard
  - Bail bond management
  - Payment tracking
  - Risk assessment
  - Client management

### **Admin Dashboard**
- **`/admin`** - AdminDashboard
  - System management
  - User analytics
  - Compliance monitoring
  - Performance metrics

---

## 🤖 **AI & Virtual Paralegal**

### **AI Virtual Paralegal**
- **`/ai-virtual-paralegal`** - AIVirtualParalegal
  - Autonomous AI system
  - Case research and analysis
  - Document generation
  - Workflow automation

### **Virtual Paralegal**
- **`/virtual-paralegal`** - VirtualParalegalPage (Protected)
  - Interactive paralegal tools
  - Case assistance
  - Document help

### **Legal AI Chat**
- **`/legal-chat`** - LegalAIChatPage
- **`/ai-chat`** - Redirects to /legal-chat
- **`/chat`** - LiveChatPage (No login required)

### **Legal Chat Nested Routes**
- **`/legal-chat/premium`** - Premium legal chat features
- **`/legal-chat/feedback`** - Feedback analytics

---

## ⚖️ **Legal Tools & Services**

### **Document Processing**
- **`/documents`** - DocumentsPage
- **`/generate-document`** - PDFGenerator
- **`/scan-document`** - DocumentScanPage (Protected)
- **`/document-scan`** - DocumentScanPage (Protected)
- **`/safety-check`** - SafetyCheckPage

### **Forms & Templates**
- **`/forms`** - FormsDashboard (Protected)
- **`/forms/:formType`** - DocumentGenerator (Protected)
- **`/expungement-toolkit`** - ExpungementWizard (Protected)

### **Legal Tools**
- **`/legal-tools`** - LegalToolsPage
- **`/expert-help`** - ExpertHelpPage

---

## 📊 **Analytics & Management**

### **User Dashboards**
- **`/dashboard`** - Dashboard (Protected)
- **`/profile`** - ProfilePage (Protected)

### **Analytics**
- **`/services/analytics`** - LegalAnalytics (Protected)

---

## 🛠️ **Services (Nested Routes)**

### **Main Services**
- **`/services`** - Services (Main services page)

### **Service Categories**
- **`/services/contracts/*`** - ContractsPage (Protected)
- **`/services/immigration/*`** - Immigration (Protected)
- **`/services/analytics`** - LegalAnalytics (Protected)

---

## 📚 **Resources (Nested Routes)**

### **Main Resources**
- **`/resources`** - Resources (Main resources page)

### **Resource Categories**
- **`/resources/rights`** - RightsPage
- **`/resources/checklist/:type`** - DocumentChecklistPage
- **`/resources/immigration`** - ImmigrationResourcesPage
- **`/resources/external`** - ExternalResourcesPage
- **`/resources/guides`** - LegalGuidesPage
- **`/resources/premium-guides`** - Premium resources

---

## 🔧 **Development & Testing**

### **Test Routes**
- **`/test-ai`** - SimpleTest (AI testing)

---

## 📄 **Footer & Support Pages**

### **Company Information**
- **`/status`** - StatusPage
- **`/help`** - HelpPage
- **`/bug-report`** - BugReportPage
- **`/feature-request`** - FeatureRequestPage
- **`/partners`** - PartnersPage
- **`/press`** - PressPage
- **`/careers`** - CareersPage
- **`/team`** - TeamPage
- **`/mission`** - OurMissionPage

### **Legal Information**
- **`/rights`** - RightsPage
- **`/rights/immigration`** - ImmigrationRightsPage
- **`/glossary`** - GlossaryPage
- **`/faq`** - FAQPage
- **`/blog`** - BlogPage

---

## 🔐 **Access Control**

### **No Authentication Required**
- Home, About, Contact
- Legal Tools, Legal Chat
- All Footer pages
- Resources (basic)

### **Authentication Required (Protected)**
- All Dashboards (Client, Lawyer, Bondsman, Admin)
- Document scanning
- Forms and templates
- User profile
- Analytics

### **Admin Only**
- Admin Dashboard
- System management features

---

## 🌐 **URL Structure Summary**

### **Main Categories:**
1. **Dashboards**: `/client-portal`, `/lawyer-dashboard`, `/bondsman-dashboard`, `/admin`
2. **AI Features**: `/ai-virtual-paralegal`, `/legal-chat`, `/virtual-paralegal`
3. **Legal Tools**: `/legal-tools`, `/documents`, `/generate-document`, `/scan-document`
4. **Services**: `/services/*` (nested routes)
5. **Resources**: `/resources/*` (nested routes)
6. **Support**: Footer pages and help sections

### **Total Routes: 50+ individual routes**
### **Nested Routes: 15+ additional nested routes**
### **Total Pages: 65+ different pages and components**

---

## 🚀 **How to Access All Pages**

### **Start the Frontend:**
```bash
cd frontend
npm start
```

### **Then visit:**
- **Main App**: http://localhost:3002
- **All dashboards**: Add `/client-portal`, `/lawyer-dashboard`, etc.
- **All tools**: Add `/legal-tools`, `/documents`, etc.
- **All resources**: Add `/resources/rights`, `/resources/guides`, etc.

**Your platform has 65+ different pages and features!** 🎉

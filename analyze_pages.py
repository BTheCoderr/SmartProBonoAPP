#!/usr/bin/env python3
"""
Analyze which pages are actually used vs unused
"""

import os
import re
from pathlib import Path

# Read App.js to find all imported/routed pages
app_js_path = Path("frontend/src/App.js")
if app_js_path.exists():
    app_content = app_js_path.read_text()
    
    # Find all imports
    imports = re.findall(r"import\s+(\w+)\s+from\s+['\"].*pages/(\w+)", app_content)
    imported_pages = {name: file for name, file in imports}
    
    # Find all Route paths
    routes = re.findall(r"<Route\s+path=[\"']([^\"']+)[\"']", app_content)
    
    # Find component usage in routes
    route_components = re.findall(r"element=\{<(\w+)\s*/>", app_content)
    
    print("📊 Page Analysis")
    print("=" * 60)
    print(f"\n✅ Imported Pages: {len(imported_pages)}")
    print(f"✅ Routes Defined: {len(routes)}")
    print(f"✅ Components Used: {len(set(route_components))}")
    
    # Get all page files
    pages_dir = Path("frontend/src/pages")
    all_pages = []
    if pages_dir.exists():
        for file in pages_dir.rglob("*.js"):
            if "node_modules" not in str(file):
                all_pages.append(file.stem)
        for file in pages_dir.rglob("*.jsx"):
            if "node_modules" not in str(file):
                all_pages.append(file.stem)
        for file in pages_dir.rglob("*.tsx"):
            if "node_modules" not in str(file):
                all_pages.append(file.stem)
    
    print(f"\n📁 Total Page Files: {len(set(all_pages))}")
    
    # Categorize pages
    essential = [
        "HomePage", "LegalAIChatPage", "DocumentScanPage", "DocumentsPage",
        "LoginPage", "RegisterPage", "Dashboard", "NotFoundPage"
    ]
    
    important = [
        "About", "Contact", "Services", "Resources", "RightsPage",
        "PrivacyPolicyPage", "TermsOfServicePage", "HelpPage",
        "BugReportPage", "FeatureRequestPage", "GlossaryPage", "FAQPage"
    ]
    
    optional = [
        "PartnersPage", "PressPage", "CareersPage", "TeamPage",
        "OurMissionPage", "BlogPage", "StatusPage", "SitemapPage",
        "AccessibilityPage", "VolunteerFormPage", "LegalHelpFormPage"
    ]
    
    dashboards = [
        "AdminDashboard", "LawyerDashboard", "BondsmanDashboard",
        "ClientPortal", "VirtualParalegalPage", "FormsDashboard",
        "ProfilePage"
    ]
    
    tools = [
        "LegalToolsPage", "CaseLawPage", "ExpertHelpPage",
        "SafetyCheckPage", "DocumentChecklistPage", "PDFGenerator"
    ]
    
    # Find unused
    used_pages = set(imported_pages.values()) | set(imported_pages.keys())
    used_pages_lower = {p.lower() for p in used_pages}
    
    unused = []
    for page in set(all_pages):
        if page not in used_pages and page.lower() not in used_pages_lower:
            # Check if it's a duplicate or test page
            if "Test" in page or "Demo" in page or "Beta" in page:
                unused.append(page)
            elif page + "Page" not in used_pages:
                unused.append(page)
    
    print("\n" + "=" * 60)
    print("📋 Page Categories:")
    print("=" * 60)
    
    print(f"\n✅ ESSENTIAL ({len(essential)}):")
    for p in essential:
        print(f"   - {p}")
    
    print(f"\n⭐ IMPORTANT ({len(important)}):")
    for p in important:
        print(f"   - {p}")
    
    print(f"\n🔧 TOOLS ({len(tools)}):")
    for p in tools:
        print(f"   - {p}")
    
    print(f"\n👥 DASHBOARDS ({len(dashboards)}):")
    for p in dashboards:
        print(f"   - {p}")
    
    print(f"\n📄 OPTIONAL ({len(optional)}):")
    for p in optional:
        print(f"   - {p}")
    
    print(f"\n❌ UNUSED/TEST ({len(unused)}):")
    for p in sorted(unused)[:20]:  # Show first 20
        print(f"   - {p}")
    if len(unused) > 20:
        print(f"   ... and {len(unused) - 20} more")
    
    print("\n" + "=" * 60)
    print(f"📊 Summary:")
    print(f"   Essential: {len(essential)} pages")
    print(f"   Important: {len(important)} pages")
    print(f"   Tools: {len(tools)} pages")
    print(f"   Dashboards: {len(dashboards)} pages")
    print(f"   Optional: {len(optional)} pages")
    print(f"   Unused: {len(unused)} pages")
    print(f"\n💡 Recommendation: Keep ~30-40 pages, remove {len(unused)}+ unused/test pages")


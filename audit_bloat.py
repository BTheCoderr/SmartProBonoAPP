#!/usr/bin/env python3
"""
Comprehensive bloat audit - find unused code, components, routes, dependencies
"""

import os
import re
from pathlib import Path
from collections import defaultdict

print("🔍 Comprehensive Bloat Audit")
print("=" * 70)

# 1. Check unused components
print("\n1️⃣ COMPONENT AUDIT")
print("-" * 70)

components_dir = Path("frontend/src/components")
all_components = []
if components_dir.exists():
    for file in components_dir.rglob("*.js"):
        if "node_modules" not in str(file) and "test" not in str(file).lower():
            all_components.append(file.stem)
    for file in components_dir.rglob("*.jsx"):
        if "node_modules" not in str(file) and "test" not in str(file).lower():
            all_components.append(file.stem)
    for file in components_dir.rglob("*.tsx"):
        if "node_modules" not in str(file) and "test" not in str(file).lower():
            all_components.append(file.stem)

print(f"Total Components: {len(set(all_components))}")

# Find test/unused components
test_components = [c for c in all_components if "Test" in c or "Demo" in c]
print(f"Test Components: {len(test_components)}")
for c in sorted(test_components)[:10]:
    print(f"   - {c}")

# 2. Check duplicate routes
print("\n2️⃣ ROUTE AUDIT")
print("-" * 70)

app_js = Path("frontend/src/App.js")
if app_js.exists():
    content = app_js.read_text()
    routes = re.findall(r'path=["\']([^"\']+)["\']', content)
    route_counts = defaultdict(int)
    for route in routes:
        route_counts[route] += 1
    
    duplicates = {r: c for r, c in route_counts.items() if c > 1}
    if duplicates:
        print(f"⚠️  Duplicate Routes Found: {len(duplicates)}")
        for route, count in duplicates.items():
            print(f"   - {route}: {count} times")
    else:
        print("✅ No duplicate routes")

# 3. Check unused imports in App.js
print("\n3️⃣ IMPORT AUDIT")
print("-" * 70)

if app_js.exists():
    imports = re.findall(r"import\s+(\w+)\s+from\s+['\"].*pages/(\w+)", content)
    imported = {name: file for name, file in imports}
    
    # Find components used in routes
    used = re.findall(r"element=\{<(\w+)\s*/>", content)
    used_set = set(used)
    
    unused_imports = []
    for name, file in imported.items():
        if name not in used_set and name + "Page" not in used_set:
            unused_imports.append((name, file))
    
    if unused_imports:
        print(f"⚠️  Unused Imports: {len(unused_imports)}")
        for name, file in unused_imports[:10]:
            print(f"   - {name} from {file}")
    else:
        print("✅ All imports are used")

# 4. Check backend routes
print("\n4️⃣ BACKEND ROUTE AUDIT")
print("-" * 70)

backend_routes = Path("backend/routes")
route_files = []
if backend_routes.exists():
    for file in backend_routes.glob("*.py"):
        route_files.append(file.name)

print(f"Backend Route Files: {len(route_files)}")
for rf in sorted(route_files)[:15]:
    print(f"   - {rf}")

# 5. Check for large files
print("\n5️⃣ FILE SIZE AUDIT")
print("-" * 70)

large_files = []
for root, dirs, files in os.walk("frontend/src"):
    if "node_modules" in root:
        continue
    for file in files:
        if file.endswith((".js", ".jsx", ".tsx")):
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                if size > 50000:  # > 50KB
                    large_files.append((filepath, size))
            except:
                pass

large_files.sort(key=lambda x: x[1], reverse=True)
if large_files:
    print(f"⚠️  Large Files (>50KB): {len(large_files)}")
    for filepath, size in large_files[:10]:
        print(f"   - {filepath}: {size/1024:.1f}KB")
else:
    print("✅ No unusually large files")

# 6. Summary
print("\n" + "=" * 70)
print("📊 AUDIT SUMMARY")
print("=" * 70)
print(f"Components: {len(set(all_components))} total")
print(f"Test Components: {len(test_components)} (can remove)")
print(f"Backend Routes: {len(route_files)} files")
print(f"Large Files: {len(large_files)} files >50KB")
print("\n💡 Recommendations:")
print("   1. Remove test components")
print("   2. Clean up unused imports")
print("   3. Review large files for optimization")
print("   4. Remove duplicate routes")


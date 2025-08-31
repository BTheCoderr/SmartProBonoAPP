#!/usr/bin/env python3
"""
SmartProBono Architecture Analysis
Comprehensive exploration of the codebase structure and components
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

class ArchitectureAnalyzer:
    def __init__(self, root_path="."):
        self.root_path = Path(root_path)
        self.analysis = {
            "timestamp": datetime.now().isoformat(),
            "project_structure": {},
            "components": {},
            "dependencies": {},
            "architecture_patterns": [],
            "recommendations": []
        }
    
    def analyze_project_structure(self):
        """Analyze the overall project structure"""
        print("📁 Analyzing Project Structure...")
        
        structure = {}
        for item in self.root_path.iterdir():
            if item.name.startswith('.'):
                continue
                
            if item.is_dir():
                structure[item.name] = self._analyze_directory(item)
            else:
                structure[item.name] = {
                    "type": "file",
                    "size": item.stat().st_size,
                    "extension": item.suffix
                }
        
        self.analysis["project_structure"] = structure
        print(f"   Found {len(structure)} top-level items")
    
    def _analyze_directory(self, dir_path, max_depth=3, current_depth=0):
        """Recursively analyze directory structure"""
        if current_depth >= max_depth:
            return {"type": "directory", "truncated": True}
        
        contents = {}
        try:
            for item in dir_path.iterdir():
                if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', '.git']:
                    continue
                    
                if item.is_dir():
                    contents[item.name] = self._analyze_directory(item, max_depth, current_depth + 1)
                else:
                    contents[item.name] = {
                        "type": "file",
                        "size": item.stat().st_size,
                        "extension": item.suffix
                    }
        except PermissionError:
            contents = {"error": "Permission denied"}
        
        return {
            "type": "directory",
            "contents": contents,
            "file_count": len([f for f in contents.values() if f.get("type") == "file"])
        }
    
    def analyze_components(self):
        """Analyze major system components"""
        print("🧩 Analyzing System Components...")
        
        components = {
            "backend": self._analyze_backend(),
            "frontend": self._analyze_frontend(),
            "langgraph": self._analyze_langgraph(),
            "database": self._analyze_database(),
            "deployment": self._analyze_deployment()
        }
        
        self.analysis["components"] = components
    
    def _analyze_backend(self):
        """Analyze backend components"""
        backend_path = self.root_path / "backend"
        if not backend_path.exists():
            return {"status": "not_found"}
        
        backend_info = {
            "type": "Python Flask/FastAPI",
            "main_files": [],
            "endpoints": [],
            "dependencies": []
        }
        
        # Find main application files
        for pattern in ["*.py", "app.py", "main.py", "api.py"]:
            for file_path in backend_path.rglob(pattern):
                if file_path.is_file():
                    backend_info["main_files"].append(str(file_path.relative_to(self.root_path)))
        
        # Check for requirements
        req_file = backend_path / "requirements.txt"
        if req_file.exists():
            with open(req_file) as f:
                backend_info["dependencies"] = [line.strip() for line in f if line.strip()]
        
        return backend_info
    
    def _analyze_frontend(self):
        """Analyze frontend components"""
        frontend_path = self.root_path / "frontend"
        if not frontend_path.exists():
            return {"status": "not_found"}
        
        frontend_info = {
            "type": "React/Next.js",
            "main_files": [],
            "dependencies": []
        }
        
        # Find main files
        for pattern in ["*.js", "*.jsx", "*.ts", "*.tsx", "package.json"]:
            for file_path in frontend_path.rglob(pattern):
                if file_path.is_file():
                    frontend_info["main_files"].append(str(file_path.relative_to(self.root_path)))
        
        # Check package.json
        package_json = frontend_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    package_data = json.load(f)
                    frontend_info["dependencies"] = list(package_data.get("dependencies", {}).keys())
            except:
                pass
        
        return frontend_info
    
    def _analyze_langgraph(self):
        """Analyze LangGraph service"""
        langgraph_path = self.root_path / "agent_service"
        if not langgraph_path.exists():
            return {"status": "not_found"}
        
        langgraph_info = {
            "type": "LangGraph Multi-Agent System",
            "components": {
                "graphs": [],
                "nodes": [],
                "services": []
            },
            "features": []
        }
        
        # Analyze graph files
        for file_path in langgraph_path.rglob("graph*.py"):
            langgraph_info["components"]["graphs"].append(str(file_path.relative_to(self.root_path)))
        
        # Analyze node files
        nodes_path = langgraph_path / "nodes"
        if nodes_path.exists():
            for file_path in nodes_path.rglob("*.py"):
                if file_path.name != "__init__.py":
                    langgraph_info["components"]["nodes"].append(str(file_path.relative_to(self.root_path)))
        
        # Check for advanced features
        if (langgraph_path / "graph_advanced.py").exists():
            langgraph_info["features"].append("Advanced Multi-Agent Workflow")
        if (langgraph_path / "human_in_loop.py").exists():
            langgraph_info["features"].append("Human-in-the-Loop")
        if (langgraph_path / "parallel_execution.py").exists():
            langgraph_info["features"].append("Parallel Execution")
        if (langgraph_path / "checkpointing.py").exists():
            langgraph_info["features"].append("Checkpointing")
        
        return langgraph_info
    
    def _analyze_database(self):
        """Analyze database setup"""
        db_info = {
            "type": "Supabase (PostgreSQL)",
            "schema_files": [],
            "tables": []
        }
        
        # Find SQL files
        for file_path in self.root_path.rglob("*.sql"):
            db_info["schema_files"].append(str(file_path.relative_to(self.root_path)))
        
        # Analyze SQL files for table definitions
        for sql_file in db_info["schema_files"]:
            try:
                with open(self.root_path / sql_file) as f:
                    content = f.read()
                    # Simple table detection
                    if "CREATE TABLE" in content.upper():
                        db_info["tables"].append(sql_file)
            except:
                pass
        
        return db_info
    
    def _analyze_deployment(self):
        """Analyze deployment configuration"""
        deployment_info = {
            "scripts": [],
            "config_files": [],
            "docker_files": []
        }
        
        # Find deployment-related files
        for pattern in ["*.sh", "docker-compose.yml", "Dockerfile", "*.yaml", "*.yml"]:
            for file_path in self.root_path.rglob(pattern):
                if file_path.is_file():
                    if pattern == "*.sh":
                        deployment_info["scripts"].append(str(file_path.relative_to(self.root_path)))
                    elif "docker" in file_path.name.lower():
                        deployment_info["docker_files"].append(str(file_path.relative_to(self.root_path)))
                    else:
                        deployment_info["config_files"].append(str(file_path.relative_to(self.root_path)))
        
        return deployment_info
    
    def analyze_dependencies(self):
        """Analyze project dependencies"""
        print("📦 Analyzing Dependencies...")
        
        dependencies = {
            "python": [],
            "node": [],
            "system": []
        }
        
        # Python dependencies
        for req_file in self.root_path.rglob("requirements.txt"):
            try:
                with open(req_file) as f:
                    deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    dependencies["python"].extend(deps)
            except:
                pass
        
        # Node dependencies
        for package_file in self.root_path.rglob("package.json"):
            try:
                with open(package_file) as f:
                    package_data = json.load(f)
                    deps = list(package_data.get("dependencies", {}).keys())
                    dependencies["node"].extend(deps)
            except:
                pass
        
        # Remove duplicates
        dependencies["python"] = list(set(dependencies["python"]))
        dependencies["node"] = list(set(dependencies["node"]))
        
        self.analysis["dependencies"] = dependencies
        print(f"   Found {len(dependencies['python'])} Python dependencies")
        print(f"   Found {len(dependencies['node'])} Node dependencies")
    
    def identify_architecture_patterns(self):
        """Identify architectural patterns used"""
        print("🏗️ Identifying Architecture Patterns...")
        
        patterns = []
        
        # Check for microservices pattern
        if (self.root_path / "agent_service").exists() and (self.root_path / "backend").exists():
            patterns.append({
                "name": "Microservices Architecture",
                "description": "Separate services for different concerns (backend API, LangGraph agents)",
                "evidence": ["agent_service/", "backend/"]
            })
        
        # Check for multi-agent pattern
        if (self.root_path / "agent_service" / "graph_advanced.py").exists():
            patterns.append({
                "name": "Multi-Agent System",
                "description": "Multiple AI agents working together with specialized roles",
                "evidence": ["graph_advanced.py", "nodes/"]
            })
        
        # Check for API Gateway pattern
        if (self.root_path / "agent_service" / "main.py").exists():
            patterns.append({
                "name": "API Gateway",
                "description": "Centralized API entry point for multiple services",
                "evidence": ["agent_service/main.py"]
            })
        
        # Check for Database per Service
        if "supabase" in str(self.root_path.rglob("*.py")):
            patterns.append({
                "name": "Database per Service",
                "description": "Each service has its own database schema/tables",
                "evidence": ["Supabase integration", "SQL schema files"]
            })
        
        self.analysis["architecture_patterns"] = patterns
        print(f"   Identified {len(patterns)} architectural patterns")
    
    def generate_recommendations(self):
        """Generate architecture improvement recommendations"""
        print("💡 Generating Recommendations...")
        
        recommendations = []
        
        # Check for missing documentation
        if not (self.root_path / "README.md").exists():
            recommendations.append({
                "priority": "high",
                "category": "Documentation",
                "title": "Add comprehensive README",
                "description": "Create a detailed README with setup instructions, architecture overview, and API documentation"
            })
        
        # Check for testing
        test_files = list(self.root_path.rglob("*test*.py"))
        if len(test_files) < 3:
            recommendations.append({
                "priority": "medium",
                "category": "Testing",
                "title": "Expand test coverage",
                "description": "Add more comprehensive unit and integration tests"
            })
        
        # Check for environment configuration
        env_files = list(self.root_path.rglob(".env*"))
        if not env_files:
            recommendations.append({
                "priority": "medium",
                "category": "Configuration",
                "title": "Add environment configuration",
                "description": "Create .env.example and proper environment variable management"
            })
        
        # Check for monitoring
        if not any("monitoring" in str(f) for f in self.root_path.rglob("*.py")):
            recommendations.append({
                "priority": "low",
                "category": "Monitoring",
                "title": "Add monitoring and logging",
                "description": "Implement comprehensive logging and monitoring for production use"
            })
        
        self.analysis["recommendations"] = recommendations
        print(f"   Generated {len(recommendations)} recommendations")
    
    def generate_report(self):
        """Generate comprehensive architecture report"""
        print("\n📊 Generating Architecture Report...")
        
        # Save detailed analysis
        report_file = f"architecture_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.analysis, f, indent=2)
        
        # Generate summary
        print("\n" + "="*60)
        print("🏗️ SMART PROBONO ARCHITECTURE ANALYSIS")
        print("="*60)
        
        print(f"\n📁 PROJECT STRUCTURE:")
        for name, info in self.analysis["project_structure"].items():
            if info.get("type") == "directory":
                file_count = info.get("file_count", 0)
                print(f"   • {name}/ ({file_count} files)")
            else:
                print(f"   • {name}")
        
        print(f"\n🧩 SYSTEM COMPONENTS:")
        for name, component in self.analysis["components"].items():
            if component.get("status") != "not_found":
                print(f"   • {name.title()}: {component.get('type', 'Unknown')}")
                if 'features' in component:
                    for feature in component['features']:
                        print(f"     - {feature}")
        
        print(f"\n🏗️ ARCHITECTURE PATTERNS:")
        for pattern in self.analysis["architecture_patterns"]:
            print(f"   • {pattern['name']}")
            print(f"     {pattern['description']}")
        
        print(f"\n📦 KEY DEPENDENCIES:")
        python_deps = self.analysis["dependencies"]["python"][:5]  # Top 5
        for dep in python_deps:
            print(f"   • {dep}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in self.analysis["recommendations"]:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            print(f"   {priority_emoji.get(rec['priority'], '⚪')} {rec['title']}")
            print(f"     {rec['description']}")
        
        print(f"\n📄 Detailed analysis saved to: {report_file}")
        return report_file

def main():
    analyzer = ArchitectureAnalyzer()
    
    print("🔍 SmartProBono Architecture Analysis")
    print("="*50)
    
    analyzer.analyze_project_structure()
    analyzer.analyze_components()
    analyzer.analyze_dependencies()
    analyzer.identify_architecture_patterns()
    analyzer.generate_recommendations()
    
    report_file = analyzer.generate_report()
    print(f"\n✅ Analysis complete! Report saved to: {report_file}")

if __name__ == "__main__":
    main()

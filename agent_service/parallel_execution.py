"""
Parallel execution system for LangGraph
Allows multiple specialists to work simultaneously
"""

import asyncio
import concurrent.futures
from typing import Dict, Any, List, Callable, Tuple
from datetime import datetime
import json

class ParallelExecutor:
    """Manages parallel execution of multiple agents"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    
    def execute_parallel(self, tasks: List[Tuple[Callable, Dict[str, Any]]]) -> List[Any]:
        """Execute multiple tasks in parallel"""
        futures = []
        
        for func, args in tasks:
            future = self.executor.submit(func, args)
            futures.append(future)
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error in parallel execution: {e}")
                results.append({"error": str(e)})
        
        return results
    
    def execute_with_timeout(self, tasks: List[Tuple[Callable, Dict[str, Any]]], 
                           timeout_seconds: int = 30) -> List[Any]:
        """Execute tasks in parallel with timeout"""
        futures = []
        
        for func, args in tasks:
            future = self.executor.submit(func, args)
            futures.append(future)
        
        results = []
        try:
            for future in concurrent.futures.as_completed(futures, timeout=timeout_seconds):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error in parallel execution: {e}")
                    results.append({"error": str(e)})
        except concurrent.futures.TimeoutError:
            print(f"Parallel execution timed out after {timeout_seconds} seconds")
            # Cancel remaining futures
            for future in futures:
                future.cancel()
        
        return results

class RoundtableExecutor:
    """Specialized executor for roundtable discussions"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ParallelExecutor(max_workers)
    
    def run_roundtable(self, agents: List[Callable], context: Dict[str, Any]) -> Dict[str, Any]:
        """Run a roundtable discussion with multiple agents"""
        
        # Prepare tasks for each agent
        tasks = []
        for i, agent in enumerate(agents):
            agent_context = context.copy()
            agent_context["agent_id"] = i
            agent_context["agent_name"] = agent.__name__
            tasks.append((agent, agent_context))
        
        # Execute in parallel
        results = self.executor.execute_parallel(tasks)
        
        # Analyze results
        return self._analyze_roundtable_results(results, context)
    
    def _analyze_roundtable_results(self, results: List[Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and synthesize roundtable results"""
        
        # Filter out errors
        valid_results = [r for r in results if "error" not in r]
        
        if not valid_results:
            return {
                "consensus": "No valid responses",
                "results": results,
                "error": "All agents failed"
            }
        
        # Simple consensus logic (can be enhanced with LLM)
        if len(valid_results) == 1:
            return {
                "consensus": valid_results[0],
                "results": results,
                "confidence": "low"
            }
        
        # Check for agreement
        first_result = valid_results[0]
        agreement_count = sum(1 for r in valid_results if r == first_result)
        
        if agreement_count == len(valid_results):
            return {
                "consensus": first_result,
                "results": results,
                "confidence": "high",
                "agreement": "unanimous"
            }
        else:
            return {
                "consensus": first_result,  # Default to first result
                "results": results,
                "confidence": "medium",
                "agreement": f"{agreement_count}/{len(valid_results)}"
            }

class SpecialistPool:
    """Pool of specialist agents for parallel execution"""
    
    def __init__(self):
        self.specialists = {}
        self.executor = ParallelExecutor()
    
    def register_specialist(self, name: str, specialist_func: Callable):
        """Register a specialist agent"""
        self.specialists[name] = specialist_func
    
    def run_specialists_parallel(self, case_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run multiple specialists in parallel for a case"""
        
        # Select relevant specialists
        relevant_specialists = self._select_specialists(case_type)
        
        if not relevant_specialists:
            return {"error": "No relevant specialists found"}
        
        # Prepare tasks
        tasks = []
        for specialist_name in relevant_specialists:
            if specialist_name in self.specialists:
                specialist_context = context.copy()
                specialist_context["specialist_name"] = specialist_name
                tasks.append((self.specialists[specialist_name], specialist_context))
        
        # Execute in parallel
        results = self.executor.execute_parallel(tasks)
        
        # Synthesize results
        return self._synthesize_specialist_results(results, relevant_specialists)
    
    def _select_specialists(self, case_type: str) -> List[str]:
        """Select relevant specialists based on case type"""
        specialist_mapping = {
            "criminal": ["criminal_lawyer", "criminal_procedure_expert"],
            "housing": ["housing_lawyer", "tenant_rights_expert"],
            "family": ["family_lawyer", "divorce_specialist"],
            "employment": ["employment_lawyer", "labor_rights_expert"],
            "immigration": ["immigration_lawyer", "visa_specialist"]
        }
        
        return specialist_mapping.get(case_type, ["general_lawyer"])
    
    def _synthesize_specialist_results(self, results: List[Any], specialist_names: List[str]) -> Dict[str, Any]:
        """Synthesize results from multiple specialists"""
        
        # Create a mapping of specialist to result
        specialist_results = {}
        for i, result in enumerate(results):
            if i < len(specialist_names):
                specialist_results[specialist_names[i]] = result
        
        # Find the most comprehensive result
        best_result = None
        best_score = 0
        
        for specialist, result in specialist_results.items():
            if "error" not in result:
                # Simple scoring based on result length and content
                score = len(str(result))
                if score > best_score:
                    best_score = score
                    best_result = result
        
        return {
            "synthesis": best_result,
            "specialist_results": specialist_results,
            "best_specialist": max(specialist_results.keys(), key=lambda k: len(str(specialist_results[k]))) if specialist_results else None
        }

# Global instances
parallel_executor = ParallelExecutor()
roundtable_executor = RoundtableExecutor()
specialist_pool = SpecialistPool()

def parallel_specialists(specialist_names: List[str]):
    """Decorator to run multiple specialists in parallel"""
    def decorator(func):
        def wrapper(ctx, *args, **kwargs):
            # Check if parallel execution is enabled
            if os.environ.get("ENABLE_PARALLEL_EXECUTION", "false").lower() != "true":
                return func(ctx, *args, **kwargs)
            
            # Run specialists in parallel
            context = ctx.state.copy()
            results = specialist_pool.run_specialists_parallel(
                context.get("case_type", "other"), context
            )
            
            # Update state with results
            ctx.state["parallel_results"] = results
            ctx.state["execution_mode"] = "parallel"
            
            return ctx.state
        
        return wrapper
    return decorator

def roundtable_discussion(agent_count: int = 3):
    """Decorator to run a roundtable discussion"""
    def decorator(func):
        def wrapper(ctx, *args, **kwargs):
            # Check if roundtable is enabled
            if os.environ.get("ENABLE_ROUNDTABLE", "false").lower() != "true":
                return func(ctx, *args, **kwargs)
            
            # Create agents for roundtable
            agents = [func] * agent_count  # Simplified - in practice, you'd have different agents
            
            # Run roundtable
            context = ctx.state.copy()
            results = roundtable_executor.run_roundtable(agents, context)
            
            # Update state with results
            ctx.state["roundtable_results"] = results
            ctx.state["execution_mode"] = "roundtable"
            
            return ctx.state
        
        return wrapper
    return decorator

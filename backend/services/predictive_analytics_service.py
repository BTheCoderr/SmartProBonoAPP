"""
Predictive Analytics Service for SmartProBono
Provides AI-powered predictions for case outcomes and legal recommendations
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random

logger = logging.getLogger(__name__)

class PredictiveAnalyticsService:
    """Service for predictive analytics and case outcome predictions"""
    
    def __init__(self):
        self.case_types = [
            "immigration", "family_law", "criminal_defense", 
            "personal_injury", "business_law", "civil_rights"
        ]
        self.outcome_factors = {
            "case_complexity": ["simple", "moderate", "complex"],
            "evidence_strength": ["weak", "moderate", "strong"],
            "legal_precedent": ["unfavorable", "neutral", "favorable"],
            "client_cooperation": ["poor", "average", "excellent"],
            "opposing_counsel": ["weak", "moderate", "strong"]
        }
    
    def predict_case_outcome(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict the likely outcome of a legal case"""
        try:
            case_type = case_data.get("case_type", "general")
            factors = case_data.get("factors", {})
            
            # Calculate prediction score based on factors
            prediction_score = self._calculate_prediction_score(factors)
            
            # Determine outcome probability
            outcome_probability = self._determine_outcome_probability(prediction_score, case_type)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(factors, case_type, prediction_score)
            
            # Calculate timeline estimate
            timeline_estimate = self._estimate_case_timeline(case_type, factors)
            
            # Generate risk assessment
            risk_assessment = self._assess_case_risks(factors, case_type)
            
            return {
                "success": True,
                "prediction": {
                    "case_type": case_type,
                    "outcome_probability": outcome_probability,
                    "confidence_score": prediction_score,
                    "timeline_estimate": timeline_estimate,
                    "risk_level": risk_assessment["overall_risk"],
                    "recommended_strategy": self._recommend_strategy(outcome_probability, factors),
                    "success_probability": outcome_probability["favorable"],
                    "settlement_likelihood": outcome_probability["settlement"],
                    "trial_likelihood": outcome_probability["trial"]
                },
                "recommendations": recommendations,
                "risk_factors": risk_assessment["factors"],
                "mitigation_strategies": risk_assessment["mitigation"],
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting case outcome: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _calculate_prediction_score(self, factors: Dict[str, Any]) -> float:
        """Calculate prediction score based on case factors"""
        score = 0.5  # Base score
        
        # Evidence strength (0.3 weight)
        evidence = factors.get("evidence_strength", "moderate")
        if evidence == "strong":
            score += 0.2
        elif evidence == "moderate":
            score += 0.1
        else:  # weak
            score -= 0.1
        
        # Legal precedent (0.25 weight)
        precedent = factors.get("legal_precedent", "neutral")
        if precedent == "favorable":
            score += 0.15
        elif precedent == "unfavorable":
            score -= 0.15
        
        # Client cooperation (0.2 weight)
        cooperation = factors.get("client_cooperation", "average")
        if cooperation == "excellent":
            score += 0.1
        elif cooperation == "poor":
            score -= 0.1
        
        # Case complexity (0.15 weight)
        complexity = factors.get("case_complexity", "moderate")
        if complexity == "simple":
            score += 0.05
        elif complexity == "complex":
            score -= 0.05
        
        # Opposing counsel strength (0.1 weight)
        opposing = factors.get("opposing_counsel", "moderate")
        if opposing == "weak":
            score += 0.05
        elif opposing == "strong":
            score -= 0.05
        
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1
    
    def _determine_outcome_probability(self, score: float, case_type: str) -> Dict[str, float]:
        """Determine outcome probabilities based on score and case type"""
        base_probabilities = {
            "favorable": score,
            "unfavorable": 1.0 - score,
            "settlement": min(0.8, score + 0.2),
            "trial": max(0.2, 1.0 - score - 0.2)
        }
        
        # Adjust based on case type
        if case_type == "immigration":
            base_probabilities["settlement"] *= 0.7  # Immigration cases rarely settle
        elif case_type == "family_law":
            base_probabilities["settlement"] *= 1.2  # Family law often settles
        elif case_type == "criminal_defense":
            base_probabilities["trial"] *= 1.3  # Criminal cases often go to trial
        
        # Normalize probabilities
        total = sum(base_probabilities.values())
        return {k: v/total for k, v in base_probabilities.items()}
    
    def _generate_recommendations(self, factors: Dict[str, Any], case_type: str, score: float) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on case analysis"""
        recommendations = []
        
        # Evidence-based recommendations
        evidence = factors.get("evidence_strength", "moderate")
        if evidence == "weak":
            recommendations.append({
                "category": "Evidence",
                "priority": "high",
                "recommendation": "Gather additional evidence to strengthen your case",
                "action_items": [
                    "Conduct thorough discovery",
                    "Interview additional witnesses",
                    "Obtain expert opinions",
                    "Review all available documentation"
                ]
            })
        
        # Cooperation recommendations
        cooperation = factors.get("client_cooperation", "average")
        if cooperation == "poor":
            recommendations.append({
                "category": "Client Management",
                "priority": "high",
                "recommendation": "Improve client communication and cooperation",
                "action_items": [
                    "Schedule regular check-ins",
                    "Provide clear expectations",
                    "Address client concerns promptly",
                    "Consider client counseling"
                ]
            })
        
        # Strategy recommendations based on case type
        if case_type == "immigration":
            recommendations.append({
                "category": "Strategy",
                "priority": "medium",
                "recommendation": "Focus on documentation and compliance",
                "action_items": [
                    "Ensure all forms are properly completed",
                    "Gather supporting documentation",
                    "Prepare for potential appeals",
                    "Stay updated on immigration law changes"
                ]
            })
        elif case_type == "family_law":
            recommendations.append({
                "category": "Strategy",
                "priority": "medium",
                "recommendation": "Consider mediation and settlement options",
                "action_items": [
                    "Explore mediation opportunities",
                    "Prepare settlement proposals",
                    "Focus on child welfare",
                    "Document all communications"
                ]
            })
        
        # Risk mitigation recommendations
        if score < 0.4:
            recommendations.append({
                "category": "Risk Mitigation",
                "priority": "high",
                "recommendation": "Consider alternative dispute resolution",
                "action_items": [
                    "Explore settlement options",
                    "Consider mediation",
                    "Prepare for potential adverse outcomes",
                    "Develop backup strategies"
                ]
            })
        
        return recommendations
    
    def _estimate_case_timeline(self, case_type: str, factors: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate case timeline based on type and complexity"""
        base_timelines = {
            "immigration": {"min_days": 90, "max_days": 365, "typical_days": 180},
            "family_law": {"min_days": 30, "max_days": 180, "typical_days": 90},
            "criminal_defense": {"min_days": 60, "max_days": 300, "typical_days": 120},
            "personal_injury": {"min_days": 120, "max_days": 730, "typical_days": 365},
            "business_law": {"min_days": 30, "max_days": 180, "typical_days": 90},
            "civil_rights": {"min_days": 180, "max_days": 1095, "typical_days": 365}
        }
        
        timeline = base_timelines.get(case_type, base_timelines["business_law"])
        complexity = factors.get("case_complexity", "moderate")
        
        # Adjust based on complexity
        if complexity == "complex":
            timeline["typical_days"] = int(timeline["typical_days"] * 1.5)
            timeline["max_days"] = int(timeline["max_days"] * 1.3)
        elif complexity == "simple":
            timeline["typical_days"] = int(timeline["typical_days"] * 0.7)
            timeline["max_days"] = int(timeline["max_days"] * 0.8)
        
        # Calculate estimated dates
        start_date = datetime.now()
        estimated_completion = start_date + timedelta(days=timeline["typical_days"])
        
        return {
            "estimated_duration_days": timeline["typical_days"],
            "estimated_completion_date": estimated_completion.isoformat(),
            "confidence_range": {
                "min_days": timeline["min_days"],
                "max_days": timeline["max_days"]
            },
            "milestones": self._generate_case_milestones(case_type, timeline["typical_days"])
        }
    
    def _generate_case_milestones(self, case_type: str, duration_days: int) -> List[Dict[str, Any]]:
        """Generate case milestones based on type and duration"""
        milestones = []
        
        if case_type == "immigration":
            milestones = [
                {"phase": "Initial Filing", "days_from_start": 0, "description": "Submit initial application"},
                {"phase": "Evidence Gathering", "days_from_start": 30, "description": "Collect supporting documents"},
                {"phase": "Interview Preparation", "days_from_start": 90, "description": "Prepare for USCIS interview"},
                {"phase": "Decision", "days_from_start": duration_days, "description": "Receive final decision"}
            ]
        elif case_type == "family_law":
            milestones = [
                {"phase": "Petition Filing", "days_from_start": 0, "description": "File divorce petition"},
                {"phase": "Discovery", "days_from_start": 30, "description": "Exchange financial information"},
                {"phase": "Mediation", "days_from_start": 60, "description": "Attempt settlement mediation"},
                {"phase": "Final Hearing", "days_from_start": duration_days, "description": "Court hearing and judgment"}
            ]
        else:
            milestones = [
                {"phase": "Case Initiation", "days_from_start": 0, "description": "File initial pleadings"},
                {"phase": "Discovery", "days_from_start": duration_days // 3, "description": "Evidence gathering phase"},
                {"phase": "Pre-trial", "days_from_start": (duration_days * 2) // 3, "description": "Pre-trial preparations"},
                {"phase": "Resolution", "days_from_start": duration_days, "description": "Case resolution"}
            ]
        
        return milestones
    
    def _assess_case_risks(self, factors: Dict[str, Any], case_type: str) -> Dict[str, Any]:
        """Assess potential risks and mitigation strategies"""
        risks = []
        mitigation = []
        
        # Evidence risks
        evidence = factors.get("evidence_strength", "moderate")
        if evidence == "weak":
            risks.append({
                "risk": "Insufficient Evidence",
                "impact": "high",
                "probability": 0.8,
                "description": "Weak evidence may lead to unfavorable outcome"
            })
            mitigation.append({
                "strategy": "Evidence Strengthening",
                "description": "Focus on gathering additional evidence and expert testimony"
            })
        
        # Cooperation risks
        cooperation = factors.get("client_cooperation", "average")
        if cooperation == "poor":
            risks.append({
                "risk": "Client Non-cooperation",
                "impact": "medium",
                "probability": 0.6,
                "description": "Poor client cooperation may hinder case progress"
            })
            mitigation.append({
                "strategy": "Client Management",
                "description": "Implement regular communication and expectation setting"
            })
        
        # Legal precedent risks
        precedent = factors.get("legal_precedent", "neutral")
        if precedent == "unfavorable":
            risks.append({
                "risk": "Unfavorable Precedent",
                "impact": "high",
                "probability": 0.7,
                "description": "Existing case law may work against your position"
            })
            mitigation.append({
                "strategy": "Legal Research",
                "description": "Find distinguishing factors and alternative legal theories"
            })
        
        # Calculate overall risk level
        if not risks:
            overall_risk = "low"
        elif any(r["impact"] == "high" for r in risks):
            overall_risk = "high"
        else:
            overall_risk = "medium"
        
        return {
            "overall_risk": overall_risk,
            "factors": risks,
            "mitigation": mitigation
        }
    
    def _recommend_strategy(self, outcome_probability: Dict[str, float], factors: Dict[str, Any]) -> str:
        """Recommend overall case strategy based on analysis"""
        favorable_prob = outcome_probability["favorable"]
        settlement_prob = outcome_probability["settlement"]
        
        if settlement_prob > 0.7:
            return "Focus on settlement negotiations"
        elif favorable_prob > 0.6:
            return "Aggressive litigation strategy"
        elif favorable_prob < 0.4:
            return "Defensive strategy with settlement focus"
        else:
            return "Balanced approach with multiple options"
    
    def get_analytics_dashboard_data(self) -> Dict[str, Any]:
        """Get data for analytics dashboard"""
        try:
            # Simulate historical case data
            historical_cases = self._generate_historical_data()
            
            # Calculate success rates by case type
            success_rates = {}
            for case_type in self.case_types:
                cases = [c for c in historical_cases if c["case_type"] == case_type]
                if cases:
                    success_rate = sum(1 for c in cases if c["outcome"] == "favorable") / len(cases)
                    success_rates[case_type] = success_rate
            
            # Calculate average timeline by case type
            timelines = {}
            for case_type in self.case_types:
                cases = [c for c in historical_cases if c["case_type"] == case_type]
                if cases:
                    avg_duration = sum(c["duration_days"] for c in cases) / len(cases)
                    timelines[case_type] = avg_duration
            
            return {
                "success": True,
                "analytics": {
                    "success_rates": success_rates,
                    "average_timelines": timelines,
                    "total_cases_analyzed": len(historical_cases),
                    "recommendation_accuracy": 0.78,  # Simulated accuracy
                    "client_satisfaction": 0.85,  # Simulated satisfaction
                    "case_completion_rate": 0.92  # Simulated completion rate
                },
                "trends": self._analyze_trends(historical_cases),
                "insights": self._generate_insights(success_rates, timelines)
            }
            
        except Exception as e:
            logger.error(f"Error getting analytics dashboard data: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_historical_data(self) -> List[Dict[str, Any]]:
        """Generate simulated historical case data"""
        cases = []
        for i in range(100):  # Generate 100 sample cases
            case_type = random.choice(self.case_types)
            outcome = random.choice(["favorable", "unfavorable", "settlement"])
            duration = random.randint(30, 365)
            
            cases.append({
                "case_id": f"CASE_{i+1:04d}",
                "case_type": case_type,
                "outcome": outcome,
                "duration_days": duration,
                "client_satisfaction": random.uniform(0.6, 1.0),
                "complexity": random.choice(["simple", "moderate", "complex"]),
                "settlement_amount": random.randint(5000, 500000) if outcome == "settlement" else None
            })
        
        return cases
    
    def _analyze_trends(self, cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in case data"""
        return {
            "most_successful_case_type": max(self.case_types, key=lambda t: 
                sum(1 for c in cases if c["case_type"] == t and c["outcome"] == "favorable") / 
                max(1, sum(1 for c in cases if c["case_type"] == t))
            ),
            "average_settlement_amount": sum(c["settlement_amount"] for c in cases if c["settlement_amount"]) / 
                max(1, sum(1 for c in cases if c["settlement_amount"])),
            "most_common_outcome": max(["favorable", "unfavorable", "settlement"], 
                key=lambda o: sum(1 for c in cases if c["outcome"] == o))
        }
    
    def _generate_insights(self, success_rates: Dict[str, float], timelines: Dict[str, float]) -> List[str]:
        """Generate insights from analytics data"""
        insights = []
        
        best_case_type = max(success_rates.keys(), key=lambda k: success_rates[k])
        insights.append(f"Highest success rate: {best_case_type} cases ({success_rates[best_case_type]:.1%})")
        
        fastest_case_type = min(timelines.keys(), key=lambda k: timelines[k])
        insights.append(f"Fastest resolution: {fastest_case_type} cases (avg {timelines[fastest_case_type]:.0f} days)")
        
        if success_rates.get("immigration", 0) > 0.7:
            insights.append("Immigration cases show strong success rates - consider expanding this practice area")
        
        if timelines.get("family_law", 0) < 90:
            insights.append("Family law cases resolve quickly - good for client satisfaction")
        
        return insights

from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
import json
from dataclasses import dataclass
from typing_extensions import TypedDict
from datetime import datetime
import os

class BusinessState(TypedDict):
    """State schema for business data analysis"""
    input_data: Dict[str, Any]
    metrics: Dict[str, float]
    alerts: List[str]
    recommendations: List[str]
    output: Dict[str, Any]

def input_node(state: BusinessState) -> BusinessState:
    """Process input business data"""
    data = state.get("input_data", {})
    
    # Validate required fields
    required_fields = ["daily_revenue", "daily_cost", "number_of_customers", 
                      "previous_day_revenue", "previous_day_cost", "previous_day_customers"]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    print(f"✅ Input data validated: {json.dumps(data, indent=2)}")
    return state

def processing_node(state: BusinessState) -> BusinessState:
    """Calculate key business metrics"""
    data = state["input_data"]
    
    # Calculate current day metrics
    daily_profit = data["daily_revenue"] - data["daily_cost"]
    current_cac = data["daily_cost"] / data["number_of_customers"] if data["number_of_customers"] > 0 else 0
    
    # Calculate previous day metrics for comparison
    prev_profit = data["previous_day_revenue"] - data["previous_day_cost"]
    prev_cac = data["previous_day_cost"] / data["previous_day_customers"] if data["previous_day_customers"] > 0 else 0
    
    # Calculate percentage changes
    revenue_change = ((data["daily_revenue"] - data["previous_day_revenue"]) / data["previous_day_revenue"] * 100) if data["previous_day_revenue"] > 0 else 0
    cost_change = ((data["daily_cost"] - data["previous_day_cost"]) / data["previous_day_cost"] * 100) if data["previous_day_cost"] > 0 else 0
    cac_change = ((current_cac - prev_cac) / prev_cac * 100) if prev_cac > 0 else 0
    
    metrics = {
        "daily_profit": daily_profit,
        "current_cac": current_cac,
        "previous_cac": prev_cac,
        "revenue_change_percent": revenue_change,
        "cost_change_percent": cost_change,
        "cac_change_percent": cac_change,
        "profit_status": "positive" if daily_profit > 0 else "negative"
    }
    
    state["metrics"] = metrics
    print(f"📊 Metrics calculated: {json.dumps(metrics, indent=2)}")
    return state

def recommendation_node(state: BusinessState) -> BusinessState:
    """Generate recommendations based on metrics"""
    metrics = state["metrics"]
    alerts = []
    recommendations = []
    
    # Profit/Loss Analysis
    if metrics["daily_profit"] < 0:
        alerts.append("⚠️ Daily profit is negative")
        recommendations.append("Reduce operational costs to improve profitability")
    else:
        recommendations.append("✅ Maintain current profitable operations")
    
    # CAC Analysis
    if metrics["cac_change_percent"] > 20:
        alerts.append(f"🚨 CAC increased by {metrics['cac_change_percent']:.1f}% (>20% threshold)")
        recommendations.append("Review marketing campaigns and optimize customer acquisition strategies")
    
    # Revenue Growth Analysis
    if metrics["revenue_change_percent"] > 10:
        recommendations.append("📈 Strong revenue growth detected - consider increasing advertising budget")
    elif metrics["revenue_change_percent"] < -10:
        alerts.append("📉 Revenue declined significantly")
        recommendations.append("Investigate market conditions and adjust sales strategy")
    
    # Cost Management
    if metrics["cost_change_percent"] > 15:
        alerts.append("💰 Costs increased significantly")
        recommendations.append("Review and optimize cost structure")
    
    # Combined Analysis
    if metrics["revenue_change_percent"] > 0 and metrics["daily_profit"] > 0:
        recommendations.append("🎯 Business is growing profitably - consider scaling operations")
    
    state["alerts"] = alerts
    state["recommendations"] = recommendations
    
    print(f"💡 Generated {len(alerts)} alerts and {len(recommendations)} recommendations")
    return state

def output_node(state: BusinessState) -> BusinessState:
    """Format final output"""
    metrics = state["metrics"]
    
    output = {
        "analysis_timestamp": datetime.now().isoformat(),
        "profit_loss_status": {
            "daily_profit": metrics["daily_profit"],
            "status": metrics["profit_status"],
            "revenue_change_percent": round(metrics["revenue_change_percent"], 2),
            "cost_change_percent": round(metrics["cost_change_percent"], 2)
        },
        "customer_acquisition": {
            "current_cac": round(metrics["current_cac"], 2),
            "previous_cac": round(metrics["previous_cac"], 2),
            "cac_change_percent": round(metrics["cac_change_percent"], 2),
            "cac_alert": metrics["cac_change_percent"] > 20
        },
        "alerts": state["alerts"],
        "recommendations": state["recommendations"],
        "summary": {
            "total_alerts": len(state["alerts"]),
            "total_recommendations": len(state["recommendations"]),
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "agent_version": "1.0.0"
        },
        "input_data": state["input_data"]
    }
    
    state["output"] = output
    print("📋 Final output generated")
    return state

def create_business_agent():
    """Create the LangGraph business intelligence agent"""
    
    # Create state graph
    workflow = StateGraph(BusinessState)
    
    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("processing", processing_node) 
    workflow.add_node("recommendation", recommendation_node)
    workflow.add_node("output", output_node)
    
    # Define edges (flow)
    workflow.add_edge(START, "input")
    workflow.add_edge("input", "processing")
    workflow.add_edge("processing", "recommendation")
    workflow.add_edge("recommendation", "output")
    workflow.add_edge("output", END)
    
    # Compile the graph
    agent = workflow.compile()
    return agent

def save_to_json(data: Dict[str, Any], filename: str = "langgraph.json") -> None:
    """Save analysis results to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Results saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to {filename}: {e}")

def run_business_analysis(input_data: Dict[str, Any], save_to_file: bool = True) -> Dict[str, Any]:
    """Run the business analysis agent"""
    agent = create_business_agent()
    
    initial_state = BusinessState(
        input_data=input_data,
        metrics={},
        alerts=[],
        recommendations=[],
        output={}
    )
    
    print("🚀 Starting business analysis...")
    result = agent.invoke(initial_state)
    print("✅ Analysis completed!")
    
    # Save to JSON file if requested
    if save_to_file:
        save_to_json(result["output"], "langgraph.json")
    
    return result["output"]

def run_multiple_scenarios():
    """Run analysis on multiple business scenarios and save each to separate files"""
    
    scenarios = {
        "profitable_growth": {
            "daily_revenue": 8000,
            "daily_cost": 5000,
            "number_of_customers": 80,
            "previous_day_revenue": 7000,
            "previous_day_cost": 4500,
            "previous_day_customers": 75
        },
        "loss_scenario": {
            "daily_revenue": 3000,
            "daily_cost": 4500,
            "number_of_customers": 30,
            "previous_day_revenue": 4000,
            "previous_day_cost": 3500,
            "previous_day_customers": 40
        },
        "high_cac_alert": {
            "daily_revenue": 6000,
            "daily_cost": 5000,
            "number_of_customers": 25,  # Low customers = high CAC
            "previous_day_revenue": 6000,
            "previous_day_cost": 3000,
            "previous_day_customers": 60  # Much higher customers before
        }
    }
    
    print("🎯 Running multiple business scenarios...")
    results = {}
    
    for scenario_name, data in scenarios.items():
        print(f"\n📊 Analyzing scenario: {scenario_name}")
        result = run_business_analysis(data, save_to_file=False)
        results[scenario_name] = result
        
        # Save individual scenario result
        filename = f"langgraph_{scenario_name}.json"
        save_to_json(result, filename)
    
    # Save combined results
    combined_results = {
        "analysis_summary": {
            "total_scenarios": len(scenarios),
            "analysis_timestamp": datetime.now().isoformat(),
            "scenarios_analyzed": list(scenarios.keys())
        },
        "results": results
    }
    
    save_to_json(combined_results, "langgraph_combined.json")
    print("\n🎉 All scenarios analyzed and saved!")
    
    return combined_results

# Example usage
if __name__ == "__main__":
    # Single analysis example
    print("=" * 60)
    print("🏢 BUSINESS INTELLIGENCE AGENT - LANGGRAPH")
    print("=" * 60)
    
    sample_data = {
        "daily_revenue": 5000,
        "daily_cost": 3000,
        "number_of_customers": 50,
        "previous_day_revenue": 4500,
        "previous_day_cost": 2500,
        "previous_day_customers": 45
    }
    
    # Run single analysis
    result = run_business_analysis(sample_data)
    
    print("\n📊 BUSINESS ANALYSIS REPORT:")
    print("=" * 50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Ask user if they want to run multiple scenarios
    print("\n" + "=" * 60)
    user_input = input("🤔 Would you like to run multiple scenarios? (y/n): ")
    
    if user_input.lower() in ['y', 'yes']:
        combined_results = run_multiple_scenarios()
        print("\n📁 Files created:")
        print("- langgraph.json (main analysis)")
        print("- langgraph_profitable_growth.json")
        print("- langgraph_loss_scenario.json") 
        print("- langgraph_high_cac_alert.json")
        print("- langgraph_combined.json (all scenarios)")
    else:
        print("📁 Main analysis saved to: langgraph.json")
    
    print("\n✨ Analysis complete! Check the JSON files for detailed results.")

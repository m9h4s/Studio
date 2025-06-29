# 🤖 Business Intelligence AI Agent

A powerful LangGraph-based AI agent that analyzes business data, provides actionable insights, and generates comprehensive reports with visual dashboards.

## ✨ Key Features

- **📊 Daily Profit Analysis**: Real-time profit/loss calculations with trend comparisons
- **💰 Customer Acquisition Cost (CAC) Monitoring**: Smart alerts when CAC increases >20%
- **📈 Revenue & Cost Trend Analysis**: Monitors percentage changes with intelligent thresholds
- **🎯 Automated Recommendations**: AI-powered actionable business advice
- **⚠️ Smart Alerts**: Proactive warnings for concerning business metrics
- **📄 JSON Export**: Structured data output for integration with other systems
- **🌐 Interactive Dashboard**: Beautiful HTML visualization of your business metrics

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Agent
```python
# Simple execution - generates JSON output
python agent.py
```

This command will:
- ✅ Analyze your business data
- 📁 Generate structured JSON output files
- 🎨 Create an interactive HTML dashboard
- 📊 Display comprehensive business insights

### 3. View Results
- **JSON Output**: Check generated `.json` files for structured data
- **Visual Dashboard**: Open `business_dashboard.html` in your browser for interactive charts
- **Console Output**: View summary directly in terminal

### 4. Custom Data Analysis
```python
from agent import run_business_analysis

# Your business data
data = {
    "daily_revenue": 5000,
    "daily_cost": 3000,
    "number_of_customers": 50,
    "previous_day_revenue": 4500,
    "previous_day_cost": 2500,
    "previous_day_customers": 45
}

result = run_business_analysis(data)
print(result)
```

### 5. Run Tests
```bash
python test_agent.py
```

## 📊 Output Formats

### JSON Export
The agent automatically generates structured JSON files containing:
- Detailed profit/loss analysis
- CAC calculations and trends
- Revenue and cost metrics
- Automated recommendations
- Business alerts and warnings

### Interactive HTML Dashboard
View your business metrics through our beautiful dashboard:
- 📈 Real-time charts and graphs
- 🎯 Key performance indicators
- 📊 Trend analysis visualizations
- 🚨 Alert notifications
- 💡 Recommendation highlights

## 🎛️ LangGraph Studio Integration

This project is fully configured for LangGraph Studio:
1. Import the entire project folder
2. Test the agent interactively
3. Visualize the workflow graph
4. Debug and optimize performance

Configuration file: `langgraph.json`

## 📥 Input Data Structure

```json
{
  "daily_revenue": 5000,
  "daily_cost": 3000,
  "number_of_customers": 50,
  "previous_day_revenue": 4500,
  "previous_day_cost": 2500,
  "previous_day_customers": 45
}
```

## 📤 Output Structure

```json
{
  "profit_loss_status": {
    "daily_profit": 2000,
    "status": "positive",
    "revenue_change_percent": 11.11,
    "cost_change_percent": 20.0
  },
  "customer_acquisition": {
    "current_cac": 60.0,
    "cac_change_percent": 8.0,
    "cac_alert": false
  },
  "alerts": [
    "💰 Costs increased significantly"
  ],
  "recommendations": [
    "✅ Maintain current profitable operations",
    "📈 Strong revenue growth detected",
    "🎯 Consider scaling operations"
  ],
  "summary": {
    "total_alerts": 1,
    "total_recommendations": 4,
    "analysis_date": "2024-01-01"
  }
}
```

## 🧮 Business Intelligence Logic

### Core Metrics
- **Daily Profit**: `daily_revenue - daily_cost`
- **CAC**: `daily_cost / number_of_customers`
- **Revenue Change**: `(current - previous) / previous × 100`
- **Cost Change**: `(current - previous) / previous × 100`

### Smart Alert System
| Condition | Alert Trigger |
|-----------|---------------|
| Negative Profit | Immediate alert |
| CAC Increase | >20% increase |
| Revenue Decline | >10% decrease |
| Cost Spike | >15% increase |

### AI Recommendations
- 💡 Cost optimization strategies
- 📈 Marketing budget adjustments
- 🎯 Scaling recommendations
- ⚠️ Risk mitigation advice

## 🏗️ Architecture

### LangGraph Workflow
```
Input → Processing → Analysis → Recommendations → Output
  ↓         ↓          ↓            ↓            ↓
Validate   Calculate   Generate     Format      Export
Data       Metrics     Insights     Report      Files
```

### Technology Stack
- **🧠 LangGraph**: Workflow orchestration and state management
- **🐍 Python**: Business logic and calculations
- **📊 JSON**: Data serialization and API integration
- **🌐 HTML/CSS/JS**: Interactive dashboard visualization
- **🧪 unittest**: Comprehensive testing framework

## 🧪 Testing Suite

Comprehensive test coverage includes:
- ✅ Profitable business scenarios
- ❌ Loss scenarios and edge cases
- 📊 High CAC alert testing
- 🔢 Metric calculation accuracy
- 💡 Recommendation logic validation
- 📥 Input validation and error handling
- 📤 Output format compliance

## 🔄 Usage Examples

### Daily Business Review
```bash
# Quick daily analysis
python agent.py

# Check dashboard
open business_dashboard.html
```

### Integration with Business Systems
```python
# API integration example
import requests
from agent import run_business_analysis

# Fetch data from your business system
business_data = fetch_daily_metrics()

# Analyze with AI agent
insights = run_business_analysis(business_data)

# Send to dashboard or notification system
update_business_dashboard(insights)
```

## 📈 Advanced Features

- **Trend Analysis**: Multi-day trend detection
- **Predictive Insights**: Future performance indicators
- **Custom Thresholds**: Configurable alert levels
- **Export Options**: Multiple output formats
- **Real-time Updates**: Live dashboard refresh

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit a pull request

## 📄 License

MIT License - Open source and free to use for commercial projects.

---

## 🎯 Getting Started in 30 Seconds

1. `python agent.py` - Run analysis
2. Open `business_dashboard.html` - View results
3. Check JSON files - Integrate with your systems

**Ready to transform your business intelligence? Start analyzing now!** 🚀

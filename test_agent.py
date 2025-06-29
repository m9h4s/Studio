import unittest
import json
from simple_agent import run_business_analysis, create_business_agent, BusinessState

class TestBusinessAgent(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.agent = create_business_agent()
        
        # Sample data for testing
        self.sample_data_profitable = {
            "daily_revenue": 5000,
            "daily_cost": 3000,
            "number_of_customers": 50,
            "previous_day_revenue": 4500,
            "previous_day_cost": 2500,
            "previous_day_customers": 45
        }
        
        self.sample_data_loss = {
            "daily_revenue": 2000,
            "daily_cost": 3000,
            "number_of_customers": 40,
            "previous_day_revenue": 2500,
            "previous_day_cost": 2000,
            "previous_day_customers": 50
        }
        
        self.sample_data_high_cac = {
            "daily_revenue": 4000,
            "daily_cost": 3000,
            "number_of_customers": 20,  # Lower customers = higher CAC
            "previous_day_revenue": 4000,
            "previous_day_cost": 2000,
            "previous_day_customers": 40  # Much higher customers before = CAC increased significantly
        }

    def test_profitable_scenario(self):
        """Test agent with profitable business scenario"""
        result = run_business_analysis(self.sample_data_profitable)
        
        # Test profit status
        self.assertEqual(result["profit_loss_status"]["status"], "positive")
        self.assertGreater(result["profit_loss_status"]["daily_profit"], 0)
        
        # Test output structure
        self.assertIn("profit_loss_status", result)
        self.assertIn("customer_acquisition", result)
        self.assertIn("alerts", result)
        self.assertIn("recommendations", result)
        self.assertIn("summary", result)
        
        # Test that we have recommendations
        self.assertGreater(len(result["recommendations"]), 0)
        
        print("✅ Profitable scenario test passed")

    def test_loss_scenario(self):
        """Test agent with loss scenario"""
        result = run_business_analysis(self.sample_data_loss)
        
        # Test profit status
        self.assertEqual(result["profit_loss_status"]["status"], "negative")
        self.assertLess(result["profit_loss_status"]["daily_profit"], 0)
        
        # Should have alerts for negative profit
        alert_messages = " ".join(result["alerts"])
        self.assertIn("negative", alert_messages.lower())
        
        # Should have cost reduction recommendation
        recommendations = " ".join(result["recommendations"])
        self.assertIn("cost", recommendations.lower())
        
        print("✅ Loss scenario test passed")

    def test_high_cac_scenario(self):
        """Test agent with high CAC increase scenario"""
        result = run_business_analysis(self.sample_data_high_cac)
        
        # Should detect CAC increase
        cac_change = result["customer_acquisition"]["cac_change_percent"]
        self.assertGreater(abs(cac_change), 20)  # Should be more than 20%
        
        # Should have CAC alert
        self.assertTrue(result["customer_acquisition"]["cac_alert"])
        
        # Should have marketing review recommendation
        alert_messages = " ".join(result["alerts"])
        recommendations = " ".join(result["recommendations"])
        
        self.assertTrue("CAC" in alert_messages or "marketing" in recommendations.lower())
        
        print("✅ High CAC scenario test passed")

    def test_metrics_calculation_accuracy(self):
        """Test accuracy of metric calculations"""
        result = run_business_analysis(self.sample_data_profitable)
        
        # Manual calculations for verification
        expected_profit = 5000 - 3000  # 2000
        expected_cac = 3000 / 50  # 60
        expected_revenue_change = ((5000 - 4500) / 4500) * 100  # 11.11%
        expected_cost_change = ((3000 - 2500) / 2500) * 100  # 20%
        
        self.assertEqual(result["profit_loss_status"]["daily_profit"], expected_profit)
        self.assertEqual(result["customer_acquisition"]["current_cac"], expected_cac)
        self.assertAlmostEqual(result["profit_loss_status"]["revenue_change_percent"], expected_revenue_change, places=1)
        self.assertAlmostEqual(result["profit_loss_status"]["cost_change_percent"], expected_cost_change, places=1)
        
        print("✅ Metrics calculation accuracy test passed")

    def test_recommendation_logic(self):
        """Test recommendation generation logic"""
        
        # Test profitable case recommendations
        result_profit = run_business_analysis(self.sample_data_profitable)
        profit_recs = " ".join(result_profit["recommendations"]).lower()
        self.assertIn("maintain", profit_recs)  # Should maintain profitable operations
        
        # Test loss case recommendations  
        result_loss = run_business_analysis(self.sample_data_loss)
        loss_recs = " ".join(result_loss["recommendations"]).lower()
        self.assertIn("reduce", loss_recs)  # Should reduce costs
        
        print("✅ Recommendation logic test passed")

    def test_input_validation(self):
        """Test input validation"""
        invalid_data = {
            "daily_revenue": 5000,
            # Missing required fields
        }
        
        with self.assertRaises(ValueError):
            run_business_analysis(invalid_data)
            
        print("✅ Input validation test passed")

    def test_edge_cases(self):
        """Test edge cases like zero customers"""
        edge_case_data = {
            "daily_revenue": 1000,
            "daily_cost": 500,
            "number_of_customers": 0,  # Zero customers
            "previous_day_revenue": 1000,
            "previous_day_cost": 500,
            "previous_day_customers": 1
        }
        
        # Should handle zero customers without crashing
        result = run_business_analysis(edge_case_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["customer_acquisition"]["current_cac"], 0)
        
        print("✅ Edge cases test passed")

    def test_output_format(self):
        """Test output format compliance"""
        result = run_business_analysis(self.sample_data_profitable)
        
        # Required output structure
        required_keys = ["profit_loss_status", "customer_acquisition", "alerts", "recommendations", "summary"]
        for key in required_keys:
            self.assertIn(key, result)
        
        # Profit/loss status should have required fields
        profit_status = result["profit_loss_status"]
        self.assertIn("daily_profit", profit_status)
        self.assertIn("status", profit_status)
        
        # Customer acquisition should have required fields
        cac_info = result["customer_acquisition"]
        self.assertIn("current_cac", cac_info)
        self.assertIn("cac_alert", cac_info)
        
        # Alerts and recommendations should be lists
        self.assertIsInstance(result["alerts"], list)
        self.assertIsInstance(result["recommendations"], list)
        
        print("✅ Output format test passed")

def run_comprehensive_test():
    """Run comprehensive test with detailed output"""
    print("🧪 RUNNING COMPREHENSIVE BUSINESS AGENT TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBusinessAgent)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n📊 TEST SUMMARY:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
        
    return result.wasSuccessful()

if __name__ == "__main__":
    # Run comprehensive tests
    run_comprehensive_test()
    
    print(f"\n🔬 SAMPLE TEST EXECUTION:")
    print("-" * 40)
    
    # Demo with sample data
    sample_data = {
        "daily_revenue": 6000,
        "daily_cost": 4000,
        "number_of_customers": 60,
        "previous_day_revenue": 5000,
        "previous_day_cost": 3000,
        "previous_day_customers": 50
    }
    
    result = run_business_analysis(sample_data)
    print("Sample Analysis Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
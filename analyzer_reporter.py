import os
import json
from datetime import datetime
from analyzer_logic import AnalyzerLogic

class AnalyzerReporter:
    def __init__(self, deals_dir, comms_dir, reports_dir):
        self.deals_dir = deals_dir
        self.comms_dir = comms_dir
        self.reports_dir = reports_dir
        self.analyzer = AnalyzerLogic(deals_dir, comms_dir)

    def run_and_report(self):
        # 1. Ensure reports directory exists
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
            print(f"Created reports directory: {self.reports_dir}")

        # 2. Run the analysis
        print("Executing analysis engine...")
        issues = self.analyzer.analyze()
        
        # 3. Prepare metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"analysis_report_{timestamp}.json"
        report_path = os.path.join(self.reports_dir, report_filename)
        
        # Count total deals processed (we can infer this from the analyzer)
        # A better way would be to expose this in AnalyzerLogic, 
        # but for now, we will count files in the deals directory.
        total_deals = len([f for f in os.listdir(self.deals_dir) if f.endswith('.json')])

        report_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_deals_analyzed": total_deals,
                "total_issues_found": len(issues),
                "engine_version": "1.0.0"
            },
            "findings": issues
        }

        # 4. Save the report
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=4)
        
        print(f"✅ Report generated successfully: {report_path}")
        return report_path

if __name__ == "__main__":
    # Paths relative to the project root
    DEALS_DIR = "hubspot_momentum/data/deals"
    COMMS_DIR = "hubspot_momentum/data/communications"
    REPORTS_DIR = "hubspot_momentum/data/reports"
    
    reporter = AnalyzerReporter(DEALS_DIR, COMMS_DIR, REPORTS_DIR)
    reporter.run_and_report()

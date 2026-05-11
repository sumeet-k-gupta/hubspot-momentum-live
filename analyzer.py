import json
import os
from datetime import datetime

class HubSpotAnalyzer:
    def __init__(self, base_path="data"):
        self.base_path = base_path
        self.deal_dir = os.path.join(self.base_path, "deals")
        self.comm_dir = os.path.join(self.base_path, "communications")
        self.reports_dir = os.path.join(self.base_path, "reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def analyze(self):
        findings = []
        
        # Load all deals
        deals = []
        if not os.path.exists(self.deal_dir):
            return {"error": "Deal directory not found"}
            
        for filename in os.listdir(self.deal_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.deal_dir, filename), 'r') as f:
                    deals.append(json.load(f))

        # Load all communications
        comms_by_deal = {deal['id']: [] for deal in deals}
        if os.path.exists(self.comm_dir):
            for filename in os.listdir(self.comm_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(self.comm_dir, filename), 'r') as f:
                        comm = json.load(f)
                        deal_id = comm['deal_id']
                        if deal_id in comms_by_deal:
                            comms_by_deal[deal_id].append(comm)

        for deal in deals:
            deal_id = deal['id']
            deal_comms = comms_by_deal.get(deal_id, [])
            
            # Metric: Last communication timestamp
            last_comm_date = None
            status = "Active"
            
            if not deal_comms:
                status = "No Communications"
            else:
                # Sort by timestamp descending
                deal_comms.sort(key=lambda x: x['timestamp'], reverse=True)
                last_comm_date = datetime.fromisoformat(deal_comms[0]['timestamp'])
                
                # Check for "Ghosting" - pattern of decay in content or long silence
                content_decay = any(c['content'] in ["K.", "...", "."] for c in deal_comms)
                
                if content_decay:
                    status = "Ghosting Detected (Content Decay)"
                elif (datetime.now() - last_comm_date).days > 15:
                    status = "Ghosting Detected (Silence)"

            findings.append({
                "deal_id": deal_id,
                "name": deal['name'],
                "stage": deal['stage'],
                "amount": deal['amount'],
                "status": status,
                "last_comm_date": last_comm_date.isoformat() if last_comm_date else None,
                "comm_count": len(deal_comms)
            })

        self._save_report(findings)
        return findings

    def _save_report(self, findings):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"analysis_report_{timestamp}.json")
        with open(report_path, 'w') as f:
            json.dump(findings, f, indent=4)
        return report_path

if __name__ == "__main__":
    analyzer = HubSpotAnalyzer(base_path="hubspot_momentum/data")
    results = analyzer.analyze()
    print(f"Analysis complete. Processed {len(results)} deals.")

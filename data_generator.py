import json
import random
import os
from datetime import datetime, timedelta

# Define the single source of truth for the data directory
PROJECT_ROOT = os.path.abspath(".")
DATA_DIR = os.path.join(PROJECT_ROOT, "hubspot_momentum", "data")
DEAL_DIR = os.path.join(DATA_DIR, "deals")
COMM_DIR = os.path.join(DATA_DIR, "communications")

class MockHubSpot:
    def __init__(self, num_deals=15):
        self.num_deals = num_deals
        self.deal_dir = DEAL_DIR
        self.comm_dir = COMM_DIR
        
        # Ensure the correct directory structure exists
        os.makedirs(self.deal_dir, exist_ok=True)
        os.makedirs(self.comm_dir, exist_ok=True)

    def generate(self):
        # We are already ensuring directories exist in __init__
        deal_ids = []
        for i in range(self.num_deals):
            deal_id = f"deal_{i}"
            deal_ids.append(deal_id)
            stage = random.choice(["Appointment Scheduled", "Qualified to Buy", "Presentation Decision Made", "Decision Maker Decision Made", "Closed Won", "Closed Lost"])
            amount = random.randint(5000, 50000)
            
            deal_data = {
                "id": deal_id,
                "name": f"Prospect {i}",
                "stage": stage,
                "amount": amount,
                "created_at": (datetime.now() - timedelta(days=random.randint(30, 90))).isoformat()
            }
            with open(os.path.join(self.deal_dir, f"{deal_id}.json"), "w") as f:
                json.dump(deal_data, f)

        for deal_id in deal_ids:
            num_comms = random.randint(3, 12)
            for comm_idx in range(num_comms):
                timestamp = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 24))
                is_dying = (deal_id == "deal_0")
                
                content_templates = ["Great meeting you!", "Following up.", "Checking in.", "Please let me know.", "Any update?", "K.", "...", "."]
                content = random.choice(content_templates)
                if is_dying and random.random() > 0.3:
                    content = random.choice(["K.", "...", "."])
                
                comm_data = {
                    "id": f"comm_{deal_id}_{comm_idx}",
                    "deal_id": deal_id,
                    "timestamp": timestamp.isoformat(),
                    "type": random.choice(["email", "note", "call"]),
                    "content": content,
                    "sender": "sales_rep@company.com",
                    "recipient": f"prospect_{deal_id}@client.com",
                    "stakeholders_count": random.randint(1, 5)
                }
                with open(os.path.join(self.comm_dir, f"{comm_data['id']}.json"), "w") as f:
                    json.dump(comm_data, f)
        print(f"Successfully generated {self.num_deals} deals in {DATA_DIR}")

if __name__ == "__main__":
    generator = MockHubSpot()
    generator.generate()

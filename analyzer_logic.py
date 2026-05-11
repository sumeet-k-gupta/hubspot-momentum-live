import os
import json
import glob
from datetime import datetime

class AnalyzerLogic:
    def __init__(self, deals_dir, comms_dir):
        self.deals_dir = deals_dir
        self.comms_dir = comms_dir
        self.ghosting_threshold_days = 7
        self.decay_threshold_days = 14

    def load_data(self):
        deals = []
        # Load deal files
        for deal_file in glob.glob(os.path.join(self.deals_dir, "deal_*.json")):
            with open(deal_file, 'r') as f:
                # The files are newline-delimited JSONs in the current setup
                # but may contain single objects. Handling both.
                try:
                    content = f.read().strip()
                    if content:
                        deals.append(json.loads(content))
                except json.JSONDecodeError:
                    pass

        # Load communications
        comms = []
        for comm_file in glob.glob(os.path.join(self.comms_dir, "comm_deal_*.json")):
            with open(comm_file, 'r') as f:
                try:
                    content = f.read().strip()
                    if content:
                        comms.append(json.loads(content))
                except json.JSONCRDecodeError:
                    pass
        
        return deals, comms

    def analyze(self):
        deals, comms = self.load_data()
        ghosting_events = []
        decay_events = []
        
        # Group comms by deal
        deal_comms = {deal['id']: [] for deal in deals}
        for comm in comms:
            d_id = comm.get('deal_id')
            if d_id in deal_comms:
                deal_comms[d_id].append(comm)

        # Sort comms by timestamp for each deal
        for d_id in deal_comms:
            deal_comms[d_id].sort(key=lambda x: x['timestamp'])

        now = datetime.now() # In a real scenario, this would be the "current" date of the simulation

        for deal in deals:
            d_id = deal['id']
            d_comms = deal_comms[d_id]
            
            if not d_comms:
                # No comms at all since creation
                ghosting_events.append({
                    "deal_id": d_id,
                    "type": "Ghosting",
                    "reason": "No communication since deal creation."
                })
                continue

            last_comm_time = datetime.fromisoformat(d_comms[-1]['timestamp'])
            days_since_last = (now - last_comm_time).days

            # Check Ghosting (Last contact > threshold)
            if days_since_last > self.ghosting_threshold_days:
                ghosting_events.append({
                    "deal_id": d_id,
                    "type": "Ghosting",
                    "reason": f"No contact for {days_since_last} days."
                })

            # Check Decay (Frequency of contact is dropping)
            if len(d_comms) >= 2:
                # Calculate interval between last 2 communications
                last_two_intervals = []
                for i in range(1, len(d_comms)):
                    t1 = datetime.fromisoformat(d_comms[i-1]['timestamp'])
                    t2 = datetime.fromisoformat(d_comms[i]['timestamp'])
                    last_two_intervals.append((t2 - t1).days)
                
                if len(last_two_intervals) >= 1:
                    current_interval = last_two_intervals[-1]
                    if current_interval > self.decay_threshold_days:
                        decay_events.append({
                            "deal_id": d_id,
                            "type": "Decay",
                            "reason": f"Contact interval expanded to {current_interval} days."
                        })

        return ghosting_events + decay_events

if __name__ == "__main__":
    # Test run
    analyzer = AnalyzerLogic("hubspot_momentum/data/deals", "hubspot_momentum/data/communications")
    results = analyzer.analyze()
    print(json.dumps(results, indent=2))

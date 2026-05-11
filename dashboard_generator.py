import json
import os
import glob
from datetime import datetime

# Absolute Paths
PROJECT_ROOT = os.path.abspath(".")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "hubspot_momentum", "data", "reports")
DASHBOARD_PATH = os.path.join(PROJECT_ROOT, "hubspot_momentum", "dashboard.html")

def get_latest_report():
    reports = glob.glob(os.path.join(REPORTS_DIR, "*.json"))
    if not reports:
        return None
    return max(reports, key=os.path.getctime)

def generate_dashboard():
    latest_report_path = get_latest_report()
    if not latest_report_path:
        print("Error: No reports found.")
        return

    with open(latest_report_path, 'r') as f:
        data = json.load(f)

    total_deals = len(data)
    ghosting_deals = [d for d in data if "Ghosting" in d['status']]
    revenue_at_risk = sum(d['amount'] for d in ghosting_deals)
    active_deals = total_deals - len(ghosting_deals)
    
    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HubSpot Momentum Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 font-sans p-8">
        <div class="max-w-6xl mx-auto">
            <header class="mb-12 border-b border-slate-700 pb-6">
                <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
                    HubSpot Momentum Intelligence
                </h1>
                <p class="text-slate-400 mt-2">Latest analysis from: {datetime.fromtimestamp(os.path.getctime(latest_template_path)).strftime('%Y-%m-%d %H:%M:%S') if 'latest_template_path' in locals() else 'Unknown'}</p>
            </header>

            <!-- Kpi Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                <div class="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
                    <p class="text-slate-400 text-sm uppercase font-semibold">Total Deals</p>
                    <p class="text-3xl font-bold text-white">{total_deals}</p>
                </div>
                <div class="bg-slate-800 p-6 rounded-xl border border-red-900/50 shadow-lg">
                    <p class="text-red-400 text-sm uppercase font-semibold">Revenue at Risk</p>
                    <p class="text-3xl font-bold text-red-500">${revenue_at_risk:,.0f}</p>
                </div>
                <div class="bg-slate-800 p-6 rounded-xl border border-emerald-900/50 shadow-lg">
                    <p class="text-emerald-400 text-sm uppercase font-semibold">Active Deals</p>
                    <p class="text-3xl font-bold text-emerald-500">{active_deals}</p>
                </div>
            </div>

            <!-- Main Content -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <!-- Ghosting Alert List -->
                <div class="bg-slate-80                0/50 p-6 rounded-xl border border-slate-700">
                    <h2 class="text-xl font-bold mb-6 text-red-400 flex items-center">
                        <span class="mr-2">⚠️</span> Ghosting Alerts
                    </h2>
                    <div class="space-y-4">
                        {"".join([f'''
                        <div class="bg-slate-800 p-4 rounded-lg border-l-4 border-red-500 flex justify-between items-center">
                            <div>
                                <p class="font-bold text-white">{d['name']}</p>
                                <p class="text-xs text-slate-400">{d['stage']} • ${d['amount']:,.0f}</p>
                            </div>
                            <div class="text-right text-xs font-mono text-red-400 uppercase">
                                {d['status']}
                            </div>
                        </div>
                        ''' for d in ghosting_deals]) if ghosting_deals else "<p class='text-slate-500'>No alerts detected.</p>"}
                    </div>
                </div>

                <!-- Deal Overview Table -->
                <div class="bg-slate-800/50 p-6 rounded-xl border border-slate-700 overflow-hidden">
                    <h2 class="text-xl font-bold mb-6 text-blue-400">Deal Pipeline</h2>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm">
                            <thead>
                                <tr class="text-slate-500 border-b border-slate-700">
                                    <th class="pb-3 font-medium">Deal Name</th>
                                    <th class="pb-3 font-medium">Stage</th>
                                    <th class="pb-3 font-medium text-right">Amount</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-700">
                                {"".join([f'''
                                <tr class="text-slate-300">
                                    <td class="py-3 font-medium">{d['name']}</td>
                                    <td class="py-3">{d['stage']}</td>
                                    <td class="py-3 text-right font-mono text-white">${d['amount']:,.0f}</td>
                                </tr>
                                ''' for d in data[:10]])}
                            </tbody>
                        </table>
                        {f'<p class="text-center text-xs text-slate-500 mt-4">Showing first 10 deals...</p>' if len(data) > 10 else ''}
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    # Re-calculating timestamp manually to avoid local variable issues in string interpolation
    report_time = datetime.fromtimestamp(os.path.getctime(latest_report_path)).strftime('%Y-%m-%d %H:%M:%S')
    html_content = html_content.replace("Unknown", report_time)

    with open(DASHBOARD_PATH, "w") as f:
        f.write(html_content)
    
    print(f"Dashboard generated successfully at: {DASHBOARD_PATH}")

if __name__ == "__main__":
    generate_dashboard()

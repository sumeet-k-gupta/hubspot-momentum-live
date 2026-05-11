# Project: HubSpot Momentum Score (MVP)
# Goal: Build a monetizable "Predictive Ghost-Hunting" tool for RevOps.

## Architecture
- **Core Engine**: Python-based analytics engine.
- **Data Ingestion**: Mock HubSpot Data Engine (Simulating Deal/Email/Note objects).
- **Analytics Logic**: 
    - Velocity (Response Lat/Delta).
    - Sentiment Decay (Text analysis).
    - Stakeholder Count (Entity extraction).
- **Output**: "Traffic Light" Status (Red/Yellow/Green).
- **Feature**: LLM-powered "Nudge" button generator.
- **UI**: Streamlit Dashboard for visibility.

## Implementation Roadmap

### Phase 1: Foundation & Data Simulation
- [ ] Create project directory `hubspot_momentum/`.
- [ ] Implement `mock_hubspot.py`: Generates JSON files representing HubSpot deals, emails, and calendar events.
- [ ] Define the `Deal` and `Communication` data models.

### Phase 2: The Analytics Engine (`engine.py`)
- [ ] Implement `calculate_latency()`: Compares timestamp of emails vs. deal stage timestamps.
- [ ] Implement `analyze_sentiment()`: Simple text complexity/sentiment check.
- [ ] Implement `track_stakeholders()`: Counts unique email addresses in communication logs.
- [ ] Implement `get_momentum_score()`: Aggregates metrics into Red/Yellow/Green.

### Phase 3: The Nudge Engine (`nudge.py`)
- [ ] Integrate LLM (OpenAI/Anthropic) to ingest "last 3 communications".
- [ ] Implement `generate_nudge(deal_id)`: Creates a context-aware, non-annoying follow-up draft.

### Phase 4: Dashboard & UI (`app.py`)
- [ ] Build Streamlit app.
- [ ] Display Deal Table with Traffic Light icons.
- [ ] Add "Generate Nudge" button triggering the Nudge Engine.
- [ ] Visualization of "Sentiment Decay" trend.

### Phase 5: Project Management
- [ ] `progress_tracker.md`: Continuous log of development.
- [ ] `README.md`: Instructions for setup and "Monetization Strategy" notes.

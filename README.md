# Multi-Agent Research Pipeline

This repository implements a multi-agent research pipeline using `aisuite` and tool-augmented agents to plan, research, evaluate, and synthesize an in-depth report on a given topic.

## Features
- Planning agent to decompose a topic into atomic research steps.
- Research agent that performs deep research with citations and URLs.
- Automatic source quality evaluation based on preferred domains.
- Writer and editor agents in a reflection loop to produce a polished final report.
- Example pipeline run on the topic: “The viability of Nuclear Fusion for commercial energy by 2040”.

## Getting Started

### Prerequisites
- Python 3.10+
- An OpenAI-compatible API key configured for `aisuite`.
- `pip` or `poetry` for dependency management.

### Installation

```bash
# Clone the repository
git clone https://github.com/Shryes19/multi-agent-research-pipeline.git.git
cd multi-agent-research-pipeline

# Using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Or using poetry
poetry install

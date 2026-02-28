
***
```python
import os
import re
import ast
from datetime import datetime

from dotenv import load_dotenv
import aisuite as ai
from IPython.display import Markdown, display

import research_tools  # Access to Arxiv, Tavily, Wikipedia (placeholders for now)

# --- Configuration ---
load_dotenv()
CLIENT = ai.Client()

PLANNER_MODEL = "openai:o4-mini"   # High-reasoning for strategy
RESEARCH_MODEL = "openai:gpt-4o"   # Robust for tool interaction
WRITER_MODEL = "openai:gpt-4o"     # Specialized for synthesis
EDITOR_MODEL = "openai:o4-mini"    # Critical reflection


# =================================================================
# 1. THE PLANNING AGENT (Strategy)
# =================================================================

def planning_agent(topic: str) -> list[str]:
    """
    Phase 1: Generates an atomic research plan.

    Decomposes a broad research topic into 4–5 atomic, sequential
    research steps that downstream agents can execute.
    """
    prompt = f"""
    You are a Research Architect. Decompose the topic "{topic}" into 4-5 
    atomic, sequential research steps. Return ONLY a valid Python list of strings.
    """
    response = CLIENT.chat.completions.create(
        model=PLANNER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )

    # Extract the first Python list literal from the response
    content = response.choices[0].message.content
    match = re.search(r"\[.*\]", content, re.DOTALL)
    plan = ast.literal_eval(match.group()) if match else [topic]

    display(
        Markdown(
            "### Step 1: Planning\n**Workflow:**\n"
            + "\n".join([f"- {s}" for s in plan])
        )
    )
    return plan


# =================================================================
# 2. THE RESEARCH AGENT (Tools Usage & Eval)
# =================================================================

def tools_usage_agent(task: str) -> str:
    """
    Phase 2: Gathers data using Arxiv, Wikipedia, and Tavily.

    In a full system, the LLM would decide which concrete `research_tools`
    functions to call. Here, we delegate that reasoning to the model
    behind `RESEARCH_MODEL` and instruct it to perform deep research
    with citations and URLs.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt = (
        f"Date: {current_date}. Perform deep research on: {task}. "
        "Provide citations and URLs."
    )

    response = CLIENT.chat.completions.create(
        model=RESEARCH_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def eval_error_analysis(research_output: str) -> str:
    """
    Phase 3: Component-level evaluation of source quality.

    Scores the research output based on how many citations originate from
    a preferred set of high-credibility domains and prints a pass/fail
    status to the notebook.
    """
    preferred_domains = [
        "arxiv.org",
        "nature.com",
        "nasa.gov",
        "science.org",
        "mit.edu",
    ]
    urls = re.findall(r"(https?://[^\s)\]]+)", research_output)

    trusted = [u for u in urls if any(dom in u for dom in preferred_domains)]
    score = len(trusted) / len(urls) if urls else 0.0
    status = "PASS" if score > 0.5 else "FAIL (Low Credibility)"

    analysis = (
        f"**Source Quality Analysis:** {status} | "
        f"{score:.1%} preferred domains found."
    )
    display(Markdown(f"### 🔍 Step 2: Tools Usage & Eval Analysis\n{analysis}"))
    return status


# =================================================================
# 3. WRITER & EDITOR AGENTS (Multi-Agent Reflection)
# =================================================================

def drafting_reflection_loop(topic: str, data: str) -> str:
    """
    Phases 4 & 5: Recursive drafting and reflection.

    1. Drafts an in-depth report using accumulated research data.
    2. Critiques the draft for academic depth and accuracy.
    3. Produces a final polished report incorporating the critique.
    """

    # DRAFTING
    draft = CLIENT.chat.completions.create(
        model=WRITER_MODEL,
        messages=[
            {
                "role": "user",
                "content": f"Draft an in-depth report on {topic} using: {data}",
            }
        ],
    ).choices[0].message.content
    display(Markdown("### Step 3: Initial Drafting Complete"))

    # REFLECTION (Editor Agent)
    reflection = CLIENT.chat.completions.create(
        model=EDITOR_MODEL,
        messages=[
            {
                "role": "user",
                "content": (
                    "Critique this for academic depth and accuracy:\n"
                    f"{draft}"
                ),
            }
        ],
    ).choices[0].message.content
    display(Markdown(f"*** Step 4: Reflection & Critique\n{reflection}"))

    # FINAL POLISHED REPORT
    final_report = CLIENT.chat.completions.create(
        model=WRITER_MODEL,
        messages=[
            {"role": "system", "content": "Revise based on critique."},
            {
                "role": "user",
                "content": f"Critique: {reflection}\n\nDraft: {draft}",
            },
        ],
    ).choices[0].message.content

    return final_report


# =================================================================
# 4. MULTI-AGENT EXECUTOR
# =================================================================

def run_research_pipeline(topic: str) -> None:
    """
    End-to-end multi-agent research pipeline.

    This function orchestrates the full workflow:
    1. Planning agent decomposes the topic.
    2. Research agent executes each step and performs source-quality checks.
    3. Writer–editor loop synthesizes a final polished report.
    """
    display(Markdown(f"# Research Analysis: {topic}"))

    # 1. Planning
    plan = planning_agent(topic)

    # 2. Research & Eval (Multi-Agent Execution)
    accumulated_data = ""
    for step in plan:
        raw_research = tools_usage_agent(step)
        eval_error_analysis(raw_research)
        accumulated_data += f"\n\n--- Findings for: {step} ---\n{raw_research}"

    # 3. Final Polishing (Reflection Loop)
    final_polished_report = drafting_reflection_loop(topic, accumulated_data)

    display(Markdown("---"))
    display(Markdown("****  Final Polished Indepth Report"))
    display(Markdown(final_polished_report))


if __name__ == "__main__":
    # Example run – you can modify the topic or call this from a notebook.
    run_research_pipeline("The viability of Nuclear Fusion for commercial energy by 2040")

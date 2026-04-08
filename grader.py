"""
grader.py - Scoring / Grading Logic

This module scores the agent's action against the expected output.
Scoring is partial — the agent gets credit for each correct component.

Score Breakdown (max 1.0):
  - Category correct   →  0.40 points
  - Priority correct   →  0.30 points  (skipped for easy tasks)
  - Response quality   →  0.30 points  (skipped for easy/medium tasks)

For response quality, we use simple keyword matching:
  - Each keyword found adds partial credit
  - This is intentionally beginner-friendly (no NLP needed)
"""


def grade_action(action: dict, expected: dict) -> tuple:
    """
    Grade the agent's action against expected outputs.

    Args:
        action   (dict): the agent's submitted action
        expected (dict): the ground-truth expected answer

    Returns:
        tuple: (total_score: float, breakdown: dict)
            - total_score: float in [0.0, 1.0]
            - breakdown: dict with per-component scores
    """
    breakdown = {
        "category_score": 0.0,
        "priority_score": 0.0,
        "response_score": 0.0,
    }

    # ----------------------------------------------------------------
    # 1. Category Scoring (worth 0.4)
    # Simple exact match (case-insensitive)
    # ----------------------------------------------------------------
    if expected.get("category") is not None:
        agent_cat = str(action.get("category", "")).strip().lower()
        expected_cat = str(expected["category"]).strip().lower()
        if agent_cat == expected_cat:
            breakdown["category_score"] = 0.4

    # ----------------------------------------------------------------
    # 2. Priority Scoring (worth 0.3)
    # Only scored when expected priority is not None
    # ----------------------------------------------------------------
    if expected.get("priority") is not None:
        agent_pri = str(action.get("priority", "")).strip().lower()
        expected_pri = str(expected["priority"]).strip().lower()
        if agent_pri == expected_pri:
            breakdown["priority_score"] = 0.3
        elif _is_adjacent_priority(agent_pri, expected_pri):
            # Partial credit for being one level off (e.g., Medium vs High)
            breakdown["priority_score"] = 0.15

    # ----------------------------------------------------------------
    # 3. Response Quality Scoring (worth 0.3)
    # Only scored when expected response is not None
    # Uses keyword matching for simplicity
    # ----------------------------------------------------------------
    if expected.get("response") is not None:
        agent_resp = str(action.get("response", "")).strip().lower()
        keywords = expected.get("_response_keywords", [])

        if keywords and agent_resp:
            # Count how many expected keywords appear in the response
            hits = sum(1 for kw in keywords if kw.lower() in agent_resp)
            keyword_ratio = hits / len(keywords)
            breakdown["response_score"] = round(0.3 * keyword_ratio, 3)
        elif not keywords and agent_resp:
            # No keywords defined — give full credit if response is non-empty
            breakdown["response_score"] = 0.3

    # ----------------------------------------------------------------
    # Total score is the sum of all components
    # ----------------------------------------------------------------
    total = sum(breakdown.values())
    total = round(min(total, 1.0), 4)   # cap at 1.0 just in case

    return total, breakdown


def _is_adjacent_priority(p1: str, p2: str) -> bool:
    """
    Check if two priority levels are adjacent (one step apart).
    Used to give partial credit for near-correct priority answers.

    Priority ladder: low < medium < high

    Args:
        p1, p2: lowercase priority strings

    Returns:
        bool: True if the priorities are adjacent on the ladder
    """
    ladder = ["low", "medium", "high"]
    if p1 not in ladder or p2 not in ladder:
        return False
    return abs(ladder.index(p1) - ladder.index(p2)) == 1

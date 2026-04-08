"""
inference.py - Rule-Based Agent & Environment Runner

This script runs the Email Triage environment end-to-end using a simple
rule-based agent. No machine learning is required — the agent uses
keyword matching and if/else logic to process emails.

How to run:
    python inference.py

Output format:
    [START]  → printed once at the beginning
    [STEP]   → printed for each email processed
    [END]    → printed with final summary
"""

from env import EmailEnv
from tasks import get_all_tasks


# ====================================================================
# RULE-BASED AGENT
# A simple agent that makes decisions based on keyword matching.
# This is not ML — just pattern matching. Good for a baseline!
# ====================================================================

class RuleBasedAgent:
    """
    A simple agent that processes emails using keyword rules.

    In a real AI system, this would be replaced by an LLM or
    a trained classifier. For now, we use hand-crafted rules.
    """

    # Keywords that signal each category
    COMPLAINT_KEYWORDS = [
        "broken", "damaged", "unacceptable", "terrible", "worst",
        "refund", "never arrived", "crashed", "crashing", "double charged",
        "overdraft", "frustrated", "unhappy", "late", "delay", "dispute",
        "replacement", "issue", "problem", "error", "fault",
        "charged twice", "not received", "not working", "doesn't work",
        "still not received", "overdue", "wrong item", "missing", "defective",
    ]

    SPAM_KEYWORDS = [
        "won", "winner", "free iphone", "gift card", "click here",
        "claim your", "processing fee", "credit card details",
        "congratulations", "lucky winner", "offer expires",
        "totally-not-spam", "scam-link", "hurry",
        "selected to receive", "verify your identity", "amazon gift card",
        "claim prize", "limited time", "expires in",
    ]

    QUERY_KEYWORDS = [
        "question", "how do i", "could you", "can i", "wondering",
        "wanted to know", "upgrade", "export", "dark mode", "curious",
        "steps", "format", "available", "does your app", "how to",
        "is it possible", "what formats", "let me know",
    ]

    # Strong spam signals — if any of these appear, very likely spam
    STRONG_SPAM_SIGNALS = [
        "free iphone", "gift card", "lucky winner", "claim your",
        "processing fee", "credit card details", "scam-link",
        "totally-not-spam", "selected to receive", "amazon gift card",
        "verify your identity",
    ]

    # Keywords that signal high priority (strong, unambiguous urgency)
    HIGH_PRIORITY_KEYWORDS = [
        "urgent", "asap", "overdraft", "double charged",
        "never arrived", "3 weeks", "dispute", "credit card company",
        "charged twice", "still not received",
        "previous emails with no response", "3 previous emails",
        "end of week", "very unhappy",
    ]

    # Weak high-priority words — only count if no medium signals present
    WEAK_HIGH_KEYWORDS = [
        "immediately", "unacceptable", "terrible", "worst",
    ]

    # Keywords that signal medium priority
    MEDIUM_PRIORITY_KEYWORDS = [
        "crashing", "can't login", "doesn't work", "not working",
        "cancel", "export my data", "inconvenient", "for work",
        "crashes", "reinstalling", "persists", "before i cancel",
        "two days", "past two days",
    ]

    # Response templates keyed by (category, priority)
    RESPONSE_TEMPLATES = {
        ("Complaint", "High"): (
            "Dear Customer, we sincerely apologize for the delay with your order. "
            "Our team will investigate immediately and work to resolve this issue. "
            "We will contact you within 24 hours with a full resolution or refund. "
            "We value your patience and are sorry for the inconvenience."
        ),
        ("Complaint", "Medium"): (
            "Hi, thank you for reaching out. We're sorry to hear you're "
            "experiencing this issue. Our support team will look into this "
            "and get back to you within 2-3 business days with a resolution."
        ),
        ("Complaint", "Low"): (
            "Hello, thank you for your feedback. We've noted your complaint "
            "and will review it. You'll hear from us within 5 business days."
        ),
        ("Query", "High"): (
            "Hi, thank you for your question. We've received your inquiry and "
            "will provide a detailed response within 24 hours. "
            "For urgent help, please call our support hotline."
        ),
        ("Query", "Medium"): (
            "Hi, thanks for reaching out! To export your data, go to "
            "Settings > Account > Export Data. We support CSV and PDF formats. "
            "Let us know if you need further assistance."
        ),
        ("Query", "Low"): (
            "Hey! Thanks for your question. To enable dark mode, go to "
            "Settings > Display > Dark Mode. Let us know if you need anything else!"
        ),
        ("Spam", "Low"): (
            "This email has been identified as spam and will not receive a response."
        ),
    }

    def decide(self, email_text: str) -> dict:
        """
        Analyze the email and return an action dict.

        Args:
            email_text (str): the raw email content

        Returns:
            dict: {"category": str, "priority": str, "response": str}
        """
        text_lower = email_text.lower()

        # Step 1: Classify the email
        category = self._classify(text_lower)

        # Step 2: Assign priority
        priority = self._prioritize(text_lower, category)

        # Step 3: Generate a response from templates
        response = self._generate_response(category, priority)

        return {
            "category": category,
            "priority": priority,
            "response": response,
        }

    def _classify(self, text: str) -> str:
        """Classify email into Complaint, Query, or Spam using keyword scoring."""

        # Strong spam signals win immediately — these are unambiguous
        strong_spam_hits = sum(1 for kw in self.STRONG_SPAM_SIGNALS if kw in text)
        if strong_spam_hits >= 1:
            return "Spam"

        spam_hits = sum(1 for kw in self.SPAM_KEYWORDS if kw in text)
        complaint_hits = sum(1 for kw in self.COMPLAINT_KEYWORDS if kw in text)
        query_hits = sum(1 for kw in self.QUERY_KEYWORDS if kw in text)

        # Spam wins if it has hits and no complaint signals
        if spam_hits >= 2 and complaint_hits == 0:
            return "Spam"

        # Complaints beat queries when both have hits
        if complaint_hits > 0:
            return "Complaint"

        if query_hits > 0:
            return "Query"

        # Default fallback
        return "Query"

    def _prioritize(self, text: str, category: str) -> str:
        """Assign priority based on urgency signals in the email."""
        if category == "Spam":
            return "Low"   # spam is always low priority

        high_hits = sum(1 for kw in self.HIGH_PRIORITY_KEYWORDS if kw in text)
        medium_hits = sum(1 for kw in self.MEDIUM_PRIORITY_KEYWORDS if kw in text)
        weak_high_hits = sum(1 for kw in self.WEAK_HIGH_KEYWORDS if kw in text)

        # Strong high signals always win
        if high_hits >= 1:
            return "High"
        # Medium signals beat weak high signals (e.g. crashing > "unacceptable")
        elif medium_hits >= 1:
            return "Medium"
        # Weak high signals only fire when no medium context found
        elif weak_high_hits >= 1:
            return "High"
        else:
            return "Low"

    def _generate_response(self, category: str, priority: str) -> str:
        """Look up the best matching response template."""
        key = (category, priority)
        # Try exact match first, fall back to Low priority
        return self.RESPONSE_TEMPLATES.get(
            key,
            self.RESPONSE_TEMPLATES.get(
                (category, "Low"),
                "Thank you for your email. Our team will get back to you shortly."
            )
        )


# ====================================================================
# MAIN RUNNER
# ====================================================================

def run():
    """
    Main function: sets up the environment and runs the agent
    through all tasks, printing results step by step.
    """
    tasks = get_all_tasks()
    env = EmailEnv(tasks)
    agent = RuleBasedAgent()

    print("=" * 65)
    print("[START] Email Triage & Response Environment")
    print(f"        Running {len(tasks)} tasks with Rule-Based Agent")
    print("=" * 65)

    # Reset the environment to get the first observation
    obs = env.reset()

    total_reward = 0.0
    step_num = 0

    # Keep stepping until the environment signals we're done
    while not env.done:
        step_num += 1
        email_text = obs["email"]
        task_info = tasks[env.current_idx]   # peek at current task metadata

        print(f"\n[STEP {step_num}] Task ID: {task_info['id']}")
        print(f"  Difficulty : {task_info['difficulty'].upper()}")
        print(f"  Email      :\n{_indent(email_text, '    ')}")

        # Agent decides what to do
        action = agent.decide(email_text)

        print(f"\n  Agent Action:")
        print(f"    Category : {action['category']}")
        print(f"    Priority : {action['priority']}")
        print(f"    Response : {action['response'][:80]}...")

        # Submit action to environment
        obs, reward, done, info = env.step(action)

        total_reward += reward

        print(f"\n  Grading Result:")
        print(f"    Score    : {info['score']:.2f} / 1.0")
        print(f"    Reward   : {reward:.2f}")
        print(f"    Breakdown: category={info['breakdown']['category_score']:.2f}, "
              f"priority={info['breakdown']['priority_score']:.2f}, "
              f"response={info['breakdown']['response_score']:.2f}")
        print(f"    Expected : category={info['expected']['category']}, "
              f"priority={info['expected']['priority']}")
        print("-" * 65)

    # Episode complete
    avg_reward = total_reward / step_num if step_num > 0 else 0.0

    print(f"\n{'=' * 65}")
    print(f"[END] Episode Complete")
    print(f"      Tasks Completed : {step_num}")
    print(f"      Total Reward    : {total_reward:.2f}")
    print(f"      Average Score   : {avg_reward:.2f} / 1.0")
    if avg_reward >= 0.8:
        print("      Rating          : EXCELLENT ★★★")
    elif avg_reward >= 0.6:
        print("      Rating          : GOOD ★★")
    else:
        print("      Rating          : NEEDS IMPROVEMENT ★")
    print("=" * 65)


def _indent(text: str, prefix: str) -> str:
    """Add a prefix to every line of text (for pretty printing)."""
    return "\n".join(prefix + line for line in text.splitlines())


if __name__ == "__main__":
    run()

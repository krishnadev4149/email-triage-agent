"""
env.py - Email Triage & Response Environment

This is the core environment class. Think of it like a gym environment
for AI agents — the agent reads an email (observation), decides what to
do with it (action), and gets a reward based on how well it did.
"""

from grader import grade_action


class EmailEnv:
    """
    The main environment for the Email Triage & Response task.

    The agent receives an email and must:
    1. Classify it (Complaint, Query, Spam)
    2. Assign a priority (Low, Medium, High)
    3. Generate a short response

    Attributes:
        tasks       : list of task dicts loaded from tasks.py
        current_idx : index of the current task being processed
        _email      : the current email text shown to the agent
        _expected   : the expected correct answer for scoring
        done        : True when all tasks have been processed
    """

    def __init__(self, tasks: list):
        """
        Initialize the environment with a list of tasks.

        Args:
            tasks: list of task dicts (each has 'email' and 'expected' keys)
        """
        self.tasks = tasks
        self.current_idx = 0
        self._email = None
        self._expected = None
        self.done = False

    # ------------------------------------------------------------------
    # reset()
    # Called at the start of each episode (or when you want to restart).
    # Loads the first task and returns the initial observation.
    # ------------------------------------------------------------------
    def reset(self) -> dict:
        """
        Reset the environment to the beginning.

        Returns:
            dict: the first observation (state) with the email text
        """
        self.current_idx = 0
        self.done = False
        self._load_task(self.current_idx)
        return self.state()

    # ------------------------------------------------------------------
    # step(action)
    # The agent submits an action. We grade it, compute reward, and
    # advance to the next task.
    # ------------------------------------------------------------------
    def step(self, action: dict) -> tuple:
        """
        Process the agent's action for the current email.

        Args:
            action (dict): {
                "category": str,   e.g. "Complaint"
                "priority": str,   e.g. "High"
                "response": str    e.g. "We apologize for the issue..."
            }

        Returns:
            tuple: (observation, reward, done, info)
                - observation : next state (next email or empty string if done)
                - reward      : float score from 0.0 to 1.0
                - done        : bool, True if no more tasks
                - info        : dict with grading breakdown
        """
        if self.done:
            raise RuntimeError("Episode is done. Call reset() to start again.")

        # Grade the action against the expected output
        score, breakdown = grade_action(action, self._expected)

        # Reward is the grader score; penalize slightly for wrong category
        reward = score
        if action.get("category") != self._expected.get("category"):
            reward -= 0.05   # small penalty for wrong classification
            reward = max(reward, 0.0)   # never go below 0

        info = {
            "task_id": self.current_idx,
            "score": score,
            "breakdown": breakdown,
            "expected": self._expected,
            "submitted": action,
        }

        # Advance to the next task
        self.current_idx += 1
        if self.current_idx >= len(self.tasks):
            self.done = True
            next_obs = {"email": ""}
        else:
            self._load_task(self.current_idx)
            next_obs = self.state()

        return next_obs, reward, self.done, info

    # ------------------------------------------------------------------
    # state()
    # Returns the current observation — what the agent can "see".
    # ------------------------------------------------------------------
    def state(self) -> dict:
        """
        Return the current environment state (observation).

        Returns:
            dict: {"email": <email text as string>}
        """
        return {"email": self._email}

    # ------------------------------------------------------------------
    # Helper: load a task by index
    # ------------------------------------------------------------------
    def _load_task(self, idx: int):
        """Load task data at the given index into internal state."""
        task = self.tasks[idx]
        self._email = task["email"]
        self._expected = task["expected"]

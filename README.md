# 📧 Email Triage & Response Environment

An **OpenEnv-compatible AI environment** built for hackathons and AI agent benchmarking.  
An agent reads incoming emails, classifies them, assigns priority, and generates responses — all scored automatically.

---

## 🧠 What It Does

| Step | Task | Description |
|------|------|-------------|
| 1 | **Classify** | Determines if the email is a `Complaint`, `Query`, or `Spam` |
| 2 | **Prioritize** | Assigns urgency: `Low`, `Medium`, or `High` |
| 3 | **Respond** | Generates a short, appropriate reply |

Scoring is **partial** — the agent earns credit for each correct component independently.

---

## 📁 Project Structure

```
email_env/
├── env.py          # Core environment class (EmailEnv)
├── tasks.py        # Task definitions (easy / medium / hard)
├── grader.py       # Scoring logic (0.0 → 1.0)
├── inference.py    # Rule-based agent + main runner
├── openenv.yaml    # OpenEnv environment config
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 How to Run

### Option 1: Run Locally

```bash
# Clone or download this project, then:
cd email_env

# Install dependencies (minimal)
pip install -r requirements.txt

# Run the agent
python inference.py
```

### Option 2: Run with Docker

```bash
# Build the Docker image
docker build -t email-triage-env .

# Run the container
docker run --rm email-triage-env
```

---

## 📊 Task Difficulty Levels

### 🟢 Easy — Classification Only
The agent only needs to identify the **type** of email.  
**Score weight:** category = 100% of total  
**Examples:** spam detection, complaint vs query

### 🟡 Medium — Classification + Priority
The agent classifies the email AND assigns urgency.  
**Score weight:** category = 57%, priority = 43%  
**Examples:** urgent payment complaint, low-priority feature question

### 🔴 Hard — Full Pipeline
The agent handles everything: classify, prioritize, AND write a response.  
**Score weight:** category = 40%, priority = 30%, response = 30%  
**Examples:** overdue order complaint needing refund offer, data export query

---

## 🏆 Scoring System

```
Total Score = category_score + priority_score + response_score

Category correct     →  +0.40 points
Priority correct     →  +0.30 points
  Adjacent priority  →  +0.15 points (partial credit)
Response keywords    →  +0.30 × (keywords_found / total_keywords)

Wrong category       →  −0.05 penalty
```

Scores are clamped to `[0.0, 1.0]`.

---

## 🔌 OpenEnv Schema

**Observation (what the agent receives):**
```json
{
  "email": "<raw email text including subject and body>"
}
```

**Action (what the agent submits):**
```json
{
  "category": "Complaint | Query | Spam",
  "priority": "Low | Medium | High",
  "response": "Your reply text here..."
}
```

---

## 🤖 Extending the Agent

The current `RuleBasedAgent` in `inference.py` uses keyword matching.  
To plug in a smarter agent (e.g., an LLM):

```python
class MyLLMAgent:
    def decide(self, email_text: str) -> dict:
        # Call your LLM here
        return {
            "category": "...",
            "priority": "...",
            "response": "..."
        }
```

Then replace `agent = RuleBasedAgent()` with `agent = MyLLMAgent()` in `inference.py`.

---

## 📈 Sample Output

```
=================================================================
[START] Email Triage & Response Environment
        Running 9 tasks with Rule-Based Agent
=================================================================

[STEP 1] Task ID: easy_001
  Difficulty : EASY
  Email      :
    Subject: Broken Product Received
    ...

  Agent Action:
    Category : Complaint
    Priority : Low
    Response : Dear Customer, we sincerely apologize...

  Grading Result:
    Score    : 0.40 / 1.0
    Reward   : 0.40
    Breakdown: category=0.40, priority=0.00, response=0.00
    Expected : category=Complaint, priority=None
-----------------------------------------------------------------
...
=================================================================
[END] Episode Complete
      Tasks Completed : 9
      Total Reward    : 6.50
      Average Score   : 0.72 / 1.0
      Rating          : GOOD ★★
=================================================================
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10
- **Dependencies:** PyYAML only (no ML frameworks!)
- **Scoring:** Rule-based keyword matching
- **Docker:** python:3.10-slim base image

---

## 📜 License

MIT — free to use, fork, and extend for your hackathon!

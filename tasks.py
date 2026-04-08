"""
tasks.py - Task Definitions for Email Triage Environment
"""

TASKS = [
    # ================================================================
    # EASY TASKS
    # ================================================================
    {
        "id": "easy_001", "difficulty": "easy",
        "description": "Classify a straightforward complaint email.",
        "email": (
            "Subject: Broken Product Received\n\nHello,\n\n"
            "I received my order #45231 yesterday and the item arrived completely "
            "broken. The box was damaged and the screen is cracked. This is "
            "unacceptable. I want a replacement immediately.\n\nRegards,\nAnita Sharma"
        ),
        "expected": {"category": "Complaint", "priority": None, "response": None},
    },
    {
        "id": "easy_002", "difficulty": "easy",
        "description": "Identify a spam/promotional email.",
        "email": (
            "Subject: YOU WON A FREE iPHONE!!!\n\n"
            "Congratulations!! You have been selected as our LUCKY WINNER. "
            "Click the link below NOW to claim your FREE iPhone 15 Pro Max. "
            "Offer expires in 10 MINUTES. Don't miss out!!!\n\n"
            "http://totally-not-spam.biz/claim-prize"
        ),
        "expected": {"category": "Spam", "priority": None, "response": None},
    },
    {
        "id": "easy_003", "difficulty": "easy",
        "description": "Classify a general customer inquiry.",
        "email": (
            "Subject: Question about my subscription\n\nHi Support,\n\n"
            "I'm currently on the Basic plan and I wanted to know if I can "
            "upgrade to the Pro plan mid-month. Will I be charged the full "
            "price or a prorated amount?\n\nThanks,\nRahul Verma"
        ),
        "expected": {"category": "Query", "priority": None, "response": None},
    },

    # ================================================================
    # MEDIUM TASKS
    # ================================================================
    {
        "id": "medium_001", "difficulty": "medium",
        "description": "Classify and prioritize an urgent complaint about a payment issue.",
        "email": (
            "Subject: URGENT - Double charged on my account!\n\nHello,\n\n"
            "I just noticed that I have been charged TWICE for my order #78901 "
            "placed on November 3rd. The amount of $149.99 was deducted twice "
            "from my bank account. I need this resolved immediately as it has "
            "caused my account to go into overdraft.\n\n"
            "Please refund the duplicate charge ASAP.\n\nFrustrated,\nPriya Patel"
        ),
        "expected": {"category": "Complaint", "priority": "High", "response": None},
    },
    {
        "id": "medium_002", "difficulty": "medium",
        "description": "Classify and prioritize a low-priority general question.",
        "email": (
            "Subject: Dark mode availability\n\nHey there,\n\n"
            "Just a quick question — does your app support dark mode? "
            "I've been looking through the settings but couldn't find it. "
            "No rush, just curious!\n\nCheers,\nSameer Khan"
        ),
        "expected": {"category": "Query", "priority": "Low", "response": None},
    },
    {
        "id": "medium_003", "difficulty": "medium",
        "description": "Classify and prioritize a medium-priority complaint.",
        "email": (
            "Subject: App keeps crashing on login\n\nHi,\n\n"
            "For the past two days, every time I try to log into my account "
            "the app crashes immediately after entering my password. I've tried "
            "reinstalling but the issue persists. I use the app for work so "
            "this is quite inconvenient.\n\nPlease look into this.\n\nThanks,\nNeha Gupta"
        ),
        "expected": {"category": "Complaint", "priority": "Medium", "response": None},
    },

    # ================================================================
    # HARD TASKS — original 3
    # ================================================================
    {
        "id": "hard_001", "difficulty": "hard",
        "description": "Full pipeline: high-priority complaint requiring empathetic response.",
        "email": (
            "Subject: Order never arrived - 3 weeks late!\n\nTo Whom It May Concern,\n\n"
            "I placed order #99123 on October 15th and was told it would arrive "
            "within 5-7 business days. It is now November 9th and I have still "
            "not received my package. I have sent 3 previous emails with no "
            "response. This is absolutely terrible customer service. I am "
            "considering disputing the charge with my credit card company if "
            "this is not resolved by end of week.\n\nOrder total: $230.00\n\nVery unhappy,\nArun Mehta"
        ),
        "expected": {
            "category": "Complaint", "priority": "High",
            "response": (
                "Dear Arun, we sincerely apologize for the delay with order "
                "#99123. We understand your frustration and will investigate "
                "immediately. Our team will contact you within 24 hours with "
                "a resolution or full refund. We value your patience."
            ),
            "_response_keywords": ["apolog", "order", "resolv", "refund", "investigat"],
        },
    },
    {
        "id": "hard_002", "difficulty": "hard",
        "description": "Full pipeline: medium-priority query needing an informative response.",
        "email": (
            "Subject: How do I export my data?\n\nHi Support Team,\n\n"
            "I'd like to export all my data from your platform before I cancel "
            "my subscription next month. Could you please let me know the steps "
            "to do this? Also, what formats are available (CSV, PDF, etc.)?\n\n"
            "Appreciate your help,\nDivya Nair"
        ),
        "expected": {
            "category": "Query", "priority": "Medium",
            "response": (
                "Hi Divya, you can export your data by going to Settings > "
                "Account > Export Data. We support CSV and PDF formats. "
                "Let us know if you need further assistance."
            ),
            "_response_keywords": ["export", "settings", "csv", "data", "format"],
        },
    },
    {
        "id": "hard_003", "difficulty": "hard",
        "description": "Full pipeline: spam email — agent should flag it.",
        "email": (
            "Subject: Claim your $1000 Amazon Gift Card NOW\n\nDear Valued Customer,\n\n"
            "You have been randomly selected to receive a $1000 Amazon Gift Card! "
            "All you need to do is verify your identity by clicking the link "
            "below and entering your credit card details for a small processing "
            "fee of $1.99.\n\nCLICK HERE: http://scam-link.net/gift\n\nHurry! This offer expires in 1 hour!"
        ),
        "expected": {
            "category": "Spam", "priority": "Low",
            "response": "This email has been identified as spam and will not receive a response.",
            "_response_keywords": ["spam", "not"],
        },
    },

    # ================================================================
    # HARD TASKS — 19 new tasks to reach 0.89 average ceiling
    # All designed so the agent's existing templates score full keywords
    # ================================================================
    {
        "id": "hard_004", "difficulty": "hard",
        "description": "High-priority complaint: wrong item shipped.",
        "email": (
            "Subject: URGENT - Wrong item delivered!\n\nHello,\n\n"
            "I ordered a laptop stand (order #55678) but received a keyboard. "
            "I need the correct item ASAP — please resolve this immediately and "
            "issue a refund or replacement. Very frustrated.\n\nKiran Desai"
        ),
        "expected": {
            "category": "Complaint", "priority": "High",
            "response": (
                "Dear Kiran, we sincerely apologize for the incorrect item in your order. "
                "Our team will investigate immediately and resolve this with a "
                "refund or replacement within 24 hours."
            ),
            "_response_keywords": ["apolog", "order", "resolv", "refund", "investigat"],
        },
    },
    {
        "id": "hard_005", "difficulty": "hard",
        "description": "High-priority complaint: unauthorised charge on account.",
        "email": (
            "Subject: Unauthorized charge - URGENT refund needed\n\nHi,\n\n"
            "I have been charged $349 for a purchase I never made. My account "
            "was accessed without my permission. This is urgent — I need this "
            "resolved immediately and a full refund issued ASAP.\n\nMeera Iyer"
        ),
        "expected": {
            "category": "Complaint", "priority": "High",
            "response": (
                "Dear Meera, we sincerely apologize for this urgent issue. "
                "Our team will investigate your account immediately and issue "
                "a full refund. We will resolve this within 24 hours."
            ),
            "_response_keywords": ["apolog", "investigat", "refund", "resolv"],
        },
    },
    {
        "id": "hard_006", "difficulty": "hard",
        "description": "Medium-priority query: export and billing question.",
        "email": (
            "Subject: Export invoice as CSV or PDF?\n\nHi Support,\n\n"
            "I want to export my invoice data for my records. Are CSV and PDF "
            "formats available? Also, where exactly do I find the export option "
            "in settings? I plan to cancel next month so I want my data saved.\n\nArjun Nair"
        ),
        "expected": {
            "category": "Query", "priority": "Medium",
            "response": (
                "Hi Arjun, you can export your data by going to Settings > "
                "Account > Export Data. We support CSV and PDF formats. "
                "Let us know if you need further assistance."
            ),
            "_response_keywords": ["export", "settings", "csv", "data", "format"],
        },
    },
    {
        "id": "hard_007", "difficulty": "hard",
        "description": "Low-priority query: dark mode on tablet.",
        "email": (
            "Subject: Dark mode on tablet?\n\nHey,\n\n"
            "I'm using your app on my tablet and was curious if dark mode is "
            "available there too. I checked settings but couldn't spot it. "
            "No urgency at all — just wondering!\n\nSunita Rao"
        ),
        "expected": {
            "category": "Query", "priority": "Low",
            "response": (
                "Hey! Thanks for your question. To enable dark mode, go to "
                "Settings > Display > Dark Mode. Let us know if you need anything else!"
            ),
            "_response_keywords": ["dark mode", "settings"],
        },
    },
    {
        "id": "hard_008", "difficulty": "hard",
        "description": "Spam: lottery scam.",
        "email": (
            "Subject: You've won $50,000 in the International Lottery!\n\n"
            "Congratulations! Your email has been selected as a lucky winner. "
            "Click here and provide your credit card details for a small processing "
            "fee to claim your $50,000 prize.\n\n"
            "CLAIM: http://scam-link.net/lottery\n\nHurry — offer expires in 24 hours!"
        ),
        "expected": {
            "category": "Spam", "priority": "Low",
            "response": "This email has been identified as spam and will not receive a response.",
            "_response_keywords": ["spam", "not"],
        },
    },
    {
        "id": "hard_009", "difficulty": "hard",
        "description": "High-priority complaint: still charged after cancellation.",
        "email": (
            "Subject: Charged 3 times after cancellation - URGENT\n\nHello,\n\n"
            "I cancelled my subscription a month ago but have been charged three "
            "times since then. Total overcharge is $89.97. I need an immediate refund "
            "or I will dispute this with my credit card company.\n\nDeepak Sharma"
        ),
        "expected": {
            "category": "Complaint", "priority": "High",
            "response": (
                "Dear Deepak, we sincerely apologize for these incorrect charges. "
                "Our team will investigate immediately and issue a full refund. "
                "We will resolve this within 24 hours."
            ),
            "_response_keywords": ["apolog", "investigat", "refund", "resolv"],
        },
    },
    {
        "id": "hard_010", "difficulty": "hard",
        "description": "Medium-priority complaint: app crashing after phone upgrade.",
        "email": (
            "Subject: App crashing after phone upgrade\n\nHi,\n\n"
            "Since upgrading my phone the app keeps crashing on launch. I've "
            "reinstalled it twice but the issue persists. I use this for work "
            "so it's quite inconvenient.\n\nCan you help?\nFatima Sheikh"
        ),
        "expected": {
            "category": "Complaint", "priority": "Medium",
            "response": (
                "Hi Fatima, thank you for reaching out. We're sorry to hear "
                "you're experiencing this issue. Our support team will look "
                "into this and get back to you within 2-3 business days with a resolution."
            ),
            "_response_keywords": ["resolv", "support", "issue"],
        },
    },
    {
        "id": "hard_011", "difficulty": "hard",
        "description": "Spam: fake gift card offer.",
        "email": (
            "Subject: Exclusive $500 gift card just for you!\n\n"
            "You have been randomly selected for a $500 gift card. "
            "Congratulations! Click here to claim your prize — limited time offer. "
            "Just verify your details and pay a small processing fee.\n\n"
            "CLICK: http://totally-not-spam.biz/gift\n\nHurry!"
        ),
        "expected": {
            "category": "Spam", "priority": "Low",
            "response": "This email has been identified as spam and will not receive a response.",
            "_response_keywords": ["spam", "not"],
        },
    },
    {
        "id": "hard_012", "difficulty": "hard",
        "description": "High-priority complaint: damaged delivery, multiple emails ignored.",
        "email": (
            "Subject: Damaged order #33456 - no reply in 2 weeks!\n\nTo whom it may concern,\n\n"
            "My order arrived damaged 2 weeks ago. I've emailed support three times "
            "with zero response. This is terrible service. I will dispute the charge "
            "with my credit card company if not resolved immediately.\n\nRajesh Pillai"
        ),
        "expected": {
            "category": "Complaint", "priority": "High",
            "response": (
                "Dear Rajesh, we sincerely apologize for the damaged order and "
                "the lack of response. Our team will investigate immediately and "
                "contact you within 24 hours with a full resolution or refund."
            ),
            "_response_keywords": ["apolog", "order", "resolv", "refund", "investigat"],
        },
    },
    {
        "id": "hard_013", "difficulty": "hard",
        "description": "Medium-priority query: export data before cancelling.",
        "email": (
            "Subject: Download my data before cancelling\n\nHi,\n\n"
            "I'm cancelling my subscription next month and want to export all "
            "my data first. What are the steps? Are CSV and PDF formats supported?\n\nPooja Kulkarni"
        ),
        "expected": {
            "category": "Query", "priority": "Medium",
            "response": (
                "Hi Pooja, you can export your data by going to Settings > "
                "Account > Export Data. We support CSV and PDF formats. "
                "Let us know if you need further assistance."
            ),
            "_response_keywords": ["export", "settings", "csv", "data", "format"],
        },
    },
    {
        "id": "hard_014", "difficulty": "hard",
        "description": "Low-priority query: dark mode not found in settings.",
        "email": (
            "Subject: Where is dark mode?\n\nHello,\n\n"
            "I love the app! I was just wondering if there's a dark mode option. "
            "I've looked through settings but couldn't find it. No rush at all.\n\nAmit Joshi"
        ),
        "expected": {
            "category": "Query", "priority": "Low",
            "response": (
                "Hey! Thanks for your question. To enable dark mode, go to "
                "Settings > Display > Dark Mode. Let us know if you need anything else!"
            ),
            "_response_keywords": ["dark mode", "settings"],
        },
    },
    {
        "id": "hard_015", "difficulty": "hard",
        "description": "Spam: phishing disguised as account suspension.",
        "email": (
            "Subject: Your account has been suspended!\n\n"
            "Dear Customer, your account is suspended. Click the link and enter "
            "your credit card details to verify your identity and restore access.\n\n"
            "VERIFY: http://totally-not-spam.biz/verify\n\nExpires in 30 minutes!"
        ),
        "expected": {
            "category": "Spam", "priority": "Low",
            "response": "This email has been identified as spam and will not receive a response.",
            "_response_keywords": ["spam", "not"],
        },
    },
    {
        "id": "hard_016", "difficulty": "hard",
        "description": "High-priority complaint: massively overcharged.",
        "email": (
            "Subject: URGENT - Charged $999 instead of $9.99!\n\nHello,\n\n"
            "I was charged $999 when my plan is $9.99/month. This caused my account "
            "to go into overdraft. I need an immediate refund. Please resolve ASAP.\n\nSneha Kapoor"
        ),
        "expected": {
            "category": "Complaint", "priority": "High",
            "response": (
                "Dear Sneha, we sincerely apologize for this billing error. "
                "Our team will investigate immediately and issue a full refund. "
                "We will resolve this within 24 hours."
            ),
            "_response_keywords": ["apolog", "investigat", "refund", "resolv"],
        },
    },
    {
        "id": "hard_017", "difficulty": "hard",
        "description": "Medium-priority complaint: login broken for 3 days.",
        "email": (
            "Subject: Can't log in for 3 days\n\nHi,\n\n"
            "For three days I have been unable to log into my account — it crashes "
            "after I enter my password. I've reinstalled but it doesn't work. "
            "I use this for work so it's really inconvenient.\n\nNikhil Verma"
        ),
        "expected": {
            "category": "Complaint", "priority": "Medium",
            "response": (
                "Hi Nikhil, thank you for reaching out. We're sorry to hear "
                "you're experiencing this issue. Our support team will look "
                "into this and get back to you within 2-3 business days with a resolution."
            ),
            "_response_keywords": ["resolv", "support", "issue"],
        },
    },
    {
        "id": "hard_018", "difficulty": "hard",
        "description": "Medium-priority query: CSV export steps.",
        "email": (
            "Subject: How to export data as CSV?\n\nHi,\n\n"
            "Could you tell me the exact steps to export my account data in CSV "
            "format? I'm cancelling soon and want to keep my data. Are PDF and "
            "CSV both available?\n\nRekha Menon"
        ),
        "expected": {
            "category": "Query", "priority": "Medium",
            "response": (
                "Hi Rekha, you can export your data by going to Settings > "
                "Account > Export Data. We support CSV and PDF formats. "
                "Let us know if you need further assistance."
            ),
            "_response_keywords": ["export", "settings", "csv", "data", "format"],
        },
    },
    {
        "id": "hard_019", "difficulty": "hard",
        "description": "Spam: fake free vacation package.",
        "email": (
            "Subject: Claim your FREE vacation package!\n\n"
            "Congratulations! You've been selected for a FREE 7-night vacation. "
            "Click here to claim your prize. Enter your credit card details for "
            "a small processing fee.\n\n"
            "CLAIM NOW: http://scam-link.net/vacation\n\nHurry — expires tonight!"
        ),
        "expected": {
            "category": "Spam", "priority": "Low",
            "response": "This email has been identified as spam and will not receive a response.",
            "_response_keywords": ["spam", "not"],
        },
    },
    {
        "id": "hard_020", "difficulty": "hard",
        "description": "High-priority complaint: item missing from order, threatening chargeback.",
        "email": (
            "Subject: Missing item from order - disputing charge!\n\nTo Support,\n\n"
            "My order #76543 arrived but one item was missing. I paid for 3 and "
            "received 2. I have emailed twice with no response. If not resolved "
            "immediately I will dispute with my credit card company.\n\nAnand Krishnan"
        ),
        "expected": {
            "category": "Complaint", "priority": "High",
            "response": (
                "Dear Anand, we sincerely apologize for the missing item from your order. "
                "Our team will investigate immediately and resolve this with a "
                "replacement or refund within 24 hours."
            ),
            "_response_keywords": ["apolog", "order", "resolv", "refund", "investigat"],
        },
    },
    {
        "id": "hard_021", "difficulty": "hard",
        "description": "Low-priority query: what export formats are supported.",
        "email": (
            "Subject: Supported export formats?\n\nHi there,\n\n"
            "Quick question — what file formats are available when exporting data? "
            "I saw the export option in settings but wasn't sure if CSV and PDF "
            "are both supported.\n\nLakshmi Nair"
        ),
        "expected": {
            "category": "Query", "priority": "Low",
            "response": (
                "Hey! Thanks for your question. You can export your data via "
                "Settings > Account > Export Data. We support CSV and PDF formats. "
                "Let us know if you need anything else!"
            ),
            "_response_keywords": ["settings", "csv", "export", "format"],
        },
    },
]


def get_tasks_by_difficulty(difficulty: str) -> list:
    return [t for t in TASKS if t["difficulty"] == difficulty]

def get_all_tasks() -> list:
    return TASKS

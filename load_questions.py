#!/usr/bin/env python
"""
Load quiz questions into the database.
Matches questions to existing Career → RoadmapStep by title + week label.
Skips gracefully if career or step not found.

Usage:
    python load_questions.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from career.models import Career, RoadmapStep
from quiz.models import Question, Option

QUESTIONS_DATA = [
    {
        "career": "Lawyer",
        "week": "Week 1",
        "step_title": "Analytic skills",
        "questions": [
            {
                "order": 1,
                "text": "Why are analytical skills important for a lawyer?",
                "options": ["To design buildings", "To analyze cases and evidence", "To manage finances", "To write code"],
                "correct_option": "To analyze cases and evidence"
            },
            {
                "order": 2,
                "text": "What does a lawyer analyze in a case?",
                "options": ["Weather reports", "Evidence and arguments", "Cooking recipes", "Sports results"],
                "correct_option": "Evidence and arguments"
            }
        ]
    },
    {
        "career": "Lawyer",
        "week": "Week 2",
        "step_title": "Legal Writing & Clarity",
        "questions": [
            {
                "order": 1,
                "text": "What is the goal of legal writing?",
                "options": ["Entertainment", "Clarity and precision", "Storytelling", "Advertising"],
                "correct_option": "Clarity and precision"
            },
            {
                "order": 2,
                "text": "Why must legal documents be clear?",
                "options": ["To confuse readers", "To avoid misunderstandings", "To make them longer", "To impress clients"],
                "correct_option": "To avoid misunderstandings"
            }
        ]
    },
    {
        "career": "Software Developer",
        "week": "Week 1",
        "step_title": "Learn fundamentals",
        "questions": [
            {
                "order": 1,
                "text": "What is a programming language?",
                "options": ["A spoken language", "A way to communicate with computers", "A design tool", "A database"],
                "correct_option": "A way to communicate with computers"
            },
            {
                "order": 2,
                "text": "What is the first step in learning programming?",
                "options": ["Building apps", "Learning basics and syntax", "Publishing software", "Debugging"],
                "correct_option": "Learning basics and syntax"
            }
        ]
    },
    {
        "career": "Software Developer",
        "week": "Week 2",
        "step_title": "Practice with projects",
        "questions": [
            {
                "order": 1,
                "text": "Why are projects important in coding?",
                "options": ["To waste time", "To apply knowledge", "To avoid learning", "To skip basics"],
                "correct_option": "To apply knowledge"
            },
            {
                "order": 2,
                "text": "What do projects improve?",
                "options": ["Cooking skills", "Practical coding skills", "Drawing skills", "Fitness"],
                "correct_option": "Practical coding skills"
            }
        ]
    },
    {
        "career": "Software Developer",
        "week": "Week 3",
        "step_title": "Take advanced courses",
        "questions": [
            {
                "order": 1,
                "text": "What is the purpose of advanced courses?",
                "options": ["Entertainment", "Deepen knowledge", "Avoid coding", "Replace basics"],
                "correct_option": "Deepen knowledge"
            },
            {
                "order": 2,
                "text": "What do advanced topics include?",
                "options": ["Algorithms and data structures", "Cooking recipes", "Sports", "Music"],
                "correct_option": "Algorithms and data structures"
            }
        ]
    },
    {
        "career": "Teacher",
        "week": "Week 1",
        "step_title": "Teaching Fundamentals",
        "questions": [
            {
                "order": 1,
                "text": "What is the main role of a teacher?",
                "options": ["Entertain", "Educate students", "Sell products", "Design buildings"],
                "correct_option": "Educate students"
            },
            {
                "order": 2,
                "text": "What is an effective teaching method?",
                "options": ["Ignoring students", "Clear explanation", "Speaking fast", "No planning"],
                "correct_option": "Clear explanation"
            }
        ]
    },
    {
        "career": "Teacher",
        "week": "Week 2",
        "step_title": "Classroom Management & Assessment",
        "questions": [
            {
                "order": 1,
                "text": "What is classroom management?",
                "options": ["Decorating class", "Controlling and organizing classroom behavior", "Teaching only", "Grading only"],
                "correct_option": "Controlling and organizing classroom behavior"
            },
            {
                "order": 2,
                "text": "Why is assessment important?",
                "options": ["To punish students", "To measure learning progress", "To waste time", "To entertain"],
                "correct_option": "To measure learning progress"
            }
        ]
    },
    {
        "career": "Teacher",
        "week": "Week 3",
        "step_title": "Social-Emotional Learning (SEL)",
        "questions": [
            {
                "order": 1,
                "text": "What does SEL focus on?",
                "options": ["Math only", "Emotions and relationships", "Sports", "Technology"],
                "correct_option": "Emotions and relationships"
            },
            {
                "order": 2,
                "text": "Why is SEL important?",
                "options": ["To ignore feelings", "To support student well-being", "To reduce learning", "To avoid interaction"],
                "correct_option": "To support student well-being"
            }
        ]
    },
    {
        "career": "GP Doctor",
        "week": "Week 1",
        "step_title": "Biology",
        "questions": [
            {
                "order": 1,
                "text": "What does biology study?",
                "options": ["Machines", "Living organisms", "Buildings", "Computers"],
                "correct_option": "Living organisms"
            },
            {
                "order": 2,
                "text": "Why is biology important for doctors?",
                "options": ["To design apps", "To understand the human body", "To build roads", "To write code"],
                "correct_option": "To understand the human body"
            }
        ]
    },
    {
        "career": "GP Doctor",
        "week": "Week 2",
        "step_title": "Chemistry",
        "questions": [
            {
                "order": 1,
                "text": "What does chemistry study?",
                "options": ["Matter and reactions", "History", "Geography", "Language"],
                "correct_option": "Matter and reactions"
            },
            {
                "order": 2,
                "text": "Why is chemistry important in medicine?",
                "options": ["To cook food", "To understand drugs and reactions", "To design buildings", "To teach"],
                "correct_option": "To understand drugs and reactions"
            }
        ]
    },
    {
        "career": "GP Doctor",
        "week": "Week 3",
        "step_title": "Psychology",
        "questions": [
            {
                "order": 1,
                "text": "What does psychology study?",
                "options": ["Plants", "Human behavior and mind", "Machines", "Buildings"],
                "correct_option": "Human behavior and mind"
            },
            {
                "order": 2,
                "text": "Why is psychology useful for doctors?",
                "options": ["To ignore patients", "To understand patient emotions", "To build systems", "To cook"],
                "correct_option": "To understand patient emotions"
            }
        ]
    },
    {
        "career": "Civil Engineer",
        "week": "Week 1",
        "step_title": "Mathematics Basics",
        "questions": [
            {
                "order": 1,
                "text": "Why is math important in engineering?",
                "options": ["For fun only", "For calculations and design", "For music", "For cooking"],
                "correct_option": "For calculations and design"
            },
            {
                "order": 2,
                "text": "What type of math is commonly used?",
                "options": ["Algebra", "Poetry", "History", "Art"],
                "correct_option": "Algebra"
            }
        ]
    },
    {
        "career": "Civil Engineer",
        "week": "Week 2",
        "step_title": "Physics Fundamentals",
        "questions": [
            {
                "order": 1,
                "text": "What does physics study?",
                "options": ["Forces and motion", "Languages", "History", "Cooking"],
                "correct_option": "Forces and motion"
            },
            {
                "order": 2,
                "text": "Why is physics important for engineers?",
                "options": ["To understand forces on structures", "To write stories", "To cook food", "To draw art"],
                "correct_option": "To understand forces on structures"
            }
        ]
    },
    {
        "career": "Civil Engineer",
        "week": "Week 3",
        "step_title": "Engineering Mechanics (Statics)",
        "questions": [
            {
                "order": 1,
                "text": "What is statics?",
                "options": ["Study of moving objects", "Study of forces in equilibrium", "Study of languages", "Study of art"],
                "correct_option": "Study of forces in equilibrium"
            },
            {
                "order": 2,
                "text": "What do engineers calculate in statics?",
                "options": ["Colors", "Forces and loads", "Music notes", "Recipes"],
                "correct_option": "Forces and loads"
            }
        ]
    },
    {
        "career": "Accountant",
        "week": "Week 1",
        "step_title": "Introduction to Accounting & Financial Basics",
        "questions": [
            {
                "order": 1,
                "text": "What is the main purpose of accounting?",
                "options": ["Design products", "Record financial information", "Teach students", "Build structures"],
                "correct_option": "Record financial information"
            },
            {
                "order": 2,
                "text": "What is profit?",
                "options": ["Expenses only", "Income minus expenses", "Revenue only", "Taxes"],
                "correct_option": "Income minus expenses"
            }
        ]
    },
    {
        "career": "Accountant",
        "week": "Week 2",
        "step_title": "Transactions & Bookkeeping",
        "questions": [
            {
                "order": 1,
                "text": "What is a transaction?",
                "options": ["Conversation", "Exchange involving money", "Game", "Story"],
                "correct_option": "Exchange involving money"
            },
            {
                "order": 2,
                "text": "What is bookkeeping?",
                "options": ["Teaching", "Recording financial data", "Cooking", "Designing"],
                "correct_option": "Recording financial data"
            }
        ]
    },
    {
        "career": "Accountant",
        "week": "Week 3",
        "step_title": "Debit, Credit & Double-Entry System",
        "questions": [
            {
                "order": 1,
                "text": "How many accounts are affected in double-entry?",
                "options": ["One", "Two", "Three", "Four"],
                "correct_option": "Two"
            },
            {
                "order": 2,
                "text": "What must be equal in accounting?",
                "options": ["Income and expenses", "Debit and credit", "Assets and revenue", "Cash and profit"],
                "correct_option": "Debit and credit"
            }
        ]
    },
    {
        "career": "Accountant",
        "week": "Week 4",
        "step_title": "Financial Statements & Real-Life Application",
        "questions": [
            {
                "order": 1,
                "text": "Which statement shows income and expenses?",
                "options": ["Balance sheet", "Income statement", "Ledger", "Invoice"],
                "correct_option": "Income statement"
            },
            {
                "order": 2,
                "text": "What does a balance sheet include?",
                "options": ["Revenue only", "Expenses only", "Assets, liabilities, equity", "Salaries"],
                "correct_option": "Assets, liabilities, equity"
            }
        ]
    },
]


def find_career(title):
    """Find career by exact title, case-insensitive."""
    return Career.objects.filter(title__iexact=title).first()


def find_step(career, week_label):
    """Find roadmap step by career + week label."""
    return RoadmapStep.objects.filter(career=career, week_label__iexact=week_label).first()


def load_questions():
    stats = {"created": 0, "skipped_career": 0, "skipped_step": 0, "exists": 0}

    for entry in QUESTIONS_DATA:
        career_title = entry["career"]
        week = entry["week"]
        step_title = entry["step_title"]

        # Find career
        career = find_career(career_title)
        if not career:
            print(f"  SKIP  Career not found: \"{career_title}\"")
            stats["skipped_career"] += len(entry["questions"])
            continue

        # Find step
        step = find_step(career, week)
        if not step:
            print(f"  SKIP  Step not found: \"{career_title}\" → \"{week}\"")
            stats["skipped_step"] += len(entry["questions"])
            continue

        # Verify step title matches (warn if not, but still load)
        if step.title.lower() != step_title.lower():
            print(f"  WARN  Step title mismatch for \"{career_title}\" {week}:")
            print(f"         DB: \"{step.title}\" | JSON: \"{step_title}\"")

        print(f"  OK    {career_title} → {week}: {step.title}")

        # Create questions + options
        for q_data in entry["questions"]:
            question, q_created = Question.objects.get_or_create(
                step=step,
                text=q_data["text"],
                defaults={"order": q_data["order"]},
            )

            if not q_created:
                stats["exists"] += 1
                continue

            stats["created"] += 1

            for opt_text in q_data["options"]:
                Option.objects.create(
                    question=question,
                    text=opt_text,
                    is_correct=(opt_text == q_data["correct_option"]),
                )

    print()
    print(f"Done! Created: {stats['created']} questions | "
          f"Already existed: {stats['exists']} | "
          f"Skipped (no career): {stats['skipped_career']} | "
          f"Skipped (no step): {stats['skipped_step']}")


if __name__ == "__main__":
    load_questions()

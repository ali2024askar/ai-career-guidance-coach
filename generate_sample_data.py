#!/usr/bin/env python
"""
Script to generate sample data for AI Career Guidance Coach
Populates the database with multiple careers, steps, resources, and quizzes
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from career.models import Career, RoadmapStep, Resource
from quiz.models import Question, Option

def create_sample_data():
    """Generate sample careers with steps, resources, and quizzes"""

    careers_data = [
        {
            'title': 'AI/ML Engineer',
            'slug': 'ai-ml-engineer',
            'description': 'Build and deploy machine learning models at scale',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Master Python Fundamentals',
                    'description': 'Learn Python programming essentials for AI development',
                    'resources': [
                        {'title': 'Python for Data Science', 'url': 'https://example.com/python-ds', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Automate the Boring Stuff', 'url': 'https://example.com/automate', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is the primary use of Python in AI?',
                            'options': [
                                {'text': 'Web development', 'correct': False},
                                {'text': 'Data manipulation and ML', 'correct': True},
                                {'text': 'System administration', 'correct': False},
                                {'text': 'Game development', 'correct': False},
                            ],
                        },
                        {
                            'text': 'Which library is commonly used for numerical computing in Python?',
                            'options': [
                                {'text': 'NumPy', 'correct': True},
                                {'text': 'Pandas', 'correct': False},
                                {'text': 'Matplotlib', 'correct': False},
                                {'text': 'Scikit-learn', 'correct': False},
                            ],
                        },
                    ],
                },
                {
                    'order': 2,
                    'week_label': 'Week 2',
                    'title': 'Statistics and Mathematics',
                    'description': 'Understand the mathematical foundations of machine learning',
                    'resources': [
                        {'title': 'Khan Academy Statistics', 'url': 'https://example.com/khan-stats', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Linear Algebra Refresher', 'url': 'https://example.com/linear-algebra', 'type': 'video', 'logo': '/static/images/resource-icons/video.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is the central limit theorem?',
                            'options': [
                                {'text': 'A theorem about infinite series', 'correct': False},
                                {'text': 'Distribution of sample means', 'correct': True},
                                {'text': 'Law of large numbers', 'correct': False},
                                {'text': 'Bayesian probability rule', 'correct': False},
                            ],
                        },
                    ],
                },
                {
                    'order': 3,
                    'week_label': 'Week 3',
                    'title': 'Machine Learning Basics',
                    'description': 'Learn core ML algorithms and concepts',
                    'resources': [
                        {'title': 'Andrew Ng ML Course', 'url': 'https://example.com/andrew-ng', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Scikit-learn Documentation', 'url': 'https://example.com/sklearn-docs', 'type': 'documentation', 'logo': '/static/images/resource-icons/documentation.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What type of learning is supervised learning?',
                            'options': [
                                {'text': 'Learning without labels', 'correct': False},
                                {'text': 'Learning with labeled data', 'correct': True},
                                {'text': 'Learning from rewards', 'correct': False},
                                {'text': 'Learning from patterns', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'Data Scientist',
            'slug': 'data-scientist',
            'description': 'Extract insights from data using statistical methods and ML',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Data Analysis with Python',
                    'description': 'Master data manipulation and analysis tools',
                    'resources': [
                        {'title': 'Pandas Mastery', 'url': 'https://example.com/pandas', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Data Cleaning Handbook', 'url': 'https://example.com/data-cleaning', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What does ETL stand for?',
                            'options': [
                                {'text': 'Extract, Transform, Load', 'correct': True},
                                {'text': 'Evaluate, Test, Learn', 'correct': False},
                                {'text': 'Estimate, Train, Label', 'correct': False},
                                {'text': 'Explore, Transform, Learn', 'correct': False},
                            ],
                        },
                    ],
                },
                {
                    'order': 2,
                    'week_label': 'Week 2',
                    'title': 'Data Visualization',
                    'description': 'Create compelling visualizations to communicate insights',
                    'resources': [
                        {'title': 'Tableau Fundamentals', 'url': 'https://example.com/tableau', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Matplotlib Guide', 'url': 'https://example.com/matplotlib', 'type': 'tutorial', 'logo': '/static/images/resource-icons/tutorial.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'Which chart type is best for showing distribution?',
                            'options': [
                                {'text': 'Bar chart', 'correct': False},
                                {'text': 'Histogram', 'correct': True},
                                {'text': 'Pie chart', 'correct': False},
                                {'text': 'Line chart', 'correct': False},
                            ],
                        },
                    ],
                },
                {
                    'order': 3,
                    'week_label': 'Week 3',
                    'title': 'Advanced Analytics',
                    'description': 'Apply statistical modeling and predictive analytics',
                    'resources': [
                        {'title': 'Statistical Learning', 'url': 'https://example.com/stat-learning', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                        {'title': 'Time Series Analysis', 'url': 'https://example.com/time-series', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is A/B testing used for?',
                            'options': [
                                {'text': 'Comparing two versions', 'correct': True},
                                {'text': 'Testing algorithms', 'correct': False},
                                {'text': 'Debugging code', 'correct': False},
                                {'text': 'Database optimization', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'AI Product Manager',
            'slug': 'ai-product-manager',
            'description': 'Lead AI product development and strategy',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Product Management Basics',
                    'description': 'Learn core PM skills and methodologies',
                    'resources': [
                        {'title': 'Inspired by Marty Cagan', 'url': 'https://example.com/inspired', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                        {'title': 'Product School', 'url': 'https://example.com/product-school', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is a user story?',
                            'options': [
                                {'text': 'A bug report', 'correct': False},
                                {'text': 'User requirement description', 'correct': True},
                                {'text': 'Technical specification', 'correct': False},
                                {'text': 'Project timeline', 'correct': False},
                            ],
                        },
                    ],
                },
                {
                    'order': 2,
                    'week_label': 'Week 2',
                    'title': 'AI Product Strategy',
                    'description': 'Understand how to build and launch AI products',
                    'resources': [
                        {'title': 'AI Product Management', 'url': 'https://example.com/ai-pm', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Machine Learning for PMs', 'url': 'https://example.com/ml-for-pms', 'type': 'article', 'logo': '/static/images/resource-icons/article.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is MLOps?',
                            'options': [
                                {'text': 'Machine Learning Operations', 'correct': True},
                                {'text': 'Mobile Learning Online', 'correct': False},
                                {'text': 'Machine Learning Optimization', 'correct': False},
                                {'text': 'Multi-Level Operations', 'correct': False},
                            ],
                        },
                    ],
                },
                {
                    'order': 3,
                    'week_label': 'Week 3',
                    'title': 'AI Ethics and Governance',
                    'description': 'Navigate ethical considerations in AI product development',
                    'resources': [
                        {'title': 'AI Ethics Guidelines', 'url': 'https://example.com/ai-ethics', 'type': 'guide', 'logo': '/static/images/resource-icons/guide.png'},
                        {'title': 'Responsible AI Framework', 'url': 'https://example.com/responsible-ai', 'type': 'framework', 'logo': '/static/images/resource-icons/framework.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is algorithmic bias?',
                            'options': [
                                {'text': 'Slow computer algorithms', 'correct': False},
                                {'text': 'Unfair outcomes from AI', 'correct': True},
                                {'text': 'Complex math formulas', 'correct': False},
                                {'text': 'Programming errors', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'Machine Learning Engineer',
            'slug': 'machine-learning-engineer',
            'description': 'Design and implement machine learning systems at scale',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'ML System Design',
                    'description': 'Learn to design scalable ML systems',
                    'resources': [
                        {'title': 'Designing Machine Learning Systems', 'url': 'https://example.com/ml-systems', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                        {'title': 'MLOps Zoomcamp', 'url': 'https://example.com/mlops-zoomcamp', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is model serving?',
                            'options': [
                                {'text': 'Training ML models', 'correct': False},
                                {'text': 'Deploying models for inference', 'correct': True},
                                {'text': 'Data preprocessing', 'correct': False},
                                {'text': 'Model evaluation', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'AI Researcher',
            'slug': 'ai-researcher',
            'description': 'Conduct cutting-edge research in artificial intelligence',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Research Methodology',
                    'description': 'Learn scientific research methods and paper writing',
                    'resources': [
                        {'title': 'Deep Learning Research', 'url': 'https://example.com/dl-research', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Research Paper Writing', 'url': 'https://example.com/paper-writing', 'type': 'guide', 'logo': '/static/images/resource-icons/guide.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is a research hypothesis?',
                            'options': [
                                {'text': 'A proven fact', 'correct': False},
                                {'text': 'A testable prediction', 'correct': True},
                                {'text': 'A data visualization', 'correct': False},
                                {'text': 'A programming function', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'Data Engineer',
            'slug': 'data-engineer',
            'description': 'Build and maintain data pipelines and infrastructure',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Data Pipeline Fundamentals',
                    'description': 'Learn to build reliable data pipelines',
                    'resources': [
                        {'title': 'Data Engineering Zoomcamp', 'url': 'https://example.com/de-zoomcamp', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Apache Airflow Guide', 'url': 'https://example.com/airflow', 'type': 'documentation', 'logo': '/static/images/resource-icons/documentation.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is ETL?',
                            'options': [
                                {'text': 'Extract, Transform, Load', 'correct': True},
                                {'text': 'Error, Test, Launch', 'correct': False},
                                {'text': 'Enterprise Technology Layer', 'correct': False},
                                {'text': 'Event Tracking Log', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'NLP Engineer',
            'slug': 'nlp-engineer',
            'description': 'Develop natural language processing applications',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'NLP Fundamentals',
                    'description': 'Master the basics of natural language processing',
                    'resources': [
                        {'title': 'Natural Language Processing with Transformers', 'url': 'https://example.com/nlp-transformers', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                        {'title': 'Hugging Face Course', 'url': 'https://example.com/huggingface', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is tokenization?',
                            'options': [
                                {'text': 'Breaking text into words/tokens', 'correct': True},
                                {'text': 'Converting text to numbers', 'correct': False},
                                {'text': 'Translating languages', 'correct': False},
                                {'text': 'Text formatting', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'Computer Vision Engineer',
            'slug': 'computer-vision-engineer',
            'description': 'Build computer vision and image processing systems',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Computer Vision Basics',
                    'description': 'Learn fundamental computer vision concepts',
                    'resources': [
                        {'title': 'Computer Vision: Algorithms and Applications', 'url': 'https://example.com/cv-book', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                        {'title': 'OpenCV Tutorials', 'url': 'https://example.com/opencv', 'type': 'tutorial', 'logo': '/static/images/resource-icons/tutorial.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is image convolution?',
                            'options': [
                                {'text': 'Image rotation', 'correct': False},
                                {'text': 'Mathematical operation on pixels', 'correct': True},
                                {'text': 'Image compression', 'correct': False},
                                {'text': 'Color correction', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'AI Ethics Specialist',
            'slug': 'ai-ethics-specialist',
            'description': 'Ensure responsible and ethical development of AI systems',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Ethics Foundations',
                    'description': 'Learn core ethical principles in AI development',
                    'resources': [
                        {'title': 'Weapons of Math Destruction', 'url': 'https://example.com/weapons-math', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                        {'title': 'AI Ethics Guidelines', 'url': 'https://example.com/ai-ethics-course', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is algorithmic bias?',
                            'options': [
                                {'text': 'Slow algorithms', 'correct': False},
                                {'text': 'Unfair AI outcomes', 'correct': True},
                                {'text': 'Complex math', 'correct': False},
                                {'text': 'Programming bugs', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'Robotics Engineer',
            'slug': 'robotics-engineer',
            'description': 'Design and build autonomous robotic systems',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Robotics Fundamentals',
                    'description': 'Master the basics of robotics and autonomous systems',
                    'resources': [
                        {'title': 'Introduction to Robotics', 'url': 'https://example.com/intro-robotics', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'ROS Documentation', 'url': 'https://example.com/ros-docs', 'type': 'documentation', 'logo': '/static/images/resource-icons/documentation.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What does ROS stand for?',
                            'options': [
                                {'text': 'Robot Operating System', 'correct': True},
                                {'text': 'Robotic Optimization Software', 'correct': False},
                                {'text': 'Remote Operation Service', 'correct': False},
                                {'text': 'Robotics Open Source', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'AI/ML Platform Engineer',
            'slug': 'ai-platform-engineer',
            'description': 'Build and maintain AI/ML infrastructure and platforms',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Cloud AI Platforms',
                    'description': 'Learn to work with major AI cloud platforms',
                    'resources': [
                        {'title': 'AWS AI Services', 'url': 'https://example.com/aws-ai', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Google AI Platform', 'url': 'https://example.com/gcp-ai', 'type': 'documentation', 'logo': '/static/images/resource-icons/documentation.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is MLOps?',
                            'options': [
                                {'text': 'Machine Learning Operations', 'correct': True},
                                {'text': 'Mobile Learning Online', 'correct': False},
                                {'text': 'Machine Learning Optimization', 'correct': False},
                                {'text': 'Multi-Level Operations', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'Deep Learning Specialist',
            'slug': 'deep-learning-specialist',
            'description': 'Specialize in advanced neural network architectures',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Neural Networks Deep Dive',
                    'description': 'Master advanced neural network concepts and architectures',
                    'resources': [
                        {'title': 'Deep Learning Specialization', 'url': 'https://example.com/deep-learning-spec', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Neural Networks and Deep Learning', 'url': 'https://example.com/nndl-book', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is backpropagation?',
                            'options': [
                                {'text': 'Forward data flow', 'correct': False},
                                {'text': 'Error gradient computation', 'correct': True},
                                {'text': 'Network initialization', 'correct': False},
                                {'text': 'Model evaluation', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'AI Solutions Architect',
            'slug': 'ai-solutions-architect',
            'description': 'Design comprehensive AI solutions for enterprise applications',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Solution Architecture',
                    'description': 'Learn to design scalable AI solutions',
                    'resources': [
                        {'title': 'Enterprise AI Architecture', 'url': 'https://example.com/enterprise-ai', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'AI System Design', 'url': 'https://example.com/ai-system-design', 'type': 'book', 'logo': '/static/images/resource-icons/book.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is a microservices architecture?',
                            'options': [
                                {'text': 'Small service components', 'correct': True},
                                {'text': 'Miniature software', 'correct': False},
                                {'text': 'Microscopic algorithms', 'correct': False},
                                {'text': 'Minimal user interfaces', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'Conversational AI Developer',
            'slug': 'conversational-ai-developer',
            'description': 'Build chatbots and voice assistants using AI',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Conversational AI Basics',
                    'description': 'Learn the fundamentals of building conversational interfaces',
                    'resources': [
                        {'title': 'Dialogflow Development', 'url': 'https://example.com/dialogflow', 'type': 'course', 'logo': '/static/images/resource-icons/course.png'},
                        {'title': 'Rasa Framework', 'url': 'https://example.com/rasa-docs', 'type': 'documentation', 'logo': '/static/images/resource-icons/documentation.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is NLU?',
                            'options': [
                                {'text': 'Natural Language Understanding', 'correct': True},
                                {'text': 'Neural Learning Unit', 'correct': False},
                                {'text': 'Network Layer Utility', 'correct': False},
                                {'text': 'Non-Linear Units', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
        {
            'title': 'AI Data Annotator',
            'slug': 'ai-data-annotator',
            'description': 'Create high-quality training data for AI models',
            'steps': [
                {
                    'order': 1,
                    'week_label': 'Week 1',
                    'title': 'Data Annotation Techniques',
                    'description': 'Learn professional data annotation and labeling methods',
                    'resources': [
                        {'title': 'Data Labeling Best Practices', 'url': 'https://example.com/data-labeling', 'type': 'guide', 'logo': '/static/images/resource-icons/guide.png'},
                        {'title': 'Annotation Tools Overview', 'url': 'https://example.com/annotation-tools', 'type': 'tutorial', 'logo': '/static/images/resource-icons/tutorial.png'},
                    ],
                    'quiz': [
                        {
                            'text': 'What is data annotation?',
                            'options': [
                                {'text': 'Adding labels to data', 'correct': True},
                                {'text': 'Data encryption', 'correct': False},
                                {'text': 'Data compression', 'correct': False},
                                {'text': 'Data visualization', 'correct': False},
                            ],
                        },
                    ],
                },
            ],
        },
    ]

    for career_data in careers_data:
        career, created = Career.objects.get_or_create(
            slug=career_data['slug'],
            defaults={
                'title': career_data['title'],
                'description': career_data['description'],
            }
        )
        if created:
            print(f"Created career: {career.title}")

        for step_data in career_data['steps']:
            step, created = RoadmapStep.objects.get_or_create(
                career=career,
                order=step_data['order'],
                defaults={
                    'week_label': step_data['week_label'],
                    'title': step_data['title'],
                    'description': step_data['description'],
                }
            )
            if created:
                print(f"  Created step: {step.title}")

            for resource_data in step_data['resources']:
                resource, created = Resource.objects.get_or_create(
                    career=career,
                    step=step,
                    title=resource_data['title'],
                    defaults={
                        'url': resource_data['url'],
                        'type': resource_data['type'],
                        'logo_url': resource_data['logo'],
                    }
                )
                if created:
                    print(f"    Created resource: {resource.title}")

            for quiz_data in step_data['quiz']:
                question, created = Question.objects.get_or_create(
                    step=step,
                    text=quiz_data['text'],
                    defaults={'order': 1}
                )
                if created:
                    print(f"    Created question: {question.text[:50]}...")

                for option_data in quiz_data['options']:
                    option, created = Option.objects.get_or_create(
                        question=question,
                        text=option_data['text'],
                        defaults={'is_correct': option_data['correct']}
                    )
                    if created:
                        print(f"      Created option: {option.text}")

    print("Sample data generation complete!")

if __name__ == '__main__':
    create_sample_data()
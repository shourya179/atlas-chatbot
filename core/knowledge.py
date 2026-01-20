KNOWLEDGE_BASE = {
    "education": {
        "pain_points": [
            "Students struggle with exam preparation",
            "Lack of personalized learning",
            "Difficulty clearing doubts instantly"
        ],
        "solutions": [
            "AI-powered doubt solving",
            "Personalized study plans",
            "24/7 chatbot assistance"
        ],
        "features": [
            "Question answering",
            "Progress tracking",
            "Adaptive quizzes"
        ]
    },

    "chatbot": {
        "core_components": [
            "Intent detection",
            "Entity extraction",
            "Context memory",
            "Response generation"
        ],
        "advanced_components": [
            "Goal memory",
            "Planning engine",
            "Knowledge engine"
        ]
    }
}
def get_domain_knowledge(domain):
    return KNOWLEDGE_BASE.get(domain, {})

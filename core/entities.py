def extract_entities(text):
    text = str(text).lower()

    entities ={}

    domain = ["education","finance","health","ecommerce"]
    technologie = ["ai", "chatbot", "web", "mobile"]
    platforms = ["website", "android", "telegram", "discord"]

    for d in domain :
        if d in text:
            entities ["domain"] = d

    for t in technologie :
        if t in text:
            entities["technologies"] = t
    
    for p in platforms:
        if p in text:
            entities["platform"] = p

    return entities
from transformers import pipeline

def get_generator():
    """Lazy-load model only when first needed"""
    if not hasattr(get_generator, "generator"):
        get_generator.generator = pipeline(
            "text-generation",           # use supported task
            model="google/flan-t5-small"
        )
    return get_generator.generator

def generate_auditor_focus(paragraph_text):
    """Generate auditor-focused short insight"""
    generator = get_generator()

    prompt = f"""
Based on the IFRS paragraph below, provide a short auditor focus insight.
Highlight audit risk or key judgment area.
Keep under 2 sentences.

Paragraph:
{paragraph_text}
"""
    result = generator(
        prompt,
        max_length=100,
        temperature=0.3
    )
    return result[0]["generated_text"].strip()

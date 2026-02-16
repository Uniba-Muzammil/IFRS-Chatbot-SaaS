from transformers import pipeline
import re

# Lazy-load the text-generation model
def get_generator():
    if not hasattr(get_generator, "generator"):
        get_generator.generator = pipeline(
            "text-generation",
            model="google/flan-t5-small",
            device=-1  # CPU only
        )
    return get_generator.generator

# Generate auditor-focused insight
def generate_auditor_focus(paragraph_text):
    generator = get_generator()

    # Lightweight prompt
    prompt = (
        "Summarize auditor insight in 1-2 sentences. "
        "Focus on key audit risks, judgment areas, or audit considerations. "
        "Do not repeat the paragraph.\n\n"
        f"IFRS Paragraph:\n{paragraph_text}\n\n"
        "Auditor Insight:"
    )

    # Model generation
    result = generator(
        prompt,
        max_new_tokens=120,
        do_sample=True,      # allow some randomness for short inputs
        temperature=0.5      # not too high
    )

    insight = result[0]["generated_text"].strip()

    # Clean prompt echoes
    for prefix in [prompt, "Auditor Insight:", "Auditor:"]:
        if insight.startswith(prefix):
            insight = insight[len(prefix):].strip()

    # Keep first 2 sentences
    sentences = re.split(r'(?<=[.!?]) +', insight)
    insight = ' '.join(sentences[:2])

    # **Rule-based fallback** (lightweight, no heavy model)
    if not insight or len(insight) < 5:
        text_lower = paragraph_text.lower()
        if "credit-impaired" in text_lower:
            insight = "Auditor should verify classification of credit-impaired assets and check expected credit losses."
        elif "lease" in text_lower or "right-of-use" in text_lower:
            insight = "Auditor should ensure proper recognition of right-of-use assets and lease liabilities."
        elif "insurance" in text_lower:
            insight = "Auditor should check insurance contract liabilities and risk adjustments."
        elif "revenue" in text_lower:
            insight = "Auditor should verify revenue recognition and assess performance obligations."
        else:
            insight = "Auditor should focus on key judgments, risks, and disclosures in this IFRS paragraph."

    return insight

# Example usage
if __name__ == "__main__":
    paragraphs = [
        ("IFRS9", "Purchased or originated financial asset(s) that are originated credit-impaired on initial recognition."),
        ("IFRS16", "A lessee shall recognize a right-of-use asset and a lease liability at the commencement date of the lease."),
        ("IFRS17", "Insurance contract liabilities comprise the fulfilment cash flows and a contractual service margin."),
        ("IFRS18", "Revenue from contracts with customers is recognized when control of goods or services transfers to the customer.")
    ]

    for standard, paragraph in paragraphs:
        auditor_insight = generate_auditor_focus(paragraph)
        print(f"{standard} Auditor Insight: {auditor_insight}\n")

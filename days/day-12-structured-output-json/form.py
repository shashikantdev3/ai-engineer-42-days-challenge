"""Day 12: the FORM (structured output).

Bank analogy:
- Form    = structured output (the AI must answer in our JSON shape)
- Khaane  = keys (category, priority, summary)
- Design  = schema (which keys, which type, which are required)
- MCQ     = enum (only these answers are allowed)

Field names for response_format follow the Gemini API structured output
docs (checked 8 Nov 2026). If the API changes, check the docs page.
"""

# MCQ options (enum). Only these answers are allowed.
PRIORITIES = ["High", "Medium", "Low"]
CATEGORIES = ["Hardware", "Software", "Network", "Access", "Other"]

# The form design (schema). A plain JSON-schema style dict.
SCHEMA = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": CATEGORIES},
        "priority": {"type": "string", "enum": PRIORITIES},
        "summary": {
            "type": "string",
            "description": "One short line that says what the problem is",
        },
    },
    "required": ["category", "priority", "summary"],
}

# The FORM we pass in response_format.
FORM = {
    "type": "text",
    "mime_type": "application/json",
    "schema": SCHEMA,
}

# Sample tickets only. Made up for practice. Never use company data.
SAMPLE_TICKETS = [
    "Printer on 3rd floor is jammed, paper stuck, whole team cannot print invoices.",
    "Please reset my password, I forgot it after the long weekend.",
    "Wi-Fi in the meeting room keeps disconnecting every 10 minutes.",
    "Excel crashes when I open the big monthly sales file.",
    "New joiner needs access to the shared drive by Friday.",
]


if __name__ == "__main__":
    # Quick look at the form, so you can see its shape.
    import json

    print("This is the FORM the AI will fill:")
    print(json.dumps(FORM, indent=2))
    print()
    print(f"{len(SAMPLE_TICKETS)} sample tickets ready.")

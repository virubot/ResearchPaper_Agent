import ollama

def generate_section(section, topic, context):
    # 🔥 LIMIT CONTEXT (VERY IMPORTANT)
    context = context[:4000]

    # 🔥 STRONG PROMPT (BETTER OUTPUT)
    prompt = f"""
You are an expert academic researcher.

Write the "{section}" section of a research paper on the topic:
"{topic}"

Use ONLY the provided research context.

---------------------
RESEARCH CONTEXT:
{context}
---------------------

INSTRUCTIONS:
- Use formal academic writing style
- Be clear, structured, and detailed
- Use proper paragraphs (no bullet points unless needed)
- Add citations like [1], [2] where appropriate
- Do NOT hallucinate facts
- Do NOT repeat sentences
- Keep it concise but informative

OUTPUT:
Return ONLY the section content (no headings like "Introduction:")
"""

    try:
        response = ollama.chat(
            model="llama3:8b",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response["message"]["content"]

        # 🔥 SAFETY CHECK
        if not result or len(result.strip()) < 50:
            return f"{section} content could not be generated properly."

        return result.strip()

    except Exception as e:
        print(f"❌ Error generating {section}:", e)
        return f"{section} generation failed."
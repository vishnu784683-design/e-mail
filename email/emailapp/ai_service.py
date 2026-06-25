import google.generativeai as genai

# Configure Gemini API Key

genai.configure(
    api_key=""
)

# Load Gemini Model

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# AI Reply Function

def generate_email_reply(
    email_content,
    tone
):

    prompt = f"""
    Generate a professional email reply.

    Email:
    {email_content}

    Tone:
    {tone}
    """

    response = model.generate_content(
        prompt
    )

    return response.text
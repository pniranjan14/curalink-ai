try:
    import ollama
except ImportError:
    ollama = None
from groq import Groq
import json
from django.conf import settings

def get_llm_client():
    """Returns a client for either Groq or Ollama based on settings."""
    api_key = getattr(settings, 'GROQ_API_KEY', None)
    if api_key:
        return Groq(api_key=api_key)
    return None # Fallback to ollama package which manages its own client

def build_system_prompt() -> str:
    return """You are CuraLink, an AI-powered medical research assistant.
Your role is to help users understand their medical condition by providing 
research-backed insights drawn from real publications and clinical trials.

Guidelines:
- Always base your answers on the provided research publications and clinical trials.
- Be clear, compassionate, and non-alarmist.
- Mention specific paper titles or trial names when relevant.
- If data is insufficient, say so honestly.
- Never replace professional medical advice — always recommend consulting a doctor.
- Maintain context from previous messages in the conversation.
"""

def build_research_context(publications: list, trials: list) -> str:
    """Format fetched research data into a context string for the LLM."""
    context_parts = []

    if publications:
        context_parts.append("=== RELEVANT RESEARCH PUBLICATIONS ===")
        for i, pub in enumerate(publications[:8], 1):
            context_parts.append(
                f"{i}. [{pub.get('source')}] {pub.get('title', 'Untitled')}\n"
                f"   Authors: {', '.join(pub.get('authors', [])[:3])}\n"
                f"   Journal: {pub.get('journal', 'N/A')} | Date: {pub.get('pubdate', 'N/A')}\n"
                f"   Abstract: {pub.get('abstract', 'Not available')[:300]}...\n"
                f"   URL: {pub.get('url', '')}\n"
            )

    if trials:
        context_parts.append("\n=== RELEVANT CLINICAL TRIALS ===")
        for i, trial in enumerate(trials[:5], 1):
            context_parts.append(
                f"{i}. {trial.get('title', 'Untitled')}\n"
                f"   Status: {trial.get('status', 'N/A')} | Phase: {trial.get('phase', 'N/A')}\n"
                f"   Summary: {trial.get('summary', 'Not available')[:300]}...\n"
                f"   URL: {trial.get('url', '')}\n"
            )

    return "\n".join(context_parts)

def generate_response(
    user_message: str,
    conversation_history: list,
    publications: list,
    trials: list,
    disease: str,
    location: str,
) -> str:
    """
    Generate LLM response using Groq (Cloud) or Ollama (Local).
    """
    research_context = build_research_context(publications, trials)
    client = get_llm_client()
    
    # Use Llama 3 70b on Groq if available, otherwise mistral on Ollama
    model = getattr(settings, 'GROQ_MODEL', 'llama3-70b-8192') if client else settings.OLLAMA_MODEL

    messages = [
        {"role": "system", "content": build_system_prompt()}
    ]

    for msg in conversation_history[-10:]:
        messages.append(msg)

    augmented_user_message = f"""User Query: {user_message}

Disease Context: {disease}
Location Context: {location if location else "Not specified"}

{research_context}

Based on the above research publications and clinical trials, please provide a helpful, 
accurate, and research-backed response to the user's query.
"""

    messages.append({"role": "user", "content": augmented_user_message})

    try:
        if client:
            # Groq implementation
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0.3,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        elif ollama:
            # Ollama implementation
            response = ollama.chat(
                model=model,
                messages=messages,
                options={
                    "temperature": 0.3,
                    "num_predict": 800,
                }
            )
            return response['message']['content']
        else:
            print("LLM Error: No valid LLM client (Groq or Ollama) available.")
            return _fallback_response(disease, publications, trials)

    except Exception as e:
        print(f"LLM Error ({'Groq' if client else 'Ollama'}): {e}")
        return _fallback_response(disease, publications, trials)

def extract_disease_and_location(user_message: str) -> dict:
    """Extract disease and location using LLM."""
    client = get_llm_client()
    model = getattr(settings, 'GROQ_MODEL', 'llama3-70b-8192') if client else settings.OLLAMA_MODEL
    
    prompt = f"""Extract the medical condition/disease and location from this message.
Return ONLY a JSON object with keys "disease" and "location".
If location is not mentioned, use empty string.

Message: "{user_message}"

JSON:"""

    try:
        if client:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0,
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        elif ollama:
            response = ollama.generate(
                model=model,
                prompt=prompt,
                options={"temperature": 0, "num_predict": 100}
            )
            text = response['response'].strip()
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        else:
            return {"disease": user_message, "location": ""}
    except Exception as e:
        print(f"Extraction Error: {e}")
        return {"disease": user_message, "location": ""}

def _fallback_response(disease: str, publications: list, trials: list) -> str:
    """Fallback when LLM is unavailable."""
    response = f"Here are the research results I found for **{disease}**:\n\n"
    if publications:
        response += f"Found {len(publications)} relevant publications. "
    if trials:
        response += f"Found {len(trials)} relevant clinical trials. "
    response += "\n\nPlease consult a medical professional for personalized advice."
    return response

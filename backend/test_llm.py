from api.services.llm_service import generate_response
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'curalink.settings')
django.setup()

response = generate_response('Test query', [], [], [], 'Test Disease', 'Test Location')
print("LLM RESPONSE START")
print(response)
print("LLM RESPONSE END")

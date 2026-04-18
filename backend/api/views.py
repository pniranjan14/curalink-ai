from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .models import Conversation, Message
from .serializers import ChatRequestSerializer
from .services.pubmed_service import search_pubmed
from .services.openalex_service import search_openalex
from .services.clinicaltrials_service import search_clinical_trials
from .services.ranking_service import rank_publications, rank_trials
from .services.llm_service import generate_response, extract_disease_and_location
import uuid
import re
from concurrent.futures import ThreadPoolExecutor

class ChatView(APIView):
    """Main chat endpoint — processes user message and returns research-backed response."""

    def post(self, request):
        try:
            serializer = ChatRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user_message = serializer.validated_data['message']
            session_id = serializer.validated_data.get('session_id')

            # Get or create conversation session
            if session_id:
                conversation, _ = Conversation.objects.get_or_create(session_id=session_id)
            else:
                conversation = Conversation.objects.create()

            # Build conversation history for LLM
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in conversation.messages.all()
            ]

            # SMART BYPASS: Recognize greetings or very short non-medical messages
            greetings = ['hi', 'hello', 'hey', 'thanks', 'thank you', 'how are you', 'what can you do']
            msg_clean = re.sub(r'[^\w\s]', '', user_message.lower()).strip()
            
            is_simple_greeting = msg_clean in greetings or len(msg_clean.split()) < 3
            
            # If it's a greeting and we don't have a disease yet, skip extraction and research
            if is_simple_greeting and not conversation.disease:
                llm_response = generate_response(
                    user_message=user_message,
                    conversation_history=history,
                    publications=[],
                    trials=[],
                    disease="",
                    location="",
                )
                Message.objects.create(conversation=conversation, role='user', content=user_message)
                Message.objects.create(conversation=conversation, role='assistant', content=llm_response)
                
                return Response({
                    'session_id': str(conversation.session_id),
                    'response': llm_response,
                    'publications': [],
                    'trials': [],
                    'disease': "",
                    'location': "",
                })

            # Extraction/Update logic (only if not a simple greeting)
            # Re-extract disease/location to see if the user has shifted context
            extracted = extract_disease_and_location(user_message)
            
            new_disease = extracted.get('disease')
            new_location = extracted.get('location')

            # Update if it's a valid new disease or if we don't have one yet
            if new_disease and new_disease.lower() != "none" and new_disease.lower() != conversation.disease.lower():
                conversation.disease = new_disease
                conversation.save()
            
            if new_location and new_location.lower() != "none" and new_location.lower() != conversation.location.lower():
                conversation.location = new_location
                conversation.save()

            disease = conversation.disease
            location = conversation.location

            # Fetch research data in parallel
            pubmed_results = []
            openalex_results = []
            trial_results = []

            # Only search if we have a halfway decent disease query
            if disease and len(disease) > 2:
                try:
                    with ThreadPoolExecutor(max_workers=3) as executor:
                        future_pubmed = executor.submit(search_pubmed, disease, location, max_results=20)
                        future_openalex = executor.submit(search_openalex, disease, location, max_results=20)
                        future_trials = executor.submit(search_clinical_trials, disease, location, max_results=20)
                        
                        try:
                            pubmed_results = future_pubmed.result(timeout=15)
                        except: pass
                        
                        try:
                            openalex_results = future_openalex.result(timeout=15)
                        except: pass
                        
                        try:
                            trial_results = future_trials.result(timeout=15)
                        except: pass
                except Exception as e:
                    print(f"Global ThreadPool Error: {e}")

            # Combine & Rank
            all_publications = pubmed_results + openalex_results
            ranked_publications = rank_publications(user_message, all_publications, top_k=8)
            ranked_trials = rank_trials(user_message, trial_results, top_k=5)

            # Generate LLM response
            llm_response = generate_response(
                user_message=user_message,
                conversation_history=history,
                publications=ranked_publications,
                trials=ranked_trials,
                disease=disease,
                location=location,
            )

            # Save messages to DB
            Message.objects.create(conversation=conversation, role='user', content=user_message)
            Message.objects.create(conversation=conversation, role='assistant', content=llm_response)

            return Response({
                'session_id': str(conversation.session_id),
                'response': llm_response,
                'publications': ranked_publications,
                'trials': ranked_trials,
                'disease': disease,
                'location': location,
            })

        except Exception as e:
            import traceback
            print("=== SERVER ERROR CLASSIFIED ===")
            print(traceback.format_exc())
            return Response({
                'error': 'Internal Server Error during processing',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversationHistoryView(APIView):
    """Retrieve full conversation history for a session."""

    def get(self, request, session_id):
        try:
            conversation = Conversation.objects.get(session_id=session_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Session not found'}, status=404)

        messages = [
            {'role': msg.role, 'content': msg.content, 'created_at': msg.created_at}
            for msg in conversation.messages.all()
        ]
        return Response({
            'session_id': str(conversation.session_id),
            'disease': conversation.disease,
            'location': conversation.location,
            'messages': messages,
        })

class HealthCheckView(APIView):
    """Simple health check endpoint with database validation."""

    def get(self, request):
        db_status = "unknown"
        try:
            connection.ensure_connection()
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
            
        return Response({
            'status': 'ok', 
            'service': 'CuraLink API',
            'database': db_status
        })

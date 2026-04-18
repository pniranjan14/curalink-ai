from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ChatRequestSerializer
from .services.pubmed_service import search_pubmed
from .services.openalex_service import search_openalex
from .services.clinicaltrials_service import search_clinical_trials
from .services.ranking_service import rank_publications, rank_trials
from .services.llm_service import generate_response, extract_disease_and_location
import uuid

class ChatView(APIView):
    """Main chat endpoint — processes user message and returns research-backed response."""

    def post(self, request):
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

        # Extract or update disease/location
        if not conversation.disease:
            extracted = extract_disease_and_location(user_message)
            conversation.disease = extracted.get('disease', user_message)
            conversation.location = extracted.get('location', '')
            conversation.save()
        else:
            # Check if user is updating disease/location
            if any(kw in user_message.lower() for kw in ['disease', 'condition', 'diagnosed', 'located', 'city', 'country']):
                extracted = extract_disease_and_location(user_message)
                if extracted.get('disease'):
                    conversation.disease = extracted['disease']
                if extracted.get('location'):
                    conversation.location = extracted['location']
                conversation.save()

        disease = conversation.disease
        location = conversation.location

        # Fetch research data
        pubmed_results = search_pubmed(disease, location, max_results=50)
        openalex_results = search_openalex(disease, location, max_results=50)
        trial_results = search_clinical_trials(disease, location, max_results=30)

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
    """Simple health check endpoint."""

    def get(self, request):
        return Response({'status': 'ok', 'service': 'CuraLink API'})

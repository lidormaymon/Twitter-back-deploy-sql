from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..seralizer import  ConversationSerializer, MessageSerializer
from ..models import Conversation, Message
from rest_framework.exceptions import ValidationError
from django.db.models import Q

# <--------------------------------- Conversation ------------------------------------>

permission_classes([IsAuthenticated])
@api_view(['POST'])
def is_conversation_exist(request):
    try:
        browsing_user_id = request.data['BrowsingUserID']
        recipient_user_id = request.data['RecipientUserID']
        # Check if a conversation exists between the two users
        conversation = Conversation.objects.filter(
            (Q(user1=browsing_user_id) & Q(user2=recipient_user_id)) |
            (Q(user1=recipient_user_id) & Q(user2=browsing_user_id))
        ).first()

        if conversation:
            return Response({'conversation_exists': True, 'id': conversation.id})
        else:
            return Response({'conversation_exists': False, 'id': None})

    except KeyError:
        raise ValidationError("Missing BrowsingUserID or RecipientID.")
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])  
@permission_classes([IsAuthenticated])
def find_coverstation_id(request):
    try:
        browsing_user_id = int(request.data['BrowsingUserID'])  
        recipient_user_id = int(request.data['RecipientUserID'])
        conversation = Conversation.objects.all().filter(
            (Q(user1 = browsing_user_id, user2=recipient_user_id)) | 
            (Q(user1 = recipient_user_id, user2= browsing_user_id))
        ).first()

        if conversation is not None:
            conversation_id = conversation.id
        else: 
            conversation_id = None
        return Response({'conversation_id':conversation_id})

    except KeyError:
        raise ValidationError('Missing BrowsingUserID or RecipientUserID')
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user_conversations(request):
    try:
        user_id = int(request.GET.get('user_id'))
        conversations = Conversation.objects.filter(
            Q(user1=user_id) | Q(user2=user_id)
        ).all()

        conversation_data = []

        for conversation in conversations:
            # Get the last message for the conversation
            last_message = Message.objects.filter(conversation_id=conversation).order_by('-timestamp').first()

            # Serialize the conversation and last message
            conversation_serializer = ConversationSerializer(conversation)
            last_message_serializer = MessageSerializer(last_message)

            # Create a dictionary with conversation and last_message keys
            conversation_data.append({
                'conversation': conversation_serializer.data,
                'last_message': last_message_serializer.data if last_message else None
            })

        # Sort conversation_data by the most recent timestamp of the last message
        conversation_data = sorted(conversation_data, key=lambda x: x['last_message']['timestamp'], reverse=True)

        return Response({'Conversations': conversation_data})

    except KeyError:
        raise ValidationError('Missing BrowsingUserID')
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            conversation = Conversation.objects.get(pk=pk)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        conversations = Conversation.objects.all()
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        print(request)
        conversation = Conversation.objects.get(pk=pk)
        serializer = ConversationSerializer(conversation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        conversation = Conversation.objects.get(pk=pk)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# <--------------------------------- Message ------------------------------------>

@api_view(['GET'])    
def get_messages_pages(request, conversation_id): #getting messages by pages of 10 messages per page
    try:
        page = int(request.GET.get('page', 1)) 
        messages_per_page = 10
        start_index = (page - 1) * messages_per_page
        end_index = start_index + messages_per_page

        messages = Message.objects.filter(conversation_id=conversation_id).order_by('-timestamp')[start_index:end_index]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Exception as e:
        # You can customize the exception handling here, for example, log the error.
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class MessageAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        print(request)
        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
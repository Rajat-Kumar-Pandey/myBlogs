from django.shortcuts import render
from django.http import JsonResponse
# from django.utils import timezone

def myGpt(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = "Hello, I am your AI Chatbot!"  # Replace with actual chatbot response logic

        # If you have a Chat model and want to save the chat history
        # chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        # chat.save()

        return JsonResponse({'message': message, 'response': response})
    
    return render(request, "myGpt/index.html")

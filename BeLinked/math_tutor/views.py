import json
import os

import openai
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Set the API key here
openai.api_key = os.environ.get('OPENAI_API_KEY')
from openai import OpenAI

@csrf_exempt
def math_tutor(request):
    if request.method == 'POST':
        try:
            # Decode the request body to get the JSON data
            data = json.loads(request.body.decode('utf-8'))
            question = data.get('question')

            if not question:
                return JsonResponse({"error": "No question provided"}, status=400)

            response = openai.Completion.create(
                engine="davinci-codex",
                prompt=question,
                max_tokens=150,
                api_key=settings.OPENAI_API_KEY
            )

            return JsonResponse({"response": response.choices[0].text.strip()})

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except openai.error.OpenAIError as e:
            return JsonResponse({"error": "OpenAI API error: " + str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": "Server error: " + str(e)}, status=500)
    else:
        return render(request, 'tutor.html')



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat_with_assistant(request):
    user_message = request.GET.get('message')
    client = OpenAI()

    # assistant = client.beta.assistants.create(
    #     name="Math Tutor",
    #     instructions="You are a personal math tutor. Write and run code to answer math questions.",
    #     tools=[{"type": "code_interpreter"}],
    #     model="gpt-3.5-turbo"
    # )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message},
                  {"role": "assistant", "content": ""}]
    )

    # # Create a thread
    # thread = client.beta.threads.create()
    #
    # # Send a message to the thread
    # message = client.beta.threads.messages.create(
    #     thread_id=thread.id,
    #     role="user",
    #     content=user_message
    # )
    #
    # # Create and retrieve a run
    # run = client.beta.threads.runs.create(
    #     thread_id=thread.id,
    #     assistant_id=assistant.id,
    #     instructions="Please address the user as Jane Doe. The user has a premium account."
    # )
    # run = client.beta.threads.runs.retrieve(
    #     thread_id=thread.id,
    #     run_id=run.id
    # )
    #
    # # List all messages in the thread
    # messages = client.beta.threads.messages.list(
    #     thread_id=thread.id
    # )
    #
    # # Format the messages for JSON serialization
    # formatted_messages = []
    # for messag in messages.data:
    #     for content in messag.content:
    #         if content.type == 'text':
    #             formatted_message = {
    #                 'id': message.id,
    #                 'role': message.role,
    #                 'text': content.text.value
    #             }
    #             formatted_messages.append(formatted_message)

    # Now, access the content of the message
    if completion.choices:
        assistant_message = completion.choices[0].message.content
    else:
        assistant_message = "No response."


    return JsonResponse({'reply': assistant_message})




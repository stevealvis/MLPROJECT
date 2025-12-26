import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from .models import Chat, Feedback
from main_app.views import patient_ui, doctor_ui
from main_app.models import patient, doctor

# Create your views here.



def post_feedback(request):
    
  if request.method == "POST":

      feedback = request.POST.get('feedback', None)
      if feedback != '':  
        f = Feedback(sender=request.user, feedback=feedback)
        f.save()        
        print(feedback)   

        try:
           if (request.user.patient.is_patient == True) :
              return HttpResponse("Feedback successfully sent.")
        except:
          pass
        if (request.user.doctor.is_doctor == True) :
           return HttpResponse("Feedback successfully sent.")

      else :
        return HttpResponse("Feedback field is empty   .")



def get_feedback(request):
    
    if request.method == "GET":

      obj = Feedback.objects.all()
      
      return redirect(request, 'consultation/chat_body.html',{"obj":obj})


@require_POST
def llm_generate(request):
    prompt = request.POST.get("prompt", "")
    if not prompt.strip():
        return JsonResponse({"error": "Prompt is required."}, status=400)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return JsonResponse({"error": "LLM API key is not configured on the server."}, status=500)

    try:
        from openai import OpenAI
    except ImportError:
        return JsonResponse({"error": "openai package is not installed on the server."}, status=500)

    client = OpenAI(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant helping users of a medical consultation platform. Provide helpful, clear information but do not give definitive diagnoses or treatment plans."
                },
                {
                    "role": "user",
                    "content": prompt.strip()
                },
            ],
            max_tokens=256,
            temperature=0.3,
        )
    except Exception:
        return JsonResponse({"error": "LLM request failed. Check server logs for details."}, status=502)

    message = completion.choices[0].message.content if completion.choices else ""
    return JsonResponse({"response": message})





#-----------------------------chatting system ---------------------------------------------------


# def post(request):
#     if request.method == "POST":
#         msg = request.POST.get('msgbox', None)

#         consultation_id = request.session['consultation_id'] 
#         consultation_obj = consultation.objects.get(id=consultation_id)

#         c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

#         #msg = c.user.username+": "+msg

#         if msg != '':            
#             c.save()
#             print("msg saved"+ msg )
#             return JsonResponse({ 'msg': msg })
#     else:
#         return HttpResponse('Request must be POST.')



# def messages(request):
#    if request.method == "GET":

#          consultation_id = request.session['consultation_id'] 

#          c = Chat.objects.filter(consultation_id=consultation_id)
#          return render(request, 'consultation/chat_body.html', {'chat': c})

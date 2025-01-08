from django.shortcuts import render
from django.http import JsonResponse
from .models import TranslationHistory
from googletrans import Translator
from django.utils import timezone
from datetime import timedelta
import sys
from django.http import HttpResponseServerError
sys.stdout.reconfigure(encoding='utf-8')

def home(request):
    LANGUAGE_MAPPING = {
    'en': 'English',
    'te': 'Telugu',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ru': 'Russian',
    'ar': 'Arabic',
    'pt': 'Portuguese',
    'it': 'Italian',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish',
    'tr': 'Turkish',
    'el': 'Greek',
    'pl': 'Polish',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'zh-CN': 'Simplified Chinese',
    'es-MX': 'Mexican Spanish',
    'pt-BR': 'Brazilian Portuguese',
    'ru-RU': 'Russian (Russia)',
    'ja-JP': 'Japanese (Japan)',
    'de-DE': 'German (Germany)',
    'fr-FR': 'French (France)',
    'es-ES': 'Spanish (Spain)',
}

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '').strip()
        from_language = request.POST.get('from_language', 'en')
        to_language = request.POST.get('to_language')
       
        if input_text:
            try:
                translator = Translator()
                translated_text = translator.translate(input_text, src=from_language, dest=to_language).text
                from_language_full_name = LANGUAGE_MAPPING.get(from_language, from_language)
                to_language_full_name = LANGUAGE_MAPPING.get(to_language, to_language)
                
                
                # Save the translation to the database
                TranslationHistory.objects.create(
                    input_text=input_text,
                    translated_text=translated_text,
                    from_language=from_language_full_name,
                    to_language=to_language_full_name
                )
                
                # Get translation history for current session
                history = TranslationHistory.objects.all().order_by('-timestamp')
                
                return render(request, 'lang.html', {
                    'input_text': input_text,
                    'translated_text': translated_text,
                    'history': history,
                    'in_language':request.POST.get('from_language'),
                    'out_language':request.POST.get('to_language')
                    
                })
            except Exception as e:
                return HttpResponseServerError(f"<h1>Error Occurred:</h1><p>{str(e)}</p>")
        
            
    
    # On GET request, just render the page with history
    
    else:
        return render(request,'lang.html',{'history': TranslationHistory.objects.all().order_by('-timestamp')})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete_old_messages(request):
    TranslationHistory.objects.all().delete()
    return render(request,'lang.html')


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .retrieval import search_ifrs
from .auditor_ai import generate_auditor_focus

ALLOWED_IFRS = ["IFRS9", "IFRS16", "IFRS17", "IFRS18"]

@csrf_exempt
def ifrs_chatbot(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        standard = data.get("standard")
        question = data.get("question")

        if not standard or not question:
            return JsonResponse({"error": "Missing 'standard' or 'question'"}, status=400)

        if standard.upper() not in ALLOWED_IFRS:
            return JsonResponse({"error": f"Standard '{standard}' not supported"}, status=400)

        # IMPORTANT FIX (lowercase for folder match)
        result = search_ifrs(standard.lower(), question)

        if not result:
            return JsonResponse({"error": "No match found"}, status=404)

        auditor_focus = generate_auditor_focus(result["text"])

        response = {
            "answer": result["text"],
            "reference": f'{result["standard"]} - {result["section"]} (ID: {result["para_id"]})',
            "auditor_focus": auditor_focus,
            "disclaimer": "For educational use only."
        }

        return JsonResponse(response)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        print(f"[ERROR] {e}")
        return JsonResponse({"error": str(e)}, status=500)

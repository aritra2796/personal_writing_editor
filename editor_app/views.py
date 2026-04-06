from django.shortcuts import render
import json
import pymysql
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline

# Load Hugging Face model
editor = pipeline("text-generation", model="distilgpt2")

@csrf_exempt
def polish_draft(request):
    if request.method == "POST":
        data = json.loads(request.body)
        draft = data.get("draft", "").strip()

        if not draft:
            return JsonResponse({"error": "Draft is empty"}, status=400)

        try:
            # Hugging Face LLM call - Refined prompt and parameters
            prompt = (
                f"Rewrite the following draft with professional polish while maintaining a personal, "
                f"clear, and engaging tone:\n\nDraft: {draft}\n\nRefined:"
            )
            
            response = editor(
                prompt, 
                max_new_tokens=150, 
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.25, 
                no_repeat_ngram_size=3,
                return_full_text=False
            )
            
            polished = response[0]["generated_text"].strip()
            
            # Post-processing: Remove everything after the first potential end-of-thought
            if "\n\n" in polished:
                polished = polished.split("\n\n")[0]

            # Save to MySQL
            conn = pymysql.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db=os.getenv('DB_NAME')
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO drafts (raw_text, polished_text) VALUES (%s, %s)", (draft, polished))
            conn.commit()
            cursor.close()
            conn.close()

            return JsonResponse({"polished": polished})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_draft(request, id):
    if request.method == "POST":
        try:
            conn = pymysql.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db=os.getenv('DB_NAME')
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM drafts WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            conn.close()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=405)

def history(request):
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME')
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, raw_text, polished_text, created_at FROM drafts ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Pass results to template
    return render(request, "history.html", {"drafts": rows})

def home(request):
    return render(request, "editor.html")
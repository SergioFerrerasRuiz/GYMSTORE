from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

load_dotenv()

app = Flask(__name__)

# Obtener configuración
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
ai_project_name = os.getenv('QA_PROJECT_NAME')
ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

# Crear cliente de Azure
credential = AzureKeyCredential(ai_key)
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

# Lista global para el historial de chat
chat_history = []

def get_answer(user_question):
    try:
        response = ai_client.get_answers(
            question=user_question,
            project_name=ai_project_name,
            deployment_name=ai_deployment_name
        )
        answers = []
        for candidate in response.answers:
            confidence = candidate.confidence

            if confidence >= 0.01:
                answers.append({
                    'answer': candidate.answer.replace("Respuesta:", "").strip(),
                    'confidence': candidate.confidence,
                    'source': candidate.source
                })
            else:
                answers.append({
                    'answer': "Solo respondo preguntas en relación con GYMSTORE.¿Que quieres saber?",
                    'confidence': "100%",
                    'source': "System"
                })
        return answers
        
    except Exception as ex:
        return {"error": str(ex)}

@app.route('/')
def home():
    return render_template("chat.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    answers = get_answer(user_question)

    # Añadir la pregunta y respuesta al historial
    chat_history.append({'user_question': user_question, 'answer': answers[0]['answer'] if answers else "Lo siento, no pude obtener una respuesta."})

    return jsonify(answers)

if __name__ == "__main__":
    app.run(debug=True)

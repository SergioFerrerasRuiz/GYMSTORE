from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Cargar variables de entorno
load_dotenv()

# Obtener configuración
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
ai_project_name = os.getenv('QA_PROJECT_NAME')
ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

# Crear cliente de Azure
credential = AzureKeyCredential(ai_key)
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

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
                    'answer': "Solo respondo preguntas en relación con GYMSTORE. ¿Qué quieres saber?",
                    'confidence': "100%",
                    'source': "System"
                })
        return answers
        
    except Exception as ex:
        return {"error": str(ex)}

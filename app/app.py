import os
from flask import Flask, render_template, request, jsonify
from azure_client import get_answer  # Asegúrate de que el import es correcto

# Obtener la ruta absoluta del directorio del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../templates"),
    static_folder=os.path.join(BASE_DIR, "../static")
)

# Lista global para el historial de chat
chat_history = []

@app.route('/')
def home():
    return render_template("chat.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    answers = get_answer(user_question)

    # Añadir la pregunta y respuesta al historial
    chat_history.append({
        'user_question': user_question,
        'answer': answers[0]['answer'] if answers else "Lo siento, no pude obtener una respuesta."
    })

    return jsonify(answers)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from models import init_db, get_all_tasks, add_task, delete_task, update_task_completion, update_task_description
from translate import translate_text, LANG_CODES

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks, languages=LANG_CODES.keys())

@app.route('/add_task', methods=['POST'])
def add_task_route():
    data = request.json
    description = data.get('description', '').strip()
    if description:
        add_task(description)
        return jsonify({"status": "success"})
    return jsonify({"status": "fail", "message": "Description required"}), 400

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    delete_task(task_id)
    return jsonify({"status": "success"})

@app.route('/toggle_complete/<int:task_id>', methods=['POST'])
def toggle_complete(task_id):
    data = request.json
    completed = data.get('completed', False)
    update_task_completion(task_id, completed)
    return jsonify({"status": "success"})

@app.route('/translate/<int:task_id>', methods=['POST'])
def translate_task(task_id):
    data = request.json
    target_lang = data.get('language', '').lower()

    if target_lang not in LANG_CODES:
        return jsonify({"status": "fail", "message": "Unsupported language"}), 400

    tasks = get_all_tasks()
    # print("all the tasks",tasks)

    task = next((t for t in tasks if t['id'] == task_id), None)
    # print("task to translate", task)

    if not task:
        return jsonify({"status": "fail", "message": "Task not found"}), 404
    
    # print("task description",task['description'])  # Debugging: print task description
    # print("target language", LANG_CODES[target_lang])  # Debugging: print target language

    translated_text = translate_text(task['description'], LANG_CODES[target_lang])
    # print("translated text",translated_text)

    if translated_text.startswith("Error") or translated_text in ["API key not set", "Unsupported language", "Translation error"]:
        return jsonify({"status": "fail", "message": translated_text}), 500

    # Optionally update the description in DB to translated text or just return translated text
    # Here, just return translated text without saving to DB
    return jsonify({"status": "success", "translated": translated_text})

if __name__ == '__main__':
    app.run(debug=True)

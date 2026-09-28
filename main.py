from flask import Flask, render_template, request
from explanation_module import explain
from summary_module import summarize
from quiz_module import generate_quiz
from learning_path import generate_path
from qna import ask_question

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = summary = quiz = answer = None
    path = []
    topic = ""

    if request.method == "POST":
        topic = request.form.get("topic", "")
        question = request.form.get("question", "")

        if question:
            answer = ask_question(topic, question)
            result = request.form.get("result", "")
            summary = request.form.get("summary", "")
            quiz = request.form.get("quiz", "")
            path = generate_path(topic)
        elif topic:
            result = explain(topic)
            summary = summarize(result)
            quiz = generate_quiz(topic)
            path = generate_path(topic)

    return render_template(
        "index.html",
        result=result,
        summary=summary,
        quiz=quiz,
        answer=answer,
        path=path,
        topic=topic,
    )

if __name__ == "__main__":
    app.run(debug=True)
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import Markup, escape

load_dotenv()

from app.components.retreiver import create_qa_chain

app = Flask(__name__)
app.secret_key = os.urandom(24)

def nl2br(text):
    return Markup("<br>\n").join(escape(text).splitlines())

app.jinja_env.filters["nl2br"] = nl2br

@app.route("/", methods=["GET", "POST"])
def index():
    if "messages" not in session:
        session["messages"] = []
    
    if request.method == "POST": 
        user_message = request.form.get("prompt")
        if user_message:
            messages = session["messages"]
            messages.append({"role": "user", "content": user_message})
            session["messages"] = messages
            try:
                qa_chain = create_qa_chain()
                response = qa_chain.invoke({"query": user_message})
                response = response.get("result","No response")
                messages.append({"role": "assistant", "content": response})
                session["messages"] = messages

            except Exception as e:
                error_message = str(e)
                return render_template("index.html", error=error_message, messages=session["messages"])

            
        return redirect(url_for("index"))
    return render_template("index.html", messages=session.get("messages", []))

@app.route("/clear", methods=["GET"])
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return {"status": "healthy"}, 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False, use_reloader=False)




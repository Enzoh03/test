from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__,template_folder="site1/templates", static_folder="site1/static")

@app.route("/")
def home():
    return render_template("form.html")



@app.route("/enviar", methods=["POST"])
def enviar():
    
    resp2 = request.form.get("respn2")
    if resp2 == "":
        resp2 = "nada Informado"
    
    nome = request.form.get("nome").title()
    
    data_info = {
        "nome"   : nome,
        "respn1" : request.form.get("respn1").title(),
        "respn2" : resp2.title(),
        "comuni" : request.form.get("comunidade"),
        "data"   : request.form.get("data")
    }
    supabase.table("Info").insert(data_info).execute()

    id_info = (supabase.table("Info").select("id").order("id", desc=True).limit(1).single().execute())
    
    id_fk = id_info.data["id"]
    
    email = request.form.get("email") 
    if email == "":
        email = "nada informado"
    
    data_contato = {
        "cel1"        : request.form.get("cel1"),
        "cel2"        : request.form.get("cel2"),
        "email"       : email,
        "key_foreign" : id_fk
    }

    
    comp = request.form.get("compl") 
    if comp == "":
        comp = "nada informado"
    
    data_ender = {
        "rua" : request.form.get("rua").title(),
        "bairro" : request.form.get("bairro").title(),
        "num" :  request.form.get("num"),
        "comple" : comp,
        "key_foreign" : id_fk
    }
    
    supabase.table("contato").insert(data_contato).execute()
    supabase.table("endereco").insert(data_ender).execute()

    
    return redirect(url_for("confirmacao", nome=nome))

@app.route("/confirmacao")
def confirmacao():
    nome = request.args.get("nome")
    return render_template("end.html", nome=nome)

if __name__ == "__main__":
    app.run(debug=True) 
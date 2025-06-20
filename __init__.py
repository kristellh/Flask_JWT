from flask import Flask
from flask import render_template
from flask import json
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from datetime import timedelta                                                                                                                                  
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clée privée
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Durée de validité de 1 heure
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html')
  
@app.route("/formulaire", methods=["GET"])
def formulaire():
    return render_template("formulaire.html")
# Création d'une route qui vérifie l'utilisateur et retour un Jeton JWT si ok.
# La fonction create_access_token() est utilisée pour générer un jeton JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
     
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401
  # Exemple : l'utilisateur "test" est un admin
    role = "admin" if username == "test" else "user"

    # On ajoute le rôle dans le token via "additional_claims"
    access_token = create_access_token(
        identity=username,
        additional_claims={"role": role}
    )
   
  
    return jsonify(access_token=access_token)
  
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"msg": "Accès interdit : vous n'êtes pas administrateur"}), 403

    return jsonify(msg="Bienvenue dans l'espace admin"), 200

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
                                                                                                               
if __name__ == "__main__":
  app.run(debug=True)

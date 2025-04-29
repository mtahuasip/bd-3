from flask import Flask, jsonify, request
from neo4j import GraphDatabase

app = Flask(__name__)

# Configurar la conexión a Neo4j
uri = "bolt://localhost:7687"  # Usualmente es localhost:7687
username = "neo4j"  # Nombre de usuario por defecto
password = "password"  # Contraseña configurada para tu base de datos

# Crear el controlador de la base de datos
driver = GraphDatabase.driver(uri, auth=(username, password))


# Función para ejecutar una consulta Cypher
def execute_query(query, parameters=None):
    session = driver.session()
    try:
        result = session.run(query, parameters or {})
        return result
    finally:
        session.close()


@app.route("/")
def home():
    return "Bienvenido a Flask con Neo4j!"


# Ruta de ejemplo para obtener nodos (personas) de la base de datos
@app.route("/personas", methods=["GET"])
def get_personas():
    query = "MATCH (p:Persona) RETURN p.nombre AS nombre"
    result = execute_query(query)
    personas = [record["nombre"] for record in result]
    return jsonify(personas)


# Ruta de ejemplo para crear un nodo
@app.route("/crear_persona", methods=["POST"])
def create_persona():
    data = request.get_json()
    nombre = data.get("nombre")
    query = "CREATE (p:Persona {nombre: $nombre}) RETURN p"
    execute_query(query, parameters={"nombre": nombre})
    return jsonify({"message": f"Persona '{nombre}' creada exitosamente!"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)

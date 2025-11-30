from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)

api = Api(
    app,
    version="1.0",
    title="API de Catálogo de Productos de Limpieza",
    description="API REST para gestionar un catálogo de productos de limpieza",
    doc="/swagger/"
)

# -------------------- Ruta raíz -------------------- #
@app.route("/")
def index():
    return {
        "mensaje": "API de Productos de Limpieza",
        "documentacion": "/swagger/",
        "endpoints_principales": [
            "/catalogos/productos",
            "/catalogos/productos/<id>",
            "/catalogos/categorias"
        ]
    }

# -------------------- Modelos -------------------- #
ns = api.namespace("catalogos", description="Operaciones del catálogo")

producto_model = api.model("Producto", {
    "id": fields.Integer(required=True, description="ID único del producto"),
    "nombre": fields.String(required=True, description="Nombre del producto"),
    "marca": fields.String(required=True, description="Marca del producto"),
    "categoria": fields.String(required=True, description="Categoría del producto"),
})

categoria_model = api.model("Categoria", {
    "id": fields.Integer(required=True, description="ID de la categoría"),
    "nombre": fields.String(required=True, description="Nombre de la categoría"),
    "descripcion": fields.String(required=True, description="Descripción corta"),
})

# -------------------- Datos de ejemplo -------------------- #
PRODUCTOS = [
    {"id": 1, "nombre": "Cloro multiusos",        "marca": "LimpioMax",   "categoria": "Desinfectantes"},
    {"id": 2, "nombre": "Detergente líquido",     "marca": "CleanWash",   "categoria": "Detergentes"},
    {"id": 3, "nombre": "Limpiador de vidrios",   "marca": "CrystalPro",  "categoria": "Limpieza de superficies"},
    {"id": 4, "nombre": "Jabón antibacterial",    "marca": "SafeHands",   "categoria": "Higiene personal"},
    {"id": 5, "nombre": "Ambientador en aerosol", "marca": "FreshAir",    "categoria": "Ambientadores"},
    {"id": 6, "nombre": "Desengrasante cocina",   "marca": "GreaseOff",   "categoria": "Desengrasantes"},
]

CATEGORIAS = [
    {
        "id": 1,
        "nombre": "Desinfectantes",
        "descripcion": "Productos para eliminar gérmenes en pisos, baños y superficies."
    },
    {
        "id": 2,
        "nombre": "Detergentes",
        "descripcion": "Productos para lavado de ropa y textiles."
    },
    {
        "id": 3,
        "nombre": "Limpieza de superficies",
        "descripcion": "Limpiadores para vidrios, muebles y superficies lisas."
    },
    {
        "id": 4,
        "nombre": "Higiene personal",
        "descripcion": "Jabones y productos enfocados en higiene de las personas."
    },
    {
        "id": 5,
        "nombre": "Ambientadores",
        "descripcion": "Productos para mejorar el olor de ambientes cerrados."
    },
    {
        "id": 6,
        "nombre": "Desengrasantes",
        "descripcion": "Productos especializados en remover grasa difícil."
    },
]

# -------------------- Endpoints -------------------- #
@ns.route("/productos")
class ProductosList(Resource):
    @ns.marshal_list_with(producto_model)
    def get(self):
        """Listar todos los productos del catálogo"""
        return PRODUCTOS


@ns.route("/productos/<int:id>")
@ns.param("id", "ID del producto")
class ProductoDetail(Resource):
    @ns.marshal_with(producto_model)
    def get(self, id):
        """Obtener un producto específico por ID"""
        for producto in PRODUCTOS:
            if producto["id"] == id:
                return producto
        api.abort(404, f"Producto con ID {id} no encontrado")


@ns.route("/categorias")
class CategoriasList(Resource):
    @ns.marshal_list_with(categoria_model)
    def get(self):
        """Listar todas las categorías disponibles"""
        return CATEGORIAS


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


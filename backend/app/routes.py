import time
import logging
from flask import Blueprint, request, jsonify
from .models import db, Aula
from .schemas import AulaSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')
aula_schema = AulaSchema()
aulas_schema = AulaSchema(many=True)

@bp.route('/planos', methods=['GET'])
def listar_planos():
    pass 

@bp.route('/planos', methods=['POST'])
def criar_plano():
    pass

@bp.route('/planos/<int:id>', methods=['PUT'])
def editar_plano(id):
    pass

@bp.route('/planos/<int:id>', methods=['DELETE'])
def excluir_plano(id):
    pass

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@bp.route('/ia/recomendar', methods=['POST'])
def smart_assist():
    start_time = time.time()
    data = request.json
    latency = round(time.time() - start_time, 2)
    logger.info(f"AI Request: Title='{data.get('titulo')}', Discipline='{data.get('disciplina')}', Latency={latency}s")
    return jsonify({
        "conteudos_complementares": "...",
        "topicos_relacionados": "...",
        "tags_recomendadas": ["Tag1", "Tag2", "Tag3"]
    })
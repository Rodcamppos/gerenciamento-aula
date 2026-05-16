import time
import logging
import os
from flask import Blueprint, request, jsonify
from .models import db, Aula
from .schemas import AulaSchema
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')
aula_schema = AulaSchema()
aulas_schema = AulaSchema(many=True)

api_key = os.environ.get("OPENAI_API_KEY")
if api_key and api_key != "sua_chave_aqui":
    client = OpenAI(api_key=api_key)
else:
    client = None

@bp.route('/planos', methods=['GET'])
def listar_planos():
    page = request.args.get('page', 1, type=int)
    busca = request.args.get('titulo', '')
    disciplina = request.args.get('disciplina', '')
    
    query = Aula.query
    if busca:
        query = query.filter(Aula.titulo.ilike(f'%{busca}%'))
    if disciplina:
        query = query.filter(Aula.disciplina == disciplina)
    
    query = query.order_by(Aula.data_criacao.desc())
    
    paginados = query.paginate(page=page, per_page=10)
    return jsonify({
        "planos": aulas_schema.dump(paginados.items),
        "total": paginados.total,
        "paginas": paginados.pages
    }), 200

@bp.route('/planos', methods=['POST'])
def criar_plano():
    data = request.json
    errors = aula_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    novo_plano = aula_schema.load(data, session=db.session)
    db.session.add(novo_plano)
    db.session.commit()
    return aula_schema.jsonify(novo_plano), 201

@bp.route('/planos/<int:id>', methods=['PUT'])
def editar_plano(id):
    plano = Aula.query.get_or_404(id)
    data = request.json
    plano_atualizado = aula_schema.load(data, instance=plano, partial=True)
    db.session.commit()
    return aula_schema.jsonify(plano_atualizado), 200

@bp.route('/planos/<int:id>', methods=['DELETE'])
def excluir_plano(id):
    plano = Aula.query.get_or_404(id)
    db.session.delete(plano)
    db.session.commit()
    return jsonify({"message": "Excluído com sucesso"}), 204

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@bp.route('/ia/recomendar', methods=['POST'])
def smart_assist():
    if client is None:
        return jsonify({"error": "Configuração de IA pendente (Chave não encontrada)"}), 500
    
    start_time = time.time()
    data = request.json
    
    titulo = data.get('titulo', '')
    disciplina = data.get('disciplina', '')
    ementa = data.get('ementa', '')
    
    prompt = f"""
    Atue como um Assistente Pedagógico. Com base no título "{titulo}", na disciplina "{disciplina}" 
    e na ementa "{ementa}", sugira conteúdos complementares, tópicos relacionados e 3 tags.
    Responda obrigatoriamente no formato JSON com as chaves: 
    "conteudos", "topicos" e "tags" (lista de 3 strings).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        resultado_ia = response.choices[0].message.content
        latency = round(time.time() - start_time, 2)
        logger.info(f"[INFO] AI Request: Title='{titulo}', Discipline='{disciplina}', Latency={latency}s")
        return resultado_ia, 200
    
    except Exception as e:
        logger.error(f"Erro na IA: {str(e)}")
        return jsonify({"error": "Falha ao consultar assistente de IA"}), 500
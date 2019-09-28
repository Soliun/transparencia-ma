from flask import Flask
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_cors import CORS

from scrapper import despesas_total, despesas_por_funcao, despesas_por_orgao


app = Flask(__name__)
CORS(app)

app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'


api = Api(app = app, 
		  version = "1.0", 
		  title = "Transparência Maranhão", 
          description = "Uma API não oficial com os dados sobre as despesas do Governo do Maranhão")
          
ns = api.namespace('despesas', description='Dados de despesas')

model = api.model('Dados sobre uma função ou orgão', {
    'codigo': fields.String(description='Código da função ou orgão', example="04"),
    'nome': fields.String(description='Nome da função ou orgão', example="ADMINISTRACAO"),
    'url_detalhe': fields.String(description='Endereço para mais detalhes', example="http://www.transparencia.ma.gov.br/app/despesas/por-funcao/2016/funcao/04?"),
    'empenhado': fields.Float(description='Valor empenhado', example=821854500.93),
    'liquidado': fields.Float(description='Valor liquidado', example=794738131.95),
    'pago': fields.Float(description='Valor pago', example=775701742.7),
})

model_credor = api.model('Dados sobre um dado credor', {
    'cpf/cnpj': fields.String(description='Número do CPF ou do CNPJ do credor', example="04"),
    'nome': fields.String(description='Nome do credor', example="ADMINISTRACAO"),
    'url_detalhe': fields.String(description='Endereço para mais detalhes', example="http://www.transparencia.ma.gov.br/app/despesas/por-funcao/2016/funcao/04?"),
    'empenhado': fields.Float(description='Valor empenhado', example=821854500.93),
    'liquidado': fields.Float(description='Valor liquidado', example=794738131.95),
    'pago': fields.Float(description='Valor pago', example=775701742.7),
})

@ns.route('/<string:ano>')
class Despesas(Resource):

    @api.marshal_with(model, mask='*')
    @api.doc(responses={ 200: 'OK', 400: 'Despesas não encontradas' }, 
			 params={ 'ano': 'Ano de referência para as despesas' })
    def get(self, ano):
        return despesas_total(ano)


@ns.route('/<string:cod_funcao>/<string:ano>')
class DespesasPorFuncao(Resource):

    @api.marshal_with(model, mask='*')
    @api.doc(responses={ 200: 'OK', 400: 'Despesas não encontradas' }, 
    params={ 'ano': 'Ano de referência para as despesas',
    'cod_funcao' : 'Código da função (educação, saúde ...) de referência para as despesas'})
    def get(self, cod_funcao, ano):
        return despesas_por_funcao(cod_funcao, ano)

@ns.route('/<string:cod_orgao>/<string:cod_funcao>/<string:ano>')
class DespesasPorOrgao(Resource):

    @api.marshal_with(model_credor, mask='*')
    @api.doc(responses={ 200: 'OK', 400: 'Despesas não encontradas' }, 
    params={ 'ano': 'Ano de referência para as despesas',
    'cod_orgao' : 'Código do orgão público de referência para as despesas'})
    def get(self, cod_orgao, cod_funcao, ano):
        return despesas_por_orgao(cod_orgao, cod_funcao, ano)

if __name__ == '__main__':
    app.run(debug=True)
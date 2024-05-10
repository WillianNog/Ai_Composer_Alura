from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__, static_folder='static')

app.template_folder = '.'

# Configuração da API do Google GenerativeAI
GOOGLE_API_KEY = 'Chave_da_Api_aqui'
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/gerar_letra', methods=['POST'])
def gerar_letra():
  # Recupera os dados do formulário
  genre = request.form['genre']
  subgenre = request.form['subgenre']
  rhythm = request.form['rhythm']
  mood = request.form['mood']
  keywords = request.form['keywords']
  
  # Mensagem para processamento da IA
  mensagem = f"Crie uma música utilizando os parametros que estou te mandando como palavras-chaves, gênero, ritmo e clima: Genero: {genre}, Subgenero: {subgenre}, Ritmo: {rhythm}, Clima:{mood}, Palavra-chave: {keywords}. Utilize rimas. E tem que fazer sentido entre si."

  # Configurações de geração de conteúdo
  generation_config = {
      "candidate_count": 1,
      "temperature": 0.5,
  }
  safety_settings = {
      'HATE': 'BLOCK_NONE',
      'HARASSMENT': 'BLOCK_NONE',
      'SEXUAL' : 'BLOCK_NONE',
      'DANGEROUS' : 'BLOCK_NONE'
  }
  
  # Inicializa o modelo Gemini 1.0 Pro
  model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                                generation_config=generation_config,
                                safety_settings=safety_settings)
  
  # Gera conteúdo criativo com base na mensagem
  response = model.generate_content(mensagem)
  
  # Retorna a resposta como JSON
  return jsonify({'letra': response.text})

if __name__ == '__main__':
  app.run(debug=True)

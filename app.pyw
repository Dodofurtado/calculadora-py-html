from flask import Flask, render_template, request, jsonify
import webview
import threading
import operator
import re

app = Flask(__name__)

# Operadores permitidos e seus mapeamentos seguros
OPERADORES = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def validar_expressao(expressao):
    """Valida se a expressão contém apenas números e operadores permitidos."""
    padrao = r'^[\d\s\+\-\*\/\.\(\)]+$'
    return bool(re.match(padrao, expressao))

def calcular(expressao):
    """Calcula a expressão matemática de forma segura."""
    try:
        if not validar_expressao(expressao):
            return 'Expressão inválida'
            
        # Remove espaços em branco
        expressao = expressao.replace(' ', '')
        
        # Avalia a expressão de forma segura
        def eval_expr(expr):
            # Converte a expressão em uma lista de tokens
            tokens = re.findall(r'[\d.]+|[+\-*/()]', expr)
            pilha = []
            operador_atual = '+'
            
            for token in tokens:
                if token in '+-*/':
                    operador_atual = token
                elif token == '(':
                    sub_expr = ''
                    parenteses = 1
                    i = tokens.index(token) + 1
                    while parenteses > 0 and i < len(tokens):
                        if tokens[i] == '(':
                            parenteses += 1
                        elif tokens[i] == ')':
                            parenteses -= 1
                        if parenteses > 0:
                            sub_expr += tokens[i]
                        i += 1
                    resultado = eval_expr(sub_expr)
                    pilha.append(resultado)
                else:
                    numero = float(token)
                    if operador_atual == '+':
                        pilha.append(numero)
                    elif operador_atual == '-':
                        pilha.append(-numero)
                    elif operador_atual == '*':
                        pilha[-1] *= numero
                    elif operador_atual == '/':
                        if numero == 0:
                            raise ZeroDivisionError
                        pilha[-1] /= numero
            
            return sum(pilha)
            
        resultado = eval_expr(expressao)
        
        # Formata o resultado
        if resultado.is_integer():
            return int(resultado)
        return round(resultado, 8)
        
    except (ValueError, ZeroDivisionError, SyntaxError, AttributeError):
        return 'Erro'
    except Exception as e:
        print(f"Erro não esperado: {str(e)}")
        return 'Erro'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular_route():
    data = request.get_json()
    expressao = data.get('expressao', '').strip()
    if not expressao:
        return jsonify({'resultado': '0'})
    resultado = calcular(expressao)
    return jsonify({'resultado': str(resultado)})

def start_server():
    """Inicia o servidor Flask em modo silencioso."""
    import logging
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(port=5000, debug=False, use_reloader=False)

def verificar_porta():
    """Verifica se a porta 5000 está disponível."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resultado = sock.connect_ex(('127.0.0.1', 5000))
    sock.close()
    return resultado != 0

if __name__ == '__main__':
    if not verificar_porta():
        import sys
        sys.exit("Erro: A porta 5000 já está em uso. Feche outros programas que possam estar usando esta porta.")

    # Inicia o servidor em uma thread separada
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # Espera o servidor iniciar
    import time
    time.sleep(1.5)

    # Configurações da janela
    window = webview.create_window(
        "Calculadora Moderna",
        "http://127.0.0.1:5000",
        width=400,
        height=600,
        resizable=True,
        min_size=(350, 500),
        text_select=False
    )

    # Inicia a aplicação
    webview.start(debug=False)

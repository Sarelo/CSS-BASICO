import http.server
import socketserver
import json

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/calculate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            num1 = float(data['num1'])
            num2 = float(data['num2'])
            operacao = data['operacao']
            resultado = None

            if operacao == 'adição':
                resultado = num1 + num2
            elif operacao == 'subtração':
                resultado = num1 - num2
            elif operacao == 'multiplicação':
                resultado = num1 * num2
            elif operacao == 'divisão':
                if num2 != 0:
                    resultado = num1 / num2
                else:
                    resultado = 'Erro: Divisão por zero não é permitida.'

            response = json.dumps({'resultado': resultado})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

Handler = MyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

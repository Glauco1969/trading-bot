from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/painel')
def painel():
    return render_template('painel.html')  # seu painel atual

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

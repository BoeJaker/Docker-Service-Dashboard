from flask import Flask, render_template
from flask_reverse_proxy import FlaskReverseProxied

app = Flask(__name__)
app.config['REVERSE_PROXY_PATH'] = '/proxy'
proxied = FlaskReverseProxied(app)

@app.route('/')
def index():
    return render_template('reverse_proxy.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006
)

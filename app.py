from flask_cors import CORS
import connexion

app = connexion.App(__name__, specification_dir='./')

app.add_api('API-spec.yaml')

CORS(app.app, origins=[ 'http://localhost:3000', 'http://localhost:5001', 'http://localhost:3001' ], supports_credentials=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
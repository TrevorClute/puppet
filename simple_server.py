from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    print("✅ Received a GET request!")
    print("Query parameters:", request.args)
    return "Hello from Raspberry Pi! GET request received.\n"

if __name__ == '__main__':
    # 0.0.0.0 allows access from other devices on the network
    app.run(host='0.0.0.0', port=5000)


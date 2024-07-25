from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_lists', methods=['POST'])
def process_lists():
    data = request.json
    list1 = data.get('list1',[])
    list2 = data.get('list2',[])
    print(list1, list2)
    
    # Process the lists here
    # For example, you can perform operations on the lists
    
    # Return the processed data
    return jsonify({'result': 'Lists processed successfully'})

@app.route('/hello', methods=['POST'])
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=False, port=5000)

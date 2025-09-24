from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# --- Scytale Cipher Functions ---

def encrypt_scytale(plaintext, key):
    """Encrypts a message using the scytale cipher."""
    plaintext = plaintext.replace(" ", "").upper()
    num_rows = math.ceil(len(plaintext) / key)
    padding_needed = (num_rows * key) - len(plaintext)
    plaintext += "_" * padding_needed
    
    grid = [['' for _ in range(key)] for _ in range(num_rows)]
    char_index = 0
    for col in range(key):
        for row in range(num_rows):
            grid[row][col] = plaintext[char_index]
            char_index += 1
            
    ciphertext = ""
    for row in range(num_rows):
        ciphertext += "".join(grid[row])
        
    return ciphertext

def decrypt_scytale(ciphertext, key):
    """Decrypts a message using the scytale cipher."""
    num_rows = len(ciphertext) // key
    
    grid = [['' for _ in range(key)] for _ in range(num_rows)]
    char_index = 0
    for row in range(num_rows):
        for col in range(key):
            grid[row][col] = ciphertext[char_index]
            char_index += 1
            
    plaintext = ""
    for col in range(key):
        for row in range(num_rows):
            plaintext += grid[row][col]
            
    return plaintext.replace("_", "")

# --- Flask Routes ---

@app.route('/')
def home():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Handles encryption requests."""
    data = request.json
    plaintext = data.get('text')
    key = int(data.get('key'))
    
    if not plaintext or not key:
        return jsonify({'error': 'Missing text or key'}), 400
        
    ciphertext = encrypt_scytale(plaintext, key)
    return jsonify({'result': ciphertext})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Handles decryption requests."""
    data = request.json
    ciphertext = data.get('text')
    key = int(data.get('key'))
    
    if not ciphertext or not key:
        return jsonify({'error': 'Missing text or key'}), 400
    
    plaintext = decrypt_scytale(ciphertext, key)
    return jsonify({'result': plaintext})

if __name__ == '__main__':
    app.run(debug=True)
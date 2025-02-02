from flask import Flask, render_template, request

app = Flask(__name__)

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Caesar Cipher Logic (handles both encryption and decryption)
def caesar_cipher(message, key, mode):
    translated = ''
    message = message.upper()  # You can remove this if you want to preserve the case
    
    for symbol in message:
        if symbol in SYMBOLS:
            num = SYMBOLS.find(symbol)
            if mode == 'encrypt':
                num = num + key
            elif mode == 'decrypt':
                num = num - key
            
            # Wrap around if necessary
            if num >= len(SYMBOLS):
                num = num - len(SYMBOLS)
            elif num < 0:
                num = num + len(SYMBOLS)
            
            translated += SYMBOLS[num]
        else:
            translated += symbol  # Non-alphabetic characters are added unchanged
    
    return translated

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error_message = None
    
    if request.method == 'POST':
        mode = request.form['mode']
        key = request.form['key']
        message = request.form['message']
        
        # Validate the key range
        try:
            key = int(key)
            if not (0 <= key <= 25):
                error_message = "Key must be between 0 and 25."
            elif not message.strip():
                error_message = "Message cannot be empty."
            else:
                # Call the caesar cipher function
                result = caesar_cipher(message, key, mode)
        except ValueError:
            error_message = "Please enter a valid integer for the key."

    return render_template('index.html', result=result, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

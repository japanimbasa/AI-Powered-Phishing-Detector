
from app import create_app
from flask import Flask, request, jsonify
import logging


app = create_app()

app.debug = True
app.logger.setLevel(logging.DEBUG)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Log the incoming request data to see what’s being sent
        app.logger.debug(f"Received data: {request.json}")
        
        # Example placeholder analysis logic (replace with your actual processing)
        if not request.json:
            raise ValueError("No JSON data received")
        
        # Proceed with the analysis
        result = {"status": "success", "data": request.json}
        
        # Log the successful result
        app.logger.debug(f"Processed data: {result}")
        
        return jsonify(result), 200

    except Exception as e:
        # Log the error and return it in the response
        app.logger.error(f"Error during /analyze: {e}")
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
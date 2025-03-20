from flask import Flask, request, send_file
from generate_gif import add_name_to_gif
import uuid

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_gif_endpoint():
    name = request.args.get('name')
    if not name:
        return "Please provide a name!", 400

    output_file = f"{uuid.uuid4()}.gif"
    add_name_to_gif("ramadan-greeting.gif", output_file, name, "Poppins.ttf", "Janna.ttf")

    return send_file(output_file, mimetype='image/gif', as_attachment=True, download_name=f"{name}.gif")

if __name__ == '__main__':
    app.run(debug=True)

#! A recape of how to handle data that a user might throw at me:
#!  - Query
#!  - Form
#!  - Json

from flask import Flask, request

app = Flask(__name__)

host_ipv4 = 'write here your host ipv4'

@app.route('/')
def index():
    return f"""<a href="http://{host_ipv4}:5000/form-example">Form-example </a> <br>
              <a href="http://{host_ipv4}:5000/query-example">Query-Exaample</a> <br>
              <a href="http://{host_ipv4}:5000/json-example">Json-Exaample</a>"""

@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None
    framework = request.args.get('framework') 
    website = request.args.get('website')

    return f'''<h1>The language value is: {language}</h1>
              <h1>The framework value is: {framework}</h1>
              <h1>The website value is: {website}'''


@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST': #this block is only entered when the form is submitted
        language = request.form.get('language') #if doesn't exsits return None
        framework = request.form['framework'] #if key doesn't exist, returns a 400, bad request error

        return f'''<h1>The language value is: {language}</h1>
                  <h1>The framework value is: {framework}</h1>'''

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


@app.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()

    #check so if the key is not there the req doesn't fail
    language = None
    framework = None
    python_version = None
    example = None
    boolean_test = None

    if request_data:
        if 'language' in request_data:
            language = request_data['language']

        if 'framework' in request_data:
            framework = request_data['framework']

        if 'version_info' in request_data:
            if 'python' in request_data['version_info']:
                python_version = request_data['version_info']['python'] # two keys are needed because of the nested object

        if 'examples' in request_data:
            if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
                example = request_data['examples'][0]  # an index is needed because of the array

        if 'boolean_test' in request_data:
            boolean_test = request_data['boolean_test']

    return f'''
           The language value is: {language}
           The framework value is: {framework}
           The Python version is: {python_version}
           The item at index 0 in the example list is: {example}
           The boolean value is: {boolean_test}'''

if __name__ == "__main__":
    app.run(debug=True, host=host_ipv4)

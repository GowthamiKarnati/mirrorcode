from flask import Flask, render_template, request, jsonify
import sys
from io import StringIO
import subprocess
import os
app = Flask(__name__)

@app.route('/')
def code_editor():
    return render_template('index.html')

@app.route('/run-python', methods=['POST'])
def run_python():
    data = request.get_json()
    code = data.get('code', '')

    output_stream = StringIO()
    sys.stdout = output_stream

    try:
        exec(code, globals(), locals())
        result = output_stream.getvalue()
        sys.stdout = sys.__stdout__

        return result
    except Exception as e:
        sys.stdout = sys.__stdout__
        return str(e)

@app.route('/run-cplusplus', methods=['POST'])
def run_cplusplus():
    data = request.get_json()
    code = data.get('code', '')

    try:
        with open('program.cpp', 'w') as f:
            f.write(code)

        compile_result = subprocess.run(['g++', 'program.cpp', '-o', 'program'], stderr=subprocess.PIPE)

        if compile_result.returncode == 0:
            execution_result = subprocess.run(['./program'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if execution_result.returncode == 0:
                output = execution_result.stdout
            else:
                output = "Execution Error: " + execution_result.stderr
        else:
            output = "Compilation Error: " + compile_result.stderr

        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/run-dart', methods=['POST'])
def run_dart():
    data = request.get_json()
    code = data.get('code', '')

    try:
        # Save the Dart code to a temporary file
        with open('temp.dart', 'w') as f:
            f.write(code)

        # Execute the Dart code and capture the output
        execution_result = subprocess.run(['dart', 'temp.dart'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if execution_result.returncode == 0:
            output = execution_result.stdout
        else:
            output = "Execution Error: " + execution_result.stderr

        return output
    except Exception as e:
        return str(e)


@app.route('/run-javascript', methods=['POST'])
def run_javascript():
    data = request.get_json()
    code = data.get('code', '')

    try:
        process = subprocess.Popen(['node', '-e', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return jsonify({'output': stdout})
        else:
            return jsonify({'error': stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/run-sql', methods=['POST'])
def run_sql():
    data = request.get_json()
    sql_code = data.get('code', '')
    import sqlite3
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()
    try:
        cursor.execute(sql_code)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return str(result)
    except Exception as e:
        return str(e)


@app.route('/run-java', methods=['POST'])
def run_java():
    data = request.get_json()
    code = data.get('code', '')

    try:
        # Save the Java code to a temporary file
        with open('temp.java', 'w') as f:
            f.write(code)

        # Compile and execute the Java code
        compile_result = subprocess.run(['javac', 'temp.java'], stderr=subprocess.PIPE)

        if compile_result.returncode == 0:
            execution_result = subprocess.run(['java', 'temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if execution_result.returncode == 0:
                output = execution_result.stdout
            else:
                output = "Execution Error: " + execution_result.stderr
        else:
            output = "Compilation Error: " + compile_result.stderr

        return output
    except Exception as e:
        return str(e)


@app.route('/run-go', methods=['POST'])
def run_go():
    data = request.get_json()
    go_code = data.get('code', '')

    try:
        # Save the Go code to a temporary file
        with open('temp.go', 'w') as f:
            f.write(go_code)

        # Execute the Go code and capture the output
        execution_result = subprocess.run(['go', 'run', 'temp.go'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if execution_result.returncode == 0:
            output = execution_result.stdout
        else:
            output = "Execution Error: " + execution_result.stderr

        return output
    except Exception as e:
        return str(e)




if __name__ == '__main__':
    app.run(debug=True)

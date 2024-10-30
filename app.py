from flask import Flask, request, render_template, redirect
from pymysql import connect, err

app = Flask(__name__,
    template_folder='/templates',
    static_folder='/static',
    static_url_path=''
)

db_config = {
    'host': 'localhost', 
    'user': 'demo',   
    'password': 'blehblehbleh', 
    'database': 'sql_injection_challenge'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        blacklist = ['union', 'select', 'from', 'where', 'UNION', 'SELECT', 'FROM', 'WHERE']

        for bad_word in blacklist:
            if bad_word in username.lower() or bad_word in password.lower():
                return "Invalid characters in input."

        if authenticate_user(username, password):
            return redirect("https://icarus-6gt4.onrender.com/")
        else:
            return "Invalid credentials. Please try again."

    return render_template('index.html')

def authenticate_user(username, password):
    conn = connect(**db_config)
    curs = conn.cursor()

    try:
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        curs.execute(query, (username, password))
        result = curs.fetchone()
        return result is not None
    except err.ProgrammingError as e:
        print(e)
        return False
    finally:
        curs.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)

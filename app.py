from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=''
)

def get_db_connection():
    conn = sqlite3.connect('challenge.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        blacklist = ["SELECT", "UNION", "FROM", "WHERE"]
        for bad_word in blacklist:
            username = username.replace(bad_word, "")
            password = password.replace(bad_word, "")
            username = username.replace(bad_word.lower(), "")
            password = password.replace(bad_word.lower(), "")

        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            cursor.execute(query)
            user = cursor.fetchone()
           
            if user:
                if user['username'] == 'b4sil1sk_ro0t' and user['password'] == 'funnelweb':
                    return redirect("https://funnelweb.onrender.com/")
                else:
                    result_str = ""
                    for column in user.keys():
                        result_str += f"{column}: {user[column]}\n"
                    return f"<pre>{result_str}</pre>"
            else:
                return "Lies, my boy, are known in a moment."

        except sqlite3.Error as e:
            return f"An error occurred: {e}"

        finally:
            conn.close()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

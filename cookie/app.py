from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)

# Route per la home page
@app.route('/')
def home():
    # Imposta il cookie admin su false
    response = make_response(render_template('home.html'))
    response.set_cookie('admin', 'false')
    return response

# Route per la pagina admin
@app.route('/admin')
def admin():
    # Verifica se il cookie admin è impostato su true
    admin_cookie = request.cookies.get('admin', 'false')
    if admin_cookie.lower() == 'true':
        return render_template('admin.html')
    else:
        return render_template('error.html', message='Non sei autorizzato ad accedere alla pagina admin.')

if __name__ == '__main__':
    app.run(debug=True, port=1337, host="0.0.0.0")

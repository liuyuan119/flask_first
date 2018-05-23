from flask import Flask, redirect, Response, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    import json
    json_dict = dict(code=200, message='adsf')
    return Response(json.dumps(json_dict))


@app.route('/login', methods={"GET", "POST"})
def login():
    return render_template('login.html')


@app.route('/logout', methods={"GET", "POST"})
def logout():
    return redirect('/login')


@app.route('/art/edit/<int:id>/', methods={"GET"})
def art_edit(id):
    mdict = dict(id=id)
    return render_template('art_edit.html', mdict=mdict)


if __name__ == '__main__':
    app.run(debug=True)

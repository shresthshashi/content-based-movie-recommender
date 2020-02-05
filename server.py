from flask import Flask, render_template, request
from recommen import code

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/form1', methods=['POST'])
def hello():
    categ = int(request.form['cat'])
    #result=['hello','you','are','a','good','boy']
    title = request.form['tit']
    k=request.form['choice']
    k=int(k)
    result=code(categ,title,k)
    if(result=='key not found'):
        return 'Oops %s<br/> <a href="/">Back Home</a>' % (result)
    elif(result=='no matched category'):
        return 'Oops %s<br/> <a href="/">Back Home</a>' % (result)
    else:
        return render_template("result.html", len = len(result), result = result)

if __name__ == '__main__':
  app.run(debug=True)
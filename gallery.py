from flask import Flask, request, render_template, g, redirect, url_for

import sqlite3

app = Flask(__name__)

def connect_db():
	sql=sqlite3.connect("/Users/adelasaraci/Documents/Gallery App/data.db")
	sql.row_factory=sqlite3.Row
	return sql

def get_db():
	if not hasattr(g, 'sqlite3'):
		g.sqlite_db=connect_db()
		return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def home():
	db = get_db()
	cur = db.execute('select id, image_url, title, year_of_publication, author from images')
	results = cur.fetchall()
	return render_template('home.html', results=results)

@app.route('/add_link', methods=['GET', 'POST'])
def add_link():

	if request.method == 'GET':
		return render_template('add_link.html')

	else:
		image_url = request.form['image_url']
		title = request.form['title']
		year_of_publication = request.form['year_of_publication']
		author = request.form['author']
		db = get_db()
		db.execute('insert into images(image_url, title, year_of_publication, author) values(?, ?, ?, ?)', [image_url, title, year_of_publication, author])
		db.commit()

		return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

	if request.method == 'GET':
		db = get_db()
		cur = db.execute('select id, image_url, title, year_of_publication, author from images where id=?', [id])
		results = cur.fetchall()

		return render_template('edit.html', results=results)

	else:
		image_url = request.form['image_url']
		title = request.form['title']
		year_of_publication = request.form['year_of_publication']
		author = request.form['author']
		db = get_db()
		db.execute('update images set image_url=?, title=?, year_of_publication=?, author=? where id=?', [image_url, title, year_of_publication, author, id])
		db.commit()

		return redirect(url_for('gallery'))

	

@app.route('/gallery')
def gallery():

	db = get_db()
	cur = db.execute('select id, image_url, title, year_of_publication, author from images')
	results = cur.fetchall()

	return render_template('gallery.html', results=results)


@app.route('/viewresults')
def viewresults():
	db=get_db()
	cur=db.execute('select id, image_url from images')
	results=cur.fetchall()
	return'<img src={}>'.format(results[1]['image_url'])

@app.route('/delete/<int:id>')
def delete_result(id):

	db = get_db()
	db.execute('delete from images where id=?', [id])
	db.commit()

	return redirect(url_for('gallery'))


if __name__ == "__main__":
	app.run(debug=True)

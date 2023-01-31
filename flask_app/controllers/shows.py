from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import show

@app.route('/new')
def create_new_show():
    if not session['user_id']:
        return redirect('/')
    return render_template('new_show.html')

@app.route('/process/new', methods=['POST'])
def process_show():
    if not show.Show.validate_show(request.form):
        session['title'] = request.form['title']
        session['network'] = request.form['network']
        session['release_date'] = request.form['release_date']
        session['description'] = request.form['description']
        return redirect('/new')
    data={
        'user_id': session['user_id'],
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description']
    }
    show.Show.create_show(data)
    session['title'] = ""
    session['network'] = ""
    session['release_date'] = ""
    session['description'] = ""
    return redirect('/shows')

@app.route('/shows/edit/<int:show_id>')
def edit_show(show_id):
    if not session['user_id']:
        return redirect('/')
    data={'id': show_id}
    return render_template('edit_show.html', show=show.Show.get_one_show_by_id(data))

@app.route('/edit/process/<int:show_id>', methods=['POST'])
def process_edit(show_id):
    if not show.Show.validate_show(request.form):
        return redirect(f'/shows/edit/{show_id}')
    data={
        'id': show_id,
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description']
    }
    show.Show.edit_show(data)
    return redirect('/shows')

@app.route('/shows/delete/<int:show_id>')
def process_delete(show_id):
    if not session['user_id']:
        return redirect('/')
    data={'id': show_id}
    show.Show.delete_show(data)
    return redirect('/shows')

@app.route('/shows/<int:show_id>')
def show_one_pie(show_id):
    if not session['user_id']:
        return redirect('/')
    data={
        'id': show_id
        }
    return render_template('show_one_pie.html', show=show.Show.get_one_show_by_id(data))
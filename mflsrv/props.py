from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from mflsrv.auth import login_required
from mflsrv.db import get_db

bp = Blueprint('props', __name__)


@bp.route('/')
def index():
    """Show all the props, most recent first."""
    db = get_db()
    props = db.execute(
        'SELECT p.id, ppin, body, created, author_id, username'
        ' FROM tprops p JOIN tuser u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('props/index.html', props=props)


def get_prop(id, check_author=True):
    """Get a prop and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of prop to get
    :param check_author: require the current user to be the author
    :return: the prop with author information
    :raise 404: if a prop with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    prop = get_db().execute(
        'SELECT p.id, ppin, body, created, author_id, username'
        ' FROM tprops p JOIN tuser u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if prop is None:
        abort(404, "Prop id {0} doesn't exist.".format(id))

    if check_author and prop['author_id'] != g.user['id']:
        abort(403)

    return prop


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new prop for the current user."""
    if request.method == 'POST':
        ppin = request.form['ppin']
        body = request.form['body']
        error = None

        if not ppin:
            error = 'PIN is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tprops (ppin, body, author_id)'
                ' VALUES (?, ?, ?)',
                (ppin, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('props.index'))

    return render_template('props/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a prop if the current user is the author."""
    prop = get_prop(id)

    if request.method == 'POST':
        ppin = request.form['ppin']
        body = request.form['body']
        error = None

        if not ppin:
            error = 'PIN is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE tprops SET ppin = ?, body = ? WHERE id = ?',
                (ppin, body, id)
            )
            db.commit()
            return redirect(url_for('props.index'))

    return render_template('props/update.html', prop=prop)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete a prop.

    Ensures that the prop exists and that the logged in user is the
    author of the prop.
    """
    get_prop(id)
    db = get_db()
    db.execute('DELETE FROM tprops WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('props.index'))

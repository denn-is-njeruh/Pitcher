from app.main.forms import CommentForm, UpdateProfile
from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from .. import db,photos
from ..models import User,Comment



@main.route('/pitch/comment/new/<int:id>', methods=['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    pitch = Comment.pitch_id
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        #updated comment instance
        new_comment = Comment(pitch_id=pitch.id,pitch_title =title,pitch_review = comment,user=current_user)

        #save review method
        new_comment.save_comment()
        return redirect(url_for('.pitch',id = pitch.id))

    title = f'{pitch.title} comment'
    return render_template('new_comment.html',title=title,comment_form=form,pitch=pitch)

@main.route('/user/<uname>/update/pic',methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))
    
    return render_template('profile/update.html',form=form)
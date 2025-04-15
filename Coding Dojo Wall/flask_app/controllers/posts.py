from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User

@app.route("/posts/create", methods=["POST"])
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    
    print("Form data received:", request.form) 
    
    if not Post.validate_post(request.form):
        return redirect('/wall')
    
    data = {
        "content": request.form['content'],
        "user_id": session['user_id']
    }
    
    post_id = Post.save(data)
    if not post_id:
        flash("Failed to create post. Please try again.", "post")
    else:
        flash("Post created successfully!", "post_success")
    
    return redirect('/wall')

@app.route("/posts/delete/<int:post_id>")
def delete_post(post_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
  
    Post.delete(post_id)
    flash("Post deleted successfully", "post_success")
    return redirect('/wall')
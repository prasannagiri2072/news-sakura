# app.py  
  
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory  
import json  
import os  
from functools import wraps  
from werkzeug.utils import secure_filename  
from datetime import datetime  
  
app = Flask(__name__)  
app.secret_key = 'your_secret_key'  # Replace with a secure secret key  
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Ensure templates reload automatically  
  
# Configuration for file uploads  
app.config['UPLOAD_FOLDER'] = 'static/uploads/videos'  
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit  
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'}  
  
# Ensure upload directory exists  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  
  
# Helper function to check allowed file extensions  
def allowed_file(filename):  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  
  
# Helper functions to load and save JSON data  
def load_json(file_path):  
    if os.path.exists(file_path):  
        with open(file_path, 'r', encoding='utf-8') as f:  
            return json.load(f)  
    else:  
        return []  
  
def save_json(data, file_path):  
    with open(file_path, 'w', encoding='utf-8') as f:  
        json.dump(data, f, indent=4, ensure_ascii=False)  
  
# Decorator to check if admin is logged in  
def login_required(f):  
    @wraps(f)  
    def decorated_function(*args, **kwargs):  
        if not session.get('logged_in'):  
            flash('You need to log in first.', 'danger')  
            return redirect(url_for('login'))  
        return f(*args, **kwargs)  
    return decorated_function  
  
# Context Processor to inject 'datetime' into templates  
@app.context_processor  
def inject_datetime():  
    return {'datetime': datetime}  
  
# Landing Page  
@app.route('/')  
def landing():  
    return redirect(url_for('index'))  
  
# Home Page  
@app.route('/home')  
@app.route('/index')  
def index():  
    articles = load_json('data/news.json')  
    categories = ['Politics', 'Technology', 'Entertainment', 'Business']  
    categorized_articles = {category: [] for category in categories}  
    for article in articles:  
        category = article.get('category', 'General').capitalize()  
        if category in categories:  
            categorized_articles[category].append(article)  
        else:  
            categorized_articles.setdefault('General', []).append(article)  
    breaking_news = load_json('data/breaking_news.json')  
    videos = load_json('data/videos.json')  
    return render_template('index.html', categorized_articles=categorized_articles,  
                           breaking_news=breaking_news, articles=articles, videos=videos)  
  
# Category Pages  
@app.route('/category/<category_name>')  
def category_page(category_name):  
    articles = load_json('data/news.json')  
    category_articles = [article for article in articles if article.get('category', '').lower() == category_name.lower()]  
    if not category_articles:  
        flash('No articles found in this category.', 'info')  
    return render_template('category.html', articles=category_articles, category_name=category_name.capitalize())  
  
# About Page  
@app.route('/about')  
def about():  
    return render_template('about.html')  
  
# Contact Page  
@app.route('/contact', methods=['GET', 'POST'])  
def contact():  
    if request.method == 'POST':  
        name = request.form['name']  
        email = request.form['email']  
        message = request.form['message']  
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
  
        messages = load_json('data/messages.json')  
        messages.append({'name': name, 'email': email, 'message': message, 'date': timestamp})  
        save_json(messages, 'data/messages.json')  
  
        flash('Your message has been sent successfully!', 'success')  
        return redirect(url_for('contact'))  
    return render_template('contact.html')  
  
# News Detail Page  
@app.route('/news/<int:news_id>')  
def news_detail(news_id):  
    articles = load_json('data/news.json')  
    if 0 <= news_id < len(articles):  
        article = articles[news_id]  
        return render_template('news_detail.html', article=article, articles=articles)  
    else:  
        flash('News article not found.', 'danger')  
        return redirect(url_for('index'))  
  
# Video Detail Page  
@app.route('/video/<int:video_id>')  
def video_detail(video_id):  
    videos = load_json('data/videos.json')  
    if 0 <= video_id < len(videos):  
        video = videos[video_id]  
        return render_template('video_detail.html', video=video)  
    else:  
        flash('Video not found.', 'danger')  
        return redirect(url_for('index'))  
  
# All Videos Page  
@app.route('/videos')  
def videos():  
    videos = load_json('data/videos.json')  
    return render_template('videos.html', videos=videos)  
  
# Serve Uploaded Videos  
@app.route('/uploads/videos/<filename>')  
def uploaded_file(filename):  
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  
  
# Admin Login  
@app.route('/login', methods=['GET', 'POST'])  
def login():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
  
        # Simple authentication (Replace with secure method)  
        if username == 'admin' and password == 'admin123':  
            session['logged_in'] = True  
            flash('You are now logged in.', 'success')  
            return redirect(url_for('admin_dashboard'))  
        else:  
            flash('Invalid credentials. Please try again.', 'danger')  
  
    return render_template('login.html')  
  
# Admin Logout  
@app.route('/logout')  
@login_required  
def logout():  
    session.pop('logged_in', None)  
    flash('You have been logged out.', 'info')  
    return redirect(url_for('login'))  
  
# Admin Dashboard  
@app.route('/admin/dashboard')  
@login_required  
def admin_dashboard():  
    messages = load_json('data/messages.json')  
    articles = load_json('data/news.json')  
    breaking_news = load_json('data/breaking_news.json')  
    videos = load_json('data/videos.json')  
    return render_template('admin_dashboard.html', messages=messages, articles=articles,  
                           breaking_news=breaking_news, videos=videos)  
  
# Admin Actions  
@app.route('/admin/action', methods=['POST'])  
@login_required  
def admin_action():  
    action = request.form.get('action')  
  
    if action == 'publish_news':  
        title = request.form['news-title']  
        description = request.form['news-description']  
        image = request.form['news-image']  
        category = request.form['news-category']  
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
  
        articles = load_json('data/news.json')  
        articles.insert(0, {  
            'title': title,  
            'description': description,  
            'image': image,  
            'category': category,  
            'date': timestamp  
        })  
        save_json(articles, 'data/news.json')  
  
        flash('News article published successfully!', 'success')  
  
    elif action == 'update_breaking_news':  
        news_text = request.form['breaking-news-text']  
        breaking_news = load_json('data/breaking_news.json')  
        breaking_news.insert(0, news_text)  
        save_json(breaking_news, 'data/breaking_news.json')  
  
        flash('Breaking news updated successfully!', 'success')  
  
    elif action == 'upload_video':  
        if 'video-file' not in request.files:  
            flash('No file part in the request.', 'danger')  
        else:  
            file = request.files['video-file']  
            video_title = request.form['video-title']  
            if file.filename == '':  
                flash('No selected file.', 'danger')  
            elif file and allowed_file(file.filename):  
                filename = secure_filename(file.filename)  
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                videos = load_json('data/videos.json')  
                videos.insert(0, {  
                    'filename': filename,  
                    'title': video_title,  
                    'date': timestamp  
                })  
                save_json(videos, 'data/videos.json')  
                flash('Video uploaded successfully!', 'success')  
            else:  
                flash('Invalid file type.', 'danger')  
  
    return redirect(url_for('admin_dashboard'))  
  
# Delete News Article  
@app.route('/admin/delete_news/<int:index>')  
@login_required  
def delete_news(index):  
    articles = load_json('data/news.json')  
    if 0 <= index < len(articles):  
        articles.pop(index)  
        save_json(articles, 'data/news.json')  
        flash('News article deleted successfully!', 'success')  
  
    return redirect(url_for('admin_dashboard'))  
  
# Delete Message  
@app.route('/admin/delete_message/<int:index>')  
@login_required  
def delete_message(index):  
    messages = load_json('data/messages.json')  
    if 0 <= index < len(messages):  
        messages.pop(index)  
        save_json(messages, 'data/messages.json')  
        flash('Message deleted successfully!', 'success')  
  
    return redirect(url_for('admin_dashboard'))  
  
# Delete Breaking News  
@app.route('/admin/delete_breaking_news/<int:index>')  
@login_required  
def delete_breaking_news(index):  
    breaking_news = load_json('data/breaking_news.json')  
    if 0 <= index < len(breaking_news):  
        breaking_news.pop(index)  
        save_json(breaking_news, 'data/breaking_news.json')  
        flash('Breaking news item deleted successfully!', 'success')  
  
    return redirect(url_for('admin_dashboard'))  
  
# Delete Video  
@app.route('/admin/delete_video/<int:index>')  
@login_required  
def delete_video(index):  
    videos = load_json('data/videos.json')  
    if 0 <= index < len(videos):  
        video = videos.pop(index)  
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], video['filename'])  
        if os.path.exists(filepath):  
            os.remove(filepath)  
        save_json(videos, 'data/videos.json')  
        flash('Video deleted successfully!', 'success')  
    else:  
        flash('Video not found.', 'danger')  
    return redirect(url_for('admin_dashboard'))  
  
if __name__ == '__main__':  
    app.run(debug=True)  
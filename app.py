from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from database import Database
from admin_auth import Admin, admin_required
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sptws-secret-key-2024-change-in-production'

# Configuration
app.config['UPLOAD_FOLDER_REPORTS'] = 'static/uploads/reports'
app.config['UPLOAD_FOLDER_GALLERY'] = 'static/uploads/gallery'
app.config['UPLOAD_FOLDER_GOS'] = 'static/uploads/gos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Create all necessary directories
os.makedirs('instance', exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_REPORTS'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_GALLERY'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_GOS'], exist_ok=True)

# Initialize database
db = Database()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please login to access the admin panel'

@login_manager.user_loader
def load_user(user_id):
    return Admin.get(user_id)

def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# ---------- Frontend Routes (Public) ----------
@app.route('/')
def home():
    events = db.get_recent_events(3)
    return render_template('index.html', events=events)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/committee')
def committee():
    members = db.get_committee_members()
    return render_template('committee.html', members=members)

@app.route('/events')
def events():
    all_events = db.get_all_events()
    return render_template('events.html', events=all_events)

@app.route('/members')
def members():
    society_members = db.get_society_members()
    return render_template('members.html', members=society_members)

@app.route('/annual-reports')
def annual_reports():
    reports = db.get_annual_reports()
    return render_template('annual_reports.html', reports=reports)

@app.route('/gallery')
def gallery():
    images = db.get_gallery_images()
    return render_template('gallery.html', images=images)

@app.route('/software-links')
def software_links():
    links = db.get_software_links()
    return render_template('software_links.html', links=links)

@app.route('/important-gos')
def important_gos():
    gos = db.get_important_gos()
    return render_template('important_gos.html', gos=gos)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/download/<file_type>/<filename>')
def download_file(file_type, filename):
    if file_type == 'report':
        return send_from_directory(app.config['UPLOAD_FOLDER_REPORTS'], filename, as_attachment=True)
    elif file_type == 'go':
        return send_from_directory(app.config['UPLOAD_FOLDER_GOS'], filename, as_attachment=True)
    return "File not found", 404

# ---------- Admin Routes (Protected) ----------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Admin credentials: Bplreddy / sptws
        if username == 'Bplreddy' and password == 'sptws':
            admin = Admin('1', username)
            login_user(admin)
            flash('Login successful! Welcome to Admin Panel.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials! Please try again.', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    events = db.get_all_events()
    committee_members = db.get_committee_members()
    society_members = db.get_society_members()
    reports = db.get_annual_reports()
    gallery_images = db.get_gallery_images()
    software_links = db.get_software_links()
    gos = db.get_important_gos()
    return render_template('admin_dashboard.html',
                         events=events,
                         committee_members=committee_members,
                         society_members=society_members,
                         reports=reports,
                         gallery_images=gallery_images,
                         software_links=software_links,
                         gos=gos)

# ---------- CRUD Operations (Admin only) ----------
@app.route('/admin/add-event', methods=['POST'])
@login_required
@admin_required
def add_event():
    title = request.form.get('title')
    description = request.form.get('description')
    event_date = request.form.get('event_date')
    location = request.form.get('location')
    if title and description:
        db.add_event(title, description, event_date, location)
        flash('Event added successfully!', 'success')
    else:
        flash('Title and description are required!', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-event/<int:event_id>', methods=['POST'])
@login_required
@admin_required
def edit_event(event_id):
    title = request.form.get('title')
    description = request.form.get('description')
    event_date = request.form.get('event_date')
    location = request.form.get('location')
    db.update_event(event_id, title, description, event_date, location)
    flash('Event updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-event/<int:event_id>')
@login_required
@admin_required
def delete_event(event_id):
    db.delete_event(event_id)
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Committee members
@app.route('/admin/add-committee-member', methods=['POST'])
@login_required
@admin_required
def add_committee_member():
    name = request.form.get('name')
    position = request.form.get('position')
    bio = request.form.get('bio')
    phone = request.form.get('phone')
    email = request.form.get('email')
    if name:
        db.add_committee_member(name, position, bio, phone, email)
        flash('Committee member added successfully!', 'success')
    else:
        flash('Name is required!', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-committee-member/<int:member_id>', methods=['POST'])
@login_required
@admin_required
def edit_committee_member(member_id):
    name = request.form.get('name')
    position = request.form.get('position')
    bio = request.form.get('bio')
    phone = request.form.get('phone')
    email = request.form.get('email')
    db.update_committee_member(member_id, name, position, bio, phone, email)
    flash('Committee member updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-committee-member/<int:member_id>')
@login_required
@admin_required
def delete_committee_member(member_id):
    db.delete_committee_member(member_id)
    flash('Committee member deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Society members
@app.route('/admin/add-society-member', methods=['POST'])
@login_required
@admin_required
def add_society_member():
    name = request.form.get('name')
    designation = request.form.get('designation')
    school = request.form.get('school')
    phone = request.form.get('phone')
    email = request.form.get('email')
    if name:
        db.add_society_member(name, designation, school, phone, email)
        flash('Society member added successfully!', 'success')
    else:
        flash('Name is required!', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-society-member/<int:member_id>', methods=['POST'])
@login_required
@admin_required
def edit_society_member(member_id):
    name = request.form.get('name')
    designation = request.form.get('designation')
    school = request.form.get('school')
    phone = request.form.get('phone')
    email = request.form.get('email')
    db.update_society_member(member_id, name, designation, school, phone, email)
    flash('Society member updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-society-member/<int:member_id>')
@login_required
@admin_required
def delete_society_member(member_id):
    db.delete_society_member(member_id)
    flash('Society member deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Gallery
@app.route('/admin/upload-gallery', methods=['POST'])
@login_required
@admin_required
def upload_gallery():
    if 'image' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('admin_dashboard'))
    file = request.files['image']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    if file and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER_GALLERY'], filename)
        file.save(filepath)
        caption = request.form.get('caption', '')
        db.add_gallery_image(filename, caption)
        flash('Image uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload image files only.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-gallery/<int:image_id>')
@login_required
@admin_required
def delete_gallery(image_id):
    image = db.get_gallery_image_by_id(image_id)
    if image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_GALLERY'], image[1])
        if os.path.exists(filepath):
            os.remove(filepath)
        db.delete_gallery_image(image_id)
        flash('Image deleted successfully!', 'success')
    else:
        flash('Image not found!', 'error')
    return redirect(url_for('admin_dashboard'))

# Annual reports
@app.route('/admin/upload-report', methods=['POST'])
@login_required
@admin_required
def upload_report():
    if 'report' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('admin_dashboard'))
    file = request.files['report']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    if file and allowed_file(file.filename, {'pdf'}):
        filename = secure_filename(f"{datetime.now().strftime('%Y')}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER_REPORTS'], filename)
        file.save(filepath)
        title = request.form.get('title', f"Annual Report {datetime.now().year}")
        year = request.form.get('year', datetime.now().year)
        db.add_annual_report(title, filename, year)
        flash('Annual report uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload PDF files only.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-report/<int:report_id>')
@login_required
@admin_required
def delete_report(report_id):
    report = db.get_annual_report_by_id(report_id)
    if report:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_REPORTS'], report[2])
        if os.path.exists(filepath):
            os.remove(filepath)
        db.delete_annual_report(report_id)
        flash('Report deleted successfully!', 'success')
    else:
        flash('Report not found!', 'error')
    return redirect(url_for('admin_dashboard'))

# Software links
@app.route('/admin/add-software-link', methods=['POST'])
@login_required
@admin_required
def add_software_link():
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    if title and url:
        db.add_software_link(title, description, url)
        flash('Software link added successfully!', 'success')
    else:
        flash('Title and URL are required!', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit-software-link/<int:link_id>', methods=['POST'])
@login_required
@admin_required
def edit_software_link(link_id):
    title = request.form.get('title')
    description = request.form.get('description')
    url = request.form.get('url')
    db.update_software_link(link_id, title, description, url)
    flash('Software link updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-software-link/<int:link_id>')
@login_required
@admin_required
def delete_software_link(link_id):
    db.delete_software_link(link_id)
    flash('Software link deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# GOs
@app.route('/admin/upload-go', methods=['POST'])
@login_required
@admin_required
def upload_go():
    if 'go_file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('admin_dashboard'))
    file = request.files['go_file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('admin_dashboard'))
    if file and allowed_file(file.filename, {'pdf'}):
        filename = secure_filename(f"go_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER_GOS'], filename)
        file.save(filepath)
        title = request.form.get('title')
        go_number = request.form.get('go_number')
        description = request.form.get('description')
        if title:
            db.add_important_go(title, go_number, filename, description)
            flash('GO uploaded successfully!', 'success')
        else:
            flash('Title is required!', 'error')
    else:
        flash('Invalid file type. Please upload PDF files only.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-go/<int:go_id>')
@login_required
@admin_required
def delete_go(go_id):
    go = db.get_important_go_by_id(go_id)
    if go:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_GOS'], go[3])
        if os.path.exists(filepath):
            os.remove(filepath)
        db.delete_important_go(go_id)
        flash('GO deleted successfully!', 'success')
    else:
        flash('GO not found!', 'error')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
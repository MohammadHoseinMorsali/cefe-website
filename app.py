from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from forms import AdminLoginForm, MenuItemForm, CafeInfoForm, BlogPostForm # Added BlogPostForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_very_secret_key_here_CHANGE_ME' # IMPORTANT: Change this in production!

INFO_KEYS = ['about_us_text', 'contact_address', 'contact_phone', 'contact_email']

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login' # Name of the login route

# --- Models ---
class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<MenuItem {self.name}>'

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

class CafeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<CafeInfo {self.key}>'

# --- Routes ---
@app.route('/')
def home():
    menu_items_from_db = MenuItem.query.all()

    cafe_info_data = {}
    for key_name in INFO_KEYS: # INFO_KEYS is already defined globally
        info_entry = CafeInfo.query.filter_by(key=key_name).first()
        cafe_info_data[key_name] = info_entry.value if info_entry and info_entry.value else None

    return render_template('index.html', menu_items=menu_items_from_db, cafe_info=cafe_info_data)

# --- Flask-Login User Loader ---
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(AdminUser, int(user_id))

# --- Admin Routes ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('admin/admin_login.html', form=form, title='Admin Login')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # This will be updated later to extend admin_base.html
    return render_template('admin/dashboard.html', title="Admin Dashboard")

# --- Cafe Info Management Route ---
@app.route('/admin/cafe-info', methods=['GET', 'POST'])
@login_required
def admin_cafe_info():
    form = CafeInfoForm()
    if form.validate_on_submit():
        for key_name in INFO_KEYS:
            info_entry = CafeInfo.query.filter_by(key=key_name).first()
            new_value = form[key_name].data if key_name in form else '' # Check if key is in form

            if info_entry:
                info_entry.value = new_value
            else:
                # This case should ideally be handled by pre-population,
                # but as a fallback:
                new_entry = CafeInfo(key=key_name, value=new_value)
                db.session.add(new_entry)
        db.session.commit()
        flash('Cafe information updated successfully!', 'success')
        return redirect(url_for('admin_cafe_info'))

    # GET request or form validation failed
    current_data = {}
    for key_name in INFO_KEYS:
        info_entry = CafeInfo.query.filter_by(key=key_name).first()
        if info_entry:
            current_data[key_name] = info_entry.value
        else:
            current_data[key_name] = '' # Default if somehow not pre-populated

    # Populate form with data from DB for GET request
    # For WTForms, when using data= argument, it expects field names to match.
    # If form field names match INFO_KEYS directly, this works.
    if request.method == 'GET':
        form = CafeInfoForm(data=current_data)

    return render_template('admin/cafe_info_form.html', form=form, title="Manage Cafe Information")

# --- Blog Post CRUD Routes ---
@app.route('/admin/blog')
@login_required
def admin_blog_list():
    posts = BlogPost.query.order_by(BlogPost.publication_date.desc()).all()
    return render_template('admin/blog_list.html', blog_posts=posts, title="Manage Blog Posts")

@app.route('/admin/blog/add', methods=['GET', 'POST'])
@login_required
def admin_blog_add():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            content=form.content.data
            # publication_date is set by default in the model
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f"Blog post '{new_post.title}' created successfully.", 'success')
        return redirect(url_for('admin_blog_list'))
    return render_template('admin/blog_form.html', form=form, form_title="Add New Blog Post", title="Add Blog Post")

@app.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def admin_blog_edit(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)
    form = BlogPostForm(obj=post) # Populate form with existing post data
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # publication_date remains the same unless explicitly changed
        db.session.commit()
        flash(f"Blog post '{post.title}' updated successfully.", 'success')
        return redirect(url_for('admin_blog_list'))
    return render_template('admin/blog_form.html', form=form, form_title=f"Edit Blog Post: {post.title}", title="Edit Blog Post")

@app.route('/admin/blog/delete/<int:post_id>', methods=['POST'])
@login_required
def admin_blog_delete(post_id):
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)
    post_title = post.title # Get title for flash message
    db.session.delete(post)
    db.session.commit()
    flash(f"Blog post '{post_title}' deleted successfully.", 'success')
    return redirect(url_for('admin_blog_list'))

# --- Menu Item CRUD Routes ---
@app.route('/admin/menu')
@login_required
def admin_menu_list():
    items = MenuItem.query.all()
    return render_template('admin/menu_list.html', menu_items=items, title="Manage Menu Items")

@app.route('/admin/menu/add', methods=['GET', 'POST'])
@login_required
def admin_menu_add():
    form = MenuItemForm()
    if form.validate_on_submit():
        new_item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash(f"Menu item '{new_item.name}' added successfully.", 'success')
        return redirect(url_for('admin_menu_list'))
    return render_template('admin/menu_form.html', form=form, form_title="Add New Menu Item", title="Add Menu Item")

@app.route('/admin/menu/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_menu_edit(item_id):
    item = db.session.get(MenuItem, item_id) # Use db.session.get for SQLAlchemy 2.0+
    if not item:
        abort(404)
    form = MenuItemForm(obj=item) # Populate form with existing item data
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        db.session.commit()
        flash(f"Menu item '{item.name}' updated successfully.", 'success')
        return redirect(url_for('admin_menu_list'))
    return render_template('admin/menu_form.html', form=form, form_title=f"Edit Menu Item: {item.name}", title="Edit Menu Item")

@app.route('/admin/menu/delete/<int:item_id>', methods=['POST']) # Should be POST for safety
@login_required
def admin_menu_delete(item_id):
    item = db.session.get(MenuItem, item_id)
    if not item:
        abort(404)
    item_name = item.name # Get name before deleting for the flash message
    db.session.delete(item)
    db.session.commit()
    flash(f"Menu item '{item_name}' deleted successfully.", 'success')
    return redirect(url_for('admin_menu_list'))

# --- Helper to create DB tables ---
def create_tables():
    with app.app_context():
        db.create_all()
        # Pre-populate CafeInfo keys if they don't exist
        for key_name in INFO_KEYS:
            if not CafeInfo.query.filter_by(key=key_name).first():
                info_entry = CafeInfo(key=key_name, value='') # Default to empty string
                db.session.add(info_entry)
        db.session.commit()
    print("Database tables created and CafeInfo keys initialized (if they didn't exist).")

# --- CLI command to create tables ---
@app.cli.command("create-tables")
def create_tables_command():
    """Creates all database tables."""
    create_tables()

# --- Initial Admin User Creation (CLI Command) ---
@app.cli.command("create-admin")
def create_admin_command():
    """Creates the initial admin user."""
    with app.app_context():
        if AdminUser.query.filter_by(username='admin').first():
            print("Admin user 'admin' already exists.")
            return

        admin_password = "changeme"
        admin_user = AdminUser(username='admin')
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user 'admin' created with password '{admin_password}'. Please change it after first login.")

if __name__ == '__main__':
    # Instructions for setup:
    # 1. Make sure requirements are installed: pip install -r requirements.txt
    # 2. Set Flask app environment variables (optional if using `python app.py`):
    #    export FLASK_APP=app.py
    #    export FLASK_ENV=development (for debug mode and to enable CLI)
    # 3. Create database tables:
    #    flask create-tables
    # 4. Create the initial admin user:
    #    flask create-admin
    # 5. Run the application:
    #    flask run  OR  python app.py
    app.run(debug=True)

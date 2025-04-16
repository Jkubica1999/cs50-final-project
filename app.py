from flask import Flask, render_template, request, redirect, g
from flask_babel import Babel, _
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os


# Flask application setup
app = Flask(__name__)


# SQLAlchemy configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Email Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # or your SMTP provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # replace with your email
app.config['MAIL_PASSWORD'] = 'your_app_password'     # use an app password (not your main email password)

mail = Mail(app)

# Product models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship('Product', backref='category', lazy=True)
    translations = db.relationship('CategoryTranslation', backref='category', lazy=True)

class CategoryTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    lang = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    translations = db.relationship('ProductTranslation', backref='product', lazy=True)

class ProductTranslation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    lang = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    specs = db.Column(db.Text)

@app.context_processor
def inject_categories():
    lang = request.path.strip('/').split('/')[0]
    categories = Category.query.all()

    category_links = []
    for cat in categories:
        trans = next((t for t in cat.translations if t.lang == lang), None)
        if trans:
            category_links.append({
                'id': cat.id,
                'name': trans.name,
                'url': f"/products/{lang}/{cat.id}"
            })

    return dict(category_links=category_links, lang=lang)

# Babel configuration
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'


# Function to determine the best match for the user's locale
@babel.localeselector
def get_locale():
    # Grab the first segment of the URL path
    lang = request.path.strip('/').split('/')[0]

    # Make sure it's a supported language
    if lang in ['en', 'pl']:
        g.locale = lang
        return lang

    # Fallback to English
    g.locale = 'en'
    return 'en'


@app.route('/')
def redirect_to_best_match():
    best_lang = request.accept_languages.best_match(['en', 'pl'])
    return redirect(f'/{best_lang or "en"}/')

# Route for the home page
@app.route('/<lang>/')
def index(lang):
    return render_template('index.html', lang=lang)



# Route for the product page
@app.route('/<lang>/products/<int:category_id>')
def products_by_category(lang, category_id):
    # Get the category
    category = Category.query.get_or_404(category_id)
    category_name = next((t.name for t in category.translations if t.lang == lang), "Unknown")

    # Get products in that category
    products = Product.query.filter_by(category_id=category_id).all()

    # Get translations
    translated_products = []
    for product in products:
        translation = next((t for t in product.translations if t.lang == lang), None)
        if translation:
            translated_products.append({
                'name': translation.name,
                'description': translation.description,
                'specs': translation.specs,
                'image': product.image
            })

    return render_template('product.html',
                           products=translated_products,
                           category_name=category_name,
                           lang=lang)


# Route for the contact page
@app.route('/<lang>/contact' , methods=['GET', 'POST'])
def contact(lang):
    # Generate the contact form
    if request.method == 'GET':
        product_name = request.args.get('product_name', '')
        return render_template('contact.html', lang=lang, product_name=product_name)
    # Handle form submission
    elif request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        product_name = request.form.get('product_name')

        # Compose the email
        msg = Message(subject=f"New Inquiry from {name}",
                    sender=email,
                    recipients=['your_email@gmail.com']) # replace with your email
        
        # Set the email body

        msg.body = f"""
        You've received a new contact form submission:

        Name: {name}
        Email: {email}
        Product: {product_name}
        Message: {message}
        """

        mail.send(msg)

        return render_template('contact_success.html', lang=lang, product_name=product_name)


# Route for the about page
@app.route('/<lang>/about')
def about(lang):
    return render_template('about.html', lang=lang)


# Route for the FAQ page
@app.route('/<lang>/faq')
def faq(lang):
    return render_template('faq.html', lang=lang)

# Route for contact success page
@app.route('/<lang>/contact_success')
def contact_success(lang):
    return render_template('contact_success.html', lang=lang)


# Route for the privacy policy page
@app.route('/<lang>/privacy-policy')
def privacy_policy(lang):
    return render_template('privacy_policy.html', lang=lang)

if __name__ == '__main__':
    app.run(debug=True)

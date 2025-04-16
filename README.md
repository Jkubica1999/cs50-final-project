# MachInnovate

#### Video Demo: https://youtu.be/e9zV3IN_1pc
#### Description:

**MachInnovate** is a demo web application for a cable separator product, built as my final project for CS50. The purpose of the website is to simulate a professional product presentation site that supports multiple languages and dynamic content loading from a database.

---

## Overview

This project is a dynamic, multilingual website built using Python’s Flask framework. The site is easily extendable — new products can be added via the database, and additional languages can be supported with minimal effort using Flask-Babel.

The application supports both English and Polish, and features include:

- A product listing page dynamically loaded from a SQLite database
- A quote request form pre-filled with the product name
- Contact form with email functionality (Flask-Mail)
- Translation-ready with Flask-Babel
- FAQ section (currently not translated)
- Responsive design using TailwindCSS
- Language switch functionality using JavaScript

---

# Project Files and Structure

## Python files

### `app.py`

This is the main Flask application file. It initializes the app, sets up configuration for:

- **Flask-Mail** – currently inactive (placeholders are in place for email credentials)
- **Flask-Babel** – for language translation support
- **SQLAlchemy** – for database ORM
- Route logic for serving pages and handling form submissions

#### Defined Classes

- **`Category`**  
  Represents a general product category. Has relationships to:
  - `products`: links to associated `Product` entries  
  - `translations`: links to `CategoryTranslation` entries for multilingual names

- **`CategoryTranslation`**  
  Stores translated names for categories. Fields:
  - `category_id`: ForeignKey to `Category`
  - `lang`: language code (e.g. `'en'`, `'pl'`)
  - `name`: translated category name

- **`Product`**  
  Defines individual products. Fields:
  - `category_id`: ForeignKey to `Category`
  - `image`: file path to an image in `/static/`
  - Relationship to `ProductTranslation` for multilingual content

- **`ProductTranslation`**  
  Stores language-specific details for each product. Fields:
  - `product_id`: ForeignKey to `Product`
  - `lang`: language code
  - `name`: translated product name
  - `description`: translated product description
  - `specs`: optional technical specifications

#### Language and Context Logic

- A function to extract the language prefix from the URL.
- A `@app.route("/")` to detect the user's browser language via `request.accept_languages.best_match()` and redirect them accordingly, with a fallback to English.
- A `@app.context_processor` that injects shared variables like `lang` and dynamically built category links into every rendered template, ensuring consistent language and navigation support site-wide.

### `seed_db.py`

This script initializes the SQLite database with multilingual product and category data.

It is designed to be run once at the start of the project to populate the database without needing to commit the actual database file to version control.

#### Functionality:
- Initializes the database context with `app.app_context()`.
- Creates a **category** object (`separators`) with:
  - English and Polish translations using the `CategoryTranslation` model.

- Creates a **product** (`Cable Separator`) with:
  - Image path set to `/static/cable-separator.jpg`
  - Translations in both English and Polish using the `ProductTranslation` model:
    - Translated name, description, and optional technical specifications (`specs`).

- Adds all created entries to the database and commits the transaction.

#### Example Data:
- **Category**: "Separators" (EN), "Separatory" (PL)
- **Product**: 
  - **EN**:
    - Name: "Cable Separator"
    - Description: "Separates copper from insulation in scrap cables."
    - Specs: Speed 100kg/h, Voltage: 230V, Blades: Steel
  - **PL**:
    - Name: "Separator Kabli"
    - Description: "Oddziela miedź od izolacji w zużytych kablach."
    - Specs: Prędkość: 100kg/h, Napięcie: 230V, Ostrza: Stalowe

This approach ensures test data is available in both supported languages and demonstrates how translations are handled via relationships between models.

## HTML Pages Summary

### `base.html`
The core layout used by all templates. Contains:
- Navigation bar with links to Home, Products, Contact, About, and FAQ
- Language switch buttons (EN / PL)
- Footer with credits
- JavaScript for switching language by rewriting the URL path
- The navbar that dynamically queries all categories, ensuring correct translation 

### `index.html`
The homepage featuring a project title, short product introduction.

### `product.html`
Displays all products for a specific category and language. Each product includes:
- Name and description
- Optional specs
- Image pulled from the `/static/` directory
- “Request a Quote” link that appends the product name as a query parameter to the contact form

### `contact.html`
Form with fields for name, email, message, and product name (autofilled from the query string if present). Upon submission:
- Sends an email using Flask-Mail (not active in this demo version)
- Redirects to a success page

### `contact_success.html`
A simple thank you message confirming the user’s contact form has been submitted.

### `about.html`
Currently empty, meant for a brief explanation of the company and its purpose.

### `faq.html`
Displays 10 placeholder questions and answers (currently only in English). Content is wrapped in translation functions for future internationalization.

## `babel.cfg`

This configuration file is used by **Flask-Babel** to extract translatable strings from the source code and templates for internationalization.

It specifies the file types and locations to scan for text marked for translation:

- `[python: **.py]`  
  Instructs Babel to look for translatable strings (e.g., wrapped in `_()`) inside all Python files.

- `[jinja2: templates/**.html]`  
  Tells Babel to also scan all HTML templates in the `templates/` directory, using the Jinja2 syntax.

This config is essential for generating `.pot` and `.po` files, which are used to manage translations for supported languages.

## `messages.pot`

The `messages.pot` file is the master translation template generated by **Flask-Babel**. It includes all the translatable strings extracted from both Python files and HTML templates using the `_()` syntax.

This file is created by running a Babel extraction command based on the configuration provided in `babel.cfg`. It contains the original English strings, along with metadata indicating the source file and line number for each string.

Key points:

- It serves as the base template from which all language-specific `.po` files are created.
- It ensures that translations stay consistent across all supported languages.
- It is automatically updated when new translatable strings are added to the codebase.

Translators use this file to generate `.po` files (e.g., `messages.po` for Polish), where they provide the corresponding translations.

To generate or update `messages.pot`, run:

`pybabel extract -F babel.cfg -o messages.pot .`

Maintaining this file helps keep translations complete, accurate, and in sync with the application's content.

## `messages.po`

The `messages.po` file contains the Polish translations for all extracted English strings used throughout the application. It is located at:  
`translations/pl/LC_MESSAGES/messages.po`

Each entry defines an English message (`msgid`) and its corresponding Polish translation (`msgstr`).

These translations are used  by **Flask-Babel** to localize text in HTML templates and replace it with its translated equivalent.

After editing, the file must be compiled into a `.mo` file.

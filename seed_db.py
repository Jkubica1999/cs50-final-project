from app import app, db, Category, CategoryTranslation, Product, ProductTranslation

with app.app_context():
    # --- Category: Cable Separators ---
    separators = Category()
    separators.translations = [
        CategoryTranslation(lang='en', name='Separators'),
        CategoryTranslation(lang='pl', name='Separatory')
    ]

    # --- Product: Cable Separator ---
    p1 = Product(image="images/cable-separator.jpg", category=separators)
    p1.translations = [
        ProductTranslation(
            lang='en',
            name='Cable Separator',
            description='Separates copper from insulation in scrap cables.',
            specs='Speed: 100kg/h\nVoltage: 230V\nBlades: Steel'
        ),
        ProductTranslation(
            lang='pl',
            name='Separator Kabli',
            description='Oddziela miedź od izolacji w zużytych kablach.',
            specs='Prędkość: 100kg/h\nNapięcie: 230V\nOstrza: Stalowe'
        )
    ]

    db.session.add_all([separators, p1])
    db.session.commit()
    print("✅ Seeded multilingual categories and products!")

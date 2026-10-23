from app.database import SessionLocal, init_db
from app.models import Category, Product

CATEGORIES = [
    ("3D printers", "3d-printers"), ("CNC machines", "cnc-machines"),
    ("Laser equipment", "laser-equipment"), ("Industrial robots", "industrial-robots"),
]
PRODUCTS = [
    ("Prusa MK4S 3D Printer", "Reliable FDM printer for prototyping and production.", 1099, 0, "https://images.unsplash.com/photo-1615375834706-58e1063dd9a6?auto=format&fit=crop&w=1000&q=85"),
    ("Bambu Lab X1 Carbon", "High-speed enclosed multicolor 3D printer.", 1449, 0, "https://images.unsplash.com/photo-1631556097152-c39479bbff3f?auto=format&fit=crop&w=1000&q=85"),
    ("Creality K1 Max Printer", "Large-format fast CoreXY 3D printer.", 899, 0, "https://images.unsplash.com/photo-1633412802994-5c058f151b66?auto=format&fit=crop&w=1000&q=85"),
    ("Formlabs Form 4 Printer", "Professional resin printer with precise detail.", 4500, 0, "https://images.unsplash.com/photo-1617957743097-0d20aa2ea762?auto=format&fit=crop&w=1000&q=85"),
    ("Shapeoko 5 Pro CNC", "Rigid CNC router for woodworking and fabrication.", 3200, 1, "https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1000&q=85"),
    ("Nomad 3 Desktop CNC", "Compact precision milling machine for the workshop.", 2800, 1, "https://images.unsplash.com/photo-1567789884554-0b844b597180?auto=format&fit=crop&w=1000&q=85"),
    ("Tormach 440 CNC Mill", "Benchtop CNC mill for metal part production.", 6500, 1, "https://images.unsplash.com/photo-1581092335878-2d9ff86ca2bf?auto=format&fit=crop&w=1000&q=85"),
    ("xTool P2 Laser Cutter", "55W CO2 laser cutter with smart camera.", 4600, 2, "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&w=1000&q=85"),
    ("Glowforge Pro Laser", "Connected laser cutter for creative production.", 6995, 2, "https://images.unsplash.com/photo-1581092795360-fd1ca04f0952?auto=format&fit=crop&w=1000&q=85"),
    ("Epilog Fusion Edge", "Industrial laser engraving and cutting system.", 18000, 2, "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1000&q=85"),
    ("Universal Robots UR5e", "Flexible collaborative robot arm for automation.", 35000, 3, "https://images.unsplash.com/photo-1565043589221-1a6fd9ae45c7?auto=format&fit=crop&w=1000&q=85"),
    ("UFACTORY xArm 6", "Compact six-axis robot for research and assembly.", 12000, 3, "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?auto=format&fit=crop&w=1000&q=85"),
    ("Dobot CR5 Robot", "Collaborative robot for machine tending and packing.", 21000, 3, "https://images.unsplash.com/photo-1581092162384-8987c1d64718?auto=format&fit=crop&w=1000&q=85"),
]


def seed():
    init_db()
    with SessionLocal() as db:
        existing = {c.slug: c for c in db.query(Category).all()}
        categories = []
        for name, slug in CATEGORIES:
            category = existing.get(slug)
            if category is None:
                category = Category(name=name, slug=slug)
                db.add(category)
            categories.append(category)
        db.flush()
        if db.query(Product).count() == 0:
            for name, description, price, category_idx, image_url in PRODUCTS:
                db.add(Product(name=name, description=description, price=price, category_id=categories[category_idx].id, image_url=image_url))
        db.commit()


if __name__ == "__main__":
    seed()
    print("Seeded 4 categories and 13 sample products (existing products were preserved).")

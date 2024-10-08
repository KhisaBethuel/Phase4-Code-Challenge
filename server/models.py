from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Define naming convention for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    super_name = Column(String, nullable=False)

    # Relationship to HeroPower
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    # Association proxy to access powers directly
    powers = association_proxy("hero_powers", "power")

    # Serialization rules
    serialize_rules = ("-hero_powers.hero", "-hero_powers")

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Relationship to HeroPower
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    # Association proxy to access heroes directly
    heroes = association_proxy("hero_powers", "hero")

    # Serialization rules
    serialize_rules = ("-hero_powers.power", "-hero_powers")
    
    # Validation for description
    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return description

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = Column(Integer, primary_key=True)
    strength = Column(String, nullable=False)
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = Column(Integer, ForeignKey('powers.id'), nullable=False)

    # Relationships
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    # Serialization rules
    serialize_rules = ("-hero.hero_powers", "-power.hero_powers")
    
    # Validation for strength
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Invalid strength value.")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'

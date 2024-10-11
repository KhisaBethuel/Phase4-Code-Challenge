from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})


db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    super_name = Column(String, nullable=False)

    
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    
    powers = association_proxy("hero_powers", "power")

    
    serialize_rules = ("-hero_powers.hero", "-hero_powers")

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    
    heroes = association_proxy("hero_powers", "hero")


    serialize_rules = ("-hero_powers.power", "-hero_powers")
    

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


    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    serialize_rules = ("-hero.hero_powers", "-power.hero_powers")
    
    
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Invalid strength value.")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'

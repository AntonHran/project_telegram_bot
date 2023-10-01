from sqlalchemy.orm import Session
from models import Country, Category, Genre
from connection import db
from src.services.constants import news_countries, news_categories, books_genres


def seed_countries(countries_: tuple, db_: Session):
    for country in countries_:
        country_ = Country(country=country)
        db_.add(country_)
        db_.commit()
    db_.close()


def seed_categories(categories_: tuple, db_: Session):
    for category in categories_:
        category_ = Category(category=category)
        db_.add(category_)
        db_.commit()
    db_.close()


def seed_genres(genres_: tuple, db_: Session):
    for genre in genres_:
        genre_ = Genre(genre=genre)
        db_.add(genre_)
        db_.commit()
    db_.close()


def main_seed():
    seed_countries(news_countries, db)
    seed_categories(news_categories, db)
    seed_genres(books_genres, db)


if __name__ == '__main__':
    main_seed()

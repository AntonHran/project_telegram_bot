import datetime

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, func, Time
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    created_at = Column(Date, default=func.now())
    article = Column(Boolean, default=False)
    books = Column(Boolean, default=False)
    quote = Column(Boolean, default=False)
    news = Column(Boolean, default=False)
    trends = Column(Boolean, default=False)
    weather = Column(Boolean, default=False)
    language = Column(String, default="eng")

    article_time = relationship("Article", backref="users")
    quote_time = relationship("Quote", backref="users")
    genres_ = relationship("Genre", secondary="books", backref="users")
    news_category = relationship("Category", secondary="news_categories", backref="users")
    news_country = relationship("Country", secondary="news_countries", backref="users")
    trends_ = relationship("Trend", backref="users")
    weather_ = relationship("Weather", backref="users")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time = Column(Time, default=datetime.time(hour=9, minute=0, second=0))


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    genre = Column(String, unique=True)


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time = Column(Time, default=datetime.time(hour=9, minute=0, second=0))


class NewsCountry(Base):
    __tablename__ = "news_countries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)


class NewsCategory(Base):
    __tablename__ = "news_categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    country = Column(String, unique=True)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    category = Column(String, unique=True)


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    city = Column(String(60), unique=False)
    country = Column(String(60), unique=False)


class Weather(Base):
    __tablename__ = "weather_"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    city = Column(String(60), unique=False)

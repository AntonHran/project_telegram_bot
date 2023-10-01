news_countries = ("ukr", "usa", "ger", "fr", "itl", "pld")
news_categories = (
    "business",
    "entert",
    "general",
    "health",
    "science",
    "sports",
    "tech",
)
books_genres = (
    "fiction",
    "mystery",
    "science fiction",
    "fantasy",
    "romance",
    "adventure",
    "biography",
    "non-fiction",
    "horror",
    "thriller",
    "comedy",
    "drama",
)
# Commands
(
    SELECTING_ACTION,
    LANG,
    DONE,
    BOOKS,
    CHANGE_LANGUAGE,
    NEWS,
    ARTICLE_TIME,
    QUOTE_TIME,
    COUNTRY,
    CATEGORY,
    CITY_WEATHER,
    TRENDS,
    GENRE,
) = range(13)

keys_ = {
    ARTICLE_TIME: "wiki",
    QUOTE_TIME: "motivation",
    NEWS: "news",
    CITY_WEATHER: "weather",
    TRENDS: "twitter_trends",
    BOOKS: "books",
    GENRE: "genres",
}

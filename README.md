This Telegram bot has the following functionality, which is already implemented:

- At the first launch, the user can choose the language (English or Ukrainian) for further use of the bot.
- The user can choose the categories that interest him, in particular:
   - Motivational phrases.
   - Weather forecast.
   - Trends.
   - News.
   - Random article.

- News category has sections like Business, Entertainment, General, Health, Science, Sports, Technology. The user can also select the desired country for news.
- User can provide additional information such as city, country and preferred time of sending messages for other categories.
- All user settings are stored in a JSON file.

However, there are some features that still need to be implemented:

- Database connections: It is necessary to create tables containing information about user settings, as well as record data about new connections to the database.
- Working with the database: It is necessary to implement the logic that will be responsible for working with the database. For example, this logic can periodically check users' settings and send them messages according to the selected time.
- Additional functions: expand the functionality of the bot by adding new features, such as interacting with users through commands, creating notifications or scheduled messages, etc.

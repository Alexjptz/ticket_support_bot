1) Download repository to your server
2) You need to add .env to project base dir.

.env conf:

BOT_TOKEN= # add your bot token
DATABASE_HOST=0.0.0.0
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=test_db
PANEL_HOST=127.0.0.1
PANEL_PORT=8000
SECRET_KEY=111

DEFAULT_CHANNEL_ID= -1001838215343 # get it with @userinfobot and replace
DEFAULT_CHANNEL_URL= 'https://t.me/CHANEL' # channel for subscription

ADMIN_PANEL_NAME= # add admin name
ADMIN_PANEL_PASSWORD= # add admin password

3) Edit config.py 'admin_ids' to use admin bot panel (use @userinfobot to get ID)
4) Install docker to your server
5) Use 'docker compose up --build -d' to start your bot

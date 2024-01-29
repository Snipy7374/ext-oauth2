# ext-oauth2
An easy to use, async, OAuth2 (login with discord) API wrapper for Discord written in Python.

Have you ever wanted to create a dashboard for your bot or wanted to use non-accesible endpoints to non-OAuth2-authenticated applications?

This library tries to help you wrapping all the authorization flow, requests and data conversion for you (just like d.py, disnake, nextcord and other libriries do).

## Key features
- Discord API wrapper agnostic
- Implements all the endpoints that requires user authorization
- Backend framework agnostic

## Installing
**Python 3.8 or higher is required.**

## Quick example using FastAPI

```py
from typing import Optional

import oauth2
from oauth2.scopes import OAuthScopes
from oauth2.utils import get_oauth2_url
from fastapi import FastAPI


app = FastAPI()
CLIENT_ID = 12345
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:8000/login"
# for developing, url where discord will redirect the user after logging in using discord
scopes = OAuthScopes.bot | OAuthScopes.connections

client = oauth2.Client(
    CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scopes=scopes,
    bot_token="BOT_TOKEN", # optional, used only for certain methods
)


@app.get("/login")
async def get_token(code: str, guild_id: Optional[int] = None, permissions: Optional[int] = None):
    session = await client.exchange_code(code)
    user = await session.fetch_current_user()
```
You can find more examples in the examples directory. For more info about the classes and their methods refer to the documentation.
# Discord_Bot_music-player

simple discord bot that plays the given url from youtube or spotify


instructions:

to run the bot, simply run the app1.py script after installing all the dependencies and filling all the required spots in the code with your information.

needed dependencies:

discord,
asyncio,
discord.ext,
discord.utils,
youtube_dl,
spotipy,
spotipy.util


from string 55 to string 57 fill the spots with your spotify api information, you can find them here:

https://developer.spotify.com/dashboard/applications

after logging in, create an application and you will get the client id and the client secret.

NOTE THAT THE SPOTIFY API ALLOWS ONLY TO LISTEN TO THE PREVIEW OF THE GIVEN LINKS AND LASTS ONLY 30 SECONDS, CONSIDER USING YOUTUBE LINKS.

next, you will need to insert your discord bot token in the string 165, you can find your discord bot token in the discord developer portal:

https://discord.com/developers/applications

click your existing application or create a new one, then go to the "bot" page and click "Reset Token".

Great! now the last step is to invite your bot to your server, just copy this link.

https://discord.com/oauth2/authorize?client_id=[YOUR APPLICATION ID]&permissions=8&scope=bot

and replace "[YOUR APPLICATION ID]" with well your application id, you can also find the application id in the discord developer portal, in the general information page
of your application.

Now the bot should be up and running! try connecting to a voice chat and type in chat: .play [youtube-link] and your bot should be reproducing your link!

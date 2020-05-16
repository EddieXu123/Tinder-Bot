# TinderBot
The first of my 10 Bots in 10 days journey, inspired by Jennifer Dewalt's 180 websites in 180 days: https://jenniferdewalt.com/. 

This was also the first bot I ever made, so I consulted Aaron Jack's TinderBot video on YouTube, which helped a lot: https://www.youtube.com/watch?v=6u0OZqrtYac. I also really liked the idea of using Selenium and Chromedriver.




How it works:

First, the bot opens up a new webpage on your browser and goes to Tinder.com. It then logs into your Tinder account via the phone number option, using PyTesseract to extract the 6-digit verification code sent to your iMessage. After logging into your account and closing all the pop-ups, the bot will auto-swipe right on every user, closing any pop-ups that may appear, until you run out of swipes. Whenever you do get a match, the bot will send the simple message "heyyy :)" to the person, and then continue swiping. After you run out of swipes, the bot will then go to the messages tab, go to each person that replied to your initial message, and engage in conversation with them.

# Shin Deshojo Watcher

this is a little flask app i made to check two sites (maplestone and mrmaple) for the shin deshojo japanese maple. it just checks every hour and emails me if it’s in stock. i was tired of refreshing the pages all the time and missing the drops.

I set it up to run on render using the free plan. uptime robot hits it every 10 minutes to keep it awake, otherwise render puts it to sleep. as long as the app stays up, it’ll send me a daily summary too around 7am with all the checks it did in the last 24 hours.

there’s also a /check endpoint if i want to trigger a check manually.

email notifications are handled through resend. super lightweight, no db or anything.

---
<img width="780" height="900" alt="Untitled diagram-2025-10-25-202151" src="https://github.com/user-attachments/assets/56c7fb7b-00d9-4090-8b2e-a6094699ddf1" />


## How to run this

clone the repo  
make a .env file with these:

RESEND_API_KEY=your-resend-api-key

EMAIL_FROM=you@yourdomain.com

EMAIL_TO=your@email.com


## Install the packages
pip install -r requirements.txt  

## Then just run it with:
python app.py
or build and run it with docker if that’s your thing.

---

## Live version

i’ve got it running on render right now. the /check endpoint is public so you can see it do its thing. just don’t spam it, i like my trees.

https://shin-checker.onrender.com/

## Why

i just really want this tree lol

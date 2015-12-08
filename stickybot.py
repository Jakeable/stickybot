
# coding=utf-8

import praw
import sqlite3
import re
import time
import os

r = praw.Reddit('sticky comment temporary replacement for r/askreddit by u/Jakeable')

username = os.envrion.get('USERNAME')
password = os.environ.get('PASSWORD')
subreddit = os.environ.get('SUBREDDIT')
phrase = '[serious]'
altphrase = "r(e|é)sum(e|é)s?"
comment = '**Attention!** Please keep in mind that the OP of this thread has chosen to mark this post with the **[Serious] replies only** tag, therefore [any replies that are jokes, puns, off-topic, or are otherwise non-contributory will be removed](http://www.reddit.com/r/AskReddit/wiki/index#wiki_--.5Bserious.5D_tags--)\n\n'
comment += 'If you don\'t fall within the scope the question is directed to, please do not reply to the question as your comment will be removed. If the question is "Bakers of reddit..." and you\'re not a baker, your comment will be removed. All top-level replies need to be from someone who is in the group the question was asked to.\n\n'
comment += 'If you see others posting comments that violate this tag, please report them to the mods!\n\n'
comment += 'Thanks for your cooperation and enjoy the discussion!'
altcomment = '**Attention!** If you plan to give examples of a bad/inappropriate email address on a resume, **do not post an email address - even if it\'s obviously fake**, rather use something like "[childish email here]", otherwise your comment will not be seen.\n\n'
altcomment += 'We do not allow any type of personal information, even if it\'s supposed to be fake. See rule #4 for more details, thanks!'

r.login(username, password, disable_warning=True)
print('logged in')

sql = sqlite3.connect('threads.db')
cursor = sql.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
print('Loaded Completed table')
sql.commit()

submissions = r.get_subreddit(subreddit).get_new(limit=100)

for post in submissions:
    cursor.execute('SELECT * FROM oldposts WHERE ID=?', [post.fullname])
    regex = re.compile(altphrase)
    if not cursor.fetchone():
        if regex.match(post.title.lower()):
            print('found: ' + post.fullname)
            post.add_comment(altcomment, sticky = True, distinguish = True)
            cursor.execute('INSERT INTO oldposts VALUES(?)', [post.fullname])
            sql.commit()
        elif "serious" in post.title.lower():
            print('found: ' + post.fullname)
            post.add_comment(comment, sticky = True, distinguish = True)
            cursor.execute('INSERT INTO oldposts VALUES(?)', [post.fullname])
            sql.commit()

time.sleep(60)

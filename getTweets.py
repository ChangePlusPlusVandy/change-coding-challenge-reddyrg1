import tweepy
import re
import random
import tkinter as tk
from tkinter import *
from tkinter import ttk


elonTweetsStr = []
kanyeTweetsStr = []

class Tweet:
    tweet = ""
    tweeter = ""

    def loadTweets():
        #APIs. I don't know exactly how to store them securely
        auth = tweepy.OAuthHandler("a9UuRQ5oe2E04zXmQSWBH16L5", "cBNJFQ89ayzzHihTHAmNo6zrIiT1uMdcTMLdZMLVb9yrexzwsb")
        auth.set_access_token("1309379012523970560-UOGK1eAMtmD25KweeiF4Rx3OaFCaie",
                              "8oreS4oMlfK6TH8qXcqxMW8gOzbYvrfI6oZZqc8H2KDpS")

        api = tweepy.API(auth)

        elonTweets = []
        tweets = api.user_timeline(screen_name="elonmusk",
                                   # 200 is the maximum allowed count
                                   count=200,
                                   include_rts=False,
                                   # Necessary to keep full_text
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode='extended'
                                   )
        oldest_id = tweets[-1].id

        while True:
            tweets = api.user_timeline(screen_name="elonmusk",
                                       # 200 is the maximum allowed count
                                       count=200,
                                       include_rts=False,
                                       max_id=oldest_id - 1,
                                       # Necessary to keep full_text
                                       # otherwise only the first 140 words are extracted
                                       tweet_mode='extended'
                                       )
            if len(tweets) == 0:
                break
            oldest_id = tweets[-1].id
            elonTweets.extend(tweets)
            # print('N of tweets downloaded till now {}'.format(len(elonTweets)))

        # filter Elon's tweets
        for tweet in elonTweets:
            if len(tweet.entities['user_mentions']) == 0:
                fullText = tweet.full_text
                fullText = re.sub(r'https?:\/\/\S*', '', fullText, flags=re.MULTILINE)
                if len(fullText) != 0:
                    elonTweetsStr.append(fullText)

        kanyeTweets = []
        tweets = api.user_timeline(screen_name="kanyewest",
                                   # 200 is the maximum allowed count
                                   count=200,
                                   include_rts=False,
                                   # Necessary to keep full_text
                                   # otherwise only the first 140 words are extracted
                                   tweet_mode='extended'
                                   )
        oldest_id = tweets[-1].id
        while True:
            tweets = api.user_timeline(screen_name="kanyewest",
                                       # 200 is the maximum allowed count
                                       count=200,
                                       include_rts=False,
                                       max_id=oldest_id - 1,
                                       # Necessary to keep full_text
                                       # otherwise only the first 140 words are extracted
                                       tweet_mode='extended'
                                       )
            if len(tweets) == 0:
                break
            oldest_id = tweets[-1].id
            kanyeTweets.extend(tweets)
            # print('N of tweets downloaded till now {}'.format(len(kanyeTweets)))

        # filter Kanye's tweets
        for tweet in kanyeTweets:
            if len(tweet.entities['user_mentions']) == 0:
                fullText = tweet.full_text
                fullText = re.sub(r'https?:\/\/\S*', '', fullText, flags=re.MULTILINE)
                if len(fullText) != 0:
                    kanyeTweetsStr.append(fullText)


    # Pre: loadTweets must be run once
    def generateTweet():
        totalTweets = len(elonTweetsStr) + len(kanyeTweetsStr)
        randNum = random.randint(0, totalTweets - 1)
        selectedTweet = ""
        user = ""
        if randNum >= len(elonTweetsStr):
            selectedTweet = kanyeTweetsStr[randNum - len(elonTweetsStr)]
            user = "kanye"
        else:
            selectedTweet = elonTweetsStr[randNum]
            user = "elon"
        Tweet.tweet = selectedTweet
        Tweet.tweeter = user

    def getTweet():
        return Tweet.tweet

    def getTweeter():
        return Tweet.tweeter

#Tkinter GUI
class App(Frame):

    def __init__(self):
        super().__init__()
        self.count = 0
        self.total = 0
        self.initUI()

    def do_nothing(self, event=None):
        return 'break'

    def initUI(self):
        self.master.title("Guess Tweet!")
        self.text = Text(height=8)
        self.text.bind(sequence='<Key>', func=self.do_nothing)
        self.entry = Entry(width = 10)
        self.checkButton = Button(text = "Check", width = 50, height = 2, command = self.check)
        self.answerLabel = Label(text='')
        self.correctLabel = Label(text='Number Correct: ')
        self.correctBox = Text(height= 1, width = 5, font=('Helvetica', 32))
        self.correctBox.bind(sequence='<Key>', func=self.do_nothing)
        self.percentLabel = Label(text='Percent Correct: ')
        self.percentBox = Text(height=1, width=8, font=('Helvetica', 32))
        self.percentBox.bind(sequence='<Key>', func=self.do_nothing)


        self.text.pack(padx=10, pady=5, fill=X)
        self.entry.pack(pady=5)
        self.checkButton.pack(pady=5)
        self.answerLabel.pack(pady=5)
        self.correctLabel.pack(pady=5)
        self.correctBox.pack(pady=5)
        self.percentLabel.pack(pady=5)
        self.percentBox.pack(pady=5)


    def set_text(self, input_str):
        self.text.insert(tk.END, input_str)

    def set_correct(self):
        self.correctBox.insert(tk.END, self.count)

    def set_percent(self):
        percent = str(round((self.count/self.total) * 100, 2)) + "%"
        self.percentBox.insert(tk.END, percent)

    #check if tweet is correct
    def check(self):
        guess = self.entry.get()
        if guess.lower() == Tweet.getTweeter():
            self.answerLabel.config(text='Correct')
            self.count += 1
        else:
            self.answerLabel.config(text='Incorrect')
        self.total += 1
        Tweet.generateTweet()
        self.text.delete("1.0", END)
        self.entry.delete(0, "end")
        self.correctBox.delete("1.0", END)
        self.percentBox.delete("1.0", END)
        self.set_correct()
        self.set_percent()
        self.set_text("Tweet: " + Tweet.getTweet() + "\n\n")
        self.set_text("Guess Elon or Kanye in the box below: ")



def main():

    root = Tk()
    root.geometry("600x500")
    app = App()

    def set_text(input_str):
        app.text.insert(tk.END, input_str)

    print("Loading...\n")
    Tweet.loadTweets()

    Tweet.generateTweet()
    set_text("Tweet: " + Tweet.getTweet() +"\n\n")
    set_text('Guess Elon or Kanye in the box below: ')

    root.mainloop()


if __name__ == '__main__':
    main()
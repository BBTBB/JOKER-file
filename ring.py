from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name,Glang
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from uuid import uuid4

from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)


def updateMsgs(client, message,redis):
  pass

def kbtotx(numBu,wonNum,k):
  tx = ""
  i = 0
  x = 0
  y = 1
  if int(wonNum) == int(k):
    while i < int(numBu) / 3:
      while x < 3:
        if y == int(wonNum):
          tx += ""
        else:
           tx += ""
        x += 1
        y += 1
      i += 1
      tx+= "\n"
      x = 0
  else:
    while i < int(numBu)/3:
      while x < 3:
        if y == int(wonNum):
          tx += ""
        elif y == int(k):
          tx += ""
        else:
          tx += ""
        x += 1
        y += 1
      i += 1
      tx+= "\n"
      x = 0
  return tx
def updateCb(client, callback_query,redis):
  if callback_query.inline_message_id:
    return False
  date = callback_query.data
  userID = callback_query.from_user.id
  userFN = callback_query.from_user.first_name
  username = callback_query.from_user.username
  chatID = callback_query.message.chat.id
  message_id = callback_query.message.message_id
  if re.search("^ring.pyplay$",date):
    start = "     "
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(" 1", callback_data="ring=1="+str(userID))
    ],[
        InlineKeyboardButton(" 2", callback_data="ring=2="+str(userID))
    ],[
        InlineKeyboardButton(" 3", callback_data="ring=3="+str(userID))
    ],[
        InlineKeyboardButton("  4", callback_data="ring=4="+str(userID))
    ]])
    Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":start,"disable_web_page_preview":True,"reply_markup":kb})

  if re.search("ring=",date):
    tx = callback_query.message.text
    p1 = date.split("=")[2]
    df = int(date.split("=")[1])
    numBu = df*3
    wonNum = random.randint(1, numBu)
    if userID == int(p1):
        i = 0
        x = 0
        k = 1
        ar = []
        a = []
        em = ""

        while i < df:
            while x < 3:
                cd = f"rg={p1}={numBu}={wonNum}={k}"
                print(cd)
                a.append(InlineKeyboardButton("",callback_data=cd))
                x += 1
                k += 1
            i += 1
            x = 0
            
            ar.append(a)
            a = []
        ar.append([InlineKeyboardButton("",url="t.me/"+BBTBB)])
        kb = InlineKeyboardMarkup(ar)

        Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":"      ","disable_web_page_preview":True,"reply_markup":kb})
    else:
        Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":"   ","show_alert":True})



  if re.search("rg=",date):
    ex = date.split("=")
    user = ex[1]
    numBu = ex[2]
    wonNum = ex[3]
    k = ex[4]
    tx = kbtotx(numBu,wonNum,k)
    txt = ""
    if int(wonNum) == int(k):
      txt += f" \n\n{tx}\n   "
    else:
      txt += f"  \n\n{tx}\n   "
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(" ",callback_data="ring.pyplay")]])
    Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":txt,"disable_web_page_preview":True,"reply_markup":kb})










  go = """{}   :- ({})
{}   :- ({})
    ({})"""
  go2 = """{}   :- ({})
{}   :- ({})
  ({})"""

  go3 = """{}   :- ({})
{}   :- ({})
 """

  if re.search("st1=",date):
    ex = date.split("=")
    user1 = ex[1]
    user2 = ex[2]
    chs = ex[3]
    try:
      getUser = client.get_users(int(user2))
      userId = getUser.id
      userFn = getUser.first_name
    except Exception as e:
      userFn = user2
    if userID != int(user1):
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":" ","show_alert":True})
      return False
    ch = ANSWERS[int(chs)]
    kb = InlineKeyboardMarkup([
      [InlineKeyboardButton("",callback_data="st2={}={}=0={}".format(user1,user2,chs)),
      InlineKeyboardButton("",callback_data="st2={}={}=1={}".format(user1,user2,chs)),
      InlineKeyboardButton("",callback_data="st2={}={}=2={}".format(user1,user2,chs)),],

      [InlineKeyboardButton("",url="t.me/"+BBTBB)]
      ])
    Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go.format("",userFN,"",userFn, userFn),"disable_web_page_preview":True,"reply_markup":kb})

  if re.search("st2=",date):
    ex = date.split("=")
    user1 = ex[1]
    user2 = ex[2]
    chs2 = ex[3]
    chs1 = ex[4]
    try:
      getUser = client.get_users(int(user1))
      userFn = getUser.first_name
    except Exception as e:
      userFn = user1
    if userID != int(user2):
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":" ","show_alert":True})
      return False
    ch1 = ANSWERS[int(chs1)]
    ch2 = ANSWERS[int(chs2)]
    pe = [user1,user2]
    winer = get_winner(ch1, ch2)
    if winer != "tie":
      if int(pe[winer]) == int(user2):
        us = userFN
        usin = user2
      elif int(pe[winer]) == int(user1):
        us = userFn
        usin = user1
      redis.hincrby("{}Nbot:{}:points".format(BOT_ID,chatID),usin,5)
      kb = InlineKeyboardMarkup([[InlineKeyboardButton(" ",callback_data="rer={}".format(user1))]])
      Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go2.format(emj(ch1),userFn,emj(ch2),userFN, us),"disable_web_page_preview":True,"reply_markup":kb})

    elif winer == "tie":
      redis.hincrby("{}Nbot:{}:points".format(BOT_ID,chatID),user1,2)
      redis.hincrby("{}Nbot:{}:points".format(BOT_ID,chatID),user2,2)
      kb = InlineKeyboardMarkup([[InlineKeyboardButton(" ",callback_data="rer={}".format(user1))]])
      Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go3.format(emj(ch1),userFn,emj(ch2),userFN),"disable_web_page_preview":True,"reply_markup":kb})



  if re.search("rps=",date):
    userid = date.split("=")[1]
    if userID == int(userid):
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":"      ","show_alert":True})
      return False
    try:
      getUser = client.get_users(userid)
      userId = getUser.id
      userFn = getUser.first_name
    except Exception as e:
      userFn = userid
    kb = InlineKeyboardMarkup([
      [InlineKeyboardButton("",callback_data="st1={}={}=0".format(userid,userID)),
      InlineKeyboardButton("",callback_data="st1={}={}=1".format(userid,userID)),
      InlineKeyboardButton("",callback_data="st1={}={}=2".format(userid,userID)),],

      [InlineKeyboardButton("",url="t.me/"+BBTBB)]
      ])

    Bot("editMessageText",{"chat_id":chatID,"message_id":message_id,"text":go.format("",userFn,"",userFN, userFn),"disable_web_page_preview":True,"reply_markup":kb})


  
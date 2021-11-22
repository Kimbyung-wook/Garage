import requests
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import time
from timer import Timer
from bs4 import BeautifulSoup
from datetime import datetime
# date = '211117'
# MovieName = '유체이탈자'
# Theater = '2D'
date = '211114'
MovieName = '이터널스'
Theater = 'IMAX관'
# Theater = '4DX'
url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date=20"+date

# For Telegram
do_stop = False
def stop_command(update, context):
  update.message.repley_text('알람 그만할게~')
  
telegram_token = ''
chat_id = ''
imax_booking_bot = telegram.Bot(token = telegram_token)
# updater = Updater(telegram_token, use_context = True)
# stop_handler = CommandHandler('stop', stop_command)
# updater.dispatcher.add_handler(stop_handler)

if __name__ == "__main__":
  
  isFirst = True
  didyouget = False
  timer  = Timer()
  prevtic = timer.get_tic()
  dt = 60*60

  now = datetime.now()
  nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
  msg = '%s : 이제 예매표 본다..! : %s 일자 %s %s'%(nowDatetime, date, MovieName, Theater)
  print(msg)
  imax_booking_bot.sendMessage(chat_id=chat_id, text=msg)
  while True:
    if True:
      resp = requests.get(url)
      html = resp.text
      soup = BeautifulSoup(html, 'html.parser')
      lists = soup.select('.col-times')
      now = datetime.now()
      nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
      for i in range(0,len(lists)):
        if MovieName in str(lists[i]) and Theater in str(lists[i]):
          if '준비중' in str(lists[i]):
            dt = 60*10
            msg = '%s : %s 일자 %s - %s - 준비중..!'%(nowDatetime, date, MovieName, Theater)
          else:
            dt = 1
            msg = '%s : %s 일자 %s - %s - 예매 ㄱㄱ!!'%(nowDatetime, date, MovieName, Theater)
          break
        else:
          msg = '%s : %s 일자 %s - %s - 아직 안뜸...ㅠ'%(nowDatetime, date, MovieName, Theater)
    # updater.start_polling(timeout=0, clean=True)
    # updater.idle()
    nowtic = timer.get_tic()
    if ((isFirst == True) | (nowtic - prevtic > dt)):
      isFirst = False
      # print('dt : ',nowtic - prevtic)
      prevtic = nowtic
      print(msg)
      imax_booking_bot.sendMessage(chat_id=chat_id, text=msg)

    time.sleep(3)
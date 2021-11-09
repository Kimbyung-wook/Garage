import requests
import telegram
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

telegram_token = ''
chat_id = ''
imax_booking_bot = telegram.Bot(token = telegram_token)

if __name__ == "__main__":
  didyouget = False
  timer  = Timer()
  prevtic = timer.get_tic()
  dt = 60*60
  while True:
    time.sleep(1)
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
    nowtic = timer.get_tic()
    if (nowtic - prevtic > dt):
      # print('dt : ',nowtic - prevtic)
      prevtic = nowtic
      print(msg)
      imax_booking_bot.sendMessage(chat_id=chat_id, text=msg)
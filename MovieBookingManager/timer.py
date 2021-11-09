import time

class Timer():
  def __init__(self):
    self.start = time.time()
    self.end = time.time()

  def tic(self):
    self.start = time.time()

  def get_tic(self):
    self.end = time.time()
    return self.end - self.start

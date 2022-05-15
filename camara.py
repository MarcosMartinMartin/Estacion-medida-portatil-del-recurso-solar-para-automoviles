import cv2, queue, threading, time

#CAPTURA DE VIDEO SIN BUFFER
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  #lee los frames tan pronto como estén disponibles, manteniendo solo el más reciente
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   #descarta el frame previo
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

import csv
import tkinter

class Record:
  def __init__(self, file_name: str):
    with open(file_name, encoding="utf-8") as f:
      reader = csv.reader(f)
      self.data = [row for row in reader]
      self.file_name = file_name

  def write(self):
    with open(self.file_name, 'w', encoding="utf-8", newline="") as f:
      writer = csv.writer(f)
      writer.writerows(self.data)


class NameList:
  def __init__(self, FILE_NAME: str):
    with open(FILE_NAME, encoding="utf-8") as f:
      reader = csv.reader(f)
      self.data = [row for row in reader]
  

class Image:
  def __init__(self, FILE_NAME: str):
    self.data = tkinter.PhotoImage(file = FILE_NAME)
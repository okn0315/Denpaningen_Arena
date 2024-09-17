import tkinter
import gui_module
import data_module


DEL_IMAGE_FILE_NAME = "del_image.png"
ENTER_IMAGE_FILE_NAME = "enter_image.png"


"""
ルーチンの構造
MainRoutine
┣━_TitleRoutine
┣━_ReadModeRoutine
┣━_PlayModeRoutine
┃ ┣━_PlayModeCharacterSelectRoutine
┃ ┣━_PlayModeNoDataRoutine
┃ ┣━_PlayModeMakeNewDataRoutine
┃ ┗━_PlayModeCalculateRoutine
┗━_DeleteModeRoutine

並列の位置にあるルーチンはいずれか1つが実行される
下層にあるルーチンは上層のルーチン内部で実行される

MainRoutineは繰り返し実行される(これにより動的な処理ができる)

routine = routine.execute()
というプログラムがあるが、これは繰り返し実行することにより任意のルーチンが
実行できるようになる仕組み。
execute()で自分自身を返すともう一度同じルーチンが実行されるが
異なるルーチンを返すと自分自身の代わりに異なるルーチンが次から実行される
"""


class Routine:
  """
  あらゆるルーチンはこれを継承すること
  ルーチン内では必ずexecute()を定義し、ルーチンを実行する場合はこれを呼び出すこと
  """
  def __init__(self, next_id = 1):
    """
    オーバーライド時はsuper()を使うなりしてこれを呼び出すこと
    """
    # ユーザの入力に応じて変化する
    # ユーザが入力をしたときに set_action() を使用して値を変化させよ
    self.action = None

    # 全てのウィンドウに配置されるラベルやボタンなどはidで管理される
    # サブルーチンでは、引数で渡すことでメインルーチンとサブルーチンのどちらでも一意に定められる
    self.next_id = next_id


  def execute(self):
    """
    この関数を実行するとルーチンが実行される
    全ルーチンはこれと同名の関数を定義すること
    この中にはルーチンで処理したい内容を記述する
    """
    pass


  def set_action(self, arg):
    """
    ユーザ入力識別用
    コールバック関数に lambda : set_action(n) を指定すれば、
    対応する入力がなされるとself.actionにnが代入される

    変数xを使ってコールバック関数を作る場合、次の2通りの書き方ができる。
    A: lambda : set_action(x)
    B: lambda _x=x : set_action(_x)
    Aの書き方は、コールバックされたときのxの値を参照する。
    Bの書き方は、lambda式を記述した時点でのxの値を参照する。
    """
    self.action = arg



class MainRoutine(Routine):
  """
  このルーチン自体は何もしない
  内部で別のルーチンを起動するだけ
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      next_id: int = 1,
      ):
    super().__init__(next_id)
    self.next_routine = _TitleRoutine(root,
                                      window_object_list,
                                      display_id_list,
                                      forget_id_list,
                                      destroy_id_list,
                                      char_name_list,
                                      record,
                                      self.next_id,)


  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    self.next_routine = self.next_routine.execute(root,
                                                  window_object_list,
                                                  display_id_list,
                                                  forget_id_list,
                                                  destroy_id_list,
                                                  char_name_list,
                                                  record,)



class _TitleRoutine(Routine):
  """
  タイトル画面
  3つのボタンから何をするか選ぶ
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      next_id: int = 1,
      ):
    
    super().__init__(next_id)
    
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id,
        place = (550, 250),
        window_object = tkinter.Label(root,
                                      text = "何をするか選択してください",
                                      font = ('Yu Gothic UI', "15")),
        ),
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 1,
        place = (340, 400),
        window_object = tkinter.Button(root,
                                       text = "統計を見る",
                                       command = lambda : self.set_action(1),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 17,
                                       height = 1,),
        ),
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 2,
        place = (560, 400),
        window_object = tkinter.Button(root,
                                       text = "ゲームを遊びながら使用",
                                       command = lambda : self.set_action(2),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 17,
                                       height = 1,),
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 3,
        place = (780, 400),
        window_object = tkinter.Button(root,
                                       text = "統計を削除",
                                       command = lambda : self.set_action(3),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 17,
                                       height = 1,),
        )
      )
    
    self.id_list = [i for i in range(self.next_id, self.next_id+4)]
    display_id_list.extend(self.id_list)
    
    self.next_id += 4


  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self
    
    if self.action in (1,2,3):
      destroy_id_list.extend(self.id_list)
      del self.id_list

      sub_routine_dict = {1: _ReadModeRoutine,
                          2: _PlayModeRoutine,
                          3: _DeleteModeRoutine,}
      next_routine = sub_routine_dict.get(self.action)(root,
                                                       window_object_list,
                                                       display_id_list,
                                                       forget_id_list,
                                                       destroy_id_list,
                                                       char_name_list,
                                                       record,
                                                       self.next_id)
      
      self.action = 0
    
    return next_routine



class _ReadModeRoutine(Routine):
  """
  ただファイルの戦績を表示するだけ
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      next_id: int = 1,
      ):
    
    super().__init__(next_id)

    self.page = 1
    self.id_list = [self.next_id+i for i in range(24)]
    self.label_str = [tkinter.StringVar(root) for i in range(21)]

    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id,
        place = (50, 50),
        window_object = tkinter.Button(root,
                                       text = "◁",
                                       command = lambda : self.set_action(1),
                                       font = ('Yu Gothic UI', "15"),
                                       width = 4,
                                       height = 1,),
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 1,
        place = (500, 600),
        window_object = tkinter.Button(root,
                                       text = "◁",
                                       command = lambda : self.set_action(2),
                                       font = ('Yu Gothic UI', "15"),
                                       width = 4,
                                       height = 1,),
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 2,
        place = (800, 600),
        window_object = tkinter.Button(root,
                                       text = "▷",
                                       command = lambda : self.set_action(3),
                                       font = ('Yu Gothic UI', "15"),
                                       width = 4,
                                       height = 1,),
        )
      )
    
    place_list = [(400, 100),
                  (550, 100),
                  (700, 100),
                  (850, 100),
                  (250, 200),
                  (400, 200),
                  (550, 200),
                  (700, 200),
                  (850, 200),
                  (250, 300),
                  (400, 300),
                  (550, 300),
                  (700, 300),
                  (850, 300),
                  (300, 400),
                  (450, 400),
                  (750, 400),
                  (900, 400),
                  (600, 600),
                  (650, 600),
                  (700, 600), ]
    window_object_list.extend([
      gui_module.WindowObject(
        id = self.next_id + 3 + i,
        place = place_list[i],
        window_object = tkinter.Label(root,
                                      textvariable = self.label_str[i],
                                      font = ('Yu Gothic UI', "15"),)
        ) for i in range(21)
      ])
    
    display_id_list.extend(self.id_list)

    self.next_id += 24

    self.flush = True
  

  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self

    if self.action in (2,3):  # ページ切り替え
      if self.action == 2:
        if self.page >= 2:
          self.page -= 1
      elif self.action == 3:
        if self.page < len(record.data):
          self.page += 1      
      self.flush = True
      self.action = 0

    if self.flush:  # 画面更新
      label_str_list = []
      if self.page > len(record.data):
        label_str_list.extend(["NO_DATA" for i in range(4)])
        label_str_list.append("WIN")
        label_str_list.extend(["NO_DATA" for i in range(4)])
        label_str_list.append("RATIO")
        label_str_list.extend(["NO_DATA" for i in range(4)])
        label_str_list.append("TOTAL")
        label_str_list.append("NO_DATA")
        label_str_list.append("DRAW")
        label_str_list.append("NO_DATA")
        label_str_list.append("0")
        label_str_list.append("/")
        label_str_list.append("0")
      else:
        index = self.page - 1
        label_str_list.extend(record.data[index][0:4])
        label_str_list.append("WIN")
        label_str_list.extend(record.data[index][5:9])
        label_str_list.append("RATIO")
        label_str_list.extend([ str(format(
          int(record.data[index][5+i])/int(record.data[index][4]) * 100,
          ".2f"
          )) + '%'
          for i in range(4)
          ])
        label_str_list.append("TOTAL")
        label_str_list.append(record.data[index][4])
        label_str_list.append("DRAW")
        label_str_list.append(record.data[index][9])
        label_str_list.append(str(index+1))
        label_str_list.append("/")
        label_str_list.append(str(len(record.data)))
        no_name_list = [i
                        for i in range(4)
                        if record.data[index][i] == ""]
        for i in no_name_list:
          label_str_list[5+i] = ""
          label_str_list[10+i] = ""
        
      for i in range(21):
        self.label_str[i].set(label_str_list[i])
      self.flush = False

    if self.action == 1:
      destroy_id_list.extend(self.id_list)
      del self.page, self.id_list, self.label_str
      self.action = 0
      next_routine = _TitleRoutine(root,
                                   window_object_list,
                                   display_id_list,
                                   forget_id_list,
                                   destroy_id_list,
                                   char_name_list,
                                   record,
                                   self.next_id)

    return next_routine



class _PlayModeRoutine(Routine):
  """
  ゲームを起動しながら使用する
  内部でさらに別のルーチンを起動
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      next_id: int = 1,
      ):
    
    super().__init__(next_id)

    self.sub_routine = _PlayModeCharacterSelectRoutine(
      root,
      window_object_list,
      display_id_list,
      forget_id_list,
      destroy_id_list,
      char_name_list,
      record,
      next_id,
      )


  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self

    self.sub_routine = self.sub_routine.execute(
      root,
      window_object_list,
      display_id_list,
      forget_id_list,
      destroy_id_list,
      char_name_list,
      record,
      )

    return next_routine



class _DeleteModeRoutine(Routine):
  """
  過去の戦績を削除する
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      next_id: int = 1,
      ):
    
    super().__init__(next_id)

    self.id_list = list(range(
      self.next_id,
      self.next_id + 3,
      ))
    
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id,
        place = (50, 50),
        window_object = tkinter.Button(root,
                                       text = "◁",
                                       command = lambda : self.set_action(1),
                                       font = ('Yu Gothic UI', "15"),
                                       width = 4,
                                       height = 1,)
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 1,
        place = (580, 500),
        window_object = tkinter.Button(root,
                                       text = "削除",
                                       command = lambda : self.set_action(2),
                                       bg = "red",
                                       font = ("Yu Gothic UI", "20", "bold"),)
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 2,
        place = (300, 300),
        window_object = tkinter.Label(root,
                                      text = "過去の統計データを削除する場合はボタンを押してください",
                                      font = ("Yu Gothic UI", "20", "bold"),)
        )
      )
    
    display_id_list.extend(self.id_list)

    self.next_id += 3


  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self

    if self.action == 2:
      record.data = []
      record.write()
      next_routine = _TitleRoutine(root,
                                   window_object_list,
                                   display_id_list,
                                   forget_id_list,
                                   destroy_id_list,
                                   char_name_list,
                                   record,
                                   self.next_id)
      destroy_id_list.extend(self.id_list)
      del self.id_list
      self.action = 0

    elif self.action == 1:
      next_routine = _TitleRoutine(root,
                                   window_object_list,
                                   display_id_list,
                                   forget_id_list,
                                   destroy_id_list,
                                   char_name_list,
                                   record,
                                   self.next_id)
      destroy_id_list.extend(self.id_list)
      del self.id_list
      self.action = 0

    return next_routine
  


class _PlayModeCharacterSelectRoutine(Routine):
  """
  _PlayModeRoutine()の内部で実行
  キャラを最大4体選択する
  記録の有無に応じて異なるルーチンを実行
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      next_id: int = 1,
      ):
    
    super().__init__(next_id)

    char_name_list_len = len(char_name_list.data)

    self.id_list = list(range(
      self.next_id,
      self.next_id + 8 + char_name_list_len
      ))
    
    self.del_img = data_module.Image(DEL_IMAGE_FILE_NAME).data
    self.enter_img = data_module.Image(ENTER_IMAGE_FILE_NAME).data
    
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id,
        place = (50, 50),
        window_object = tkinter.Button(root,
                                       text = "◁",
                                       command = lambda : self.set_action(1),
                                       font = ('Yu Gothic UI', "15"),
                                       width = 4,
                                       height = 1,)
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 1,
        place = (900, 50),
        window_object = tkinter.Button(root,
                                       image = self.del_img,
                                       command = lambda : self.set_action(2))
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 2,
        place = (1100, 50),
        window_object = tkinter.Button(root,
                                       image = self.enter_img,
                                       command = lambda : self.set_action(3))
        )
      )
    
    for i in range(char_name_list_len):
      window_object_list.append(
        gui_module.WindowObject(
          id = self.next_id + 3 + i,
          place = (50 + 122*(i%10), 200 + 47*(i//10)),
          window_object = tkinter.Button(root,
                                         text = char_name_list.data[i][0],
                                         command = lambda _i=i : self.set_action(4+_i),
                                         width = 14,
                                         height = 2,
                                         font = ('Yu Gothic UI', "10", "bold"))
          )
        )
      
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 3 + char_name_list_len,
        place = (400, 80),
        window_object = tkinter.Label(root,
                                      text = "対戦キャラを選択してください",
                                      font = ('Yu Gothic UI', "13"),)
        )
      )
    
    self.selected_char_name_list = [tkinter.StringVar(root, "") for i in range(4)]

    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = self.next_id + 4 + char_name_list_len + i,
          place = (150 + 170*i, 120),
          window_object = tkinter.Label(root,
                                        textvariable = self.selected_char_name_list[i],
                                        font = ('Yu Gothic UI', "15"),)
          )
        )

    display_id_list.extend(self.id_list)

    self.next_id += 8 + char_name_list_len
    

  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self

    char_name_list_len = len(char_name_list.data)

    def change_suggestion_color():
      selecting_char_name_list = []
      for i in range(4):
        name = self.selected_char_name_list[i].get()
        if name != "":
          selecting_char_name_list.append(name)
      if len(selecting_char_name_list) != 0:
        selecting_list = [char_name_list.data.index([name])
                          for name in selecting_char_name_list]
        suggestion_name_set = set()
        for i in range(len(record.data)):
          all_in = True
          for each_selecting_char_name in selecting_char_name_list:
            if each_selecting_char_name not in record.data[i][0:4]:
              all_in = False
              break
          if all_in:
            for each_name in record.data[i][0:4]:
              if each_name != "" and each_name not in selecting_char_name_list:
                suggestion_name_set.add(each_name)
        suggestion_set = set()
        for each_name in suggestion_name_set:
          suggestion_set.add(char_name_list.data.index([each_name]))
        for i in range(char_name_list_len):
          window_object_list[self.next_id-6-char_name_list_len+i].window_object.configure(
            bg = "white"
          )
        for i in selecting_list:
          window_object_list[self.next_id-6-char_name_list_len+i].window_object.configure(
            bg = "green"
          )
        for i in suggestion_set:
          window_object_list[self.next_id-6-char_name_list_len+i].window_object.configure(
            bg = "yellow"
          )
      else:
        for i in range(char_name_list_len):
          window_object_list[self.next_id-6-char_name_list_len+i].window_object.configure(
            bg = "white"
          )

    if self.action in list(range(4, 4+char_name_list_len)):
      new_index = 0
      while new_index < 4:
        if self.selected_char_name_list[new_index].get() != "":
          new_index += 1
        else:
          break
      if new_index < 4:
        self.selected_char_name_list[new_index].set(char_name_list.data[self.action-4][0])
      change_suggestion_color()
      self.action = 0

    elif self.action == 2:
      last_index = -1
      while last_index < 3:
        if self.selected_char_name_list[last_index+1].get() != "":
          last_index += 1
        else:
          break
      if last_index >= 0:
        self.selected_char_name_list[last_index].set("")
      change_suggestion_color()
      self.action = 0

    elif self.action == 3:
      destroy_id_list.extend(self.id_list)
      str_list = [self.selected_char_name_list[i].get() for i in range(4)]
      record_index = None
      for i in range(len(record.data)):
        if set(str_list) == set(record.data[i][0:4]):
          record_index = i
      if record_index != None:
        next_routine = _PlayModeCalculateRoutine(root,
                                                 window_object_list,
                                                 display_id_list,
                                                 forget_id_list,
                                                 destroy_id_list,
                                                 char_name_list,
                                                 record,
                                                 str_list,
                                                 record_index,
                                                 self.next_id,)
      else:
        next_routine = _PlayModeNoDataRoutine(
          root,
          window_object_list,
          display_id_list,
          forget_id_list,
          destroy_id_list,
          char_name_list,
          record,
          str_list,
          self.next_id,
          )

      del self.id_list, self.selected_char_name_list
      self.action = 0

    elif self.action == 1:
      destroy_id_list.extend(self.id_list)
      del self.id_list, self.selected_char_name_list
      self.action = 0
      next_routine = _TitleRoutine(root,
                                   window_object_list,
                                   display_id_list,
                                   forget_id_list,
                                   destroy_id_list,
                                   char_name_list,
                                   record,
                                   self.next_id)

    return next_routine



class _PlayModeNoDataRoutine(Routine):
  """
  _PlayModeRoutine()の内部で実行
  選択されたキャラのデータが存在しない場合の確認画面
  戻るか新しくデータを作るか選べ、それに応じて異なるルーチンを実行
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      selected_char_name_list: list[str],
      next_id: int = 1,
      ):
    
    super().__init__(next_id)

    self.id_list = list(range(self.next_id, self.next_id+7))
    self.selected_char_name_list = selected_char_name_list

    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id,
        place = (550, 500),
        window_object = tkinter.Button(root,
                                       text = "新規データ作成",
                                       command = lambda : self.set_action(1),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 15,
                                       height = 2,)
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 1,
        place = (550, 600),
        window_object = tkinter.Button(root,
                                       text = "キャラ選択にもどる",
                                       command = lambda : self.set_action(2),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 15,
                                       height = 2,)
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = self.next_id + 2,
        place = (450, 100),
        window_object = tkinter.Label(root,
                                      text = "該当するキャラの過去の戦績が存在しません",
                                      font = ("Yu Gothic UI", "15"),),
        )
      )
    
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = self.next_id + 3 + i,
          place = (250 + 200*i, 200),
          window_object = tkinter.Label(root,
                                        text = self.selected_char_name_list[i],
                                        font = ("Yu Gothic UI", "15"),
                                        width = 15,
                                        height = 2,),
          )
        )
        
    display_id_list.extend(self.id_list)

    self.next_id += 7


  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self

    if self.action == 1:
      destroy_id_list.extend(self.id_list)
      self.action = 0
      next_routine = _PlayModeMakeNewDataRoutine(root,
                                                 window_object_list,
                                                 display_id_list,
                                                 forget_id_list,
                                                 destroy_id_list,
                                                 char_name_list,
                                                 record,
                                                 self.selected_char_name_list,
                                                 self.next_id)
      del self.id_list, self.selected_char_name_list

    elif self.action == 2:
      destroy_id_list.extend(self.id_list)
      self.action = 0
      next_routine = _PlayModeCharacterSelectRoutine(root,
                                                     window_object_list,
                                                     display_id_list,
                                                     forget_id_list,
                                                     destroy_id_list,
                                                     char_name_list,
                                                     record,
                                                     self.next_id)
      del self.id_list, self.selected_char_name_list

    return next_routine



class _PlayModeMakeNewDataRoutine(Routine):
  """
  _PlayModeRoutine()の内部で実行
  新しく戦績を作成
  勝ったキャラまたは引き分けを選択
  戦績作成後はキャラ選択画面に戻る
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      selected_char_name_list: list[str],
      next_id: int = 1,
      ):
    
    super().__init__(next_id)

    self.id_list = list(range(next_id, next_id+16))
    self.selected_char_name_list = selected_char_name_list
    self.no_char_list = [i
                         for i in range(4)
                         if self.selected_char_name_list[i] == ""]

    window_object_list.append(
      gui_module.WindowObject(
        id = next_id,
        place = (50, 50),
        window_object = tkinter.Button(root,
                                       text = "◁",
                                       command = lambda : self.set_action(1),
                                       font = ('Yu Gothic UI', "15"),
                                       width = 4,
                                       height = 1,),
        )
      )
    
    for i in range(4):
      window_object_list.append(
      gui_module.WindowObject(
        id = next_id + 1 + i,
        place = (300 + 200*i, 690),
        window_object = tkinter.Button(root,
                                       text = self.selected_char_name_list[i],
                                       command = lambda _i=i : self.set_action(2+_i),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 15,
                                       height = 2,),
        )
      )
    forget_id_list.extend([next_id+1+i for i in self.no_char_list])

    window_object_list.append(
      gui_module.WindowObject(
        id = next_id + 5,
        place = (1100, 690),
        window_object = tkinter.Button(root,
                                       text = "DRAW",
                                       command = lambda _i=i : self.set_action(6),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 15,
                                       height = 2,),
        )
      )

    self.entry_list = [tkinter.Entry(root,
                                     font = ("Yu Gothic UI", "20"),
                                     width = 10,
                                     bg = "gray97",) for i in range(4)]
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = next_id + 6 + i,
          place = (300 + 200*i, 410),
          window_object = self.entry_list[i],
          )
        )
    forget_id_list.extend([next_id+6+i for i in self.no_char_list])
      
    window_object_list.append(
      gui_module.WindowObject(
        id = next_id + 10,
        place = (100, 400),
        window_object = tkinter.Label(root,
                                      text = "オッズ",
                                      font = ("Yu Gothic UI", "15"),
                                      width = 15,
                                      height = 2,),
        )
      )
    window_object_list.append(
      gui_module.WindowObject(
        id = next_id + 11,
        place = (100, 700),
        window_object = tkinter.Label(root,
                                      text = "結果",
                                      font = ("Yu Gothic UI", "15"),
                                      width = 15,
                                      height = 2,),
        )
      )
    
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = next_id + 12 + i,
          place = (300 + 200*i, 100),
          window_object = tkinter.Label(root,
                                        text = self.selected_char_name_list[i],
                                        font = ("Yu Gothic UI", "15"),
                                        width = 15,
                                        height = 2,),
          )
        )
    forget_id_list.extend([next_id+12+i for i in self.no_char_list])

    display_id_list.extend(self.id_list)

    self.next_id += 16


  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self

    if self.action in range(1, 7):
      if self.action == 1:
        next_routine = _PlayModeCharacterSelectRoutine(root,
                                                       window_object_list,
                                                       display_id_list,
                                                       forget_id_list,
                                                       destroy_id_list,
                                                       char_name_list,
                                                       record,
                                                       self.next_id,)

      elif self.action in range(2, 7):
        # キャラクター名を番号と対応付ける
        # 選択されていないキャラは最後のキャラ+1にする（複数いた場合はさらに+2,+3して区別）
        char_name_index_list = []
        over_index_to_sort_none_data = 0
        for i in range(4):
          if i not in self.no_char_list:
            for index in range(len(char_name_list.data)):
              if char_name_list.data[index][0] == self.selected_char_name_list[i]:
                break
          else:
            index = len(char_name_list.data) + over_index_to_sort_none_data
            over_index_to_sort_none_data += 1
          char_name_index_list.append(index)

        sorted_char_name_index_list = sorted(char_name_index_list)
        
        index_dict = {}
        for i in range(4):
          index = sorted_char_name_index_list.index(char_name_index_list[i])
          index_dict[i] = index
          # 同じ名前or選択されていないキャラが複数いた場合区別するために既に使った名前をありえない値にセット
          sorted_char_name_index_list[index] = -1
        index_dict[4] = 4

        sorted_selected_char_name_list = [""] * 4
        for i in range(4):
          sorted_selected_char_name_list[index_dict.get(i)] = self.selected_char_name_list[i]

        def tofloat(num: str):
          try:
            ret = float(num)
          except ValueError:
            ret = 0
          return ret

        odds_list = [tofloat(self.entry_list[i].get()) for i in range(4)]
        sorted_odds_list = [0] * 4
        for i in range(4):
          sorted_odds_list[index_dict.get(i)] = odds_list[i]

        new_record = []
        new_record.extend(sorted_selected_char_name_list)
        new_record.append("1")
        for i in range(index_dict.get(self.action-2)):
          new_record.append("0")
        new_record.append("1")
        for i in range(4-index_dict.get(self.action-2)):
          new_record.append("0")
        new_record.extend(sorted_odds_list)

        record.data.append(new_record)
        record.write()

        next_routine = _PlayModeCharacterSelectRoutine(root,
                                                      window_object_list,
                                                      display_id_list,
                                                      forget_id_list,
                                                      destroy_id_list,
                                                      char_name_list,
                                                      record,
                                                      self.next_id)


      destroy_id_list.extend(self.id_list)
      del self.id_list, self.selected_char_name_list, self.entry_list
  
      self.action = 0

    return next_routine



class _PlayModeCalculateRoutine(Routine):
  """
  キャラの名前、勝率、オッズが入力された場合にリターン率を表示
  勝ったキャラもしくは引き分けを選択
  戦績作成後はキャラ選択画面に戻る
  """
  def __init__(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      selected_char_name_list: list[str],
      record_index: int,
      next_id: int = 1,
      ):
    
    super().__init__(next_id)

    self.id_list = list(range(next_id, next_id+26))
    self.selected_char_name_list = selected_char_name_list
    self.record_index = record_index
    self.no_char_list = [i
                         for i in range(4)
                         if self.selected_char_name_list[i] == ""]

    self.char_index_dict = {}
    for i in range(4):
      self.char_index_dict[i] = record.data[self.record_index].index(self.selected_char_name_list[i])
    self.char_index_dict[4] = 4

    window_object_list.append(
      gui_module.WindowObject(
        id = next_id,
        place = (50, 50),
        window_object = tkinter.Button(root,
                                       text = "◁",
                                       command = lambda : self.set_action(1),
                                       font = ('Yu Gothic UI', "15"),
                                       width = 4,
                                       height = 1,),
        )
      )
    
    for i in range(4):
      window_object_list.append(
      gui_module.WindowObject(
        id = next_id + 1 + i,
        place = (300 + 200*i, 690),
        window_object = tkinter.Button(root,
                                       text = self.selected_char_name_list[i],
                                       command = lambda _i=i : self.set_action(2+_i),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 15,
                                       height = 2,),
        )
      )
    forget_id_list.extend([next_id+1+i for i in self.no_char_list])
    window_object_list.append(
      gui_module.WindowObject(
        id = next_id + 5,
        place = (1100, 690),
        window_object = tkinter.Button(root,
                                       text = "DRAW",
                                       command = lambda _i=i : self.set_action(6),
                                       font = ("Yu Gothic UI", "15"),
                                       width = 15,
                                       height = 2,),
        )
      )
    
    self.entry_list = [
      tkinter.Entry(
        root,
        textvariable = tkinter.StringVar(root, record.data[record_index][10+self.char_index_dict.get(i)]),
        font = ("Yu Gothic UI", "20"),
        width = 10,
        bg = "gray97",
        )
      for i in range(4)
      ]
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = next_id + 6 + i,
          place = (300 + 200*i, 410),
          window_object = self.entry_list[i],
          )
        )
    forget_id_list.extend([next_id+6+i for i in self.no_char_list])
      
    self.textvariable_list_rtp = [tkinter.StringVar(root, "") for i in range(4)]
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = next_id + 10 + i,
          place = (300 + 200*i, 550),
          window_object = tkinter.Label(root,
                                        textvariable = self.textvariable_list_rtp[i],
                                        font = ("Yu Gothic UI", "15"),
                                        width = 15,
                                        height = 2,),
          )
        )
    forget_id_list.extend([next_id+10+i for i in self.no_char_list])
    
    text_list = ["勝率","オッズ","リターン率","結果"]
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = next_id + 14 + i,
          place = (100, 250 + 150*i),
          window_object = tkinter.Label(root,
                                        text = text_list[i],
                                        font = ("Yu Gothic UI", "15"),
                                        width = 15,
                                        height = 2,),
          )
        )
      
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = next_id + 18 + i,
          place = (300 + 200*i, 100),
          window_object = tkinter.Label(root,
                                        text = self.selected_char_name_list[i],
                                        font = ("Yu Gothic UI", "15"),
                                        width = 15,
                                        height = 2,),
          )
        )
    forget_id_list.extend([next_id+18+i for i in self.no_char_list])
      
    for i in range(4):
      window_object_list.append(
        gui_module.WindowObject(
          id = next_id + 22 + i,
          place = (300 + 200*i, 250),
          window_object = tkinter.Label(
            root,
            text = str( format(
              int(record.data[record_index][5+self.char_index_dict.get(i)])/int(record.data[record_index][4]) * 100,
                               '.2f') ) + "%",
            font = ("Yu Gothic UI", "15"),
            width = 15,
            height = 2,
            )
          )
        )
    forget_id_list.extend([next_id+22+i for i in self.no_char_list])

    display_id_list.extend(self.id_list)

    self.next_id += 26

  
  def execute(
      self,
      root: tkinter.Tk, 
      window_object_list: list[gui_module.WindowObject],
      display_id_list: list[int],
      forget_id_list: list[int],
      destroy_id_list: list[int],
      char_name_list: data_module.NameList,
      record: data_module.Record,
      ):
    next_routine = self

    def tofloat(str_num):
      ret = None
      try :
        ret = float(str_num)        
      except ValueError:
        ret = None
      return ret
      
    odds_list = [tofloat(self.entry_list[i].get()) for i in range(4)]
    
    def tortp(odds, player: int):
      # rtp = (win_ratio * odds) + (draw_ratio * 1)
      #     = win_ratio * odds + draw_ratio
      if (odds == None) or (player not in range(4)):
        return ""
      else:
        total_fight = int(record.data[self.record_index][4])
        win_ratio = int(record.data[self.record_index][5+self.char_index_dict.get(player)]) / total_fight
        draw_ratio = int(record.data[self.record_index][9]) / total_fight
        return str(format((win_ratio * odds + draw_ratio) * 100, ".2f")) + "%"

    for i in range(4):
      self.textvariable_list_rtp[i].set(tortp(odds_list[i], i))


    if self.action in range(1, 7):
      if self.action in range(2, 7):
        record.data[self.record_index][4] = str(int(record.data[self.record_index][4])+1)
        record.data[self.record_index][5+self.char_index_dict.get(self.action-2)] = str(int(
          record.data[self.record_index][5+self.char_index_dict.get(self.action-2)]
          )+1)
        
        def get_odds_num(index: int):
          try:
            ret = float(self.entry_list[index].get())
          except ValueError:
            ret = 0
          return ret

        for i in range(4):
          record.data[self.record_index][10+self.char_index_dict.get(i)] = get_odds_num(i)
        record.write()
      
      destroy_id_list.extend(self.id_list)
      del self.id_list, self.record_index, self.textvariable_list_rtp, self.char_index_dict, self.entry_list
      self.action = 0

      next_routine = _PlayModeCharacterSelectRoutine(root,
                                                     window_object_list,
                                                     display_id_list,
                                                     forget_id_list,
                                                     destroy_id_list,
                                                     char_name_list,
                                                     record,
                                                     self.next_id)

    return next_routine
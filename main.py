import data_module
import gui_module
import ui_module
import tkinter
import copy


CHAR_FILE_NAME = "char_name.csv"
RECORD_FILE_NAME = "record.csv"


# [0]から順に描画
# 背景は[0]に指定した方がいい
window_object_list = []
display_id_list = []
forget_id_list = []
destroy_id_list = []


def refresh(
    window_object_list: list[gui_module.WindowObject],
    display_id_list: list[int],
    forget_id_list: list[int],
    destroy_id_list: list[int],
    routine: ui_module.MainRoutine,
    root: tkinter.Tk,
    char_name_list: data_module.NameList,
    record: data_module.Record,
    ):

  routine.execute(root,
                  window_object_list,
                  display_id_list,
                  forget_id_list,
                  destroy_id_list,
                  char_name_list,
                  record)


  finished_id_list = []
  for each_id in display_id_list:
    for each_object in window_object_list:
      if each_id == each_object.id:
        if each_object.state in (gui_module.WindowObject.UNLOADED, gui_module.WindowObject.HIDDEN):
          each_object.display()
          each_object.state = gui_module.WindowObject.DISPLAYING
          finished_id_list.append(each_id)
  for each_id in finished_id_list:
    display_id_list.remove(each_id)

  finished_id_list = []
  for each_id in forget_id_list:
    for each_object in window_object_list:
      if each_id == each_object.id:
        if each_object.state == gui_module.WindowObject.DISPLAYING:
          each_object.forget()
          each_object.state = gui_module.WindowObject.HIDDEN
          finished_id_list.append(each_id)
  for each_id in finished_id_list:
    forget_id_list.remove(each_id)

  finished_id_list = []
  for each_id in destroy_id_list:
    for each_object in window_object_list:
      if each_id == each_object.id:
        each_object.destroy()
        finished_id_list.append(each_id)
  for each_id in finished_id_list:
    destroy_id_list.remove(each_id)



char_name_list = data_module.NameList(CHAR_FILE_NAME)
record = data_module.Record(RECORD_FILE_NAME)


window = gui_module.Window(window_size = (1300, 900),
                           title = "電波人間カジノ闘技場統計",
                           )

routine = ui_module.MainRoutine(
                  window.root,
                  window_object_list,
                  display_id_list,
                  forget_id_list,
                  destroy_id_list,
                  char_name_list,
                  record)

window.start_refresh_loop(
  lambda: refresh(window_object_list,
                  display_id_list,
                  forget_id_list,
                  destroy_id_list,
                  routine,
                  window.root,
                  char_name_list,
                  record),
  250
  )

window.canvas.mainloop()
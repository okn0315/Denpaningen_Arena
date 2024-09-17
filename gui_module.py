import tkinter
from typing import Callable


class Window:
  def __init__(
      self,
      window_size: tuple[int, int],
      title: str = "",
      bg: str = "white",
      ):
    
    self.root = tkinter.Tk()
    self.root.title(title)
    self.canvas = tkinter.Canvas(
      self.root,
      width = window_size[0],
      height = window_size[1],
      bg = bg
      )
    self.canvas.pack()
    self.root.bind("<Motion>", self._mouse_move)
    self.root.bind("<ButtonPress>", self._mouse_press)
    self.root.bind("<ButtonRelease>", self._mouse_release)

    self.mouse_x = 0
    self.mouse_y = 0
    self.mouse_c = False

    self._refreshing = False


  def start_refresh_loop(
      self,
      refresh_loop_function: Callable,
      loop_distance_ms: int,
      ):
    self._refreshing = True
    self._refresh_loop(refresh_loop_function, loop_distance_ms)

  def stop_refresh_loop(self):
    self.refreshing = False

  
  def _refresh_loop(
      self,
      refresh_loop_function: Callable,
      loop_distance_ms: int,
      ):
    
    if self._refreshing :
      refresh_loop_function()
      self.root.after(
        loop_distance_ms,
        lambda : self._refresh_loop(refresh_loop_function, loop_distance_ms)
        )

    
  def _mouse_move(self, event):
    self.mouse_x = event.x
    self.mouse_y = event.y

  def _mouse_press(self, event):
    self.mouse_c = True

  def _mouse_release(self, event):
    self.mouse_c = False


class WindowObject:
  UNLOADED    = 1
  DISPLAYING  = 2
  HIDDEN      = 3

  def __init__(
      self,
      id: int,
      place: tuple[int, int],
      window_object,
      ):
    self.id = id
    self.place = place
    self.window_object = window_object
    self.state = self.UNLOADED

  def display(self):
    self.window_object.place(x = self.place[0], y = self.place[1])
    self.state = self.DISPLAYING

  def forget(self):
    self.window_object.place_forget()
    self.state = self.HIDDEN

  def destroy(self):
    self.window_object.destroy()
    self.state = self.UNLOADED

#!/usr/bin/env python3
# snake.py

import gi, random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

field_size = 25
win_size = 800
speed = 100
init_parts = 3

class objects:
    x_coord = random.randint(0,  field_size-1)
    y_coord = random.randint(0, field_size-1)

    def set_x_y(self,x: int,y: int):
        self.x_coord = x
        self.y_coord = y

    def get_x(self) -> int:
        return self.x_coord
    
    def get_y(self) -> int:
        return self.y_coord
    
    def rand_coord(self):
        self.x_coord = random.randint(0,  field_size-1)
        self.y_coord = random.randint(0,  field_size-1)

class snake_obj(objects):
    pass

class fruit(objects):
    pass

"""adds a snake part behind the snake"""
def add_snake():
    snake_part = snake_obj()
    snake_part.set_x_y(snake[len(snake)-1].get_x(), snake[len(snake)-1].get_y())
    snake.append(snake_part)

"""moves the Snake in Directions:
        0 for up
        1 for down
        2 for left
        3 for right
        """
def move(direction: int): 
    if direction == 0:
        #up
        snake[len(snake)-1].set_x_y(snake[0].get_x(),snake[0].get_y()-1)
    elif direction == 1:
        #down
        snake[len(snake)-1].set_x_y(snake[0].get_x(),snake[0].get_y()+1)
    elif direction == 2:
        #left
        snake[len(snake)-1].set_x_y(snake[0].get_x()-1,snake[0].get_y())
    elif direction == 3:
        #right
        snake[len(snake)-1].set_x_y(snake[0].get_x()+1,snake[0].get_y())
    
    #checks if the snake reached one edge of the field
    if snake[len(snake)-1].get_x() >=   field_size:
        snake[len(snake)-1].set_x_y(0,snake[len(snake)-1].get_y())
    elif snake[len(snake)-1].get_x() < 0:
        snake[len(snake)-1].set_x_y(  field_size, snake[len(snake)-1].get_y())
    elif snake[len(snake)-1].get_y() >=   field_size:
        snake[len(snake)-1].set_x_y(snake[len(snake)-1].get_x(),0)
    elif snake[len(snake)-1].get_y() < 0:
        snake[len(snake)-1].set_x_y(snake[len(snake)-1].get_x(),   field_size)

    snake[len(snake)-1]
    snake.insert(0, snake[len(snake)-1])
    snake.pop()

"""checks if the head of the snake is on a fruit then adds a part to the snake. After that checks if the fruit did not respawn on the snake"""
def eat():
    if snake[0].get_x() == fruit.get_x() and snake[0].get_y() == fruit.get_y():
        add_snake()
        for i in snake:
            while i.get_x() == fruit.get_x() and i.get_y() == fruit.get_y():
                fruit.rand_coord()

"""ckecks if the the snakes head is on the snake"""
def game_over() -> bool:
    for i in snake[1:]:
        if i.get_x() == snake[0].get_x() and i.get_y() == snake[0].get_y() and len(snake) > init_parts:
            return True
    return False

class win(Gtk.Window):

    def __init__(self):
        super(win,self).__init__()

        self.init_ui()
        self.direc = random.randint(0,3)
        self.timeout_on = True
        self.allow_change = True
    
    # initialize the Gui
    def init_ui(self):

        self.field = Gtk.DrawingArea()
        self.field.connect("draw", self.on_draw)
        self.field.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)  
        self.field.queue_draw()
        self.add(self.field)

        self.connect("key-press-event", self.on_key_pressed)

        self.resize(win_size,win_size)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.win_size = self.get_size()
        self.width =  self.win_size[1]/ field_size

        self.init_timeout()
        
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
    
    #draws the field
    def on_draw(self, wid, cr):
        
        cr.set_line_width(1)

        for n in snake:
            self.draw_rect(wid,cr,n.get_x()*self.width,n.get_y()*self.width)
        
        cr.set_source_rgb(1, 0, 0)
        self.draw_rect(wid,cr,fruit.get_x() * self.width, fruit.get_y() * self.width)
        cr.set_source_rgb(0, 0, 0)
    
    # a function to draw a rect with the upper left corner as a starting point
    def draw_rect(self, wid, cr, x, y):

        cr.move_to(x,y)
        cr.line_to(x,y + self.width)
        cr.line_to(x + self.width,y + self.width)
        cr.line_to(x + self.width,y)
        cr.line_to(x,y)
        cr.fill()

        cr.stroke()

    # the timeout funktion that repeats every few seconds
    def on_timeout(self, *args, **kwargs) -> bool:
        if game_over():
            self.timeout_on = False
            return False
                    
        move(self.direc)
        self.allow_change = True
        self.field.queue_draw()
        eat()
        return True
    
    # adds the timeout to the Gtk.Window
    def init_timeout(self):
        self.timeout_id = GLib.timeout_add(speed,self.on_timeout, None)
        self.timeout_on = True
    
    def on_key_pressed(self, widget,event):

        if (event.keyval == Gdk.KEY_w or event.keyval == Gdk.KEY_Up) and self.direc != 1 and self.allow_change:
            self.direc = 0
            self.allow_change = False
        elif (event.keyval == Gdk.KEY_s or event.keyval == Gdk.KEY_Down) and self.direc != 0 and self.allow_change:
            self.direc = 1
            self.allow_change = False
        elif (event.keyval == Gdk.KEY_a or event.keyval == Gdk.KEY_Left) and self.direc != 3 and self.allow_change:
            self.direc = 2
            self.allow_change = False
        elif (event.keyval == Gdk.KEY_d or event.keyval == Gdk.KEY_Right) and self.direc != 2 and self.allow_change:
            self.direc = 3
            self.allow_change = False
        elif event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
        elif event.keyval == Gdk.KEY_r:
            self.restart()

    #restarts the game
    def restart(self):
        snake.clear()
        init_snake()
        fruit.rand_coord()
        if self.timeout_on:
            GLib.source_remove(self.timeout_id)
        self.init_timeout()
	#self.direc = random.randint(0,3)

"""initilize the array of snake pats"""
def init_snake():
    snake_part = snake_obj()
    snake_part.rand_coord()
    snake.append(snake_part)
    while len(snake) < init_parts:
        add_snake()

if __name__ == "__main__":
    snake = [] #init a snake as an array
    fruit = fruit()
    init_snake()
    app = win()
    Gtk.main()

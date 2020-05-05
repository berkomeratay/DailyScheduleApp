# -*- coding: utf-8 -*-
"""
@author: berkomeratay
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import pandas as pd
import os


class MyGrid(GridLayout):
    def __init__(self,**kwargs):
        super(MyGrid,self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text = "Event: "))
        self.writer = TextInput(multiline = True,text = " ")
        self.add_widget(self.writer)
        
        self.add_widget(Label(text = "Time: "))
        self.book = TextInput(multiline = True,text = " ")
        self.add_widget(self.book)
        
        self.addtolist = Button(text="Add to List")
        self.addtolist.bind(on_press = self.pressed)
        self.add_widget(self.addtolist)        
        
        self.showlist = Button(text = "Show My Schedule")
        self.showlist.bind(on_press = self.show_func)
        self.add_widget(self.showlist)
        
        self.clearlist = Button(text = "Clear My Schedule")
        self.clearlist.bind(on_press = self.clear_func)
        self.add_widget(self.clearlist)
        
        self.exit_button = Button(text = "Close the App")
        self.exit_button.bind(on_press = self.exit_func)
        self.add_widget(self.exit_button)
        
    def pressed(self,instance):
        global book_name, writer_name
        book_name = self.book.text
        writer_name = self.writer.text
        print("Kitap Yazarı: {}\nKitap Adı: {}".format(writer_name,book_name))
        try:
            bookData = pd.read_csv("bookDatabase.csv")
        except Exception:
            bookData = pd.DataFrame(columns = ["Writer","Book"])
        bookData.loc[len(bookData),"Writer"] = writer_name
        bookData.loc[len(bookData)-1,"Book"] = book_name
        self.writer.text = ""
        self.book.text = ""
        bookData.to_csv("bookDatabase.csv",index = False)
        print(LibApp.screen_manager.screens)

    def show_func(self,instance):

        LibApp.create_lib_page()
        LibApp.screen_manager.transition.direction = "left"
        LibApp.screen_manager.current = "LG"
    
    def clear_func(self,instance):
        try:
            os.remove("bookDatabase.csv")
        except Exception:
            pass
        LibApp.create_lib_page()
        LibApp.screen_manager.transition.direction = "left"
        LibApp.screen_manager.current = "LG"
    def exit_func(self,instance):

        App.get_running_app().stop()
        Window.close()
        
        
class LibraryGrid(GridLayout):
    def __init__(self,**kwargs):
        super(LibraryGrid,self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text = "Event"))
        self.add_widget(Label(text = "Time"))
        try:
            self.bookData_2 = pd.read_csv("bookDatabase.csv").dropna().reset_index()
            
            for i in list(range(0,len(self.bookData_2))):
                self.add_widget(Label(text = str(self.bookData_2.loc[i,"Writer"]),font_size = 13))
                self.add_widget(Label(text = str(self.bookData_2.loc[i,"Book"]),font_size = 13))
        except Exception:
            pass
        self.backButton = Button(text = "Add New Event")
        self.backButton.bind(on_press = self.back_func)
        self.add_widget(self.backButton)
        
        self.exit_button = Button(text = "Close the App")
        self.exit_button.bind(on_press = self.exit_func)
        self.add_widget(self.exit_button)
    def back_func(self,instance):
      
        LibApp.screen_manager.switch_to(LibApp.screen_manager.screens[0],direction='right')
        
    def exit_func(self,instance):
        App.get_running_app().stop()
        Window.close()

class DailyScheduleAppApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.mygrid = MyGrid()
        screen = Screen(name="MG")
        screen.add_widget(self.mygrid)
        self.screen_manager.add_widget(screen)
        return self.screen_manager
        
        
    def create_lib_page(self):
        self.libgrid = LibraryGrid()
        screen_2 = Screen(name="LG")
        screen_2.add_widget(self.libgrid)
        self.screen_manager.add_widget(screen_2)
        
        
if __name__ == "__main__":
    LibApp = DailyScheduleAppApp()
    LibApp.run()







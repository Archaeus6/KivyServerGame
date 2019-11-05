import socket
import os
import random
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_string("""

<main_screen>:
    BoxLayout:
        orientation: "vertical"
        Label:
            id: label1
            text: "hi"
        Button:
            text: "Server"
            on_press: root.activate_network()
        Button:
            text: "Cards"
            on_press: app.root.current = "cards"
            
<player_select>:
    size_hint: .5,.5
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "Player Number"
        TextInput:
            id: player
        Label:
        Button:
            text: "Save"
            on_press: root.save_player()
            
<card_screen>:
    BoxLayout:
        orientation: 'vertical'
        Label: 
            id: card_stats
            text: 'test'
        BoxLayout:
            id: card_layout

""")

class card_button(ButtonBehavior, Image):
    pass

class screen_manager(ScreenManager):
    pass

class main_screen(Screen):
    
    def activate_network(self):
        global player
        #n = Network()
        n.send(player)
        self.ids.label1.text = n.response
        
class card_screen(Screen):
    def on_enter(self):
        self.card_list = []
        for card in os.listdir('/storage/emulated/0/pythonscripts/Server/cards'):
            self.card_list.append(card)
        for card_amount in range(0,8):
            rand_card = random.randint(0,13)
            self.bttn = card_button(id= self.card_list[rand_card],source='/storage/emulated/0/pythonscripts/Server/cards/'+self.card_list[rand_card])
            self.ids.card_layout.add_widget(self.bttn)
            self.bttn.bind(on_press=self.card_label)
          
    def card_label(self,widget_id):
        self.ids.card_stats.text = widget_id.id
        for child in self.ids.card_layout.children[:]:
            if child.id == widget_id.id:
                n.send(widget_id.id)
                self.ids.card_layout.remove_widget(child)
        new_card = random.randint(0,len(self.card_list))
        self.bttn_new = card_button(id= self.card_list[new_card],source='/storage/emulated/0/pythonscripts/Server/cards/'+self.card_list[new_card])
        self.ids.card_layout.add_widget(self.bttn_new)
        self.bttn_new.bind(on_press=self.card_label)
          

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.16"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)
        self.response = ""

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            self.response = self.client.recv(2048).decode()
            #return response
        except socket.error as e:
            print(e)
  
class player_select(Popup):
    def save_player(self):
        global player
        player = self.ids.player.text
        self.dismiss()
        

sm = screen_manager()
sm.add_widget(main_screen(name='main'))
sm.add_widget(card_screen(name='cards'))
player = ""
n = Network()

class TestApp(App):
    def build(self):
        return sm

    def on_start(self):
        z = player_select()
        z.open()

if __name__ == '__main__':
    TestApp().run()

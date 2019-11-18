import socket
import pickle
import random
from _thread import *
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
import threading
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import mainthread
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.core.window import Window


Builder.load_string("""



<main_screen>:
    canvas.before:
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'distopian.jpeg'
    BoxLayout:
        padding: 20
        spacing: 20
        id: main_screen_layout
        orientation: 'vertical'
        BoxLayout:
            padding: 20
            spacing: 20
            id: AI_layout
            BoxLayout:
                canvas.before:
                    Rectangle:                       
                        size: self.size
                        pos: self.pos
                        source: 'Radar.png'
                id: AI_radar
                size_hint: .5,1
            ProgressBar:
                id: AI_progress
                max: 100
                value: 0
        BoxLayout:
            BoxLayout:
                orientation: 'vertical'
                Label:
                    id: server_lbl_player_1
                    text: "player 1"
                BoxLayout:
                    size_hint: 1,.3
                    id: player_1_icons
            BoxLayout:
                orientation: 'vertical'
                Label:
                    id: server_lbl_player_2
                    text: "player 2"
                BoxLayout:
                    size_hint: 1,.3
                    id: player_2_icons
        
        Button:
            id: start_bttn
            size_hint: 1,.2
            background_color: 1,9,5,.3
            text: 'Start'
            on_press: root.server_thread()

<fight_screen>:
    canvas.before:
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'card_board.jpg'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Creature Screen'
        BoxLayout:
            id: creature_layout
        

""")

class card_image(Image, ButtonBehavior):
    pass

class main_screen(Screen):
    def on_touch_move(self,touch):
        print(touch.x, touch.y, 'touch')
    
    @mainthread
    def load_radar(self):
        
        self.radar = Image(source = 'radar_centre_small.png')       
        self.ids.AI_radar.add_widget(self.radar)
        with self.canvas.after:
            self.radar_dot = Image(pos=(100,500),source = 'radar_dot_small.png')
        
        
            
    @mainthread
    def creature_radar(self):
        global say
        randomx = random.randint(50,300)
        randomy = random.randint(400,900)
        self.radar_dot.pos = (randomx,randomy)
        #print(self.radar_dot.pos)
        x_difference = self.radar_dot.pos[0] - self.radar.pos[0]
        y_difference = self.radar_dot.pos[1] - self.radar.pos[1]
        #print(x_difference, y_difference)
        if x_difference <= 120 and y_difference <=130:
            
            self.ids.server_lbl_player_1.text = "smash"
            say = "fight"
        else:
            self.ids.server_lbl_player_1.text = "miss"
            say = 'no fight'
        
        
    
    @mainthread
    def load_card(self,card):
        if card == "1 factory":
            image_path = 'production.png'
            card_img = card_image(source=image_path)
            self.ids.player_1_icons.add_widget(card_img)
        if card == "1 barracks":
            image_path = 'barracks.png'
            card_img = card_image(source=image_path)
            self.ids.player_1_icons.add_widget(card_img)
        if card == "1 culture":
            image_path = 'culture.png'
            card_img = card_image(source=image_path)
            self.ids.player_1_icons.add_widget(card_img)

    def server_thread(self):
        self.load_radar()
        threading.Thread(target=self.server).start()
        self.ids.main_screen_layout.remove_widget(self.ids.start_bttn)

    def server(self):
        server = "192.168.0.16"
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(2)
        print("Waiting for a connection, Server Started")
        #self.ids.server_lbl.text = "Waiting for a connection, Server Started"


        def threaded_client(conn):
            global say
            pickle_connected = pickle.dumps("Connected")
            conn.send(pickle_connected)
            reply = ""
            say = "hi"
            while True:
                try:
                    data = conn.recv(2048)
                    reply = pickle.loads(data)
                    

                    if not data:
                        print("Disconnected")
                        break

                    elif reply == "1 end turn":
                        self.ids.AI_progress.value += 10
                        self.creature_radar()
                        print(say)

                    elif reply == "1 factory" or reply == "1 barracks" or reply == "1 culture":
                        self.load_card(reply)

                    
                    else:
                        print("Received: ", reply)
                        self.ids.server_lbl_player_2.text = str(reply)
                        
                                                

                    conn.sendall(pickle.dumps(say))
                except:
                    break

            print("Lost connection")
            conn.close()


        while True:
            conn, addr = s.accept()
            print("Connected to:", addr)
            start_new_thread(threaded_client, (conn,))

class fight_screen(Screen):
    pass
            

class screen_manager(ScreenManager):
    pass

say = ""
sm = screen_manager()
sm.add_widget(main_screen(name='main'))
sm.add_widget(fight_screen(name='fight'))


class TestApp(App):
    def build(self):
        
        return sm

#Window.fullscreen = True

if __name__ == '__main__':
    TestApp().run()

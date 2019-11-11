import socket
import pickle
from _thread import *
import sys
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
from kivy.clock import Clock
import threading
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import mainthread
from kivy.uix.progressbar import ProgressBar


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
            Label:
                id: server_lbl
                text: "AI"
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
        BoxLayout:
            id: player2_cards
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
    @mainthread
    def load_card(self,card):
        if card == "1 factory":
            image_path = 'production.png'
            card_img = card_image(source=image_path)
            self.ids.player_1_icons.add_widget(card_img)

    def server_thread(self):
        threading.Thread(target=self.server).start()
        self.ids.main_screen_layout.remove_widget(self.ids.start_bttn)

    def server(self):
        server = "192.168.0.19"
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(2)
        print("Waiting for a connection, Server Started")
        self.ids.server_lbl.text = "Waiting for a connection, Server Started"


        def threaded_client(conn):
            pickle_connected = pickle.dumps("Connected")
            conn.send(pickle_connected)
            reply = ""
            say = pickle.dumps("hi")
            while True:
                try:
                    data = conn.recv(2048)
                    reply = pickle.loads(data)
                    

                    if not data:
                        print("Disconnected")
                        break

                    elif reply == "1 end turn":
                        self.ids.AI_progress.value += 10

                    elif reply == "1 factory":
                        self.load_card(reply)
                    
                    else:
                        print("Received: ", reply)
                        self.ids.server_lbl_player_2.text = str(reply)
                        
                                                

                    conn.sendall(say)
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


sm = screen_manager()
sm.add_widget(main_screen(name='main'))
sm.add_widget(fight_screen(name='fight'))


class TestApp(App):
    def build(self):
        
        return sm


if __name__ == '__main__':
    TestApp().run()

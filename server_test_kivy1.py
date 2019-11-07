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


Builder.load_string("""



<main_screen>:
    canvas.before:
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'card_board.jpg'
    BoxLayout:
        id: main_screen_layout
        orientation: 'vertical'
        Label:
            id: server_lbl
            text: "player 1"
        Label:
            id: server_lbl_player_2
            text: "player 2"
        BoxLayout:
            id: player2_cards
        Button:
            id: start_bttn
            size_hint: 1,.2
            background_color: 1,9,5,.3
            text: 'Start'
            on_press: root.server_thread()

<creature_screen>:
    canvas.before:
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'card_board.jpg'
    BoxLayout:
        Label:

""")

class card_image(Image, ButtonBehavior):
    pass

class main_screen(Screen):
    @mainthread
    def load_card(self,card):
        image_path = '/home/archaeus/my_files/python_files/KivyServerGame/cards/'+card
        card_img = card_image(source=image_path)
        self.ids.player2_cards.add_widget(card_img)

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
                    else:
                        print("Received: ", reply)
                        self.ids.server_lbl_player_2.text = str(reply)
                        if reply == "creature_screen":
                            sm.current = "creature"
                        else:
                            self.load_card(reply[0])
                        #if reply == "2":
                            #self.ids.server_lbl_player_2.text = reply
                            #say = "I say you dumb"
                            #print("Sending : ", say)
                        #if reply == "1":
                            #self.ids.server_lbl.text = reply
                            #say = "Too bad"
                            #print("Sending : ", say)
                        #if "creature" in reply:
                            #self.ids.server_lbl.text = reply

                    conn.sendall(say)
                except:
                    break

            print("Lost connection")
            conn.close()


        while True:
            conn, addr = s.accept()
            print("Connected to:", addr)
            start_new_thread(threaded_client, (conn,))

class creature_screen(Screen):
    pass

class screen_manager(ScreenManager):
    pass


sm = screen_manager()
sm.add_widget(main_screen(name='main'))
sm.add_widget(creature_screen(name='creature'))


class TestApp(App):
    def build(self):
        
        return sm


if __name__ == '__main__':
    TestApp().run()

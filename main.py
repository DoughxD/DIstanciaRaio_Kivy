import kivy
from kivy import Config
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

kivy.require('1.7.0')

__version__ = "0.1.0"

from kivy.app import App
from kivy.graphics.context import Clock

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')
Config.write()



class TextoClick(ButtonBehavior, Label):
    cor = ListProperty([0.1, 0.5, 0.7, 0])
    cor2 = ListProperty([0.1, 0.1, 0.1, 0])


class Botao(ButtonBehavior, Label):
    cor = ListProperty([0.1, 0.5, 0.7, 1])
    cor2 = ListProperty([0.1, 0.1, 0.1, 1])

    def __init__(self, **kwards):
        super(Botao, self).__init__(**kwards)
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def on_press(self, *args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_release(self, *args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_cor(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)

            Ellipse(size=(self.height, self.height), pos=self.pos)

            Ellipse(size=(self.height, self.height), pos=(self.x + self.width - self.height, self.y))

            Rectangle(size=(self.width - self.height, self.height), pos=(self.x + self.height / 2.0, self.y))


class DistanciaRaio(App):
    def build(self, *args):
        self.icon = 'icon.png'

        self.permissao = False
        self.cont = 0
        self.gerenciador = ScreenManager()
        self.tela = Screen(name='tela')
        self.tela2 = Screen(name='tela2')
        self.help = Screen(name='help')


        #adiciona ao ScreenManager as telas
        self.gerenciador.add_widget(self.tela)
        self.gerenciador.add_widget(self.tela2)
        self.gerenciador.add_widget(self.help)

        #Cria e adiciona o ActionBar
        self.actionbox = BoxLayout(orientation='vertical')
        self.actionbar = ActionBar()
        self.actionbox.add_widget(self.actionbar)
        self.tela.add_widget(self.actionbox)

        #Cria o resto da BoxLayout Principal
        self.box = BoxLayout(orientation='vertical', padding='100sp', spacing='60sp')
        self.texto = Label(text='0', font_size='60')
        self.botao = Botao(text='iniciar', font_size='60')
        self.box.add_widget(self.texto)
        self.box.add_widget(self.botao)
        self.tela.add_widget(self.box)



        self.botao.bind(on_release=self.inicia)

        return self.gerenciador

    def inicia(self, *args):
        self.permissao = True
        Clock.schedule_interval(self.timer, 1)
        self.box.remove_widget(self.botao)
        self.botao2 = Botao(text='parar', font_size='60', id='botao2')
        self.box.add_widget(self.botao2)
        self.botao2.bind(on_release=self.parar)

    def timer(self, *args):
        if self.permissao == True:
            self.cont += 1
            self.texto.text = str(self.cont)
            print('contando')
        else:
            Clock.unschedule(self.timer)

    def parar(self, *args):
        self.permissao = False
        print('teste')
        self.box2 = BoxLayout(orientation='vertical')
        self.texto2 = TextoClick(text='O raio caiu a {:.2f}m'.format(self.cont * 340.29), font_size= '60sp')
        self.box2.add_widget(self.texto2)
        self.tela2.add_widget(self.box2)
        self.gerenciador.current = 'tela2'
        self.texto2.bind(on_release=self.voltar)

    def voltar(self, *args):
        print('funfando')
        self.cont = 0
        self.texto.text = '0'
        self.box2.remove_widget(self.texto2)
        self.box.remove_widget(self.botao2)
        self.box.add_widget(self.botao)
        self.gerenciador.current = 'tela'

DistanciaRaio().run()
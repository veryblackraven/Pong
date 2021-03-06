from pandac.PandaModules import *
from Jugador import *
from Pelota import *
from IA import *
from ManejadorDeColisiones import *
from marcador import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import ConfigVariableString





class MyApp(ShowBase):
    def __init__(self):
            ShowBase.__init__(self)

            #cambiando variables de configuracion
            ConfigVariableString('clock-mode','limited')
            ConfigVariableDouble('clock-frame-rate','60')
            ConfigVariableString('audio-library-name','p3openal_audio')

            # Disable the camera trackball controls.
            self.disableMouse()

            #iniciamos la partida
            self.inicia_partida()

            #self.taskMgr.add(player1c,'control del jugador 1', extraArgs=[self], appendTask=True)
            #self.taskMgr.add(player2c,'control del jugador 2', extraArgs=[self], appendTask=True)



    def init_variables(self):
        #inicializa variables
        self.p1 = 1
        self.p2 = 1
        self.px = 1
        self.py = 0
        self.pz = 20
        self.i=5
        self.a=0
        self.abajo1 = False
        self.arriba1 = False
        self.abajo2 = False
        self.arriba2 = False
        #variable para determinar el tipo de IA que se va a aplicar
        self.versusIA=True
        #variable para los puntos del jugador
        self.puntos1=0
        #variable para los puntos de la IA
        self.puntos2=0
        

    def loadmodels(self):
        #aqui se deben cargar los modelos para el juego
        #carga los jugadores
        
        self.player1 = Jugador(self)

        self.player2 = Jugador(self,False)

        #coloca al jugador 1
        self.player1.modelo.setR(90)
        self.player1.modelo.setPos(-130,0,20)

        #coloca al jugador 2
        self.player2.modelo.setR(90)
        self.player2.modelo.setPos(170,0,20)

        #iniciar marcador
        self.marcador=Marcador(self)

        #inicia y coloca pelota
        self.pelota = Pelota(self)
        
        #inicia el manejador de los eventos de las colisiones
        self.manejador = ManejadorDeColisiones(self)

        #cargamos el fondo
        self.fondo= loader.loadModel("Modelos/fondo");
        self.fondo.reparentTo(render)

        #colocamos el fondo
        self.fondo.setPos(20,300,-15)
        self.t=7
        self.fondo.setScale(self.t,self.t,self.t)
        self.fondo.setHpr(90, 0, -90)

        #cargamos la textura del fondo
        self.tex = loader.loadTexture('Img/fondo.jpg')
        self.fondo.setTexture(self.tex)
        #si activamos esta parte no se veran marcas grises a los lados. Aun espero que me digais como queda mejor
        """
        
        self.fondo2= loader.loadModel("Modelos/fondo");
        self.fondo2.reparentTo(render)
        self.fondo2.setPos(20,320,-15)
        self.t2=200
        self.fondo2.setScale(self.t2,self.t2,self.t2)
        self.fondo2.setHpr(90, 0, -90)
        self.tex = loader.loadTexture('Img/fondo.jpg')

        self.fondo2.setTexture(self.tex)
        """

        #coloca la camara
        self.camera.setPos(20,-500,-20)

        #carga y coloca la luz 1
        dlight = DirectionalLight('my dlight')
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(20, 20, 0)
        render.setLight(dlnp)

        #carga y coloca la luz 2
        dlight2 = DirectionalLight('my dlight2')
        dlight2.setColor(Vec4(0.2, 0.2, 0.2, 0.1))
        dlnp2 = render.attachNewNode(dlight2)
        dlnp2.setHpr(180, -20, 0)
        render.setLight(dlnp2)

        #cargando sonidos
        self.sonidofondo = base.loader.loadSfx("sound/fondo.mp3")
        self.gol=base.loader.loadSfx("sound/gol.mp3")
        self.golpe = base.loader.loadSfx("sound/golpe.mp3")
        self.sonidovictoria=base.loader.loadSfx("sound/victoria.mp3")
        self.sonidoderrota=base.loader.loadSfx("sound/derrota.mp3")
        #ponemos en un bucle el sonido de fondo
        self.sonidofondo.setLoop(True)
        #empezamos a reproducir el sonido de fondo
        self.sonidofondo.play()


    def pelotac(self,task):
            self.pelota.modelo.setPos(self.px,self.py,self.pz)
            self.px = self.px + 1
            if self.px > 100:
                    self.px = -100

            #self.pelota.setR(self.a)
            #self.a+=50
            #if self.a>360:
            #    self.a=0
            #self.i+=0.1
            return task.cont



    def arriba1true(self):
            self.player1.arriba= True
    def arriba1false(self):
            self.player1.arriba= False
    def abajo1true(self):
            self.player1.abajo= True
    def abajo1false(self):
            self.player1.abajo= False
    def arriba2true(self):
            self.player2.arriba= True
    def arriba2false(self):
            self.player2.arriba= False
    def abajo2true(self):
            self.player2.abajo= True
    def abajo2false(self):
            self.player2.abajo= False

    def puntojugador2(self):
        self.puntos2+=1
        self.pelota.start()

    def puntojugador1(self):
        self.puntos1+=1
        self.pelota.start()

    def inicia_partida(self):

            # inicializa variables
            self.init_variables()
            #cargar los modelos graficos y de sonido
            self.loadmodels()
            #introducimos las teclas que debe escuchar por teclado para el jugador 1
            self.accept('w',self.arriba1true)
            self.accept('w-up',self.arriba1false)
            self.accept('s',self.abajo1true)
            self.accept('s-up',self.abajo1false)
            #inicia la IA o habilita el control del segundo jugador segun la variable "versusIA"
            if(self.versusIA==False):
                #introducimos las teclas que debe escuchar por teclado para el jugador 2
                self.accept('o',self.arriba2true)
                self.accept('o-up',self.arriba2false)
                self.accept('l',self.abajo2true)
                self.accept('l-up',self.abajo2false)
                
            else:
                #si vamos a jugar con IA elegimos con la que queremos jugar
                self.Ia=IA2(self)
                #metemos el metodo update de la IA al task Manager
                self.taskMgr.add(self.Ia.update,'IA', extraArgs=[self], appendTask=True)
 
app = MyApp()
app.run()
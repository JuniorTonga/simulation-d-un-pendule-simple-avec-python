import tkinter as tk
import random as rd
import numpy as np

couleur = ['black', 'white', 'red', 'orange', 'yellow', 'green',
          'turquoise', 'blue', 'purple', 'magenta']


# Classe principale qui herite de la classe Tk.
class AppliPendule(tk.Tk):
    """Classe principale de l'application (contient la fenetre Tk).
    """

    def __init__(self):
        # Appel du constructeur de la classe génitrice.
        # L'instance de la fenetre principale se retrouve dans le self.donc on pourra le self dans la suite
        tk.Tk.__init__(self)
        # etat du  mouvement (0 immobile, > 0 en mouvement).
        self.is_moving = 0
        # Grandeurs physiques initiales
        self.t = 0  # temps (s)
        self.dt = 0.05  # intervalle de temps très petit (s)
        self.g = 9.8  # accélération gravitationnelle (m/s^2)
        self.theta = 0.25* np.pi  # angle initial
        self.dtheta = 0.0  # vitesse angulaire ,le pend.ule est au repos
        self.L = 1  # longueur de la tige  (m)
        self.x = np.sin(self.theta) * self.L
        self.y = -np.cos(self.theta) * self.L
        # Conversion x, y en coord dans le canevas
        self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)
        # Creation du canevas dans la fenetre.
        self.canv = tk.Canvas(self, bg='gray', height=400, width=400)
        # creation du pivot.
        self.canv.create_oval(190, 190, 210, 210, width=1, fill="blue")
        # creation de la balle.
        self.size = 30  # Taille de la balle ds le repère du canvas.
        self.balle = self.canv.create_oval(self.x_c - (self.size / 2),
                                             self.y_c - (self.size / 2),
                                             self.x_c + (self.size / 2),
                                             self.y_c + (self.size / 2),
                                             width=1, fill="blue")
        # Creation de la tige.
        self.tige = self.canv.create_line(200, 200, self.x_c,
                                          self.y_c, fill="blue")
        # Creation d'une ligne
        self.canv.create_line(0, 200, 400, 200, dash=(3, 3))
        self.canv.create_line(200, 0, 200, 400, dash=(3, 3))
        # Creation des boutons.
        btn1 = tk.Button(self, text="Quitter", command=self.quit)
        btn2 = tk.Button(self, text="Demarrer", command=self.start)
        btn3 = tk.Button(self, text="Arreter", command=self.stop)
        # Creation de la règlette
        self.theta_scale = tk.Scale(self, from_=-np.pi, to=np.pi,
                                    resolution=0.001,
                                    command=self.update_theta_scale)
        self.theta_scale.set(self.theta)
        scale_description = tk.Label(self, text="valeur\ninitiale\nde theta",
                                     fg="blue")
        signature=tk.Label(self,text="Made with tkinter ",fg="blue")
        # Creationtion d'un Label pour voir les caracteristiques de la Balle.
        # On utilise une Stringvar (permet de mettre à jour l'affichage).
        self.stringvar_pos_display = tk.StringVar()
        display_theta = tk.Label(self, textvariable=self.stringvar_pos_display,
                                 fg="blue", font=("Courier New", 12))
        # Placement des widgets dans la fenetre Tk.
        self.canv.pack(side=tk.LEFT)
        btn1.pack(side=tk.BOTTOM)  # boutton quitter
        btn2.pack()
        btn3.pack()
        display_theta.pack()
        signature.pack(side=tk.BOTTOM)
        # Puis la règle et sa description.
        scale_description.pack(side=tk.LEFT)
        self.theta_scale.pack(side=tk.RIGHT)
        #mise à jour
        self.stringvar_pos_display.set(self.get_pos_displ())

    def get_pos_displ(self):
        """Retourne une chaine avec la position et la vitesse (angulaire) de la balle.
        """
        return "{:>5s} {:>10s}\n{:>5s} {:>10s}\n{:>5.1f} {:>10.1f}".format(
            "theta", "dtheta", "(rad)", "(rad/dt)", self.theta, self.dtheta)

    def map_realcoor2canvas(self, x, y):
        # L = 1 m --> 100 pixel dans le canvas.
        conv_factor = 100
        xprime = x * conv_factor + 200
        yprime = -y * conv_factor + 200
        return xprime, yprime

    def update_theta_scale(self, value):
        """mise à jour dela reglette balle qd la reglette est touchée
        """
        # fin du mouvement du pendule.
        self.stop()
        self.dtheta = 0.0
        # mise à jour du pendule avec la nouvelle valeur.
        self.theta = float(value)
        self.x = np.sin(self.theta) * self.L
        self.y = -np.cos(self.theta) * self.L
        # Conversion ds le repere du canvas.
        self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)
        # mise à jour des coordonées (balle + tige).
        self.canv.coords(self.balle,
                         self.x_c - (self.size / 2),
                         self.y_c - (self.size / 2),
                         self.x_c + (self.size / 2),
                         self.y_c + (self.size / 2))
        self.canv.coords(self.tige, 200, 200, self.x_c, self.y_c)
        # mise à jour de la zone de texte.
        self.stringvar_pos_display.set(self.get_pos_displ())
        # mise à  0 le temps.
        self.t = 0

    def move(self):
        """deplace la balle ,mets à jour les coordonnées et s'auto-rappelle après 20 ms.
        """
        # Calcul du nouveau theta avec un la methode Euler semi-implicite..
        self.d2theta = -(self.g / self.L) * np.sin(self.theta)
        self.dtheta += self.d2theta * self.dt
        self.theta += self.dtheta * self.dt
        # Conversion theta -> x & y.
        self.x = np.sin(self.theta) * self.L
        self.y = -np.cos(self.theta) * self.L
        # Conversion ds le repÃ¨re du canvas.
        self.x_c, self.y_c = self.map_realcoor2canvas(self.x, self.y)
        # On met à jour les coordonnées (balle + tige).
        self.canv.coords(self.balle,
                         self.x_c - (self.size / 2),
                         self.y_c - (self.size / 2),
                         self.x_c + (self.size / 2),
                         self.y_c + (self.size / 2))
        self.canv.coords(self.tige, 200, 200, self.x_c, self.y_c)
        # presence de la trace au passage de la balle
        self.canv.create_line(self.x_c, self.y_c, self.x_c + 1,
                              self.y_c + 1, fill=self.color_trace)
        # On met à jour la zone de texte.
        self.stringvar_pos_display.set(self.get_pos_displ())
        self.t += self.dt
        # On refait appel  à la  methode.move().
        if self.is_moving > 0:
            self.after(20, self.move)  # boucle toutes les 20ms

    def start(self):
        """demarrer la simulation
        """
        self.color_trace = rd.choice(couleur) #choix d'une couleur dans la liste couleur de facon aleatoire
        self.is_moving += 1
        # on appele la fonction move une seule fois
        if self.is_moving == 1:
            self.move()

    def stop(self):
        """mettre fin à la simulation
        """
        self.is_moving = 0

#demarrage du gestionnaire element
if __name__ == "__main__":
    simu_pendule = AppliPendule()
    simu_pendule.title("simulation d'un Pendule simple")
    simu_pendule.mainloop()

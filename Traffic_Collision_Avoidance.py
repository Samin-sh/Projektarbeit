import box
import puck
from Server import box_server
import math as m
import numpy as np
from Server.box_server import Box_Server
import numpy.linalg as la

# berechnet den Betrag eines zweidimensionalen Vektors
#def betrag(x, y):
    #return m.sqrt(x ** 2 + y ** 2)

# berechnet die Differenz zweier Vektoren
def delta(t1, t2):
    return t1 - t2

# time for closest approach
def t_ca(del_r, del_v):
    return -np.dot(del_r, del_v)/ np.dot(del_v, del_v)      #negative Zeiten können vernachlässigt werden

# Sicherheitsabstand
def r_ca(del_r, del_v):
    return del_r - np.dot(del_r, del_v)/ np.dot(del_v, del_v)

# notwendige Beschleunigung, um auszuweichen
def acceleration(r_ca, t_ca):
    return 2 * (2.5 - r_ca) / t_ca ** 2

#sortiert eine unsortierte Liste aus Tupeln rekursiv anhand des 0ten Elements eines Tupels
def merge_sort(l):
    if len(l) > 1:
        half = len(l) // 2
        left_l = l[:half]
        right_l = l[half:]

        merge_sort(left_l)
        merge_sort(right_l)

        i = 0
        j = 0
        k = 0

        while i < len(left_l) and j < len(right_l):
            if left_l[i][0] < right_l[j][0]:
                l[k] = left_l[i]
                i += 1
            else:
                l[k] = right_l[j]
                j += 1
            k += 1

        while i < len(left_l):
                l[k] = left_l[i]
                k += 1
                i += 1

        while j < len(right_l):
                l[k] = right_l[j]
                k += 1
                j += 1

def worker_shambayati(id, secret, q_request, q_reply):
    global puck_self
    V_MIN = 10.0
    V_MAX = 42.0
    A_MAX = 100.0

    q_request.put(('SET_NAME', 'shambayati', secret, id))
    name = q_reply.get()

    # eigenen Puck rausfinden
    q_request.put(('GET_SIZE', id))
    # Gesamtanzahl der Pucks
    size = q_reply.get()[1]
    for n in range(0, size - 1):
        q_request.put(('GET_PUCK', n, id))
        puck = q_reply.get()[1]
        if puck.get_id() == id:
            puck_self = puck
            n_self = n
            break

    # Grenzen abfragen
    q_request.put(('GET_BOX', id))
    grenzen = q_reply.get()[1]
    x_koordinaten = grenzen.get_x_limits()
    xmin = x_koordinaten[0]
    xmax = x_koordinaten[1]
    y_koordinaten = grenzen.get_y_limits()
    ymin = y_koordinaten[0]
    ymax = y_koordinaten[1]

    # auf mögliche Kollisionsgefahr prüfen
    while True:
        zeiten = []
        # eigene Position
        r_0 = puck_self.get_position()
        # eigene Geschwindigkeit
        v_0 = puck_self.get_velocity()
        for i in range (0, size-1):
            q_request.put(('GET_PUCK', i, id))
            puck_i = q_reply.get()[1]
            if puck_i != None:
                r_1 = puck_i.get_position()
                v_1 = puck_i.get_velocity() # andere variante, um gesschwindigkeit zu bekommen?
                del_v = delta(v_0, v_1)  # geschwindigkeitsdifferenz zweier Pucks
                del_r = delta(r_0, r_1)  # Abstand
                t_i = t_ca(del_r, del_v)
                zeiten.append((t_i, puck_i))

        zeiten_positiv = []
        zeiten_negativ = []
        for tupel in zeiten:
            if tupel[0] >= 0:
                zeiten_positiv.append(tupel)
            else:
                zeiten_negativ.append(tupel)

        # liste aufsteigend sortieren
        merge_sort(zeiten_positiv)
        merge_sort(zeiten_negativ)

        zeiten_sortiert = zeiten_positiv + zeiten_negativ

        # benötigte beschleunigung berechnen und setzten


        # Geschwindigkeit abfragen
        v_vektor = puck_self.get_velocity()
        vx = v_vektor[0]
        vy = v_vektor[1]
        v = la.norm([vx, vy])

        # Richtung der Beschleunigung durch v als normierten Einheitsvektor rausfinden
        v_norm = v_vektor / v
        a_betrag = v_norm * 5

        # V_MIN nicht unterschreiten
        # (entweder nach jeder Beschleunigung oder in kleinen Zeitabschnitten)
        if v == V_MIN + 1:
            q_request.put(('SET_ACCELERATION', a_betrag, secret, id))
            q_reply.get()
            q_request.put(('SET_ACCELERATION', np.array([0, 0]), secret, id))
            q_reply.get()

        # V_MAX nicht überschreiten
        if v == V_MAX - 1:
            q_request.put('SET_ACCELERATION', -a_betrag, secret, id)
            q_reply.get()
            q_request.put('SET_ACCELERATION', np.array([0, 0]), secret, id)
            q_reply.get()

        # nach dem Ausscheiden aus dem Spiel aufhören
        if puck_self.is_alive() == False:
            break

            # überprüfen ob Schnittpunkt existiert -> boolean

    # maximalbeschleunigung nicht überschreiten
    a = puck_self.get_acceleration()
    if la.norm(a) > A_MAX:
        raise ValueError('exceding max acceleration')
        a = a * (A_MAX / la.norm(a))        #A_MAX skalieren
        q_request.put('SET_ACCELERATION', a, secret, id)
        q_reply.get()
        q_request.put(('GET_ACCELERATION', np.array[0, 0] , secret, id))
        q_reply.get()

    # Verhalten nach einer Reflexion
    #die negativen Zeiten betrachten
    #s = puck_self.get_position()
    #if s[0] - puck_self.Puck.RADIUS <= xmin or s[0] + puck_self.Puck.RADIUS >= xmax or s[1] - puck_self.Puck.RADIUS <= ymin or s[
        #1] + puck_self.Puck.RADIUS >= ymax:
    # mehrere Abfragen


'''
def main():
    # die request queue erzeugen
    # manager = mp.Manager()
    # q_request = manager.Queue()

    # Queues erzeugen
    # q_reply = Queue()
    # q_request = Queue()


if __name__ == "__main__":
    main()
'''
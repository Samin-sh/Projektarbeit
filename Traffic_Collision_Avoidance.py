from params import A_MAX
from params import V_MIN
from params import V_MAX
import box
import puck
from Server import box_server
from Server.box_server import Box_Server
import math as m
import numpy as np
import numpy.linalg as la


# berechnet die Differenz zweier Vektoren
def delta(t1, t2):

    # falls die Längen sich unterscheiden
    if len(t1) != len(t2):
        raise ValueError

    # falls falsche Datentypen als Eingabe verwendet werden
    if not (type(t1) in [list, np.ndarray] or type(t2) in [list, np.ndarray]):
        raise TypeError

    return np.array(t1) - np.array(t2)

# time for closest approach
def t_ca(del_r, del_v):

    # falls falsche Datentypen als Eingabe verwendet werden
    if not (type(del_r) in [list, np.ndarray] or type(del_v) in [list, np.ndarray]):
        raise TypeError

    # falls die Längen sich unterscheiden
    if len(del_r) != len(del_v):
        raise ValueError

    del_v = np.array(del_v)
    del_r  = np.array(del_r)

    nenner = np.dot(del_v, del_v)
    if nenner == 0:
        return 1e9
    return -np.dot(del_r, del_v)/ np.dot(del_v, del_v)      #negative Zeiten können vernachlässigt werden

# Sicherheitsabstand
def r_ca(del_r, del_v):
    del_v = np.array(del_v)
    del_r = np.array(del_r)

    # falls falsche Datentypen als Eingabe verwendet werden
    if not (type(del_r) in [list, np.ndarray] or type(del_v) in [list, np.ndarray]):
        raise TypeError

    # falls die Längen sich unterscheiden
    if len(del_r) != len(del_v):
        raise ValueError

    nenner = np.dot(del_v, del_v)
    if nenner == 0:
        return del_r - 1e9
    return del_r - np.dot(del_r, del_v)/ np.dot(del_v, del_v)

# notwendige Beschleunigung, um auszuweichen
def acceleration(r_ca, t_ca):

    # falsche Anzahl an Komponenten
    if len(r_ca) != 2:
        raise ValueError

    # falls falsche Datentypen als Eingabe verwendet werden
    if not (type(r_ca) in [list, np.ndarray] and type(t_ca) in [float, int]):
        raise TypeError

    # falls der Nenner Null ergeben sollte
    if t_ca == 0:
        raise ValueError

    return 2 * (2.5 - np.array(r_ca)) / t_ca ** 2

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

    # namen setzen
    q_request.put(('SET_NAME', 'shambayati', secret, id))
    name = q_reply.get()

    # eigenen Puck herausfinden
    puck_self = None
    q_request.put(('GET_SIZE', id))
    # Gesamtanzahl der Pucks
    size = q_reply.get()[1]
    for n in range(0, size - 1):
        q_request.put(('GET_PUCK', n, id))
        puck = q_reply.get()[1]

        if puck and puck.get_id() == id:
            puck_self = puck
            break
    if puck_self is None:
        return

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
        q_request.put(('SET_ACCELERATION', np.array([0, 0]), secret, id))
        q_reply.get()
        zeiten = []
        # eigene Position
        r_0 = puck_self.get_position()
        # eigene Geschwindigkeit
        v_0 = puck_self.get_velocity()
        for i in range (0, size-1):
            q_request.put(('GET_PUCK', i, id))
            puck_i = q_reply.get()[1]
            if puck_i is not None:
                r_i = puck_i.get_position()
                v_i = puck_i.get_velocity() # andere variante, um geschwindigkeit zu bekommen?
                del_v = delta(v_0, v_i)  # geschwindigkeitsdifferenz zweier Pucks
                del_r = delta(r_0, r_i)  # Abstand
                t_i = t_ca(del_r, del_v)
                zeiten.append((t_i, r_i, puck_i))
        # Liste in negative und positive zeiten aufteilen
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

        # benötigte beschleunigung berechnen und setzten
        for i in range(len(zeiten_positiv)):
            puck_i = zeiten_positiv[i][2]
            del_r = delta(puck_self.get_position(), puck_i.get_position())
            del_v = delta(puck_self.get_velocity(), puck_i.get_velocity())

            if t_i > 0:
                r = r_ca(del_r, del_v)
                if np.linalg.norm(r) > 0:
                    a = acceleration(np.linalg.norm(r), t_i)
                    q_request.put(('SET_ACCELERATION', a, secret, id))
                    q_reply.get()

                    # Geschwindigkeit abfragen
                    v_vektor = puck_self.get_velocity()
                    vx = v_vektor[0]
                    vy = v_vektor[1]
                    v = la.norm([vx, vy])

                    # Richtung der Beschleunigung durch v als normierten Einheitsvektor rausfinden
                    v_norm = v_vektor / v
                    a_betrag = v_norm * 6

                    # V_MIN nicht unterschreiten
                    if v == V_MIN + 6.5:
                        q_request.put(('SET_ACCELERATION', a_betrag, secret, id))
                        q_reply.get()
                        q_request.put(('SET_ACCELERATION', np.array([0, 0]), secret, id))
                        q_reply.get()

                    # V_MAX nicht überschreiten
                    if v == V_MAX - 6.5:
                        q_request.put(('SET_ACCELERATION', -a_betrag, secret, id))
                        q_reply.get()
                        q_request.put(('SET_ACCELERATION', np.array([0, 0]), secret, id))
                        q_reply.get()

                    # maximalbeschleunigung nicht überschreiten
                    a = puck_self.get_acceleration()
                    if la.norm(a) > A_MAX:
                        raise ValueError('exceding max acceleration')
                        a = a * (A_MAX / la.norm(a))  # A_MAX skalieren
                        q_request.put(('SET_ACCELERATION', a, secret, id))
                        q_reply.get()
                        q_request.put(('SET_ACCELERATION', np.array[0, 0], secret, id))
                        q_reply.get()

            # nach dem Ausscheiden aus dem Spiel aufhören
                if puck_self.is_alive() == False:
                    break
'''
# Verhalten nach einer Reflexion
#die negativen Zeiten betrachten
#negative geschwindigkeit betrachten wenn man kurz vor einer Grenze ist
#s = puck_self.get_position()
#if s[0] - puck_self.Puck.RADIUS <= xmin or s[0] + puck_self.Puck.RADIUS >= xmax or s[1] - puck_self.Puck.RADIUS <= ymin or s[
    #1] + puck_self.Puck.RADIUS >= ymax:
'''
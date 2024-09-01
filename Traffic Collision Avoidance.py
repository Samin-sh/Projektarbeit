import box
import puck
from Server import box_server
import math as m
import numpy as np


# berechnet den Betrag eines zweidimensionalen Vektors
def betrag(x, y):
    return m.sqrt(x ** 2 + y ** 2)  # wenn die beschleunigung negativ ist?


# berechnet die Differenz zweier Vektoren
def delta(t1, t2):
    return t1 - t2

def worker_shambayati(id, secret, q_request, q_reply):
    global puck_self
    V_MIN = 10.0
    V_MAX = 42.0
    A_MAX = 100.0

    q_request.put(('SET_NAME', 'shambayati', secret, id))

    # eigenen Puck rausfinden
    q_request.put(('GET_SIZE', id))
    # Gesamtanzahl der Pucks
    size = q_reply.get()[1]
    for n in range(0, size - 1):
        q_request.put(('GET_PUCK', n, id))
        puck = q_reply.get()[1]
        if puck.get_id() == id:
            puck_self = puck
            break

    # Grenzen abfragen
    q_request.put(('GET_BOX', id))
    grenzen = q_reply.get()[1]
    from Server.box_server import Box_Server
    box = Box_Server(grenzen[0], grenzen[1], grenzen[2], grenzen[3])
    x_koordinaten = box.get_x_limits()
    xmin = x_koordinaten[0]
    xmax = x_koordinaten[1]
    y_koordinaten = box.get_y_limits()
    ymin = y_koordinaten[0]
    ymax = y_koordinaten[1]

    # Verhalten nach einer Reflexion
    s = puck.get_position()
    if s[0] - puck.Puck.RADIUS <= xmin or s[0] + puck.Puck.RADIUS >= xmax or s[1] - puck.Puck.RADIUS <= ymin or s[
        1] + puck.Puck.RADIUS >= ymax:
    # mehrere Abfragen

    # Geschwindigkeit abfragen
    v_vektor = puck_self.get_velocity()
    v = betrag(v_vektor)

    # Geschwindigkeitsgrenzen nicht überschreiten
    # (entweder nach jeder Beschleunigung oder in kleinen Zeitabschnitten)
    if v == V_MIN + 1:
        q_request.put('SET_ACCELERATION', np.array([1, 1]), secret, id)
        q_reply.get('SET_ACCELERATION', np.array([1, 1]))
        q_request.put('SET_ACCELERATION', np.array([0, 0]), secret, id)
    if v == V_MAX - 1:
        q_request.put('SET_ACCELERATION', -np.array([1, 1]), secret, id)
        q_reply.get('SET_ACCELERATION', -np.array([1, 1]))
        q_request.put('SET_ACCELERATION', np.array([0, 0]), secret, id)

    # s = ort
    # d = abstand
    # v = geschwindigkeit
    # a = beschleunugung
    # t = Zeit

    # verhalten bei möglicher Kollision
    '''
    als Funktionen schreiben
    überprüfen ob Schnittpunkt existiert -> boolean
    del_v = v_1,0-v_2,0
    del_r = r_1,0-r_2,0
    t_ca = - del_r*del_v/ del_v*del_v
    r_ca = del_r-(del_r*del_v)/del_v*del_v)*del_v
    a = 2*(2.5-r_ca) / t_ca**2
    '''


def main():
    z = delta(3, 2)
    print(z)
    # die request queue erzeugen
    # manager = mp.Manager()
    # q_request = manager.Queue()

    # Queues erzeugen
    # q_reply = Queue()
    # q_request = Queue()


if __name__ == "__main__":
    main()

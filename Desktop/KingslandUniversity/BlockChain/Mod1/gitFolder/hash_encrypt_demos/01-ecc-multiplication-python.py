from pycoin.ecdsa import Point
from pycoin.ecdsa import Curve

curve = Curve.Curve(17, 0, 7)
print("Curve = " + str(curve))

G = Point.Point(15, 13, curve)
print("G = " + str(G))

for k in range(0, 6) :
  print(str(k) + " * G = " + str(k * G))

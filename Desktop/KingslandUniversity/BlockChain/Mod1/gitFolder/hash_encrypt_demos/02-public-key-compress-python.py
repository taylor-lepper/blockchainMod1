from pycoin.ecdsa import Curve, Point
from nummaster.basic import sqrtmod

def compress_key_pair(key_pair):
  return (key_pair[0], key_pair[1] % 2)

def uncompress_key(curve, compressed_key):
  x, is_odd = compressed_key
  p, a, b = curve._p, curve._a, curve._b
  y = sqrtmod(pow(x, 3, p) + a * x + b, p)
  if bool(is_odd) == bool(y & 1):
    return (x, y)
  return (x, p - y)

curve = Curve.Curve(17, 0, 7)
p = Point.Point(10, 15, curve)
print(f"original key = {p}")
compressed_p = compress_key_pair(p)
print(f"compressed = {compressed_p}")
restored_p = uncompress_key(curve, compressed_p)
print(f"uncompressed = {restored_p}")

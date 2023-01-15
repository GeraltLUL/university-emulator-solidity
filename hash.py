import rsa
import hashlib

name = "sasha".encode()
hs = hashlib.sha256(name).hexdigest() #297581d6cd198a6e6df740f13288cb13a1e76cebe3f0ebc3fe259977addfd646


rsa
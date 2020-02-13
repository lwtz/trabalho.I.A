#Indique el numero de discos que desee en la torre.
DISCOS= int(input("Insira o numero de disco para jogar: "))

#Estas funciones son creadas para que se vean bien las imagenes de los pasos.

def espaco():
 return 2

def LarguraDisco(tamanho):
 return 2 * tamanho + 3

def AnchoTorre(tamanho):
 return 2 * tamanho + 3

def AlturaTorre(tamanho):
 return tamanho + 2

def PosicaoTorre(tamanho, i):
 return i * (AnchoTorre(tamanho) + espaco())

def CentroTorre(tamanho, i):
 return AnchoTorre(tamanho) // 2 + PosicaoTorre(tamanho, i)

def AlturaImagen(tamanho):
 return AlturaTorre(tamanho) + 3

def AnchuraImagen(tamanho):
 return AnchoTorre(tamanho) * 3 + 2 * espaco()

#---------------------------------

#Esta funcion otorga los movimientos para mover el numero de discos de principio a fim

def ObtMovimento(inicio, fim, n_discos):
 if n_discos == 1:
   yield (inicio, fim)
 else:
   midObjetivo = 3 - inicio - fim
   yield from ObtMovimento(inicio, midObjetivo, n_discos - 1)
   yield (inicio,fim )
   yield from ObtMovimento(midObjetivo, fim, n_discos - 1)

def HacerMovimiento(mover, discos):
#Ejecuta el movimiento
 inicio, fim = mover
 discos[fim].append(discos[inicio].pop())
 #-------------------------------------
# Ahora en lo siguiente me aseguraré que se impriman bien los pasos.
# Un "StringArt" es una funcion que toma dos parametros (x,y) y regresa un caracter o un espaco transparente, x representa la fila, y representa la columna.

TRANSPARENTE = ""

def Art_vacio():    # Crea un "StringArt" vacío
 return lambda x, y: TRANSPARENTE

def crearStringArt(string): # Crea un "StringArt" (Creacion de tipo cadena) de una variable string la cual toma una fila
 def resultado(x, y):
   if x == 0 and y >= 0 and y < len(string):
     return string[y]
   else:
     return TRANSPARENTE
 return resultado
 def TrasladarStringArt(stringArt, i, j): # Traslada un "StringArt" a otra pocision
 return lambda x, y: stringArt(x - i, y - j)

def TransponerStringArt(stringArt): # Transpone un "StringArt" cambiando las cordenadas de x,y
 return lambda x, y: stringArt(y, x)

def stringArtUnion(stringArts): # Toma una lista de "StringArts" y regresa un "StringArt"
 def resultado(x, y):             # el cual a su vez nos da el primero valor visible.
   for art in stringArts:
     if art(x, y) != TRANSPARENTE:
       return art(x, y)
   return TRANSPARENTE
 return resultado

#-------------------------------------
# Los siguientes son los métodos para imprimir los "StringArts"

def resolverChar(char):  # Hace que se pueda impirmir una figura de una "StringArt".
 return  " " if char == TRANSPARENTE else char

def printStringArt(stringArt, sizeX, sizeY):  # Imprime un "StringArt" en un rectangulo de
 for i in range(sizeX):                      # tamanhoX x tamanho Y
   line = "".join([resolverChar(stringArt(i, j)) for j in range(sizeY)])
   print(line)

#---------------------------------
#A partir de ahora tratamos los elementos que realmente queremos mostrar

def CrearTorreBaseySoporte(tamanho):  # Ésta funcion hace que se despliegue el la base y el 
 Altura = AlturaTorre(tamanho)       # soporte de la torre.
 Anchura = AnchoTorre(tamanho)
 soporte = TransponerStringArt(crearStringArt("|" * Altura))
 soporte = TrasladarStringArt(soporte, 0, Anchura // 2)
 base = crearStringArt("=" * Anchura)
 base = TrasladarStringArt(base, Altura - 1, 0)
 return stringArtUnion([base, soporte])

def crearflecha(inicio, fim):        # Ésta funcion crea un flecha que nos indica 
 izquierda_fim = min([inicio, fim]) #de que torre a que torre estamos moviendo el disco.
 derecha_fim = max([inicio, fim])
 v = crearStringArt("v")
 v = TrasladarStringArt(v, 0, fim)
 fila = crearStringArt("-" * (derecha_fim - izquierda_fim + 1))
 fila = TrasladarStringArt(fila, 0, izquierda_fim)
 return stringArtUnion([v, fila])
 
def crearDisco(tamanho, centro):          # Esta función crea un "StringArt" que va a
 stoneString = "o" * LarguraDisco(tamanho) # representar un disco de la torre.
 return crearStringArt(stoneString.center(2 * centro + 1))

def crearTorreconDiscos(tamanho, ListaDisco):      # Esta función crea un "String Art" para
 BaseTorreArt = CrearTorreBaseySoporte(tamanho)   # una torre, incluyendo los discos que
 DiscoArts = []                                  # estan en la torre.
 AlturaDisco = tamanho
 center = tamanho + 1
 for stoneSize in ListaDisco:
   DiscoArt = crearDisco(stoneSize, center)
   DiscoArts.append(TrasladarStringArt(DiscoArt, AlturaDisco, 0))
   AlturaDisco -= 1
 return stringArtUnion([BaseTorreArt] + DiscoArts)

def crearImagenTorre(size, ListaDisco, i):     # Esta funcion Crea la imagen para la torre i
 posicao = PosicaoTorre(size, i)            # y la traslada a su respectiva posición.   
 TorreArt = crearTorreconDiscos(size, ListaDisco)
 return TrasladarStringArt(TorreArt, 2, posicao)
def crearFlechaPaso(tamanho, SeguintePasso):  # Crea un "StringArt" para la flecha
 if SeguintePasso != None:
   inicioIndice, fimIndice = SeguintePasso
   inicio = CentroTorre(tamanho, inicioIndice)
   fim = CentroTorre(tamanho, fimIndice)
   result = crearflecha(inicio, fim)
 else:
   result = Art_vacio()
 return result

def createFullArt(tamanho, discos, SeguintePasso):   # Esta funcion crea un "StringArt" de un
 flecha = crearFlechaPaso(tamanho, SeguintePasso)   # paso, incluyendo la flecha.
 TorreArts = [crearImagenTorre(tamanho, discos[i], i) for i in range(3)]
 TorresArt = stringArtUnion(TorreArts)
 return stringArtUnion([flecha, TorresArt])

def imprimirpasos(tamanho):     # Esta función imprime todos los pasos correspondientes.
 discos = [list(range(DISCOS))[::-1], [], []]
 Altura_Imagen = AlturaImagen(tamanho)
 Anchura_Imagen = AnchuraImagen(tamanho)
 for mover in ObtMovimento(0, 2, tamanho):
   print("Mover o disco da torre {0} para a {1}".format(*mover))
   printStringArt(createFullArt(tamanho, discos, mover), Altura_Imagen, Anchura_Imagen)
   HacerMovimiento(mover, discos)
 print("fimalizado com um total de  :", 2**DISCOS-1, "movimentos.")
 printStringArt(createFullArt(tamanho, discos, None), Altura_Imagen, Anchura_Imagen) 
 imprimirpasos(DISCOS)





#Indique el numero de discos que desee en la torre.
DISCOS= int(input("Ingrese el numero de discos que quiere en la torre: ")) 

#Estas funciones son creadas para que se vean bien las imagenes de los pasos.

def Espacio():
  return 2

def AnchoDisco(tamaño):
  return 2 * tamaño + 3

def AnchoTorre(tamaño):
  return 2 * tamaño + 3

def AlturaTorre(tamaño):
  return tamaño + 2

def PosicionTorre(tamaño, i):
  return i * (AnchoTorre(tamaño) + Espacio())

def CentroTorre(tamaño, i):
  return AnchoTorre(tamaño) // 2 + PosicionTorre(tamaño, i)

def AlturaImagen(tamaño):
  return AlturaTorre(tamaño) + 3

def AnchuraImagen(tamaño):
  return AnchoTorre(tamaño) * 3 + 2 * Espacio()

#---------------------------------

#Esta funcion otorga los movimientos para mover el numero de discos de principio a fin

def ObtMovimiento(inicio, fin, n_discos):
  if n_discos == 1:
    yield (inicio, fin)
  else:
    midObjetivo = 3 - inicio - fin
    yield from ObtMovimiento(inicio, midObjetivo, n_discos - 1)
    yield (inicio,fin )
    yield from ObtMovimiento(midObjetivo, fin, n_discos - 1)

def HacerMovimiento(mover, discos):
 
 #Ejecuta el movimiento 
 
  inicio, fin = mover
  discos[fin].append(discos[inicio].pop())
  
#-------------------------------------
# Ahora en lo siguiente me aseguraré que se impriman bien los pasos. 
# Un "StringArt" es una funcion que toma dos parametros (x,y) y regresa un caracter o un espacio transparente, x representa la fila, y representa la columna.

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
  for i in range(sizeX):                      # TamañoX x Tamaño Y
    line = "".join([resolverChar(stringArt(i, j)) for j in range(sizeY)])
    print(line) 

#---------------------------------
#A partir de ahora tratamos los elementos que realmente queremos mostrar

def CrearTorreBaseySoporte(tamaño):  # Ésta funcion hace que se despliegue el la base y el  
  Altura = AlturaTorre(tamaño)       # soporte de la torre.
  Anchura = AnchoTorre(tamaño)
  soporte = TransponerStringArt(crearStringArt("|" * Altura))
  soporte = TrasladarStringArt(soporte, 0, Anchura // 2)
  base = crearStringArt("=" * Anchura)
  base = TrasladarStringArt(base, Altura - 1, 0)
  return stringArtUnion([base, soporte])

def crearflecha(inicio, fin):        # Ésta funcion crea un flecha que nos indica  
  izquierda_fin = min([inicio, fin]) #de que torre a que torre estamos moviendo el disco.
  derecha_fin = max([inicio, fin])
  v = crearStringArt("v")
  v = TrasladarStringArt(v, 0, fin)
  fila = crearStringArt("-" * (derecha_fin - izquierda_fin + 1))
  fila = TrasladarStringArt(fila, 0, izquierda_fin)
  return stringArtUnion([v, fila])
   
def crearDisco(tamaño, centro):          # Esta función crea un "StringArt" que va a 
  stoneString = "o" * AnchoDisco(tamaño) # representar un disco de la torre.
  return crearStringArt(stoneString.center(2 * centro + 1))

def crearTorreconDiscos(tamaño, ListaDisco):      # Esta función crea un "String Art" para 
  BaseTorreArt = CrearTorreBaseySoporte(tamaño)   # una torre, incluyendo los discos que 
  DiscoArts = []                                  # estan en la torre. 
  AlturaDisco = tamaño
  center = tamaño + 1
  for stoneSize in ListaDisco:
    DiscoArt = crearDisco(stoneSize, center)
    DiscoArts.append(TrasladarStringArt(DiscoArt, AlturaDisco, 0))
    AlturaDisco -= 1
  return stringArtUnion([BaseTorreArt] + DiscoArts)

def crearImagenTorre(size, ListaDisco, i):     # Esta funcion Crea la imagen para la torre i
  posicion = PosicionTorre(size, i)            # y la traslada a su respectiva posición.    
  TorreArt = crearTorreconDiscos(size, ListaDisco)
  return TrasladarStringArt(TorreArt, 2, posicion)
 
def crearFlechaPaso(tamaño, SiguientePaso):  # Crea un "StringArt" para la flecha
  if SiguientePaso != None:
    inicioIndice, finIndice = SiguientePaso
    inicio = CentroTorre(tamaño, inicioIndice)
    fin = CentroTorre(tamaño, finIndice)
    result = crearflecha(inicio, fin)
  else:
    result = Art_vacio()
  return result

def createFullArt(tamaño, discos, SiguientePaso):   # Esta funcion crea un "StringArt" de un
  flecha = crearFlechaPaso(tamaño, SiguientePaso)   # paso, incluyendo la flecha.
  TorreArts = [crearImagenTorre(tamaño, discos[i], i) for i in range(3)]
  TorresArt = stringArtUnion(TorreArts)
  return stringArtUnion([flecha, TorresArt]) 

def imprimirpasos(tamaño):     # Esta función imprime todos los pasos correspondientes. 
  discos = [list(range(DISCOS))[::-1], [], []]
  Altura_Imagen = AlturaImagen(tamaño)
  Anchura_Imagen = AnchuraImagen(tamaño)
  for mover in ObtMovimiento(0, 2, tamaño):
    print("Mueve el disco de la torre {0} a la {1}".format(*mover))
    printStringArt(createFullArt(tamaño, discos, mover), Altura_Imagen, Anchura_Imagen)
    HacerMovimiento(mover, discos)
  print("¡Y queda listo!, despues de realizar :", 2**DISCOS-1, "movimientos.")
  printStringArt(createFullArt(tamaño, discos, None), Altura_Imagen, Anchura_Imagen)  
  
imprimirpasos(DISCOS) 



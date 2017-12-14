#!/usr/bin/env python
import numpy as np

def def_matrix():
    matrix = np.zeros([9,9])

    # Load Structure
    """
    matrix[0,3]=9
    matrix[0,4]=1
    matrix[0,7]=5
    matrix[1,4]=6
    matrix[1,6]=3
    matrix[1,8]=1
    matrix[2,4]=8
    matrix[2,5]=2
    matrix[2,8]=9
    matrix[3,0]=7
    matrix[3,2]=3
    matrix[3,6]=8
    matrix[3,7]=6
    matrix[3,8]=4
    matrix[4,2]=4
    matrix[4,3]=2
    matrix[4,5]=8
    matrix[5,0]=9
    matrix[5,2]=8
    matrix[5,4]=7
    matrix[6,2]=9
    matrix[6,5]=6
    matrix[6,6]=5
    matrix[6,7]=4
    matrix[7,3]=3
    matrix[7,8]=6
    matrix[8,1]=2
    matrix[8,2]=7
    matrix[8,5]=5
    matrix[8,7]=1

    matrix[0,1]=1
    matrix[0,4]=5
    matrix[0,8]=6
    matrix[1,0]=5
    matrix[1,1]=7
    matrix[1,2]=6
    matrix[1,5]=8
    matrix[2,0]=4
    matrix[2,3]=9
    matrix[2,7]=5
    matrix[4,0]=9
    matrix[4,5]=7
    matrix[4,7]=3
    matrix[4,8]=4
    matrix[5,1]=8
    matrix[5,2]=2
    matrix[5,3]=4
    matrix[5,8]=1
    matrix[6,0]=1
    matrix[6,1]=9
    matrix[6,2]=5
    matrix[6,3]=7
    matrix[7,0]=8
    matrix[7,6]=4
    matrix[7,7]=2
    matrix[8,1]=2
    matrix[8,4]=6
    matrix[8,6]=7
    """
    matrix[0,3]=2
    matrix[0,4]=6
    matrix[0,6]=7
    matrix[0,8]=1
    matrix[1,0]=6
    matrix[1,1]=8
    matrix[1,4]=7
    matrix[1,7]=9
    matrix[2,0]=1
    matrix[2,1]=9
    matrix[2,5]=4
    matrix[2,6]=5
    matrix[3,0]=8
    matrix[3,1]=2
    matrix[3,3]=1
    matrix[3,7]=4
    matrix[4,2]=4
    matrix[4,3]=6
    matrix[4,5]=2
    matrix[4,6]=9
    matrix[5,1]=5
    matrix[5,5]=3
    matrix[5,7]=2
    matrix[5,8]=8
    matrix[6,2]=9
    matrix[6,3]=3
    matrix[6,7]=7
    matrix[6,8]=4
    matrix[7,1]=4
    matrix[7,4]=5
    matrix[7,7]=3
    matrix[7,8]=6
    matrix[8,0]=7
    matrix[8,2]=3
    matrix[8,4]=1
    matrix[8,5]=8
    """
    """
    # One of the Worlds most difficult sudokus
    matrix[0,0]=8
    matrix[1,2]=3
    matrix[1,3]=6
    matrix[2,1]=7
    matrix[2,4]=9
    matrix[2,6]=2
    matrix[3,1]=5
    matrix[3,5]=7
    matrix[4,4]=4
    matrix[4,5]=5
    matrix[4,6]=7
    matrix[5,3]=1
    matrix[5,7]=3
    matrix[6,2]=1
    matrix[6,7]=6
    matrix[6,8]=8
    matrix[7,2]=8
    matrix[7,3]=5
    matrix[7,7]=1
    matrix[8,1]=9
    matrix[8,6]=4
    """
    return matrix

def prepare(coords_x, coords_y, matrix):
    conjunto = []
    for i in range(coords_x[0],coords_x[1]):
        for j in range(coords_y[0],coords_y[1]):
            if matrix[i,j] != 0:
                conjunto.append(np.array([int(matrix[i,j])]))
            else:
                values = np.concatenate((matrix[i,:], matrix[:,j]))
                values = np.unique(values)
                conjunto.append(np.setdiff1d(range(1,10),values))
    return conjunto

# First approach
def first(conjunto):
    c = 0
    for i0 in conjunto[0]:
        elegido = np.zeros((1,9))
        elegido[0][0] = i0
        c += 1
        if c == 1:
            square1 = np.empty_like(elegido)
            square1[:] = elegido
        else:
            square1 = np.concatenate((square1,elegido), axis=0)
    return square1

def second2(conjunto,square1,Z):
    c=0
    for i,_ in enumerate(square1):
        elegido = np.zeros((1,9))
        elegido[0] = square1[i]
        for i1 in conjunto[Z]:
            if i1 not in elegido[0]:
                elegido[0][Z]=i1
                #print elegido
                c += 1
                if c == 1:
                    square2 = np.empty_like(elegido)
                    square2[:] = elegido
            #        print square2
                else:
                    square2 = np.concatenate((square2,elegido), axis=0)
                elegido[0] = square1[i]
    square1 = np.empty_like(square2)
    square1[:] = square2
    return square1

def compute(matrix):
    info = []
    square_x = np.array([[0,3], [0,3], [0,3], [3,6],[3,6],[3,6],[6,9],[6,9],[6,9]])
    square_y = np.array([[0,3], [3,6], [6,9], [0,3],[3,6],[6,9],[0,3],[3,6],[6,9]])
    for index,_ in enumerate(square_x):

        coords_x = square_x[index]
        coords_y = square_y[index]
        conjunto = prepare(coords_x,coords_y,matrix)

        square1 = first(conjunto)
        for Z in range(1,9):
            square1=second2(conjunto,square1,Z)
        info.append(square1)
    return info

def sudokito(lista,info,i):
    if i in (0,3,6):
        objeto = np.empty_like(info[i])
        objeto[:] = info[i]
    else:
        #objeto = np.empty_like(lista)
        objeto = lista

    lista = []
    for index,vector in enumerate(objeto):
        if i in (0,3,6):
            panel = np.reshape(vector,(3,3))
        else:
            panel = vector

        for index2,vector2 in enumerate(info[i+1]):
            panel2 = np.reshape(vector2,(3,3))

            panelsuma = np.concatenate([panel, panel2],axis=1)

            # Check
            c = 0
            for row in range(panelsuma.shape[0]):
                if len(np.unique(panelsuma[row,:])) < panelsuma.shape[1]:
                    break
                else:
                    c += 1
            if c == panelsuma.shape[0]:
                for col in range(panelsuma.shape[1]):
                    if len(np.unique(panelsuma[:,col])) < panelsuma.shape[0]:
                        break
                    else:
                        c += 1
            if c == sum(panelsuma.shape):
                lista.append(panelsuma)
    return lista

def sudokuto(info):
    lista_0 = []
    lista_0 = sudokito(lista_0,info,0)
    lista_0 = sudokito(lista_0,info,1)

    lista_1 = []
    lista_1 = sudokito(lista_1,info,3)
    lista_1 = sudokito(lista_1,info,4)

    lista_2 = []
    lista_2 = sudokito(lista_2,info,6)
    lista_2 = sudokito(lista_2,info,7)

    for lista0 in lista_0:
        for lista1 in lista_1:
            for lista2 in lista_2:
                sudoku = np.concatenate([lista0,lista1,lista2],axis=0)
                # Check
                c = 0
                for row in range(sudoku.shape[0]):
                    if len(np.unique(sudoku[row,:])) < sudoku.shape[1]:
                        break
                    else:
                        c += 1
                if c == sudoku.shape[0]:
                    for col in range(sudoku.shape[1]):
                        if len(np.unique(sudoku[:,col])) < sudoku.shape[0]:
                            break
                        else:
                            c += 1
                if c == sum(sudoku.shape):
                    print sudoku

if __name__ == "__main__":
    matrix = def_matrix()
    info = compute(matrix)
    sudokuto(info)

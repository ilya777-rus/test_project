

def pointInTriangle(point, triangle):
    a = [triangle[0][0], triangle[0][1]]

    b = [triangle[1][0], triangle[1][1]]

    c = [triangle[2][0], triangle[2][1]]

    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    x3 = c[0]
    y3 = c[1]

    x = point['x']
    y = point['y']

    a1 = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)

    b1 = (x2 - x) * (y3 - y2) - (x3 - x2) * (y2 - y)

    c1 = (x3 - x) * (y1 - y3) - (x1 - x3) * (y3 - y)

    t = False
    if ((a1 >= 0 and b1 >= 0 and c1 >= 0) or (a1 <= 0 and b1 <= 0 and c1 <= 0)):
        print("Принадлежит треугольнику", triangle)
        return triangle

    else:
        # print("Не принадлежит треугольнику")
        return False



def interpolation_delone(triangles, points, point):
    for triangle in triangles:
        triangle1 = pointInTriangle(point, triangle)
        # print(triangle1)
        if triangle1!=False:
            # print('YES',point_array)
            # print(len(point_array))
            sza = []
            count = 0
            for p in points:
                for i in range(3):
                    if p['glon'] == triangle1[i][0] and p['glat'] == triangle1[i][1]:
                        sza.append([p['glon'], p['glat'], p['sza'], p['iaga']])
                        count += 1
                if count == 3:
                    print('break')
                    print("333333", sza)
                    break
            # try:
            #     print('tryy')
            #     x,y =point['x'],point['y']
            # except:
            # print('except', point)
            x, y = point['x'], point['y']
            # print("SZAAAAAAAAAAAAAA", sza)
            print('---------------------------')
            Y1 = sza[0][1]
            Y2 = sza[1][1]
            Y3 = sza[2][1]
            X1 = sza[0][0]
            X2 = sza[1][0]
            X3 = sza[2][0]
            Z1 = sza[0][2]
            Z2 = sza[1][2]
            Z3 = sza[2][2]
            print('---------------------------')
            # Y1 = triangle.vertex1.glat
            # Y2 = triangle.vertex2.glat
            # Y3 = triangle.vertex3.glat
            # X1 = triangle.vertex1.glon
            # X2 = triangle.vertex2.glon
            # X3 = triangle.vertex3.glon
            # Z1 = triangle.vertex1.sza
            # Z2 = triangle.vertex2.sza
            # Z3 = triangle.vertex3.sza
            print(X1, Y1, Z1)
            print(X2, Y2, Z2)
            print(X3, Y3, Z3)
            a = Y1 * (Z2 - Z3) + Y2 * (Z3 - Z1) + Y3 * (Z1 - Z2)
            b = Z1 * (X2 - X3) + Z2 * (X3 - X1) + Z3 * (X1 - X2)
            c = X1 * (Y2 - Y3) + X2 * (Y3 - Y1) + X3 * (Y1 - Y2)
            d = X1 * (Y2 * Z3 - Y3 * Z2) + X2 * (Y3 * Z1 - Y1 * Z3) + X3 * (Y1 * Z2 - Y2 * Z1)
            d = d * (-1)
          
            result = (-1) * (a * x + b * y + d) / c
            result = round(result, 5)
            return result











# def interpolation_delone(triangles, point):
#     for triangle in triangles:
#         triangle1 = triangle.get_list()
#         print(triangle1)
#         if pointInTriangle(point, triangle1):
#             # print('YES',point_array)
#             # print(len(point_array))
#             # sza = []
#             # count = 0
#             # for p in points:
#             #     for i in range(3):
#             #         if p['merx'] == triangl[i][0] and p['mery'] == triangl[i][1]:
#             #             sza.append([p['merx'], p['mery'], p['sza']])
#             #             count += 1
#             #     if count == 3:
#             #         print('break')
#             #         print("333333", sza)
#             #         break
#             # try:
#             #     print('tryy')
#             #     x,y =point['x'],point['y']
#             # except:
#             # print('except', point)
#             x, y = point['x'], point['y']
#             # print("SZAAAAAAAAAAAAAA", sza)
#             Y1 = triangle.vertex1.glat
#             Y2 = triangle.vertex2.glat
#             Y3 = triangle.vertex3.glat
#             X1 = triangle.vertex1.glon
#             X2 = triangle.vertex2.glon
#             X3 = triangle.vertex3.glon
#             Z1 = triangle.vertex1.sza
#             Z2 = triangle.vertex2.sza
#             Z3 = triangle.vertex3.sza
#             # print(X1, Y1, Z1)
#             # print(X2, Y2, Z2)
#             # print(X3, Y3, Z3)
#             a = Y1 * (Z2 - Z3) + Y2 * (Z3 - Z1) + Y3 * (Z1 - Z2)
#             b = Z1 * (X2 - X3) + Z2 * (X3 - X1) + Z3 * (X1 - X2)
#             c = X1 * (Y2 - Y3) + X2 * (Y3 - Y1) + X3 * (Y1 - Y2)
#             d = X1 * (Y2 * Z3 - Y3 * Z2) + X2 * (Y3 * Z1 - Y1 * Z3) + X3 * (Y1 * Z2 - Y2 * Z1)
#             d = d * (-1)
#
#             result = (-1) * (a * x + b * y + d) / c
#             result = round(result, 5)
#             return result
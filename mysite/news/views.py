import json
import math
from typing import List

import pyproj
import requests
from pyproj import Proj, transformer, Transformer

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from scipy.spatial import Delaunay

import multiprocessing

from .models import Point, Triangles
from .utils.main import main
from .utils.my_functions import pointInTriangle, interpolation_delone
from .utils.supermagapi import SuperMAGGetInventory, SuperMAGGetData
import datetime
import time

from django.db import connection
from .utils.typing import Vertex
from .utils.triangulate import scatter_vertices, delaunay


def index(request):
    Point.objects.all().delete()
    Triangles.objects.all().delete()

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='news_point';")
    with connection.cursor() as cursor:
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name='news_point';")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='news_triangles';")
    with connection.cursor() as cursor:
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name='news_triangles';")

    return render(request, 'index.html')

def triangulate (request):

    request.session.clear()

    Point.objects.all().delete()
    Triangles.objects.all().delete()

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='news_point';")
    with connection.cursor() as cursor:
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name='news_point';")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='news_triangles';")
    with connection.cursor() as cursor:
        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name='news_triangles';")

    logon = 'qwert123'

    if request.POST:
        start = request.POST.get('datatime','2012-01-01T00:00')
        z=request.POST.get('z','sza')
    print(z)

    # if z!='sza':
    #     z=z.split()
    # else:
    #     z='sza'
    print(start)
    (status, stations) = SuperMAGGetInventory(logon, start, 3600)
    print(stations)
    print(len(stations))
    flagstring = "all"
    dc = {'FORMAT': 'list'}
    points_api = []
    stations_err = []

    import datetime

    # Get the current date and time
    start_time = datetime.datetime.now()

    # Simulate some processing time

    # time.sleep(5)

    import threading
    import queue

    # Создаем синхронизированную очередь
    queue_lock = threading.Lock()
    points_queue = queue.Queue()

    def get_data_for_station(station,z):
        status, data = SuperMAGGetData(logon, start, 3600, flagstring, station, **dc)
        queue_lock.acquire()

        try:
            # with queue_lock:
            if z!='sza':
                z=z.split()
                print(z)
                points_queue.put([data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0][z[0]][z[1]]])
                print(station, [data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0][z[0]][z[1]]])
            else:
                points_queue.put([data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0]['sza']])
                print(station, [data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0]['sza']])

        except:
            print('errrr')
            stations_err.append(station)
        # time.sleep(0.2)
        queue_lock.release()

    # Создаем список потоков и запускаем их
    threads = []
    for i in range(len(stations) - 1):
        t = threading.Thread(target=get_data_for_station, args=(stations[i],z))
        threads.append(t)
        t.start()

    # Ждем, пока все потоки завершат работу
    for t in threads:
        t.join()

    # Извлекаем данные из очереди
    points_api = []
    while not points_queue.empty():
        points_api.append(points_queue.get())


    def getst(station,z):
        status, data = SuperMAGGetData(logon, start, 3600, flagstring, station, FORMAT='list')
        try:
            with queue_lock:
                if z != 'sza':
                    z = z.split()
                    print(z)
                    points_queue.put([data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0][z[0]][z[1]]])
                    print(station, [data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0][z[0]][z[1]]])
                else:
                    points_queue.put([data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0]['sza']])
                    print(station, [data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0]['sza']])
        except:
            print('errr')

    threads1 = []
    for i in range(len(stations_err) - 1):
        t = threading.Thread(target=getst, args=(stations_err[i],z))
        threads1.append(t)
        t.start()
    for t in threads1:
        t.join()





    print(len(points_api))

    end_time = datetime.datetime.now()

    # Calculate the difference between the two times
    time_diff = end_time - start_time

    print(f"Processing time: {time_diff}")

    # points_api1=main()

    mer_points=[]
    mercator = Proj(proj='merc')


    points1=[[p[0],p[1],p[2],p[3]] for p in points_api if -85.0<p[1]]




    points_mer = [mercator(p[0], p[1]) for p in points1]


    points_api2=[]
    # преобразуем каждую точку в проекцию Меркатора
    for point in points1:

        # x, y = transformer.transform( point[0], point[1])
        x, y = mercator(point[0], point[1])

        # pointt = Point.objects.create(iaga=point[2], glon=x, glat=y,
        #                               sza=point[3])
        # pointt.save()
        # print("SAVEEEEE")
        mer_points.append([x, y])
        points_api2.append([x,y,point[2],point[3]])

    pointss_db = [Point(iaga=point[2], glon=point[0], glat=point[1], sza=point[3]) for point in points_api2]
    Point.objects.bulk_create(pointss_db)
    print("SAVEEEEE")
    val = Point.objects.get(id=1)
    print(type(val))
    print(val.get_glon_glat())


    def vert(lst) -> List[Vertex]:
        vertices: List[Vertex] = []

        for p in lst:
            vertices.append(
                Vertex(
                    x=p[0],
                    y=p[1]
                )
            )
        return vertices

    mer_points1=vert(mer_points)

    trii = delaunay(
        vertices=mer_points1,
        delete_super_shared=True)


    triangles3 = []
    for t in trii:
        triangles3.append([[v.x, v.y] for v in t.vertices])

    triangles_db=[]
    for triangle in triangles3:
        v1, v2, v3 = 0, 0, 0
        for i in range(3):
            for point_db in pointss_db:
                if triangle[i][0]==point_db.glon and triangle[i][1]==point_db.glat:
                      if v1==0:
                          v1=point_db
                      elif v2==0:
                          v2=point_db
                      elif v3==0:
                          v3 = point_db
                      elif v1!=0 and v2!=0 and v3!=0:
                           break
        triangles_db.append(Triangles(vertex1=v1,vertex2=v2,vertex3=v3))
    Triangles.objects.bulk_create(triangles_db)
    ll=Triangles.objects.all()
    triangles33=[tr.get_list() for tr in ll]
    pointss_db1=Point.objects.all()
    points_api2=[[point.glon,point.glat,point.iaga,point.sza]  for point in pointss_db1]
    print(len(triangles3))
    print(len(points_api2))
    data = {
        'triangles': triangles33,
        'points':[{'glon':point[0],'glat':point[1],'iaga':point[2], 'sza':point[3]} for point in points_api2]
    }




    return JsonResponse(data)


def inter(request):




    if request.method=='POST':
        mercator = Proj(proj='merc')
        # print('POSTPOST',request.method)
        json_data = json.loads(request.body)
        triangl = json_data.get('triangl', None)
        points = json_data.get('points')
        point = json_data.get('point',None)
        del_triangls=json_data.get('del_triangls',None)

        del_points=json_data.get('del_points', None)

        # print('PPPPPPOOOOOOOOINTTTT', point['x'],point['y'])
        # print('mecorator',mercator(-14.989422314802818,-68.57808523238243))
        if point == None:
            # i=0
            print('Triangl', triangl)
            # for tring in del_triangls:
            for ind in range(len(del_points)):
                print('TrianglLLLLLLLLLLLLLLLLLLL', del_triangls[ind])
                sza=[]
                count=0
                for p in points:
                    for i in range(3):
                        if p['merx']== del_triangls[ind][i][0] and p['mery']== del_triangls[ind][i][1] :
                            sza.append([p['merx'],p['mery'],p['sza']])
                            count+=1
                    if count == 3:
                        print('break')
                        print("333333", sza)
                        break
                # try:
                #     print('tryy')
                #     x,y =point['x'],point['y']
                # except:
                print('Удалленная точка', del_points[ind])
                print('Удалленный треугольник для нее',  del_triangls[ind])
                x,y = del_points[ind]['merx'], del_points[ind]['mery']
                Zxy=del_points[ind]['sza']
                print("SZAAAAAAAAAAAAAA", sza)
                Y1 = sza[0][1]
                Y2 = sza[1][1]
                Y3 = sza[2][1]
                X1 = sza[0][0]
                X2 = sza[1][0]
                X3 = sza[2][0]
                Z1 = sza[0][2]
                Z2 = sza[1][2]
                Z3 = sza[2][2]
                a = Y1 * (Z2 - Z3) + Y2 * (Z3 - Z1) + Y3 * (Z1 - Z2)
                b = Z1 * (X2 - X3) + Z2 * (X3 - X1) + Z3 * (X1 - X2)
                c = X1 * (Y2 - Y3) + X2 * (Y3 - Y1) + X3 * (Y1 - Y2)
                d = X1 * (Y2 * Z3 - Y3 * Z2) + X2 * (Y3 * Z1 - Y1 * Z3) + X3 * (Y1 * Z2 - Y2 * Z1)
                d = d * (-1)
                print()
                result = (-1) * (a * x + b * y + d) / c
                print('MYINTERPOL:ATIOOOONNNNNNNNNNNNNN', a * x + b * y + c * result + d == 0)
                result = round(result, 5)

                denominator = (X1 - X2) * (Y1 - Y3) + (X2 - X3) * (Y1 - Y2)


                a1 = ((Y3 - Y2) * (Z1 - Z2) + (Y1 - Y2) * (Z2 - Z3)) / denominator

                b1 = ((X2 - X3) * (Z1 - Z2) + (X1 - X2) * (Z2 - Z3)) / denominator

                c1 = Z2 - a1 * X2 - b1 * Y2

                zz = a1*X1 + b1*Y1 + c1
                zz2 = a1 * X2 + b1 * Y2 + c1
                zz3 = a1 * X3 + b1 * Y3 + c1

                print("Проверкаааа1",zz, '==', sza[0])
                print("Проверкаааа1", zz2, '==', sza[1])
                print("Проверкаааа1", zz3, '==', sza[2])
                print(zz==Z1)
                print(zz == Z2)
                print(zz == Z3)

                # a2 = (Z2 - Z1) / (X2 - X1)
                # b2 = (Z3 - Z1) / (Y3 - Y1)
                # c2 = Z1 - a2 * X1 - b2 * X1
                #
                # f = a2 * x + b2 * y + c2
                #Норм
                # dd = X1*(Y2-Y3) + X2*(Y3-Y1) + X3*(Y1-Y2)
                # d1 = x * (Y2 - Y3) + X2 * (Y3 - y) + X3 * (y - Y2)
                # d2 = X1 * (y - Y3) + x * (Y3 - Y1) + X3 * (Y1 - y)
                # d3 = X1 * (Y2 - y) + X2 * (y - Y1) + x * (Y1 - Y2)
                # f = (Z1*d1 +Z2*d2 +Z3*d3)/dd

                # dd = (X2 - X1) * (Y3 - Y1) - (X3 - X1) * (Y2 - Y1)
                # aa1 = ( (X2*Y3 -X3*Y2) +x*(Y2-Y3) + y*(X3-X2))/dd
                # bb1 = ((X3*Y1 -X1*Y3) +x*(Y3-Y1) + y*(X1-X3))/dd
                # cc1 = 1 - aa1 - bb1
                # print(aa1,bb1,cc1)
                # f = Z1 * aa1 + Z2 * bb1 + Z3 * cc1

                points2=[(pp['merx'],pp['mery']) for pp in points]

                sorted_points = sorted(points2, key=lambda p: math.dist( (del_points[ind]['merx'],del_points[ind]['mery']), p))
                print('closestPoints',sorted_points[:4])

                srtp=sorted_points[:4]
                Z_val=[]
                c=0
                for p in points:
                    for i in range(len(srtp)):
                      if p['merx'] == srtp[i][0] and p['mery'] == srtp[i][1]:
                          Z_val.append([srtp[i][0],srtp[i][1],p['sza']])
                          c+=1
                    if c==len(srtp):
                        print('BREAAAAAAAAAAAAAK  SORTEDDD_POINTSSSSSSSS')
                        break


                print('Z_VVVVVVVVAAAAAAALLLLLLL',Z_val)

                #иНТерполяци2
                # X1,Y1=srtp[0][0],srtp[0][1]
                # X2, Y2 = srtp[1][0], srtp[1][1]
                # a3 = (Z1*Y2 - Z2*Y1) / (X1*Y2 - X2*Y1)
                # b3 = (Z1*X2 - Z2*X1) / (Y1*X2 - Y2*X1)
                # c3 = Z1 - a3*X1 - b3*Y1


                distances = [math.dist((del_points[ind]['merx'],del_points[ind]['mery']), p) for p in srtp]
                print(distances)
                sum_weight=0
                sum=0
                for i in range(len(distances)):
                    sum_weight+=1/distances[i]
                    sum+=Z_val[i][2]*(1/distances[i])

                # weight1 = 1 / distances[0]
                #
                # weight2 = 1 / distances[1]
                #
                #
                # f = (Z_val[0][2] * weight1 + Z_val[1][2] * weight2) / (weight1 + weight2)
                f=sum/sum_weight


                print('ffffff',f)


                error1=((Zxy-result)/Zxy)*100
                error2 = ((Zxy - f) / Zxy) * 100
                del_points[ind]['error1'] = round(error1,6)
                del_points[ind]['error2'] = round(error2,6)
                # f=a3*x + b3*y + c3

                # zz12 = a3 * X1 + b3 * Y1 + c1
                # print("Провверка23333333333333122", zz12==Z1)
                # print(sza[0], Z1,zz12)

                linres= a1*x + b1*y +c1
                del_points[ind]['linres']= linres
                del_points[ind]['f'] = f


                # i+=1
                del_points[ind]['myz']=result
                # break

        else:

            delp= request.session.get('del', None)

            pointsdb = Point.objects.all()
            point_array = list(pointsdb.values())
            print('олучение удаленной',  delp)


            # triangles = [tr.get_list() for tr in Triangles.objects.all()]
            triangles_db = Triangles.objects.all()
            triangles_db1 = [tr.get_list() for tr in triangles_db]

            triangles = request.session.get('triangles',triangles_db1)
            points_arr = request.session.get('points', point_array)

            # print(triangles1)
            print(points_arr)
            # print(len(points_arr))

            result = interpolation_delone(triangles,  points_arr, point)

            print('Результат интерполяции на триангуляции после клика', result)
        data = {
            'res':result,
            'del_points':del_points
        }

        return JsonResponse(data)


def vallin(request):

    request.session.clear()

    json_data = json.loads(request.body)
    del_point= json_data.get('del_point', None)

    request.session['del'] = del_point
    # pointss_db = Point.objects.all()
    # points = [[point.glon, point.glat, point.iaga, point.sza] for point in pointss_db]
    pointsdb = Point.objects.all()
    points = list(pointsdb.values())
    # points=json_data.get('points', None)
    print(del_point)
    print('ДЛИНА ДО',len(points))
    for p in points:
        if p['iaga']==del_point['iaga']:
            print('УДАЛЯЕММММ',p)
            points.remove(p)
            break
    print(len(points))


    def vert(lst) -> List[Vertex]:
        vertices: List[Vertex] = []

        for p in lst:
            vertices.append(
                Vertex(
                    x=p['glon'],
                    y=p['glat']
                )
            )
        return vertices

    mer_points3 = vert(points)

    trii3 = delaunay(
        vertices=mer_points3,
        delete_super_shared=True)

    triangles33 = []
    for t in trii3:
        triangles33.append([[v.x, v.y] for v in t.vertices])

    request.session['triangles']=triangles33
    request.session['points']=points
    result = interpolation_delone(triangles33, points, del_point)

    Zxy=del_point['sza']
    points2 = [(pp['glon'], pp['glat']) for pp in points]

    sorted_points = sorted(points2, key=lambda p: math.dist((del_point['x'], del_point['y']), p))
    print('closestPoints', sorted_points[:4])

    srtp = sorted_points[:4]
    Z_val = []
    c = 0
    for p in points:
        for i in range(len(srtp)):
            if p['glon'] == srtp[i][0] and p['glat'] == srtp[i][1]:
                Z_val.append([srtp[i][0], srtp[i][1], p['sza']])
                c += 1
        if c == len(srtp):
            print('BREAAAAAAAAAAAAAK  SORTEDDD_POINTSSSSSSSS')
            break


    print('DEELLL',del_point)

    distances = [math.dist((del_point['x'], del_point['y']), p) for p in srtp]
    print(distances)
    sum_weight = 0
    sum = 0
    for i in range(len(distances)):
        sum_weight += 1 / distances[i]
        sum += Z_val[i][2] * (1 / distances[i])


    f = sum / sum_weight

    print('ffffff', f)
    print(result)

    error1 = ((Zxy - result) / Zxy) * 100
    error2 = ((Zxy - f) / Zxy) * 100
    print(error1)
    print(error2)

    del_point['error1'] = round(error1, 6)
    del_point['error2'] = round(error2, 6)

    del_point['f'] = f

    # i+=1
    del_point['myz'] = result


    data = {
        'triangles': triangles33,
        'points':points,
        'del_point':[del_point]
    }

    return JsonResponse(data)


from django.shortcuts import render
from django.http import HttpResponse

def index (request):
    return render(request, "index.html")


def triangulate (request):



    logon = 'qwert123'

    if request.POST:
        start = request.POST.get('datatime','2012-01-01T00:00')
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

    def get_data_for_station(station):
        status, data = SuperMAGGetData(logon, start, 3600, flagstring, station, **dc)
        queue_lock.acquire()
        try:
            # with queue_lock:
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
        t = threading.Thread(target=get_data_for_station, args=(stations[i],))
        threads.append(t)
        t.start()

    # Ждем, пока все потоки завершат работу
    for t in threads:
        t.join()

    # Извлекаем данные из очереди
    points_api = []
    while not points_queue.empty():
        points_api.append(points_queue.get())


    def getst(station):
        status, data = SuperMAGGetData(logon, start, 3600, flagstring, station, FORMAT='list')
        try:
            with queue_lock:
                points_api.append([data[0]['glon'], data[0]['glat'], data[0]['iaga'], data[0]['sza']])
                print([data[0]['iaga'], data[0]['glon'], data[0]['glat']])
        except:
            print('errr')

    threads1 = []
    for i in range(len(stations_err) - 1):
        t = threading.Thread(target=getst, args=(stations_err[i],))
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

        mer_points.append([x, y])
        points_api2.append([x,y,point[2],point[3]])



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



    data = {
        'triangles': triangles3,
        'points':[{'merx':point[0],'mery':point[1],'iaga':point[2], 'sza':point[3]} for point in points_api2]
    }




    return JsonResponse(data)

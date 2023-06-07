require([
        "esri/Map",
        "esri/views/SceneView",
        "esri/geometry/Point",
        "esri/Graphic",
        "esri/geometry/Polyline",
        "esri/geometry/Polygon",
        "esri/layers/GraphicsLayer",
        "esri/geometry/Circle",
        "esri/layers/TileLayer",
        "esri/layers/FeatureLayer",
        "esri/geometry/Extent",
        "esri/geometry/SpatialReference",
        "esri/PopupTemplate",
        "esri/layers/GeoJSONLayer",
        "esri/renderers/SimpleRenderer",
        "esri/symbols/SimpleFillSymbol",
        "esri/geometry/support/webMercatorUtils",
        "esri/geometry/geometryEngine",
        "esri/layers/support/LabelClass",
        "esri/symbols/TextSymbol",
        "dojo/domReady!"
      ], function(Map, SceneView, Point, Graphic, Polyline, Polygon, GraphicsLayer, Circle, TileLayer, FeatureLayer, Extent,SpatialReference, PopupTemplate, GeoJSONLayer, SimpleRenderer,SimpleFillSymbol,webMercatorUtils, geometryEngine,LabelClass, TextSymbol)
      {





        var map = new Map({
          basemap: "satellite",
           spatialReference: {wkid: 3857}
        });



       var graphicsLayer = new GraphicsLayer(new SpatialReference({ wkid: 3857}) );

        graphicsLayer.selectionEnabled = true;

        // установка режима выбора нескольких объектов
graphicsLayer.selectionMode = "extended";


       const fl = new FeatureLayer({
          url: "https://sampleserver6.arcgisonline.com/arcgis/rest/services/Census/MapServer/3"
        });
          // adds the layer to the map

       map.add(graphicsLayer);






          var view = new SceneView({
            container: "viewDiv",
            map: map,
            camera: {
              position: {
                latitude: 40,
                longitude: -100,
                z: 3000000
              },
              tilt: 0
            }

          });



console.log("VIEWWW",map.spatialReference)




        function addTriangles(triangles)
        {


         triangles.forEach(function(triangle) {
            // создаем полигон из трех вершин
            let polygon = new Polygon({
              rings: triangle,
              spatialReference:{wkid: 3857}
            });


<!--               wkid: 4326 3857-->

            var polygonGraphic = new Graphic({
                geometry: polygon,
                symbol: {
                  type: "simple-line",
                  style: "solid",
                  color:  [255, 0, 0],
                  width: 3
                  }
                });


          graphicsLayer.add(polygonGraphic);
 });
         }

           function addpoints2(points){
            console.log(points.length)
             console.log(points[0])

            var selectElement = document.getElementById("mySelect");
            var selectedValue = selectElement.value;
            console.log(selectedValue)

            for (var i = 0; i < points.length; i++) {
            var point = new Point({
              x: points[i]['x'],
              y: points[i]['y'],
               spatialReference:{wkid: 3857}
            });

             console.log('points[i].myz',points[i].myz)
            var pointGraphic = new Graphic({
              geometry: point,


              symbol: {
                type: "simple-marker",
                color: "blue",
                size: "14px"
              },
            attributes: {
              Name: "Точка",
              Lon: point.longitude,
              Lat: point.latitude,
              X:point.x,
              Y:point.y,
              IAGA:points[i].iaga,
              name_z:selectedValue.toUpperCase(),
              Z:points[i].sza,
              myZ:points[i].myz,
              linres:points[i].linres,
              f:points[i].f,
              er1:points[i].error1,
              er2:points[i].error2,
            },
//           <br>X:{X}<br>Y:{Y}
              popupTemplate: {
                title: "Координаты станции {IAGA}, {name_z}:{Z} ",
                content: "Долгота:{Lon}<br>Широта:{Lat}<br>Интерполяция методом TIN,{name_z}:{myZ}<br>Интерполяция методом IDW, {name_z}:{f}<br>Ошибка интерполяции TIN:{er1} %<br>Ошибка интерполяции IDW:{er2} %",
                 actions: [{
                            name: "deleteFeature",
                             title: "Удалить",
                              className: "esri-icon-trash",
                            id: "delete-feature"
                          }]
              }
            });

             graphicsLayer.add(pointGraphic);
          }
         }


         function addpoints(points){
            console.log(points.length)
             console.log(points[0])

            var pointSymbol = {
                      type: "point-3d",
                      symbolLayers: [{
                        type: "icon",
                        resource: {
                          primitive: "circle"
                        },
                        size: 10,
                        material: {
                          color: "green"
                        }
                      }]
                    };



            let selectElement = document.getElementById("mySelect");
            let selectedValue = selectElement.value;

            for (var i = 0; i < points.length; i++) {
            var point = new Point({
              x: points[i]['glon'],
              y: points[i]['glat'],
               spatialReference:{wkid: 3857}
            });




            let NEZ='NEZ';
            let title='Координаты были получены SZA';

            var pointGraphic = new Graphic({
              geometry: point,
//               symbol: pointSymbol,

              symbol: {
                type: "simple-marker",
                color: "green",
                size: "10px"
              },
            attributes: {
              Name: "Точка",
              Lon: point.longitude,
              Lat: point.latitude,
              X:point.x,
              Y:point.y,
              IAGA:points[i].iaga,
              Z:points[i].sza,
              name_z:selectedValue.toUpperCase()
            },
              popupTemplate: {
                title: "Координаты станции {IAGA}, {name_z}:{Z} ",
                content: "Долгота:{Lon}<br>Широта:{Lat}",
                 actions: [{
                            name: "deleteFeature",
                             title: "Удалить",
                              className: "esri-icon-trash",
                            id: "delete-feature"
                          }]
              }
            });

            var labelGraphic = new Graphic({
                geometry: point,
                symbol: {
                  type: "text",  // autocasts as new TextSymbol()
                  color: "white",
                  haloColor: "black",
                  haloSize: "1px",
                  text: points[i].iaga,
                  xoffset: 3,
                  yoffset: 5,
                  font: {  // autocasts as new Font()
                    size: 8,
                    family: "Josefin Slab",
                    weight: "bold"
                  }
                }
              });


//             graphicsLayer.add(pointGraphic);
              graphicsLayer.addMany([pointGraphic, labelGraphic]);

          }
         }


        console.log('graphicsLayer', graphicsLayer)
//          var xhr
          const formdata = document.getElementById('formdata')



          formdata.addEventListener('submit',function(e){



          e.preventDefault();
          let thisForm = e.target;
          let end = thisForm.getAttribute('action');
          let data = new FormData(thisForm);

          var xhr = new XMLHttpRequest();
          xhr.open('POST', '/triangulate/', true);
           if (graphicsLayer!=undefined)
                 graphicsLayer.removeAll();
          xhr.send(data);

          xhr.responseType='json';



          xhr.onload = function() {
           if (xhr.status === 200) {
           console.log("УСПЕЕЕЕЕХХХХХХХХХХХ");

           console.log(xhr.response.triangles);
           console.log(typeof(xhr.response));
//           requestInProgress=false;


           var response = xhr.response;



           triangles = response.triangles

<!--          var response = JSON.parse(xhr.response);-->

          addTriangles(triangles);

          var points = response.points;


          addpoints(points);

//код нажатия и созданитя точки



        }
        else{
        console.log('Ошибка запроса');
        }


    }




          console.log("EEEEEEEEEEEEEEEEEE BOYYYYYYYYY");

          function pointInTriangle1(point, triangle) {
  // Создаем многоугольник для заданного треугольника
          var polygon = new Polygon({
            rings: [triangle],
            spatialReference: { wkid: 3857 }
          });

          // Создаем точку для заданной точки
//          var pt = new Point({
//            longitude: point.longitude,
//            latitude: point.latitude,
//            spatialReference: { wkid: 3857 }
//          });

           var pt = new Point({
            x: point.x,
            y: point.y,
            spatialReference: { wkid: 3857 }
          });

          // Проверяем, содержится ли точка внутри треугольника
          return polygon.contains(pt);
        };

            function pointInTriangle2(point, triangle) {
  // Создаем многоугольник для заданного треугольника
          var polygon = new Polygon({
            rings: [triangle],
            spatialReference: { wkid: 3857 }
          });

          // Создаем точку для заданной точки
//          var pt = new Point({
//            longitude: point.longitude,
//            latitude: point.latitude,
//            spatialReference: { wkid: 3857 }
//          });

           var pt = new Point({
            x: point.merx,
            y: point.mery,
            spatialReference: { wkid: 3857 }
          });

          // Проверяем, содержится ли точка внутри треугольника
          return polygon.contains(pt);
        };


    });



const checkbox = document.getElementById("checkbox");


var flag = false;

checkbox.addEventListener("change", function() {
         if (this.checked) {
        flag = true;
              console.log("Пошлооооооооооо");}

              else{
              flag = false;
    console.log('НЕЛЬЗЯ')
    }
     });

    view.on("click", function(evt)
         {



     if (flag){

         console.log("Сработал POST для интерполяции")
          var point = view.toMap({x: evt.x, y: evt.y});

          console.log('Широта и долгота созданной точки',point.longitude,point.latitude)
          console.log('WEBmecorator созданной точки', point.x, point.y)

          const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

          var xhr1 = new XMLHttpRequest();

          xhr1.open('POST', '/triangulate/inter/', true);



          xhr1.setRequestHeader('X-CSRFToken', csrfToken);

          xhr1.responseType='json';

          var existingPoint = graphicsLayer.graphics.find(function(graphic) {
            return graphic.geometry.type === "point" &&
              graphic.geometry.x === point.x &&
              graphic.geometry.y === point.y;
          });

          // Проверяем, попадает ли точка внутрь каждого треугольника
//          var isInsideTriangle = triangles.find(function(triangle) {
//
//
//            return pointInTriangle1(point, triangle);
//
//          });

          json = JSON.stringify({
//                  triangl:isInsideTriangle,
//                  points:points,
                  point:point
               });


          xhr1.send(json);

          xhr1.onerror = function() {
            console.error("Request failed.");
          };


          if (existingPoint)
          {
            console.log("Точка СУЩЕСТВУЕТ");

          }

            var  selectElement2 = document.getElementById("mySelect");
      var selectedValue2 = selectElement2.value;


          if ( !existingPoint) {
            console.log("Точка находится внутри треугольника.");
//            console.log('triangll',  isInsideTriangle);

            xhr1.onload = function()
            {
                if (xhr1.status===200) {

                    var resp = xhr1.response;

                    console.log(resp);
                    let gr= new Graphic({geometry:point,
                    symbol: {
                        type: "simple-marker",
                        color: "green",
                        size: "10px"
                    },
                    attributes: {
                    Name: "Точка",
                    Lon: point.longitude,
                    Lat: point.latitude,
                    X:point.x,
                    Y:point.y,
                    // IAGA:points[i].iaga,
                    Z:resp['res'],
                    name_z:selectedValue2.toUpperCase()
                    },
                    popupTemplate: {
                        title: "Значение {name_z}, полученное с помощью метода TIN:{Z}  ",
                        content: "Долгота:{Lon}<br>Широта:{Lat}",
                        actions: [{
                            name: "deleteFeature",
                             title: "Удалить",
                              className: "esri-icon-trash",
                            id: "delete-feature"
                          }]
                    }

                    } )


                    graphicsLayer.add(gr);

             graphicsLayer.on("click", function(evt) {
             console.log('XMMMMMMMMMMMMMMMMMMMM');
                      var x = evt.pointGraphic.geometry.x;
                      var y = evt.pointGraphic.geometry.y;
                      console.log("QXXXXXXXXXXXXX: ", x, "Y: ", y);
                    });

              }
              else{
                console.error("Request failed with status code", xhr1.status)
              }
            };


        } else {
          console.log("Точка находится вне треугольника. На другой точке");
        }

    }


    });




                let del_point;
             function DeleteFeature() {

                         var selectElement = document.getElementById("mySelect");
                        var selectedValue = selectElement.value;
                        var int1 = document.getElementById("int1");
                            var int2 = document.getElementById("int2");
                            var d = int1.value;
                            var b = int2.value;

                        if (view.popup.selectedFeature) {
                          // удалить графический объект из слоя
                         const feature = view.popup.selectedFeature;
                        const geometry = feature.geometry;
                        const attributes=feature.attributes
                        console.log(attributes.X, attributes.Y, attributes.IAGA);
//                        console.log(geometry);
                        del_point = {'iaga':attributes.IAGA,
                                         'x':  geometry.x,
                                          'y': geometry.y,
                                           'sza': attributes.Z };
                        console.log(del_point);
                        const coordinates = geometry.type === "point" ? [geometry.x, geometry.y] : geometry.paths[0];
                        // сохранить координаты в переменную coordinates
//                        console.log('Длина перед',points.length);
//                        console.log('Длина перед',points);
                        console.log("Координаты точки:", coordinates);

////
                        let xhr3 = new XMLHttpRequest();

                               xhr3.responseType = 'json';

                              const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                              xhr3.open('POST', '/triangulate/vallin/', true);
//                              xhr3.open('POST', '/triangulate/inter/', true);

                              xhr3.setRequestHeader('X-CSRFToken', csrfToken);




                              json = JSON.stringify({
                                     del_point:del_point,
                                     selectedValue:selectedValue,
                                     d:d,
                                     b:b
                                   });

                                console.log(json);

                              xhr3.send(json);

                              xhr3.onload = function(){
                                  if (xhr3.status===200)
                                  {
                                  if (graphicsLayer!=undefined)
                                         graphicsLayer.removeAll();
                                  var resp3 = xhr3.response ;
                                  var tr=resp3.triangles;
                                  var pt = resp3.points;
                                  var dl = resp3.del_point;

                                     console.log('DLLLddddd',dl)
                                     console.log('TRRRRRRRRRRRR',tr)

                                     addTriangles(tr);
                                     addpoints(pt);
                                     addpoints2(dl);
//                                      let isInsideTriangle2 ;

//                                 for (let i=0;i<dl.length;i++){
////
//////                                 let closestPoints = geometryEngine.nearestVertices(pt, dl[i], 2);
//////                                 console.log('closestPoints ',closestPoints )
////
//                                   isInsideTriangle2 = tr.find(function(triangle) {
//
//                                           return pointInTriangle2(dl[i], triangle);
//                                          });
//                                          del_triangls.push(isInsideTriangle2);
//
//                                         }
//                                         console.log('isInsideTriangle2 ',del_triangls)

//                                      let xhr4 = new XMLHttpRequest();
//                                           xhr4.responseType = 'json';
//
//                                          const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//
//                                          xhr4.open('POST', '/triangulate/inter/', true);
//
//                                          xhr4.setRequestHeader('X-CSRFToken', csrfToken);


//                                          json = JSON.stringify({
//                                                    del_triangls:del_triangls,
//
//                                                  points:points,
//                                                  del_points:del_points,
//
//                                               });


//                                          xhr4.send(json);

//                                          xhr4.onload = function(){
//                                          if (xhr4.status===200){
//                                          var resp=xhr4.response;
//                                          console.log(resp.del_points);
//                                          addpoints2(resp.del_points);
//
//                                          }else{
//                                          console.log('ошибкааааа', xhr4.status)
//                                          }
//                                        }



                              }
                              else{
                              console.log('ERRRRRRRRROORRR',xhr3.status);
                              }
                            }




                              view.popup.selectedFeature.layer.remove(view.popup.selectedFeature);
                              // закрыть всплывающее окно
                              view.popup.close();
                         }


                        };




                                 view.popup.on("trigger-action", (event) => {
//                              id: "delete-feature",
                               if (event.action.id === "delete-feature") {
                                       DeleteFeature();
                                                     }

                                            });








    });
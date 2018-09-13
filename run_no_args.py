from shapefileClasses import ShapeGenerate
from functions.classes import GetData, ProcessData
from functions.types import esri_geometry,shape_types

url = '' # Query URL e.g. 'http://www2.lynxgis.com/arcgis/rest/services/LosGatos/TLGBuildings/MapServer/0/query'
output = '' # Name of output shapefile


params1 = {'where':'1=1', 'f':'pjson', "returnGeometry":"false","outFields":'*','returnIdsOnly':'true'  }
params2 = {'f':'pjson', 'where':'','outSR':'4326',"outFields":'*'}


shape = ShapeGenerate()




gets = GetData(url, params1)
gets.get_request()
oids = gets.data['objectIds']





print("Number of Features: {0}".format(len(oids)))
noids = len(oids)
loids = list(range(0,len(oids),500))

if len(oids)> 1000:


    start = 0
    for count,block in enumerate(loids[1:]):
        if count ==0:
            params2['objectIds'] = ",".join(map(str,oids[start:block]))
            gets = GetData(url, params2)
            gets.get_request_urllib()
            gets.create_fields()
            shape.create(esri_geometry[gets.data["geometryType"]])
            print("Geometry Type of Feature: {0}".format(shape_types[esri_geometry[gets.data["geometryType"]]]))
            fields = gets.fields

            process = ProcessData(gets.data, fields)
            process.create_geometries() 
            process.create_attributes() 

            for field in process.fields:
                shape.make_fields(field)

            for row in process.attributes:
                shape.process_atts(row)

            for geom in process.geometries:
                shape.process_geom(geom)
            print("Features: {0} to {1}".format(start+1,block))
        else:
            print("Features: {0} to {1}".format(start+1,block))
            params2['objectIds'] = ",".join(map(str,oids[start:block]))
            gets = GetData(url, params2)
            gets.get_request_urllib()
            process = ProcessData(gets.data, fields)

            process.create_geometries() 
            process.create_attributes() 


            for row in process.attributes:
                shape.process_atts(row)

            for geom in process.geometries:
                shape.process_geom(geom)

        start=block
    if len(oids) % block >0:
        print("Features: {0} to {1}".format(start+1,len(oids)))
        params2['objectIds'] = ",".join(map(str,oids[start:len(oids)]))
        gets = GetData(url, params2)
        gets.get_request_urllib()

        process = ProcessData(gets.data, fields)

        process.create_geometries() 
        process.create_attributes() 


        for row in process.attributes:
            shape.process_atts(row)

        for geom in process.geometries:
            shape.process_geom(geom) 
        
else:
    print("Features: {0} to {1}".format(1,len(oids)))
    params2['objectIds'] = ",".join(map(str,oids))
    gets = GetData(url, params2)
    gets.get_request_urllib()
    gets.create_fields()
    shape.create(esri_geometry[gets.data["geometryType"]])
    print("Geometry Type of Feature: {0}".format(shape_types[esri_geometry[gets.data["geometryType"]]]))
    fields = gets.fields

    process = ProcessData(gets.data, fields)
    process.create_geometries() 
    process.create_attributes() 

    for field in process.fields:
        shape.make_fields(field)

    for row in process.attributes:
        shape.process_atts(row)

    for geom in process.geometries:
        shape.process_geom(geom) 

shape.save(output)
# mapservicereader
Read data from a map service and write to a shapefile 

Python 2 and Python 3 compatible

Uses PySHP (shapefile.py) version 1.2.11 (will have to be rewritten to work with the brand new PySHP 2.0)

Pass command line arguments to run.py like this:

python run.py -u http://www2.lynxgis.com/arcgis/rest/services/Alameda/AlamedaBase/MapServer/12/query -o C:/Data/County


Parameters:

required:

-url, -u: the ArcServer MapServer Service to pull from

-output, -o: The filepath and name of the shapefile
	

optional:
	 
-srid, -s: SRID to be returned (defaults to 4326)


Required modules:

requests (included with Python 3)

PySHP (version is included with code as shapefile.py)

Known Issues:

Having trouble with some data fields when run using Python 2 (seems to be re-organizing fields)


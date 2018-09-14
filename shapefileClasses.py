import shapefile



class ShapeGenerate():
	
	def create(self, shapetype=1):
		self.writer = shapefile.Writer(shapeType=shapetype)


	def make_fields(self,field):
		if len(field)==2:
			self.writer.field(*field)
		else:
			if field[1]=='C':
				self.writer.field(field[0],field[1],size=field[2])
			elif field[1] in ('F','N'):
				self.writer.field(field[0],field[1],decimal=field[2])

	def process_atts(self,attributes):
		self.writer.record(*attributes)


	def process_geom(self, geom):
		if 'rings' in geom.keys():
			self.make_poly(geom['rings'])
		elif 'paths' in geom.keys():
			self.make_line(geom['paths'])
		else:
			self.make_point((float(geom['x']),float(geom['y']) ))


	def make_point(self, coords):
		self.writer.point(*coords) 

	def make_line(self, parts):
		self.writer.line(parts= parts) 

	def make_poly(self, parts):
		self.writer.poly(parts= parts) 

	def save(self, filename):
		self.writer.save(filename)
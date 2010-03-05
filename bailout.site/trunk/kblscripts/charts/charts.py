
import xml.etree.ElementTree as ET


class Chart():
    """Base class for SVG chart generation\n
       Data is expected in a list of lists, with (x,y) tuples:\n
            [ [(1, 2),(2, 3), ..], [...] ]\n
       
       or with labels instead of x values:\n
    
            [ [('risk transfers', 300), ('loans', 200), ..], ... ] \n

    """
    def __init__(self, height, width, data, chart_type, stylesheet=None, **kwargs):
        
        self.height = height
        self.width = width
        self.data = data
        self.type = chart_type
        self.number_of_series = len(data)
        self.max_x_value, self.max_y_value = self.find_maximum()        
        self.labels = self.extract_labels()
        self.stylesheet = stylesheet
        self.padding = 30
        self.y_scale = self.height / self.max_y_value
        
        #find the width of each point in each series
        self.x_scale = ((self.width - (self.padding * 2)) / self.number_of_series) / len(self.data[0])
         
        for key in kwargs:
            self.__dict__[key] = kwargs[key] 
 
        #create svg node as root element in tree
        self.svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1", background="white",  height=str(self.height), width=str(self.width) )
        self.svg.attrib["xmlns:svg"] = "http://www.w3.org/2000/svg"
    
        #there really isn't a graceful way for loading an external stylesheet when you're not in a browser
        temp = []
        stylesheet = open(self.stylesheet, 'r')
        for x in stylesheet.readlines():
            temp.append(x)
             
        self.svg.append(ET.XML('<style type="text/css">' + "\n".join(temp)  + '</style>'))
        self.setup_chart()

    def find_maximum(self):
                
        max_x_value = 0
        max_y_value = 0

        for series in self.data:
            for point in series:
                if not isinstance(point[0], "".__class__) and point[0] > max_x_value: max_x_value = point[0]
                if not isinstance(point[1], "".__class__) and point[1] > max_y_value: max_y_value = point[1]
 
        return [max_x_value, max_y_value]

    def extract_labels(self):
        
        labels = []

        for series in self.data:
            for point in series:
                if isinstance(point[0], "".__class__):
                    if not point[0] in labels: labels.append(point[0])

    def setup_chart(self):

        #First, add x and y axes
        x_axis, y_axis = [ET.Element("g", id="x_axis"), ET.Element("g", id="y_axis")]
        x_axis.attrib['class'], y_axis.attrib['class'] = ['x-axis', 'y-axis']

        x_axis_path = ET.Element("path", d="M %d %d L %d %d" % (self.padding, self.height - self.padding, self.width - self.padding, self.height - self.padding))
        x_axis_path.attrib['class'] = 'x-axis-path'

        x_axis.append(x_axis_path)

        y_axis_path = ET.Element("path", d="M %d %d L %d %d" % (self.padding, self.height - self.padding, self.padding, self.padding))
        y_axis_path.attrib['class'] = 'y-axis-path'

        y_axis.append(y_axis_path)
    
        grid_space = (self.height - (self.padding * 2)) / 10
    
        for i in range(1, 10):

            gridline = ET.Element("path", d="M %d %d L %d %d" % (self.padding, (i * grid_space) + self.padding , self.width - self.padding, (i * grid_space) + self.padding))
            gridline.attrib['class'] = 'y-gridline'
            y_axis.append(gridline)

        self.svg.append(x_axis)
        self.svg.append(y_axis)

        #TO DO: add another y axis, change this method for Pie charts, add x gridlines


class Column(Chart):
    """Subclass of Chart class, specific to an n-series column chart """
    
    def set_background(self):
        #add x axis
        #self.svg.append('<g id="x_axis" ><path d="M 0,%d %d,%d" style="fill:none; stroke: #a7a9ac; stroke-width:1; stroke-opacity:1" /></g>"\n' % (self.height, self.width, self.height))
        pass
        
   
    def output(self):
        
        print ET.dump(ET.ElementTree(self.svg))
        stylesheet = open(self.stylesheet,'r')

        f = open("test.svg", 'w')
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
#        f.write('<?xml-stylesheet type="text/css" href="charts.css" ?>\n')
        f.write(ET.tostring(self.svg) )
    


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
        self.max_x_value, self.max_y_value, self.max_data_points = self.find_maximum()        
        self.labels = self.extract_labels()
        self.stylesheet = stylesheet
        self.padding = 30
        self.x_padding = 10
        self.x_inner_padding = 5
        self.y_inner_padding = 5
        self.y_scale = (self.height - (self.padding * 2)) / self.max_y_value
        
        #find the width of each point in each series
        #self.x_scale = (((self.width - (self.padding * 2)) / self.number_of_series) / self.max_data_points) - self.x_padding
        self.x_scale = int(float((float(self.width - (self.padding * 2)) / self.max_data_points) / self.number_of_series) - self.x_padding)
        #width of each data point grouping over multiple series
        self.x_group_scale = self.x_scale * self.number_of_series

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
        self.data_series()
        self.set_labels()

    def find_maximum(self):
                
        max_x_value = 0
        max_y_value = 0
        current_max = 0
        max_count = 0

        for series in self.data:

            for point in series:

                max_count += 1
                if not isinstance(point[0], "".__class__) and point[0] > max_x_value: max_x_value = point[0]
                if not isinstance(point[1], "".__class__) and point[1] > max_y_value: max_y_value = point[1]
            if max_count > current_max: current_max = max_count
            max_count = 0

        return [max_x_value, max_y_value, current_max]

    def extract_labels(self):
        
        labels = []

        for series in self.data:
            for point in series:
                if isinstance(point[0], "".__class__):
                    if not point[0] in labels: labels.append(point[0])

        return labels

    def setup_chart(self):

        #setup background color
        self.svg.append(ET.Element("rect", x="0", y="0", height="%s" % self.height, width="%s" % self.width, fill="white"))

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
        
    def data_series(self):

        series_count = 0
        left_offset = self.padding  
        bottom_offset = self.padding

        for series in self.data:

            series_count += 1
            data_point_count = 0

            for point in series:
            
                width = self.x_scale
                height = self.y_scale * point[1]
                x_position = left_offset + self.x_padding + (data_point_count * (self.x_group_scale + self.x_padding) ) + ((series_count - 1) * width)
                y_position = bottom_offset + (( self.height - (bottom_offset * 2)) - height )
                data_point = ET.Element("rect", x="%s" % x_position, y="%s" % y_position, height="%s" % height, width="%s" % width  )
                data_point.attrib['class'] = 'series-%s-point' % series_count

                data_point_inner = ET.Element("rect", x="%s" % (x_position + self.x_inner_padding), y="%s" % (y_position + self.y_inner_padding), height="%s" % (height - self.y_inner_padding), width="%s" % (width - (2  * self.x_inner_padding))  )
                data_point_inner.attrib['class'] = 'series-%s-point-inner' % series_count

                self.svg.append(data_point)
                self.svg.append(data_point_inner)
                data_point_count += 1

    def set_labels(self):
        label_count = 0

        for l in self.labels:
            text_item = ET.Element("text", x="%s" % (self.padding + (self.x_group_scale / 2) + (label_count * (self.x_group_scale + self.x_padding))), y="%s" % (self.height - self.x_padding), width="%s" % self.x_group_scale) 
            
            text_item.text = l
            text_item.attrib['class'] = 'x-axis-label'
            self.svg.append(text_item)
            label_count += 1


    def output(self):
       
        for x in self.__dict__.keys():
            print "%s : %s\n" % (x, self.__dict__[x]) 

        print ET.dump(ET.ElementTree(self.svg))
        stylesheet = open(self.stylesheet,'r')

        f = open("test.svg", 'w')
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
#        f.write('<?xml-stylesheet type="text/css" href="charts.css" ?>\n')
        f.write(ET.tostring(self.svg) )
    

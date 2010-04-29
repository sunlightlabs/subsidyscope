
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import math

CURRENCY = [( 10**3, 'Th'), (10**6, 'M'), (10**9, 'B'), (10**12, 'Tr')]


class Chart(object):
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
        self.labels = self.extract_labels()
        self.stylesheet = stylesheet
        self.padding = 30
        self.x_padding = 10
        self.y_padding = 0
        self.x_label_height = 15
        self.y_label_padding = 5
        self.y_label_height = 15
        self.x_inner_padding = 2
        self.y_inner_padding = 2
        self.label_intervals = 1
        self.gridline_percent = .15
        #change these to be passed in
        self.currency = True
        self.units = 'B'
 
        #create svg node as root element in tree
        self.svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1", height=str(self.height), width=str(self.width) )
        self.svg.attrib["xmlns:svg"] = "http://www.w3.org/2000/svg"
         
        #there really isn't a graceful way for loading an external stylesheet when you're not in a browser so we parse it in and spit it out inside style tags
        temp = []
        stylesheet = open(self.stylesheet, 'r')
        for x in stylesheet.readlines():
            temp.append(x)
             
        self.svg.append(ET.XML('<style type="text/css">' + "\n".join(temp)  + '</style>'))


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
                #if isinstance(point[0], "".__class__):
                if not point[0] in labels: labels.append(point[0])

        return labels

    def output(self, write_file):
       
        #DEBUG - Dump properties
        for x in self.__dict__.keys():
            print "%s : %s\n" % (x, self.__dict__[x]) 

        txt = ET.tostring(self.svg)
        print parseString(txt).toprettyxml()

        f = open(write_file, 'w')
        f.write(parseString(txt).toprettyxml() )
   
class PieChart(Chart):
    """Subclass of Chart, containing functions relevant to all pie charts"""

    def __init__(self, height, width, data, chart_type, stylesheet=None, **kwargs):

        self.legend_width = 40 
        self.legend_x_padding = 5

        super(PieChart, self).__init__(height, width, data, chart_type, stylesheet, **kwargs)
        
        #find sum of values, only needed for pie charts
        self.total = 0
        for series in self.data:
            for point in series:
                self.total += point[1]
        
        self.diameter = self.width - (self.x_padding * 2) - self.legend_width
        self.radius = self.diameter / 2
        self.x_origin = self.x_padding + (self.diameter / 2)
        self.y_origin = self.height / 2
        
        #Chart subclass should have this method to setup the chart background, axes, and gridlines
        self.setup_chart()

        #Chart subclass should have this method to chart the data series
        self.data_series()

    def setup_chart(self):
        
        #attach stage element
        self.svg.append(ET.Element("rect", x="0", y="0", height="%s" % self.height, width="%s" % self.width, fill="white"))

    def data_series(self):

        total_angle = 0
        count = 1
        last_point = [self.radius, 0]
        arc = 0 #draw the short arc by default
        for series in self.data:
            for point in series:
                angle = (point[1]  / float(self.total)) * 360
                total_angle += angle
                if angle > 180:
                    arc = 1  #draw the long arc

                point1 = "M %s,%s " % (self.x_origin, self.y_origin)
                point2 = "l %s,%s " % (last_point[0], -last_point[1])

                x = int(math.cos(math.radians(total_angle)) * self.radius)
                y = int(math.sin(math.radians(total_angle)) * self.radius)
               
                point3 = "a%s,%s 0 %s,0 %s,%s z" % (self.radius, self.radius, arc, (x - last_point[0]), -(y - last_point[1]))
                last_point = [x, y]
                end = " " 
                path = ET.Element("path", d="%s %s %s" % (point1, point2, point3))
                path.attrib['class'] = 'slice-%s' % count
                self.svg.append(path)
                count += 1


    
class GridChart(Chart):
    """Subclass of Chart, containing functions relevant to all charts that use a grid"""
    def __init__(self, height, width, data, chart_type, stylesheet=None, **kwargs):

        super(GridChart, self).__init__(height, width, data, chart_type, stylesheet, **kwargs)
        #Catch passed in keyword argument overrides of defaults
        for key in kwargs:
            self.__dict__[key] = kwargs[key] 

        #set the baseline coordinates of the actual grid
        self.grid_y1_position = self.padding + self.y_padding
        self.grid_y2_position = self.height - self.x_label_height - self.padding - self.y_padding
        self.grid_x1_position = self.padding + self.x_padding
        self.grid_x2_position = self.width - self.padding - self.x_padding
        self.grid_height = self.grid_y2_position - self.grid_y1_position
        self.grid_width = self.grid_x2_position - self.grid_x1_position

        #where and how often for gridlines
        self.max_x_value, self.max_y_value, self.max_data_points = self.find_maximum()        
        self.gridline_interval = self.gridline_percent * self.grid_height #in pixels
        self.gridlines = int(self.grid_height / self.gridline_interval)
        self.max_y_axis_value = self.max_y_value + (self.max_y_value * .1)
        self.y_scale = self.grid_height / float(self.max_y_axis_value)


        #find the width of each point in each series
        self.x_scale = self.set_scale()
        
        #width of each data point grouping over multiple series
        self.x_group_scale = self.x_scale * self.number_of_series
        
        #Chart subclass should have this method to setup the chart background, axes, and gridlines
        self.setup_chart()

        #Chart subclass should have this method to chart the data series
        self.data_series()
        self.set_labels()
         
    def setup_chart(self):

        #setup background color
        self.svg.append(ET.Element("rect", x="0", y="0", height="%s" % self.height, width="%s" % self.width, fill="white"))
        self.grid = ET.Element("g", id="grid", transform="translate(%s, %s)" % (self.grid_x1_position, self.grid_y1_position))

        self.svg.append(self.grid)

        #add x and y axes
        x_axis, y_axis = [ET.Element("g", id="x_axis"), ET.Element("g", id="y_axis")]
        x_axis.attrib['class'], y_axis.attrib['class'] = ['x-axis', 'y-axis']

        x_axis_path = ET.Element("path", d="M %d %d L %d %d" % (0, self.grid_height, self.grid_width, self.grid_height))
        x_axis_path.attrib['class'] = 'x-axis-path'

        x_axis.append(x_axis_path)

        y_axis_path = ET.Element("path", d="M %d %d L %d %d" % (0, self.grid_height, 0, 0))
        y_axis_path.attrib['class'] = 'y-axis-path'

        y_axis.append(y_axis_path)
        
        y_axis_path2 = ET.Element("path", d="M %d %d L %d %d" % (self.grid_width, self.grid_height, self.grid_width, 0))    
        y_axis_path2.attrib['class'] = 'y-axis-path-2'

        y_axis.append(y_axis_path2)

        grid_space = self.grid_height / self.gridlines
   
        grid_value_increment = self.max_y_axis_value / self.gridlines
         
        for i in range(0, self.gridlines):
            #draw the gridline
            gridline = ET.Element("path", d="M %d %d L %d %d" % (0, (i * grid_space), self.grid_width, (i * grid_space)))
            gridline.attrib['class'] = 'y-gridline'
            y_axis.append(gridline)

            #draw the text label
            gridline_label = ET.Element("text", x="%s" % (-self.y_label_padding), y="%s" % ( (i * grid_space) ) )
            num = self.max_y_axis_value - (i * grid_value_increment)
            text = "%s" % num
            text = self.convert_units(num)

            gridline_label.text = text
            gridline_label.attrib['class'] = 'y-axis-label'
            y_axis.append(gridline_label)

        self.grid.append(x_axis)
        self.grid.append(y_axis)

    def data_point_label(self, value, x, y):
        dp_label = ET.Element("text", x="%s" % x, y="%s" % y)
        text = str(value)
        text = self.convert_units(value)
        dp_label.text = "%s" % text
        dp_label.attrib['class'] = 'data-point-label'
        self.grid.append(dp_label)

    def convert_units(self, value):
        text = ""
        if self.currency:
            text = "$"
        for unit in reversed(CURRENCY):
            if value / float(unit[0]) >= 1:
                print value / float(unit[0])
                text = text + "%.1d" % (value / float(unit[0]))
                if self.units:
                    text = text + unit[1]
                return text
                break

        return str(value)



class Line(GridChart):

    def set_scale(self):
        #pixels between data points
        return int(float(self.width - (self.padding * 2) - (self.x_padding * 2) ) / (self.max_data_points - 1) )

    def data_series(self):
        
        series_count = 0
        left_offset = self.padding  
        bottom_offset = self.padding
        g_container = ET.Element('g')

        for series in self.data:

            series_count += 1
            data_point_count = 0

            #move path to initial data point
            path_string = "M %s %s" % (self.x_padding, self.grid_height - (series[0][1] * self.y_scale))

            for point in series:

                if data_point_count == 0: 
                    data_point_count += 1
                    continue
                     
                path_string += " L "
                x = int(data_point_count * self.x_scale)                
                point_height = self.y_scale * point[1]                
                y = self.grid_height - point_height
    
                path_string += "%s %s" % (x, y)

                data_point_count += 1
                
                #put point markers in here at some point?

            line = ET.Element("path", d=path_string)
            line.attrib['class'] = 'series-%s-line' % series_count
            g_container.append(line)
        
        self.grid.append(g_container)
    
    def set_labels(self):

        label_count = 0

        for l in self.labels:

            if  label_count % self.label_intervals == 0:
                text_item = ET.Element("text")
                text_item.attrib['x'] = "%s" % (self.x_padding + (label_count * self.x_scale))
                text_item.attrib['y'] = "%s" % (self.grid_height + self.x_label_height) 
                text_item.text = "%s" % l
                text_item.attrib['class'] = 'x-axis-label'
                self.grid.append(text_item)

            label_count += 1


class Column(GridChart):
    """Subclass of GridChart class, specific to an n-series column chart """
    
    def set_scale(self):
        
        return (self.grid_width / self.max_data_points / self.number_of_series) - self.x_padding

    def data_series(self):

        series_count = 0
        left_offset = self.padding  
        bottom_offset = self.padding

        for series in self.data:

            series_count += 1
            data_point_count = 0

            for point in series:
            
                point_width = self.x_scale
                point_height = self.y_scale * point[1]
                x_position = (data_point_count * (self.x_group_scale + self.x_padding) ) + ((series_count - 1) * point_width)
                y_position = (self.grid_height - point_height)
                data_point = ET.Element("rect", x="%s" % x_position, y="%s" % y_position, height="%s" % point_height, width="%s" % point_width  )
                data_point.attrib['class'] = 'series-%s-point' % series_count

                data_point_inner = ET.Element("rect", x="%s" % (x_position + self.x_inner_padding), y="%s" % (y_position + self.y_inner_padding), height="%s" % (point_height - self.y_inner_padding), width="%s" % (point_width - (2  * self.x_inner_padding))  )
                data_point_inner.attrib['class'] = 'series-%s-point-inner' % series_count

                self.grid.append(data_point)
                self.grid.append(data_point_inner)

                self.data_point_label(point[1], x_position + (point_width / 2), y_position - 5)
                data_point_count += 1

    def set_labels(self):
        label_count = 0

        for l in self.labels:
            text_item = ET.Element("text", x="%s" % (int(self.x_padding + (self.x_group_scale / 2) + (label_count * (self.x_group_scale + self.x_padding)))), y="%s" % (self.grid_height + self.x_label_height))
            
            text_item.text = l
            text_item.attrib['class'] = 'x-axis-label'
            self.grid.append(text_item)
            label_count += 1



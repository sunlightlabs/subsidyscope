
	import flash.display.DisplayObject;
	import flash.display.Graphics;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.filesystem.*;
	import flash.net.FileFilter;
	import flash.utils.ByteArray;

	
	flash.utils.ByteArray;
	
	import flash.geom.Rectangle;


	import flash.events.Event;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.net.FileReference;
	
	import org.vanrijkom.shp.*;
	import org.vanrijkom.dbf.*;
	
	import flash.geom.Point;
	import flash.events.MouseEvent;


    	private var s: Sprite = new Sprite();
	    private var g: Graphics = s.graphics;

		private var mapData:Object = new Object;
		private var counties:Array = new Array;

		private var dbf:ByteArray = new ByteArray();
		private var shp:ByteArray = new ByteArray();
		
		
		public function loadShapefile()
		{
			var fileToOpen:File = new File();
			var txtFilter:FileFilter = new FileFilter("Shapefile", "*.shp");
			
			try 
			{
			    fileToOpen.browseForOpen("Open", [txtFilter]);
			    fileToOpen.addEventListener(Event.SELECT, fileSelected);
			}
			catch (error:Error)
			{
			    trace("Failed:", error.message);
			}
			
			function fileSelected(event:Event):void 
			{
				
			    var shp_fs:FileStream = new FileStream();
			    shp_fs.open(File(event.target), FileMode.READ);
			    
			    var dbf_path:String = File(event.target).nativePath
			    
			    var path_parts:Array = dbf_path.split(".");
			    
			    dbf_path = path_parts[0] + "." + "dbf";
			    
			    var dbf_fs:FileStream = new FileStream();
			    dbf_fs.open(new File(dbf_path), FileMode.READ);
			   
			   	dbf = new ByteArray();
				shp = new ByteArray();
			   
			   	shp_fs.readBytes(shp);
			   	dbf_fs.readBytes(dbf);
			   	
			   	load();	
			}
		}
		
		public function dbfCompleteHandler(event:Event)
		{
			var loader:URLLoader = URLLoader(event.target);
			
			dbf = loader.data;
			
			if(dbf && shp)
				load();
		}
		
		public function shpCompleteHandler(event:Event)
		{
			var loader:URLLoader = URLLoader(event.target);
			
			shp = loader.data;
			
			if(dbf && shp)
				load();	
		}
		
		
		public function load()
		{			
			mapData = new Object;
			counties = new Array;	
		
			var dbfHeader: DbfHeader = new DbfHeader(dbf);

	        // ShpTools.drawPolyShpFile methods reads a SHP file header,
	        // and traverses all Polygon or Polyline records in it. The
	        // foung objects get drawn to Graphics instance g using the
	        // Flash drawing API
	        
	        var header:ShpHeader = new ShpHeader(shp);
	        
	        var data:Array = ShpTools.readRecords(shp)
	        
	        var minX:Number = 0;
	        var minY:Number = 0;
	        var maxX:Number = 0;
	        var maxY:Number = 0;
	        
	        var firstShape:Boolean = true;
	        
	        for each(var record:ShpRecord in data)
	        {
	        	if(record.shape != null)
	        	{
	        		var rect:Rectangle = ShpPolygon(record.shape).box;
	        		
	        		if(firstShape)
	        		{
	        			firstShape = false;
	        			minY = rect.top;
	        			maxY = rect.bottom;
	        			minX = rect.left;
	        			maxX = rect.right;
	        		}
	        		else
	        		{
			        	if(minY > rect.top)
			        		minY = rect.top;
			        	if(maxY < rect.bottom)
			        		maxY = rect.bottom;
			        	
						if(minX > rect.left)
			        		minX = rect.left;
			        	if(maxX < rect.right)
			        		maxX = rect.right;
			        }
	        	}
	        }
	        
	      
	        
	        var yOffset:Number = 0;
	        var xOffset:Number = 0;
	        
	        if(minY < 0)
	        	yOffset = Math.abs(minY);
	        else
	        	yOffset = 0 - minY;
	        	
	        if(minX < 0)
	        	xOffset = Math.abs(minX);
	        else
	        	xOffset = 0 - minX;
	        
	        
	      	minX = minX + xOffset;
	        minY = minY + yOffset;
	        maxX = Math.abs(maxX + xOffset);
	        maxY = maxY + yOffset;
	        
//	        firstShape = true;
//	        
//	        for each(var record:ShpRecord in data)
//	        {
//	        	if(record.shape != null)
//	        	{
//	        		if(firstShape)
//	        		{
//	        			firstShape = false;
//	        			minY = rect.top;
//	        			maxY = rect.bottom;
//	        			minX = rect.left;
//	        			maxX = rect.right;
//	        		}
//	        		
//		        	var rect:Rectangle = ShpPolygon(record.shape).box;
//		        	if(minY > rect.top + yOffset)
//		        		minY = rect.top + yOffset;
//		        	if(maxY < rect.bottom + yOffset)
//		        		maxY = rect.bottom + yOffset;
//		        		
//		        	if(minX > rect.left + xOffset)
//		        		minX = rect.left + xOffset;
//		        	if(maxX < rect.right + xOffset)
//		        		maxX = rect.right + xOffset;
//		        }
//	        }
	        
	        var aspect:Number = maxY / maxX;
	        
	       	var yScale:Number = 5000 / maxX;
	       	var xScale:Number = 5000 / maxY;
	        
	        yOffset = yOffset * yScale;
	        xOffset = xOffset * xScale;
	        
	        mapData.aspect = aspect;
	        
	        var strHelper:StringHelper = new StringHelper();
	        
	        var i = 0;
	        for each(var record:ShpRecord in data)
	        {
	        	if(record.shape != null)
	        	{
		        	var shape:ShpPolygon = ShpPolygon(record.shape);	
		        	
		        	var dbfRecord:DbfRecord = DbfTools.getRecord(dbf, dbfHeader, i); 
	
		        	if(i==33)
		        		trace(i);
		        	var county:Object = new Object;
		        	
		        	county.rings = new Array;
		        	county.name = strHelper.trim(dbfRecord.values['NAME'], " ");
		        	county.id = int(dbfRecord.values['STATE']);// + dbfRecord.values['COUNTY']); 
		        	county.state = int(dbfRecord.values['STATE']); 
		        	//county.county = int(dbfRecord.values['COUNTY']);
		        	
		        	
		        	for each(var ring:Array in shape.rings)
		        	{
		        		var newRing:Array = new Array;
		        		for each(var point:ShpPoint in ring)
		        		{
		        			var intX = int(((point.x) * xScale) + xOffset);
		        			var intY = int(((point.y) * yScale) + yOffset);
		        			var p:Object = new Object;
		        			p.x = intX;
		        			p.y = intY;
		        			
		        			newRing.push(p);
		        		}
		        		
		        		county.rings.push(newRing);
		        	}
		        	
		        	counties.push(county);
		        }
		        else
		        {
		        	var dbfRecord:DbfRecord = DbfTools.getRecord(dbf, dbfHeader, i); 
		        	trace(dbfRecord);
		        }
	        	i++;
	        }
	        	
	        g.clear();
	        s.scaleX = 1;	
	        s.scaleY = 1;
	        
	        for each(var p:Object in counties) {	
	        	g.lineStyle(0.001,0x606060);
            	
            	if(p.id == 6)
            		g.beginFill(0xf0c0c0);
            	else
            		g.beginFill(0xc0c0f0);
	        			
				for each(var r: Array in p.rings) {
					if (r.length) {
						g.moveTo(r[0].x,-r[0].y);
					}
					for (var i=1; i<r.length; i++)
						g.lineTo(r[i].x,-r[i].y);				
				}
			} 
			
			
			s.scaleX = 0.05//750 / s.width;
			s.scaleY = 0.5//750 / s.height;
			
		   	                
	        // add sprite to canvas:
	        if(!this.mapCanvas.rawChildren.contains(s))
	        	this.mapCanvas.rawChildren.addChild(s);
	        
	        //s.x = 400;    
	        s.y = 400;
	        // scale the clip to nicely fit our canvas:        
	        //scaleToFitCanvas(s,shp,z);        
	    
	    	//s.addEventListener(MouseEvent.CLICK, saveFile);    
		}
		
		public function saveFile():void
		{
			mapData.data = counties
			
			var encodedShp = encode(mapData);
	        
	        var fR:FileReference = new FileReference();
	 
	        fR.save(encodedShp,"states.map");	
		}
		
		public function scaleToFitCanvas(t: DisplayObject, shp: ShpHeader, zoom: Number): void 
		{
	        // fit to requested width/height:
	        var r: Rectangle     = getBounds(t);        
	        var f: Number         = Math.min
	                                ( stage.stageHeight / r.height
	                                , stage.stageWidth / r.width
	                                );
	        
	        // set calculated scale:
	        if (f!=Infinity) 
	            t.scaleX = t.scaleY = f;
	        
	        // maintain top-left position:
	        t.x = -shp.boundsXY.left * zoom * f;
	        t.y = (shp.boundsXY.bottom-shp.boundsXY.top) * zoom * f;        
	    }
	    
	    function encode(object:*):ByteArray {

			var bytes:ByteArray = new ByteArray();
			bytes.writeObject(object);
			bytes.compress()
			bytes.position = 0;

			return bytes;
		
		}
		
		function decode(bytes:ByteArray):* {

			bytes.position = 0;
			bytes.uncompress();

			return bytes.readObject();
			
		}
		


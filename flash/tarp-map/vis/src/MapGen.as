package
{
	import flash.display.DisplayObject;
	import flash.display.Graphics;
	import flash.display.Sprite;
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

	[SWF(width="2500", height="2500", backgroundColor="#ffffff", frameRate="30")]
	public class MapGen extends Sprite
	{
    	private var s: Sprite = new Sprite();
	    private var g: Graphics = s.graphics;

		private var mapData:Object = new Object;
		private var counties:Array = new Array;

		private var dbf:ByteArray;
		private var shp:ByteArray;
		
		
		
		public function MapGen()
		{
			super();
			
			var shapefileRequest:URLRequest = new URLRequest("co99_d00_reprojected_lower48_25percent_clean.shp");
			//co99_d00_reprojected_lower48_25percent_clean.shp
			//st99_d00_lower48_25percent_clean.shp
			
			var shapefileLoader:URLLoader = new URLLoader();
			shapefileLoader.dataFormat = URLLoaderDataFormat.BINARY;
		
			shapefileLoader.addEventListener(Event.COMPLETE, shpCompleteHandler); 

					
			var dbfRequest:URLRequest = new URLRequest("co99_d00_reprojected_lower48_25percent_clean.dbf")
			//co99_d00_reprojected_lower48_25percent_clean.dbf
			//st99_d00_lower48_25percent_clean.dbf
		
			var dbfLoader:URLLoader = new URLLoader();
			dbfLoader.dataFormat = URLLoaderDataFormat.BINARY;
			
			dbfLoader.addEventListener(Event.COMPLETE, dbfCompleteHandler); 

            try {
                shapefileLoader.load(shapefileRequest);
                dbfLoader.load(dbfRequest);
            } catch (error:Error) {
                trace("Unable to load requested document.");
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
	        
	        for each(var record:ShpRecord in data)
	        {
	        	if(record.shape != null)
	        	{
		        	var rect:Rectangle = ShpPolygon(record.shape).box;
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
	        
	        var aspect:Number = (maxY - minY) / (maxX - minX)
	        var xScale:Number = 5000 / (maxX - minX);
	        var yScale:Number = 5000 / (maxY - minY);
	        
	        mapData.aspect = aspect;
	        
	        var strHelper:StringHelper = new StringHelper();
	        
	        var i = 0;
	        for each(var record:ShpRecord in data)
	        {
	        	if(record.shape != null)
	        	{
		        	var shape:ShpPolygon = ShpPolygon(record.shape);	
		        	
		        	var dbfRecord:DbfRecord = DbfTools.getRecord(dbf, dbfHeader, i); 
	
		        	
		        	var county:Object = new Object;
		        	county.rings = new Array;
		        	county.name = strHelper.trim(dbfRecord.values['NAME'], " ");
		        	county.id = int(dbfRecord.values['STATE'] + dbfRecord.values['COUNTY']); 
		        	county.state = int(dbfRecord.values['STATE']); 
		        	county.county = int(dbfRecord.values['COUNTY']);
		        	
		        	
		        	for each(var ring:Array in shape.rings)
		        	{
		        		var newRing:Array = new Array;
		        		for each(var point:ShpPoint in ring)
		        		{
		        			var intX = int(point.x * xScale)
		        			var intY = int(point.y * yScale)
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
			s.scaleX = 750 / s.width;
			s.scaleY = 750 * aspect / s.height;  
		   	                
	        // add sprite to canvas:
	        addChild(s);
	        
	        s.x = s.width / 1.75;    
	        s.y = s.height / 1.75;
	        // scale the clip to nicely fit our canvas:        
	        //scaleToFitCanvas(s,shp,z);        
	    
	    	s.addEventListener(MouseEvent.CLICK, saveFile);    
		}
		
		public function saveFile(event:Event):void
		{
			mapData.data = counties
			
			var encodedShp = encode(mapData);
	        
	        var fR:FileReference = new FileReference();
	        
	        //fR.save(encodedShp,"states.map");	
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
		
	}
}

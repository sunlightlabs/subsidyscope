package
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.utils.ByteArray;
	import flash.utils.Dictionary;

	public class Map extends Sprite
	{
		public var MAP_WIDTH = 700;
		public var MAP_HEIGHT = 700;
		
		
		
		public var vis:MapVis;
		public var map:Object;
		
		
		
		
		public var features:Dictionary = new Dictionary();
		
		public var fill:uint;
		public var outline:uint;
		public var selectable:Boolean;
		
		
		var aspect:Number;
		
		
		public function Map(mapDataURL:String, v:MapVis, a:Number)
		{
			super();
			
			aspect = a;
			vis = v;
			
			var mapRequest:URLRequest = new URLRequest(mapDataURL);
			
			var mapLoader:URLLoader = new URLLoader();
			mapLoader.dataFormat = URLLoaderDataFormat.BINARY;
		
			mapLoader.addEventListener(Event.COMPLETE, mapLoaded);
			
			try 
            {
                mapLoader.load(mapRequest);
                this.vis.showLoader();
            } 
            catch (error:Error) 
            {
                trace("Unable to load requested document.");
            }	
		}
		
		public function draw():void
		{
			for each(var f:Feature in features) 
	        {	 		        	
	        	f.draw();	
	        }
		}
		
		public function mapLoaded(event:Event)
		{
			var loader:URLLoader = URLLoader(event.target);
			
			map = decode(loader.data); 
		
			if(aspect != 0)
				map.aspect = aspect;
			
	        for each(var featureData:Object in map.data) 
	        {	
	        	var feature:Feature;
	        	
	        	if(featureData.id in features)
	        	{
	        		feature = features[featureData.id];
	        		feature.addElement(featureData);
	        	}
	        	else
	        	{
	        		feature = new Feature(featureData, this);
	        		features[featureData.id] = feature;
	        		this.addChild(feature);
	        	}
	        	
	        	feature.draw();
			} 
		   	            	        			
			if(map.aspect > 1)  	            	        			
			{
				this.scaleX = MAP_WIDTH * (1+ (1/map.aspect))  / this.width;
				this.scaleY = MAP_HEIGHT / this.height;
			}
			else
			{
				this.scaleX = MAP_WIDTH  / this.width;
				this.scaleY = MAP_HEIGHT * map.aspect / this.height;
			} 
	        
	        //this.x = this.width / 1.75;    
	        //this.y = 700; //this.height / 1.75;
	        
	        this.vis.hideLoader();
		}
	
		
		private function decode(bytes:ByteArray):* 
		{
			bytes.position = 0;
			bytes.uncompress();

			return bytes.readObject();
		}
	}
}
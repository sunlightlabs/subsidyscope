package
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.utils.ByteArray;
	import flash.utils.Dictionary;
	
	public class Layer extends Sprite
	{
		public var LAYER_WIDTH = 700;
		public var LAYER_HEIGHT = 700;
		
		public var layer:Object;
		
		public var features:Dictionary = new Dictionary();
		
		public var fill:uint;
		public var outline:uint;
		public var selectable:Boolean;
		
		public var preDraw:Function;
		public var hover:Function;
		
		
		var aspect:Number;
		var layerDataURL:String
		
		
		public function Layer(url:String, a:Number)
		{
			super();
			
			layerDataURL = url;
			aspect = a;
			
			this.addEventListener(Event.ADDED_TO_STAGE, addedToStage);
			
			
		}
		
		public function addedToStage(event:Event):void
		{
			var layerRequest:URLRequest = new URLRequest(layerDataURL);
			
			var layerLoader:URLLoader = new URLLoader();
			layerLoader.dataFormat = URLLoaderDataFormat.BINARY;
			
			layerLoader.addEventListener(Event.COMPLETE, layerLoaded);
			layerLoader.addEventListener(IOErrorEvent.IO_ERROR, layerLoadFailed);
			
			try 
            {
                layerLoader.load(layerRequest);
                this.dispatchEvent(new LoaderEvent(LoaderEvent.LOADER_STARTING));
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
	        	this.preDraw(f);
	        	
	        	f.draw();	
	        }
		}
		
		public function layerLoadFailed(event:Event)
		{
		
		}
		
		public function layerLoaded(event:Event)
		{
			var loader:URLLoader = URLLoader(event.target);
			
			layer = decode(loader.data); 
		
			if(aspect != 0)
				layer.aspect = aspect;
			
	        for each(var featureData:Object in layer.data) 
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
		   	            	        			
			if(layer.aspect > 1)  	            	        			
			{
				this.scaleX = LAYER_WIDTH * (1+ (1/layer.aspect))  / this.width;
				this.scaleY = LAYER_HEIGHT / this.height;
			}
			else
			{
				this.scaleX = LAYER_WIDTH  / this.width;
				this.scaleY = LAYER_HEIGHT * layer.aspect / this.height;
			} 
	        
	        this.dispatchEvent(new LoaderEvent(LoaderEvent.LOADER_FINSHED));
		}
	
		
		private function decode(bytes:ByteArray):* 
		{
			bytes.position = 0;
			bytes.uncompress();

			return bytes.readObject();
		}
	}
}
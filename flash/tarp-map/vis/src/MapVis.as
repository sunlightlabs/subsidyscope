package
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.external.ExternalInterface;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.utils.Dictionary;

	[SWF(width="800", height="650", backgroundColor="#ffffff", frameRate="15")]
	public class MapVis extends Sprite
	{
		public var state_map:StateMap;
		public var county_map:CountyMap;
		
		public var state_ak_map:StateMap;
		public var county_ak_map:CountyMap;
		
		public var state_hi_map:StateMap;
		public var county_hi_map:CountyMap;
		
		public var key:ColorKey;
		
		public var loader:Loader = new Loader();
		
		private var loaderCount:int = 0 ;
		
		
		public var data:Dictionary = new Dictionary();
		public var dataField:int;
		var mode:int;
		var filter:int;
		
		public var bankName:String;
		
		public const MODE_TARP = 1;
		public const MODE_BANK = 2;
		
		public const FILTER_BRANCHES = 1;
		public const FILTER_DEPOSITS = 2;
		public const FILTER_LOANS = 3;
		
		public var path:String;
		
		public function MapVis()
		{
			super();
			
			path = "/media/data/";
			
			//state_map = new StateMap("/media/data/states_25percent.map", this);
			state_map = new StateMap(path + "states.map", this, 0);
			state_map.outline = 0xb0b0b0;
			state_map.fill = null;
			state_map.selectable = false;
						
			//county_map = new CountyMap("/media/data/counties_25percent.map", this);
			county_map = new CountyMap(path + "counties.map", this, 0);
			county_map.outline = null;
			county_map.selectable = true;
			
			//state_map = new StateMap(path + "states_25percent.map", this);
			state_ak_map = new StateMap(path + "states_ak.map", this, 7.3);
			state_ak_map.outline = 0xb0b0b0;
			state_ak_map.fill = null;
			state_ak_map.selectable = false;
						
			//county_map = new CountyMap(path + "counties_25percent.map", this);
			county_ak_map = new CountyMap(path + "counties_ak.map", this, 7.3);
			county_ak_map.outline = null;
			county_ak_map.selectable = true;
			
			//state_map = new StateMap("/media/data/states_25percent.map", this);
			state_hi_map = new StateMap(path + "states_hi.map", this, 0);
			state_hi_map.outline = 0xb0b0b0;
			state_hi_map.fill = null;
			state_hi_map.selectable = false;
						
			//county_map = new CountyMap(path + "counties_25percent.map", this);
			county_hi_map = new CountyMap(path + "counties_hi.map", this, 0);
			county_hi_map.outline = null;
			county_hi_map.selectable = true;
			
			ExternalInterface.addCallback("showBranches", showBranches);
			ExternalInterface.addCallback("showDeposits", showDeposits);
			ExternalInterface.addCallback("showLending", showLending);
			
			ExternalInterface.addCallback("loadBankShare", loadBankShare);
			ExternalInterface.addCallback("loadTARPShare", loadTARPShare);
			
			
			county_map.y = 500;
			state_map.y = 500;
			
			this.addChild(county_map);	
			this.addChild(state_map);	
			
			
			county_ak_map.MAP_HEIGHT = 200;
			county_ak_map.MAP_WIDTH = 200;
			
			state_ak_map.MAP_HEIGHT = 200;
			state_ak_map.MAP_WIDTH = 200;
			
			county_ak_map.y = 650;
			state_ak_map.y = 650;
			
			county_ak_map.x = 0;
			state_ak_map.x = 0;
			
			this.addChild(county_ak_map);	
			this.addChild(state_ak_map);	
			
			
			county_hi_map.MAP_HEIGHT = 750;
			county_hi_map.MAP_WIDTH = 75;
			
			state_hi_map.MAP_HEIGHT = 750;
			state_hi_map.MAP_WIDTH = 75;
			
			county_hi_map.y = 650;
			state_hi_map.y = 650;
			
			county_hi_map.x = 300;
			state_hi_map.x = 300;
			
			
			this.addChild(county_hi_map);	
			this.addChild(state_hi_map);
			
			key = new ColorKey(this);
			
			key.x = 450;
			key.y = 600;
			
			this.addChild(key);
			this.addChild(loader)
			
			loadInitialData();	
			
		}	
		
		public function showLoader()
		{
			loaderCount++;
			
			loader.visible = true;
			loader.draw();
					
		}
		
		public function hideLoader()
		{
			loaderCount--;
			
			if(loaderCount == 0)
			{
				loader.visible = false;
			}		
		}
		
		public function draw()
		{
			county_map.draw();
			county_ak_map.draw();
			county_hi_map.draw();
			key.draw();
		}
		
		
		public function loadInitialData()
		{
			filter = FILTER_DEPOSITS;
			dataField = 4;
			
			loadTARPShare();
			
		}
		
		public function showBranches():void
		{
			filter = FILTER_BRANCHES;
			dataField = 7;
			draw();
		}
		
		public function showDeposits():void
		{
			filter = FILTER_DEPOSITS;
			dataField = 4;
			draw();
		}
		
		public function showLending():void
		{
			filter = FILTER_LOANS;
			dataField = 10;
			draw();
		}
		
		public function loadBankShare(bankId:int, name:String):void
		{
			if(bankId == -1)
			{
				data = new Dictionary();
				draw();
				return;
			}
			
			bankName = name;
			
			var dataRequest:URLRequest = new URLRequest("/projects/bailout/tarp/map/filter/institution/" + String(bankId) + "/");
			
			var dataLoader:URLLoader = new URLLoader();
			dataLoader.dataFormat = URLLoaderDataFormat.TEXT;
		
			dataLoader.addEventListener(Event.COMPLETE, bankDataLoaded);

            try 
            {
                dataLoader.load(dataRequest);
                showLoader();
            } 
            catch (error:Error) 
            {
                trace("Unable to load requested document.");
            }
		}
		
		
		public function loadTARPShare():void
		{
			//var dataRequest:URLRequest = new URLRequest("/media/data/tarp_analysis.csv");
			var dataRequest:URLRequest = new URLRequest(path + "tarp_map_data.csv");
			
			var dataLoader:URLLoader = new URLLoader();
			dataLoader.dataFormat = URLLoaderDataFormat.TEXT;
		
			dataLoader.addEventListener(Event.COMPLETE, tarpDataLoaded);

            try 
            {
                dataLoader.load(dataRequest);
                showLoader();
            } 
            catch (error:Error) 
            {
                trace("Unable to load requested document.");
            }
		}
		
		public function tarpDataLoaded(event:Event)
		{
			var loader:URLLoader = URLLoader(event.target);
			
			data = new Dictionary();
			mode = MODE_TARP;
			
			county_map.fill = 0x005395;
			county_ak_map.fill = 0x005395;
			county_hi_map.fill = 0x005395;
			
			var rows:Array = loader.data.split("\r\n");
			
			
			
			
			for each(var row:String in rows)
			{
				var cols:Array = row.split(",");
				
				var id:int = cols.shift();
				data[id] = cols;
			}
			
			draw();
			
			hideLoader();
		}
		
		public function bankDataLoaded(event:Event)
		{
			var loader:URLLoader = URLLoader(event.target);
			
			data = new Dictionary();
			mode = MODE_BANK;
			
			county_map.fill = 0x7B0094;
			county_ak_map.fill = 0x7B0094;
			county_hi_map.fill = 0x7B0094;
						
	
			var rows:Array = loader.data.split("\r\n");
			
			for each(var row:String in rows)
			{
				var cols:Array = row.split(",");
				
				var id:int = cols.shift();
				data[id] = cols;
			}
			
			draw();
			
			hideLoader();
		}
		
		
	}
}

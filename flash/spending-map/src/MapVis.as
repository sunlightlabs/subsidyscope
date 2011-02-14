package
{
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.external.ExternalInterface;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.net.URLVariables;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.utils.Dictionary;

	[SWF(width="800", height="650", backgroundColor="#ffffff", frameRate="15")]
	public class MapVis extends Sprite
	{
		public var state_layer:Layer;		
		public var state_ak_layer:Layer;
		public var state_hi_layer:Layer;
		
		public var key:ColorKey;
		
		public var loader:Loader;
		
		private var loaderCount:int = 0 ;
		
		public var data:Dictionary = new Dictionary();
		public var dataField:int;
		
		public var maxValues:Array = new Array();
				
		public var mapPath:String;
		public var dataPath:String;
		public var dataQuery:String;
		
		public function MapVis()
		{
			super();
			
			this.addEventListener(Event.ADDED_TO_STAGE, appLoaded);
			
			
			
			ExternalInterface.addCallback("setDataField", setDataField);
			ExternalInterface.addCallback("setLabelText", setLabelText);
			
			mapPath = this.loaderInfo.parameters.mapPath
			dataPath = this.loaderInfo.parameters.dataPath
			dataQuery = this.loaderInfo.parameters.dataQuery
			
		}	
		
		
		
		public function appLoaded(event:Event):void
		{
			this.stage.addEventListener(Event.RESIZE, stageResized);
			
			this.loader = new Loader();
			
			state_layer = new Layer(mapPath + "states.map", 0);
			state_layer.outline = 0xb0b0b0;
			state_layer.fill = 0x005395;
			state_layer.selectable = true;
			state_layer.preDraw = preDraw;
			state_layer.hover = hover;
			
			state_layer.addEventListener(LoaderEvent.LOADER_STARTING, showLoader);
			state_layer.addEventListener(LoaderEvent.LOADER_FINSHED, hideLoader);
			
					
			state_ak_layer = new Layer(mapPath + "states_ak.map", 7.3);
			state_ak_layer.outline = 0xb0b0b0;
			state_ak_layer.fill = 0x005395;
			state_ak_layer.selectable = true;
			state_ak_layer.preDraw = preDraw;
			state_ak_layer.hover = hover;
			
			state_ak_layer.addEventListener(LoaderEvent.LOADER_STARTING, showLoader);
			state_ak_layer.addEventListener(LoaderEvent.LOADER_FINSHED, hideLoader);
						
						
						
			state_hi_layer = new Layer(mapPath + "states_hi.map", 0);
			state_hi_layer.outline = 0xb0b0b0;
			state_hi_layer.fill = 0x005395;
			state_hi_layer.selectable = true;
			state_hi_layer.preDraw = preDraw;
			state_hi_layer.hover = hover;
			
			state_hi_layer.addEventListener(LoaderEvent.LOADER_STARTING, showLoader);
			state_hi_layer.addEventListener(LoaderEvent.LOADER_FINSHED, hideLoader);
			
			
			state_layer.y = 500;
		
			this.addChild(state_layer);	
			
			
			state_ak_layer.LAYER_HEIGHT = 200;
			state_ak_layer.LAYER_WIDTH = 200;
			
			state_ak_layer.x = 0;
			state_ak_layer.y = 650;

			this.addChild(state_ak_layer);		
			
			
			state_hi_layer.LAYER_HEIGHT = 750;
			state_hi_layer.LAYER_HEIGHT = 75;
			
			state_hi_layer.LAYER_HEIGHT = 750;
			state_hi_layer.LAYER_WIDTH = 75;
			
			state_hi_layer.y = 650;
			state_hi_layer.x = 300;

			this.addChild(state_hi_layer);	

			
			key = new ColorKey(this);
			
			key.x = 450;
			key.y = 600;
			
			this.addChild(key);
			
			
			this.addChild(loader);
			loader.draw();
			
			loadInitialData();	
		}
		
		public function stageResized(event:Event):void
		{
			loader.draw();
		}
		
	
		public function preDraw(f:Feature):void 
		{
			if(this.data)
    		{
        		if(this.data[f.data.id])
        		{
        			if(Number(this.data[f.data.id][this.dataField]) != 0)
        				f.fillAlpha = (Math.abs(Number(this.data[f.data.id][this.dataField])) * 0.90) + 0.1;
        			else
        				f.fillAlpha = 0;
        		}
        		else
        			f.fillAlpha = 0;
        	}
		}
		
		public function hover(f:Feature, event:MouseEvent):void
		{
			if(f.infoTip == null && this.data[f.data.id] != null)
			{
				f.infoTip = new Sprite();
				
				var title:String;
				 
				title = f.data.name;
				
				var dataLabelsTitle:TextField = new TextField();
				dataLabelsTitle.text = title;
				dataLabelsTitle.wordWrap = true;
				dataLabelsTitle.width = 250;
				dataLabelsTitle.height = 75;
				dataLabelsTitle.selectable = false;
				dataLabelsTitle.setTextFormat(new TextFormat("Helvetica", 11, 0x000000, true));
				
				dataLabelsTitle.x = 5;
				dataLabelsTitle.y = 5;
				 
				f.infoTip.addChild(dataLabelsTitle);
				
				var dataLabels:String;
				
				dataLabels = "Total Spending (FY 2000-2010): $" + convertNumber(Number(this.data[f.data.id][0])) + "\n"
				dataLabels = dataLabels + "Per Capita Spending (FY 2000-2010): $" + convertNumber(Number(this.data[f.data.id][2])) + "\n"
				 
				var dataLabelsText:TextField = new TextField();
				dataLabelsText.text = dataLabels;
				dataLabelsText.wordWrap = true;
				dataLabelsText.width = 250;
				dataLabelsText.height = 75;
				//dataLabelsText.autoSize = TextFieldAutoSize.LEFT;
				dataLabelsText.selectable = false;
				dataLabelsText.setTextFormat(new TextFormat("Helvetica", 11, 0x000000, false));
				 
				dataLabelsText.x = 5;
				dataLabelsText.y = 25;
				 
				f.infoTip.addChild(dataLabelsText);
				 
				if(f.infoTip.width < 200)
					f.infoTip.width = 200;
				 
				f.infoTip.graphics.beginFill(0xffffff, 1);
				f.infoTip.graphics.lineStyle(1, 0x000000);
				f.infoTip.graphics.drawRoundRect(0, 0, f.infoTip.width + 5, f.infoTip.height + 5, 10);
			}
			
			if(f.infoTip)
			{
				f.infoTip.x = event.stageX + 25;
				f.infoTip.y = event.stageY;
				 
	
				if(f.infoTip.x + f.infoTip.width + 25 > this.stage.width)
				{
					f.infoTip.x = f.infoTip.x - (f.infoTip.width + 50);
				}
				 
				if(f.infoTip.y + f.infoTip.height + 25 > this.stage.height)
				{
					f.infoTip.y = f.infoTip.y - (f.infoTip.height + 25);
				}
				 
				this.stage.addChild(f.infoTip);
			}
			 
			draw();
		}
		
		public function setDataField(field:int):void
		{
			this.dataField = field;
			
			setMaxKeyValue();
			
			this.draw();	
		}
		
		public function setLabelText(text:String):void
		{
			this.key.labelText = text;
			
			this.key.draw();	
		}
		
		public function setMaxKeyValue():void
		{
			var displayField = this.dataField - 1;
			
			this.key.maxValueText = "$" + String(convertNumber(this.maxValues[displayField]));
			
			this.key.draw();
			
		}
		
		public function showLoader(even:Event):void
		{
			loaderCount++;
			
			loader.visible = true;
			if(this.contains(loader))
				loader.draw();			
		}
		
		public function hideLoader(event:Event):void
		{
			loaderCount--;
			
			if(loaderCount == 0)
			{
				loader.visible = false;
			}		
		}
		
			
		public function convertNumber(number:Number, abreviation:Boolean=false):String
		{
			var scale:String;
			if(number >= 1000000000)
			{
				number = number / 1000000000;
				
				if(abreviation)
					scale = "B";
				else
					scale = " billion";
			}
			else if(number >= 1000000)
			{
				number = number / 1000000;
				
				if(abreviation)
					scale = "M";
				else
					scale = " million";
				
			}
			else if(number >= 1000)
			{
				var returned = number.toString().split('.');
				var numberStr:String = returned[0];
				var tempStr:String = new String();
				
				
				var splitPoint:int = numberStr.length - 3;
				
				var firstHalf:String = numberStr.slice(0, splitPoint);
				var secondHalf:String = numberStr.slice(splitPoint);
			
				return firstHalf + "," + secondHalf;
			}
			else if(number >= 1)
			{
				var returned = number.toString().split('.');
				
				number = returned[0]
				
				if(number == 0)
					return "";
				else
					return String(number);	
			}
			else 
			{
				if(number == 0)
					return "";
				else
					return "<1";	
			}
			
			var numberParts:Array = number.toString().split('.');
								
			var numberString:String = numberParts[0];
			if(numberParts.length > 1)
				numberString += '.' + String(numberParts[1]).substring(0, 1);
				
			return numberString + scale;
		}
		
		public function draw()
		{
			state_layer.draw();
			state_ak_layer.draw();
			state_hi_layer.draw();
			
			key.draw();
		}
		
		
		public function loadInitialData()
		{
			dataField = 1;
			
			
			
			loadMapData();	
		}
		
		public function loadMapData():void
		{
			var dataRequest:URLRequest = new URLRequest(dataPath);
			
			if(this.dataQuery != null)
			{
				var variables:URLVariables = new URLVariables();
				variables.q = this.dataQuery;
				dataRequest.data = variables;
			}
			
			var dataLoader:URLLoader = new URLLoader();
			dataLoader.dataFormat = URLLoaderDataFormat.TEXT;
		
			dataLoader.addEventListener(Event.COMPLETE, mapDataLoaded);

            try 
            {
                dataLoader.load(dataRequest);
                showLoader(null);
            } 
            catch (error:Error) 
            {
                trace("Unable to load requested document.");
            }
		}
		
		public function mapDataLoaded(event:Event)
		{
			var loader:URLLoader = URLLoader(event.target);
			
			maxValues = new Array();
			
			data = new Dictionary();
		
			var rows:Array = loader.data.split("\n");
			
			for each(var row:String in rows)
			{
				var cols:Array = row.split(",");
				
				var id:int = cols.shift();
				
				var i:int = 0;
				for each(var col:Number in cols)
				{
					if(maxValues[i] == null || maxValues[i] < col)
						maxValues[i] = col;
						
					i++;		
				}	
				
				data[id] = cols;
			}
			
			setMaxKeyValue();
			
			draw();
			
			hideLoader(null);
		}
		
	}
}
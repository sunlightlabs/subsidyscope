package {
	import flare.animate.Transitioner;
	import flare.data.DataField;
	import flare.data.DataSchema;
	import flare.data.DataSet;
	import flare.data.DataSource;
	import flare.data.DataUtil;
	import flare.display.TextSprite;
	import flare.scale.ScaleType;
	import flare.util.Colors;
	import flare.util.Shapes;
	import flare.util.palette.ColorPalette;
	import flare.vis.Visualization;
	import flare.vis.controls.HoverControl;
	import flare.vis.data.Data;
	import flare.vis.data.NodeSprite;
	import flare.vis.events.SelectionEvent;
	import flare.vis.operator.encoder.ColorEncoder;
	import flare.vis.operator.layout.AxisLayout;
	
	import flash.display.LoaderInfo;
	import flash.display.Sprite;
	import flash.display.StageAlign;
	import flash.display.StageScaleMode;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.external.ExternalInterface;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	import flash.net.URLLoader;
	import flash.system.Security;
	import flash.text.TextFormat;
	import flash.utils.Dictionary;
	
	
	
	
	[SWF(backgroundColor="#ffffff", frameRate="30")]
	public class TARPVis extends Sprite
	{
		private var vis:Visualization;
		private var colorEncoder:ColorEncoder;
		private var schema:DataSchema;
		
		private var amounts:Dictionary;
		
		private var selectedId:Number;
		
		public function TARPVis()
		{
			Security.allowDomain("data.subsidyscope.com");
			
			var params:Object = LoaderInfo(this.root.loaderInfo).parameters;
				
	
			stage.scaleMode = StageScaleMode.NO_SCALE;
			stage.align = StageAlign.TOP_LEFT;
			
			amounts = new Dictionary();
			
			ExternalInterface.addCallback("clearFilter", clearFilter);
			ExternalInterface.addCallback("filterState", filterState);
			ExternalInterface.addCallback("selectNodeByTransactionId", selectNodeByTransactionId);
			
			
			schema = new DataSchema();
			schema.addField(new DataField("date", DataUtil.DATE));
			schema.addField(new DataField("amount", DataUtil.NUMBER));
			
			var url:String = "/projects/bailout/tarp/visualization/data/";
			var useLocalhost:Boolean = true;
			
			if(params['useLocalhost'] == "true")
				url = "http://localhost:8000" + url;
			
			var ds:DataSource = new DataSource(
                url, "json", schema);
                
            var loader:URLLoader = ds.load();
            
            loader.addEventListener(Event.COMPLETE, function(evt:Event):void {
                var ds:DataSet = loader.data as DataSet;
                visualize(Data.fromDataSet(ds));
            });
            
            //this.addEventListener(MouseEvent.CLICK, filterAZ);
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
				number = number / 1000;
				
				if(abreviation)
					scale = "k";
				else
					scale = " thousand";	
			}
			else 
			{
				if(number == 0)
					return "";
				else
					return String(number);	
			}
			
			var numberParts:Array = number.toString().split('.');
								
			var numberString:String = numberParts[0];
			if(numberParts.length > 1)
				numberString += '.' + String(numberParts[1]).substring(0, 1);
				
			return numberString + scale;
		}
		
		public function filterAZ(event:MouseEvent):void
		{
			filterState("AZ");
		}
		
		public function clearFilter(update:Boolean=true)
		{
			vis.data.nodes.visit(function(n:NodeSprite){
				n.data.amount = amounts[n.data.id];
			});
			
			if(update)
			{
				var transition:Transitioner = new Transitioner(1);
				vis.update(transition).play();
			}
		}
		
		public function filterState(state:String)
		{
			clearFilter(false);
			
			vis.data.nodes.visit(function(n:NodeSprite){
				if(n.data.state != state)
					n.data.amount = 0;	
			});
			
			var transition:Transitioner = new Transitioner(1);
			vis.update(transition).play();
		}
		
		public function selectNodeByTransactionId(nodeId:Number):void
		{
			vis.data.nodes.visit(function(n:NodeSprite){
					if(n.data.id == nodeId)
						selectNode(n);
				});
		}
		
		public function selectNode(node:NodeSprite):void
		{
			clearSelection();
			
			selectedId = node.data.id;
			
			ExternalInterface.call('TARP_highlight_table_row',selectedId,'false');	
			
			node.alpha = 1;
			//node.fillColor = Colors.gray(225);//Colors.brighter(node.fillColor, 1);
			
			node.lineColor = Colors.rgba(0, 0, 0);
			
			var infoDate:Date = new Date(Date.parse(node.data.date));
			var infoAmount:String = convertNumber(node.data.amount);
		
			var infoString = node.data.name + "\n" + (infoDate.month + 1) + "/" + (infoDate.date + 1) + "/" + infoDate.fullYear + "\n$" + infoAmount;
			
			var infoTip:TextSprite = new TextSprite(infoString, new TextFormat("Helvetica", 11, 0x000000, false));
			
			var stagePosition:Point = node.localToGlobal(new Point(0,0));
			infoTip.x = stagePosition.x + (node.width / 2);
			infoTip.y = stagePosition.y;
			
			if((infoTip.height + 15) > vis.xyAxes.yAxis.height - node.y)
				infoTip.y -= (infoTip.height + 15) - (vis.xyAxes.yAxis.height - node.y);
			
			node.stage.addChild(infoTip);
		}
		
		
		public function clearSelection():void
		{
			vis.data.nodes.visit(function(n:NodeSprite){
				
				if(selectedId == n.data.id)
					deselectNode(n);
			});
		}
		
		public function deselectNode(node:NodeSprite)
		{
			if(selectedId == node.data.id)
			{
				node.alpha = 0.75;
				//node.fillColor = colorEncoder.colors;
				
				node.lineColor = null;
				
				colorEncoder.operate();
				node.stage.removeChildAt(node.stage.numChildren - 1);
				
				selectedId = null;
			}
		} 
		
		public function visualize(data:Data):void
		{
			if(vis == null)
			{
				// create the visualization
				vis = new Visualization(data);
				vis.bounds = new Rectangle(0, 0, 750, 200);
			
				vis.data.nodes.setProperties({
					shape: Shapes.VERTICAL_BAR,
					lineAlpha: 0,
					alpha: 0.85,
					fillColor: flare.util.Colors.gray(128),
					size: 3//2.5 * vis.bounds.height / vis.data.nodes.length
				});
				
				vis.data.nodes.visit(function(n:NodeSprite){
					amounts[n.data.id] = n.data.amount;
				});
				
	
				var colors:Array = [
				 Colors.rgba(77,85,133),Colors.rgba(172, 181, 174),Colors.rgba(116,116,181),Colors.rgba(184, 194, 186),Colors.rgba(156,156,215),Colors.rgba(203,219,156),Colors.rgba(180,204,106),Colors.rgba(196, 207, 198)
				];
				
				colorEncoder = new ColorEncoder("data.id", "nodes", "fillColor", ScaleType.CATEGORIES, new ColorPalette(colors))
				
				var layout:AxisLayout = new AxisLayout("data.date", "data.amount", false, true)
				layout.yScale.zeroBased = true;
				
				vis.operators.add(layout);
				vis.operators.add(colorEncoder);
				
				vis.xyAxes.yAxis.labelFormater = function(number:Number):String{
					
					var scale:String;
					if(number >= 1000000000)
					{
						number = number / 1000000000;
						scale = "B";
					}
					else if(number >= 1000000)
					{
						number = number / 1000000;
						scale = "M";
					}
					else if(number >= 1000)
					{
						number = number / 1000;
						scale = "k";
					}
					else 
					{
						if(number == 0)
							return "";
						else
							return String(number);	
					}
					
					var numberParts:Array = number.toString().split('.');
										
					var numberString:String = numberParts[0];
					if(numberParts.length > 1)
						numberString += '.' + String(numberParts[1]).substring(0, 1);
						
					return "$" + numberString + scale;
		
				};
				
				vis.xyAxes.yAxis.gridLines.alpha = 0.25
				
				vis.xyAxes.yAxis.labelTextFormat = new TextFormat("Helvetica", 10, 0x666666, false);
				vis.xyAxes.xAxis.labelTextFormat = new TextFormat("Helvetica", 10, 0x666666, false);
				
				vis.xyAxes.yAxis.numLabels = 5;
				
				//vis.xyAxes.xAxis.showLines = false;
				
				vis.controls.add(new HoverControl(NodeSprite, HoverControl.DONT_MOVE, 
								function(event:SelectionEvent):void {
									selectNode(event.node);
									
								},
								function(event:SelectionEvent):void {
									deselectNode(event.node);
								}));
				
				vis.update();
				addChild(vis);
				vis.x = 50; vis.y = 20;
						
			}
			else
			{
				if(data.length == vis.data.nodes.length)
				{
					var max:Number = 0;
					
					data.nodes.visit(function(newData:NodeSprite) {
						
						vis.data.nodes.visit(function(oldData:NodeSprite) {
							
							if(newData.data.date.valueOf() == oldData.data.date.valueOf())
							{
								oldData.data.amount = newData.data.amount;
								if(newData.data.amount > max)
								 	max = newData.data.amount;
							}
						});
						
					});			
					
					var transition:Transitioner = new Transitioner(1);
					
					vis.update(transition).play();
				}
				else
				{
					vis.data = data;
					
					var maxY:Number = 0;
					var maxX:Date = new Date();
					
					data.nodes.visit(function(newData:NodeSprite) {
						if(newData.data.amount > maxY)
							maxY = newData.data.amount;
							
						var newDate = DataUtil.parseValue(newData.data.date, DataUtil.DATE);
													
						if(newDate.valueOf() > maxX.valueOf())
							maxX = newDate;
					});
					
					vis.data.nodes.setProperties({
						shape: Shapes.VERTICAL_BAR,
						lineAlpha: 0,
						alpha: 0.75,
						fillColor: flare.util.Colors.gray(128),
						size: 3
					});
					
					vis.xyAxes.xAxis.axisScale.max = maxX;
					vis.xyAxes.yAxis.axisScale.max = maxY;
					
					vis.update();	
				}
			}
		}
	}
}

package {
    import flare.data.DataField;
    import flare.data.DataSchema;
    import flare.data.DataSet;
    import flare.data.DataSource;
    import flare.data.DataUtil;
    import flare.util.Colors;
    import flare.util.Shapes;
    import flare.util.palette.ColorPalette;
    import flare.util.palette.SizePalette;
    import flare.vis.Visualization;
    import flare.vis.controls.HoverControl;
    import flare.vis.data.Data;
    import flare.vis.data.NodeSprite;
    import flare.vis.events.SelectionEvent;
    import flare.vis.legend.Legend;
    import flare.vis.operator.encoder.ColorEncoder;
    import flare.vis.operator.encoder.SizeEncoder;
    import flare.vis.operator.layout.CirclePackingLayout;
    
    import flash.display.LoaderInfo;
    import flash.display.Sprite;
    import flash.events.Event;
    import flash.geom.Point;
    import flash.geom.Rectangle;
    import flash.net.URLLoader;
    import flash.system.Security;
    import flash.text.TextField;
    import flash.text.TextFieldAutoSize;
    import flash.text.TextFormat;
    import flash.text.TextFormatAlign;
    import flash.utils.Dictionary;
    
    [SWF(width="700", height="550", backgroundColor="#ffffff", frameRate="30")]
    public class TARPBubbles extends Sprite
    {
        private var vis:Visualization;
 		private var colorEncoder:ColorEncoder;
 		private var sizeEncoder:SizeEncoder;
 		
 		private var stopWords:Dictionary;
 		
        public function TARPBubbles()
        {
        	Security.allowDomain("data.subsidyscope.com");
        	
        	stopWords = new Dictionary();
        	
        	stopWords['the'] = true;
        	stopWords['inc'] = true;
        	stopWords['incorporated'] = true;
        	stopWords['corporation'] = true;
        	stopWords['company'] = true;
        	
            loadData();
        }
 
        private function loadData():void
        {
            var schema:DataSchema = new DataSchema();
			schema.addField(new DataField("amount", DataUtil.NUMBER));
			
			var params:Object = LoaderInfo(this.root.loaderInfo).parameters;
			
			var url = "/projects/bailout/tarp/visualization/institution/";
			
			if(params['useLocalhost'] == "true")
				url = "http://localhost:8000" + url;
			
			var ds:DataSource = new DataSource(
                url, "json", schema);
                
            var loader:URLLoader = ds.load();
            loader.addEventListener(Event.COMPLETE, function(evt:Event):void {
                var ds:DataSet = loader.data as DataSet;
                visualize(Data.fromDataSet(ds));
            });
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
 
        private function visualize(data:Data):void
        {
        	
            vis = new Visualization(data);
            vis.bounds = new Rectangle(0, 0, 700, 700);
            vis.y = -75;
            addChild(vis);
 	
 			vis.data.nodes.setProperties({
					lineAlpha: 0,
					alpha: 0.75
				});
 	
 			//vis.operators.add(new Labeler("data.name",));
 			sizeEncoder = new SizeEncoder("data.amount", Data.NODES, new SizePalette(0.0075, 15))
            vis.operators.add(sizeEncoder);
            
            var colors:Array = [
            Colors.rgba(77,85,133),Colors.rgba(116,116,181),Colors.rgba(156,156,215),Colors.rgba(203,219,156),Colors.rgba(180,204,106)];
            
            colorEncoder = new ColorEncoder("data.type", Data.NODES, "fillColor", null, new ColorPalette(colors));
            
            vis.operators.add(colorEncoder);
            vis.operators.add(new CirclePackingLayout(1, false));


			sizeEncoder.operate();
			colorEncoder.operate();

			var typeDict:Dictionary = new Dictionary();
            
            var labelFormat:TextFormat = new TextFormat("Helvetica", 10, 0xffffff, false);
            labelFormat.align = TextFormatAlign.CENTER;            
        	vis.data.nodes.visit(function(n:NodeSprite):void{
        		
        		typeDict[n.data.type] = {color: n.fillColor, shape: Shapes.CIRCLE, label: n.data.type};
        		
        		if(n.width > 7)
        		{
        			var namePartsRaw = n.data.name.replace(/[^A-z ]/, "").replace(/[^A-z ]/, "").split(' ')
        			var nameParts:Array = new Array();
        			
        			for each(var word:String in namePartsRaw)
        			{
        				if(! stopWords[word.toLowerCase()])
        					nameParts.push(word);
        			}
        			
        			var infoAmount:String = convertNumber(n.data.amount);
        			var infoName:String = nameParts.join(" ");
        			var infoString = infoName + "\n$" + infoAmount;
        			
        			if(n.data.percent > -1)
					{
						var percent:Number = Math.round(n.data.percent * 1000);
						percent = percent / 10;
						infoString += "\n" + percent + "%";
					}
        			
        			var labelText:TextField = new TextField();
					labelText.text = infoString;
					labelText.autoSize = TextFieldAutoSize.LEFT;
					labelText.selectable = false;
					labelText.setTextFormat(labelFormat);
					labelText.mouseEnabled = false;
					
					var showLabel = true;
					
					var nameCount:int = nameParts.length;
					
					while(labelText.textWidth > (n.width * 3) )
					{
						if(infoName.length < 10)
						{
							showLabel = false;
							break;
						}
						else
						{
						
							nameCount--;
							
							infoName = nameParts.slice(0, nameCount).join(" ");
							
							if(infoName.length > infoAmount.length)
								infoString = infoName + "\n$" + infoAmount;
							else
								infoString = infoName;
							
							
							
							if(n.data.percent > -1)
							{
								var percent:Number = Math.round(n.data.percent * 1000);
								percent = percent / 10;
								infoString += "\n" + percent + "%";
							}
							
							
							labelText.text = infoString;
							labelText.setTextFormat(labelFormat);
						}
						
					}
					
					
					// pew dosen't want percents by themselves in bubbles
					// 
					/*if(!showLabel)
					{
						var percent:Number = Math.round(n.data.percent * 1000);
						percent = percent / 10;
						infoString = percent + "%";
						
						labelText.text = infoString;
						labelText.setTextFormat(labelFormat);
						
						if(labelText.textWidth > (n.width * 0.1))
							showLabel = true;
					}*/
					
					labelText.x -= labelText.textWidth / 2;
					labelText.y -= (labelText.textHeight / 2) + 2;
					
					if(showLabel)
						n.addChild(labelText);
        		}
        		
        	});

			var typeArray:Array = new Array();
			
			for each(var item:Object in typeDict)
			{
				typeArray.push(item);
			}

            var legend:Legend = Legend.fromValues("Recipient Types", typeArray); 
			
			addChild(legend);
            
           	vis.controls.add(new HoverControl(NodeSprite, HoverControl.DONT_MOVE, 
								function(event:SelectionEvent):void {
									
									//event.node.fillColor = Colors.brighter(event.node.fillColor, 0.75);
									event.node.lineColor = Colors.rgba(0, 0, 0);
									
									var infoAmount:String = convertNumber(event.node.data.amount);
								
									var infoString = event.node.data.name + "\n$" + infoAmount;
									
									if(event.node.data.percent > -1)
									{
										var percent:Number = Math.round(event.node.data.percent * 1000);
										percent = percent / 10;
										infoString += "\n" + percent + "%";
									}
									else
									{
										infoString += "\n less than 0.1%";
									}
									
									var infoTip:Sprite = new Sprite();
									
									
									var infoTipText:TextField = new TextField();
									infoTipText.text = infoString;
									infoTipText.autoSize = TextFieldAutoSize.LEFT;
									infoTipText.selectable = false;
									infoTipText.setTextFormat(new TextFormat("Helvetica", 11, 0x000000, false));
									
									
									
									infoTip.addChild(infoTipText);
									infoTipText.x = 2.5;
									infoTipText.y = 2.5;
									
									infoTip.graphics.beginFill(0xffffff, 1);
									infoTip.graphics.lineStyle(1, 0x000000);
									infoTip.graphics.drawRoundRect(0, 0, infoTipText.textWidth + 5, infoTipText.textHeight + 5, 10); 
									
									var stagePosition:Point = event.node.localToGlobal(new Point(0,0));
									infoTip.x = stagePosition.x + event.node.width / 2.5;
									
									if((event.node.width / 2) > infoTip.height)
										infoTip.y = stagePosition.y - (event.node.width / 2);
									else
										infoTip.y = stagePosition.y - infoTip.height;
									
									if(infoTip.x + infoTip.width > event.node.stage.width)
									{
										infoTip.x = infoTip.x - (infoTip.x + infoTip.width - event.node.stage.width);
										infoTip.y = infoTip.y - (event.node.width / 2);
									}
									
									if(infoTip.y - infoTip.height < 0)
									{
										infoTip.y = stagePosition.y +  20;
									}
									
									
									event.node.stage.addChild(infoTip);
								},
								function(event:SelectionEvent):void {
									
									//event.node.fillColor = colorEncoder.colors;
									//colorEncoder.operate();
									
									event.node.stage.removeChildAt(event.node.stage.numChildren - 1);
									event.node.lineColor = null;
								}));
	            
            vis.data.nodes.setProperties({fillColor:0, lineWidth:2});
            vis.update();
        }
       
    }
}
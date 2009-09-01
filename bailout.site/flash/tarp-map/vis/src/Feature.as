package
{
	import flash.display.Sprite;
	import flash.events.MouseEvent;
	import flash.text.TextField;
	import flash.text.TextFormat;


	class Feature extends Sprite
	{
		private var selected:Boolean = false;
		private var map:Map;
		
		public var data:Object;
		
		public var elements:Array = new Array();
		
		private var infoTip:Sprite;
		
		public function Feature(d:Object, m:Map):void
		{
			data = d;
			elements.push(d.rings);
			map = m;
			
			if(map.selectable)
				this.addEventListener(MouseEvent.MOUSE_OVER, mouseOver);
		}
		
		public function addElement(d:Object):void
		{
			elements.push(d.rings);
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
		
		public function mouseOver(event:MouseEvent)
		{
			event.stopPropagation();
			this.stage.addEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			this.addEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			selected = true;
			
			if(infoTip && this.stage.contains(infoTip))
				this.stage.removeChild(infoTip);
			
			infoTip = new Sprite();
			
			//var infoTipTitleText:TextField = new TextField();
			
			var stateName:String;
			
			if(data.state == 2)
				stateName = map.vis.state_ak_map.features[data.state].data.name;
			else if(data.state == 15)
				stateName = map.vis.state_hi_map.features[data.state].data.name;
			else
				stateName = map.vis.state_map.features[data.state].data.name;
			
			
			//infoTipTitleText.text = data.name + " County, " + stateName;
			
			/*if(map.vis.mode == map.vis.MODE_TARP)
			{
				infoTipTitleText.text = data.name + " County, " + stateName;
				
			}
			else if(map.vis.mode == map.vis.MODE_BANK)
			{
				infoTipTitleText.text = map.vis.bankName + "\n" + data.name + " County, " + stateName;
			}*/
			
			//infoTipTitleText.autoSize = TextFieldAutoSize.LEFT;
			//infoTipTitleText.selectable = false;
			//infoTipTitleText.setTextFormat(new TextFormat("Helvetica", 11, 0x000000, true));
			
			//infoTip.addChild(infoTipTitleText);
			//infoTipTitleText.x = 2.5;
			//infoTipTitleText.y = 2.5;
			
			
			var dataLabels:String;
			
			dataLabels = data.name + " County, " + stateName + " ";  
			 
			if(map.vis.filter == map.vis.FILTER_BRANCHES)
			{
				if(Number(map.vis.data[data.id][5]) > 1)
					dataLabels += "has " + Number(map.vis.data[data.id][5]) + " bank branches; ";
				else
					dataLabels += "has " + Number(map.vis.data[data.id][5]) + " bank branch; ";
			}
			else if(map.vis.filter == map.vis.FILTER_DEPOSITS)
			{
				dataLabels += "has $" + convertNumber(Number(map.vis.data[data.id][2])) + " in deposits; ";
			}
			else if(map.vis.filter == map.vis.FILTER_LOANS)
			{
				if(Number(map.vis.data[data.id][8]) > 1)
					dataLabels += "received " + Number(map.vis.data[data.id][8]) + " HMDA loans; ";
				else
					dataLabels += "received " + Number(map.vis.data[data.id][8]) + " HMDA loan; ";
			}
			
			
			if(map.vis.mode == map.vis.MODE_TARP)
			{
				dataLabels += "TARP recipient institutions ";
				
				if(map.vis.filter == map.vis.FILTER_BRANCHES)
				{
					dataLabels += "operate ";
				}
				else if(map.vis.filter == map.vis.FILTER_DEPOSITS)
				{
					dataLabels += "manage ";
				}
				else if(map.vis.filter == map.vis.FILTER_LOANS)
				{
					dataLabels += "originated ";
				}
			}
			else if(map.vis.mode == map.vis.MODE_BANK)
			{
				dataLabels += map.vis.bankName + " ";
				
				if(map.vis.filter == map.vis.FILTER_BRANCHES)
				{
					dataLabels += "operates ";
				}
				else if(map.vis.filter == map.vis.FILTER_DEPOSITS)
				{
					dataLabels += "manages ";
				}
				else if(map.vis.filter == map.vis.FILTER_LOANS)
				{
					dataLabels += "originated ";
				}
			}
			
			var percent:Number = 0;
			
			if(map.vis.filter == map.vis.FILTER_BRANCHES)
			{
				percent = Number(map.vis.data[data.id][6]) / Number(map.vis.data[data.id][5]);
				
				if(Number(map.vis.data[data.id][6]) > 1)
					dataLabels += Number(map.vis.data[data.id][6]) + " branches";
				else if(Number(map.vis.data[data.id][6]) == 1)
					dataLabels += Number(map.vis.data[data.id][6]) + " branch";
				else
					dataLabels += "no branches";
			}
			else if(map.vis.filter == map.vis.FILTER_DEPOSITS)
			{
				percent = Number(map.vis.data[data.id][3]) / Number(map.vis.data[data.id][2]);
				
				if(Number(map.vis.data[data.id][3]) > 0)
					dataLabels += "$" + convertNumber(Number(map.vis.data[data.id][3])) + " in deposits";
				else
					dataLabels += "no deposits";
			}
			else if(map.vis.filter == map.vis.FILTER_LOANS)
			{
				percent = Number(map.vis.data[data.id][9]) / Number(map.vis.data[data.id][8]);
				
				if(Number(map.vis.data[data.id][9]) > 1)
					dataLabels += Number(map.vis.data[data.id][9]) + " loans";
				else if(Number(map.vis.data[data.id][9]) == 1)
					dataLabels += Number(map.vis.data[data.id][9]) + " loan";
				else
					dataLabels += "no loans";
					
			}
			
			if(percent * 100 > 1)
			{
				dataLabels += " (" + Math.round(percent * 100 ) + "%)."
			}
			else if(percent == 0)
			{
				dataLabels += ".";
			}
			else if(percent * 100 < 1)
			{
				dataLabels += " (<1%).";
			}
			
			
			
			var dataLabelsText:TextField = new TextField();
			dataLabelsText.text = dataLabels;
			dataLabelsText.wordWrap = true;
			dataLabelsText.width = 250;
			dataLabelsText.height = 75;
			//dataLabelsText.autoSize = TextFieldAutoSize.LEFT;
			dataLabelsText.selectable = false;
			dataLabelsText.setTextFormat(new TextFormat("Helvetica", 11, 0x000000, false));
			
			dataLabelsText.x = 5;
			dataLabelsText.y = 5;
			
			infoTip.addChild(dataLabelsText);
			
			/*var dataLabels:String
			
			if(map.vis.mode == map.vis.MODE_TARP)
			{
			 	dataLabels= "TARP Deposits:\nTARP Branches:\nTARP Loans:";
			}
			else if(map.vis.mode == map.vis.MODE_BANK)
			{
				dataLabels= "Deposits:\nBranches:\nLoans:";
			}
			
			var dataLabelsText:TextField = new TextField();
			dataLabelsText.text = dataLabels;
			dataLabelsText.autoSize = TextFieldAutoSize.LEFT;
			dataLabelsText.selectable = false;
			dataLabelsText.setTextFormat(new TextFormat("Helvetica", 11, 0x000000, false));
			
			
			infoTip.addChild(dataLabelsText);
			dataLabelsText.x = 2.5;
			
			
			var dataLabels:String = "";
			
			if(map.vis.mode == map.vis.MODE_TARP)
			{
				dataLabelsText.y = 20;
				
				dataLabels = "$" + Number(map.vis.data[data.id][3]) 
				
				if(Number(map.vis.data[data.id][3]) && Number(map.vis.data[data.id][2]))
					dataLabels = dataLabels + " (" + Math.round(Number(map.vis.data[data.id][3])/Number(map.vis.data[data.id][2]) * 100) + "%)";
					
				dataLabels = dataLabels + "\n" + Number(map.vis.data[data.id][6])
				
				if(Number(map.vis.data[data.id][5]) && Number(map.vis.data[data.id][6]))
					dataLabels = dataLabels + " (" + Math.round(Number(map.vis.data[data.id][6])/Number(map.vis.data[data.id][5]) * 100) + "%)";
					
				dataLabels = dataLabels + "\n" + Number(map.vis.data[data.id][9])
				
				if(Number(map.vis.data[data.id][10]))
					dataLabels = dataLabels + " (" + Math.round(Number(map.vis.data[data.id][10]) * 100) + "%)";
			}
			else if(map.vis.mode == map.vis.MODE_BANK)
			{
				dataLabelsText.y = 35;
				
				if(data.id in map.vis.data)
				{
					dataLabels = "$" + Number(map.vis.data[data.id][3]) 
					
					if(Number(map.vis.data[data.id][3]) && Number(map.vis.data[data.id][2]))
						dataLabels = dataLabels + " (" + Math.round(Number(map.vis.data[data.id][3])/Number(map.vis.data[data.id][2]) * 100) + "%)";
						
					dataLabels = dataLabels + "\n" + Number(map.vis.data[data.id][6])
					
					if(Number(map.vis.data[data.id][5]) && Number(map.vis.data[data.id][6]))
						dataLabels = dataLabels + " (" + Math.round(Number(map.vis.data[data.id][6])/Number(map.vis.data[data.id][5]) * 100) + "%)";
					
					dataLabels = dataLabels + "\n" + Number(map.vis.data[data.id][9])
				
					if(Number(map.vis.data[data.id][10]))
						dataLabels = dataLabels + " (" + Math.round(Number(map.vis.data[data.id][10]) * 100) + "%)";
				}
				else
				{
					dataLabels = "$0\n0\n0";
				}
			}
				
			var dataValuesText:TextField = new TextField();
			dataValuesText.text = dataLabels;
			//dataLabelsText.autoSize = TextFieldAutoSize.LEFT;
			dataValuesText.selectable = false;
			dataValuesText.setTextFormat(new TextFormat("Helvetica", 11, 0x000000, false));
			
			
			infoTip.addChild(dataValuesText);
			dataValuesText.width = 150;
			dataValuesText.height = 60;
			dataValuesText.x = 95;
			dataValuesText.y = dataLabelsText.y;*/
			
			
			if(infoTip.width < 200)
				infoTip.width = 200;
			
			infoTip.graphics.beginFill(0xffffff, 1);
			infoTip.graphics.lineStyle(1, 0x000000);
			infoTip.graphics.drawRoundRect(0, 0, infoTip.width + 5, infoTip.height + 5, 10); 
			
			infoTip.x = event.stageX + 25;
			infoTip.y = event.stageY;
			
			
			
			if(infoTip.x + infoTip.width > this.stage.width)
			{
				infoTip.x = infoTip.x - (infoTip.width + 50);
			}
			
			if(infoTip.y + infoTip.height > this.stage.height)
			{
				infoTip.y = infoTip.y -  (infoTip.height + 25);
			}
			
			
			this.stage.addChild(infoTip);
			
			draw();
		}
		
		public function mouseOut(event:MouseEvent)
		{
			this.stage.removeEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			this.removeEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			
			selected = false;
			
			if(infoTip && this.stage.contains(infoTip))
				this.stage.removeChild(infoTip);
			
			draw();
		}
		
		public function draw():void
		{
			this.graphics.clear();
            
            for each(var element:Array in elements)
            {
            
	            if(map.fill)
	            {
		        	if(selected)
		        	{
		        		this.graphics.beginFill(0xcfb862);
		        	}
		        	else
		        	{
		        		if(map.vis.data)
		        		{
			        		if(map.vis.data[data.id])
			        		{
			        			var value:Number;
			        			
			        			if(Number(map.vis.data[data.id][map.vis.dataField]) != 0)
			        				value = (Math.abs(Number(map.vis.data[data.id][map.vis.dataField])) * 0.90) + 0.1;
			        			else
			        				value = 0;
			        				
			        			this.graphics.beginFill(map.fill, value);
			        		}
			        		else
			        			this.graphics.beginFill(0xffffff);
			        	}
			        	else
			        		this.graphics.beginFill(map.fill);
			        	
		        	}
	            }
	            
	            if(map.outline)
	            {
	            	this.graphics.lineStyle(0,map.outline);
	            }
	            
				for each(var r: Array in element) 
				{
					if (r.length) 
					{
						this.graphics.moveTo(r[0].x,-r[0].y);
					}
					for (var i=1; i<r.length; i++)
						this.graphics.lineTo(r[i].x,-r[i].y);				
				}
            }

		}
	}	

}
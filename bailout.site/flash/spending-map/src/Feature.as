package
{
	import flash.display.Sprite;
	import flash.events.MouseEvent;


	class Feature extends Sprite
	{
		private var selected:Boolean = false;
		private var map:Layer;
		
		public var data:Object;
		
		public var fillAlpha:Number = 0;
		
		public var elements:Array = new Array();
		
		public var infoTip:Sprite;
		
		public function Feature(d:Object, m:Layer):void
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
		
		
		public function mouseOver(event:MouseEvent)
		{
			event.stopPropagation();
			this.stage.addEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			this.addEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			selected = true;
			
			this.map.hover(this, event);
			
		}
		
		public function mouseOut(event:MouseEvent)
		{
			this.stage.removeEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			this.removeEventListener(MouseEvent.MOUSE_OUT, mouseOut);
			
			selected = false;
			
			if(infoTip && this.stage.contains(infoTip))
				this.stage.removeChild(infoTip);
			
			this.draw();
		}
		
		
		public function draw():void
		{
			this.graphics.clear();
			
			for each(var element:Array in elements)
			{
				this.graphics.lineStyle(1, this.map.outline);
				
				if(this.selected)
					this.graphics.beginFill(0xcfb862);
				else
					this.graphics.beginFill(this.map.fill, this.fillAlpha);
				
				for each(var r: Array in element) 
				{
					if (r.length) 
					{
						this.graphics.moveTo(r[0].x,-r[0].y);
					}
					for (var i=1; i<r.length; i++)
						this.graphics.lineTo(r[i].x,-r[i].y);				
				}
				
				this.graphics.endFill();
            }
		}
	}	

}
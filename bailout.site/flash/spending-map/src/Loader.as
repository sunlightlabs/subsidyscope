package
{
	import flash.accessibility.Accessibility;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;
	
	public class Loader extends Sprite
	{
		private var text:TextField;
		
		public function Loader()
		{
			super();
			
			text = new TextField();
			text.text = "Loading data...";
			text.autoSize = TextFieldAutoSize.LEFT;
			text.selectable = false;
			text.setTextFormat(new TextFormat("Helvetica", 14, 0x000000, true));
			
			this.addChild(text);
		}
		
		public function draw()
		{
			this.graphics.clear();
			
			this.graphics.beginFill(0xffffff, 0.5);
			this.graphics.moveTo(0,0);
			this.graphics.lineTo(this.stage.stageWidth , 0);
			this.graphics.lineTo(this.stage.stageWidth , this.stage.stageHeight);
			this.graphics.lineTo(0, this.stage.stageHeight);
			this.graphics.lineTo(0, 0);
		
			text.x = (this.stage.stageWidth / 2) - (text.textWidth / 2);
			text.y = (this.stage.stageHeight / 2) - (text.textHeight / 2);
		}
		
	}
}
package
{
	import flash.display.*;
	import flash.geom.*;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	import flash.text.TextFormat;

	

	public class ColorKey extends Sprite
	{
		var label:TextField = new TextField();
		var maxValueLabel:TextField = new TextField();
		
		var vis:MapVis;
		
		public var labelText:String = "Total Spending";
		public var maxValueText:String = ""; 
		
		public function ColorKey(v:MapVis)
		{
			super();
				
			vis = v;
					
			label.autoSize = TextFieldAutoSize.LEFT;
			label.selectable = false;
			
			label.x = 25
			label.y = -25;
			
			this.addChild(label);
			
			var zeroPercent:TextField = new TextField();
			zeroPercent.autoSize = TextFieldAutoSize.LEFT;
			zeroPercent.text = "$0";
			zeroPercent.selectable = false;
			zeroPercent.setTextFormat(new TextFormat("Helvetica", 12, 0x000000, false));
			
			this.addChild(zeroPercent);
			
			maxValueLabel.autoSize = TextFieldAutoSize.LEFT;
			maxValueLabel.selectable = false;
			maxValueLabel.text = maxValueText;
			maxValueLabel.setTextFormat(new TextFormat("Helvetica", 12, 0x000000, false));
			maxValueLabel.x = 125;
			this.addChild(maxValueLabel);
			
			this.visible = false;
			
		}
		
		public function draw():void
		{
			var colors:Array = [0xFFFFFF, 0x005395];
			
			label.text = labelText;
			label.setTextFormat(new TextFormat("Helvetica", 12, 0x000000, false));
			
			maxValueLabel.text = maxValueText;
			maxValueLabel.setTextFormat(new TextFormat("Helvetica", 12, 0x000000, false));
			
			var fillType:String = GradientType.LINEAR;
			
			var alphas:Array = [1, 1];
			var ratios:Array = [0x00, 0xFF];
			var matr:Matrix = new Matrix();
			
			matr.createGradientBox(100, 20, 0, 25, 0);
			var spreadMethod:String = SpreadMethod.PAD;
			this.graphics.beginGradientFill(fillType, colors, alphas, ratios, matr, spreadMethod);
			this.graphics.lineStyle(1, 0xb0b0b0);
			this.graphics.drawRect(25,0,100,20);
			
			this.visible = true;

		}
		
	}
}
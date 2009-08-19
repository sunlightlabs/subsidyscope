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
		var vis:MapVis;
		
		public function ColorKey(v:MapVis)
		{
			super();
				
			vis = v;
					
			label.autoSize = TextFieldAutoSize.LEFT;
			label.selectable = false;
			
			
			label.x = 25
			label.y = -45;
			
			this.addChild(label);
			
			var zeroPercent:TextField = new TextField();
			zeroPercent.autoSize = TextFieldAutoSize.LEFT;
			zeroPercent.text = "0%";
			zeroPercent.selectable = false;
			zeroPercent.setTextFormat(new TextFormat("Helvetica", 12, 0x000000, false));
			
			this.addChild(zeroPercent);
			
			var hundredPercent:TextField = new TextField();
			hundredPercent.autoSize = TextFieldAutoSize.LEFT;
			hundredPercent.text = "100%";
			hundredPercent.selectable = false;
			hundredPercent.setTextFormat(new TextFormat("Helvetica", 12, 0x000000, false));
			hundredPercent.x = 125;
			this.addChild(hundredPercent);
			
			
		}
		
		public function draw():void
		{
			if(this.vis.filter == this.vis.FILTER_BRANCHES)
				label.text = "Percent of Branches Managed";
			else if(this.vis.filter == this.vis.FILTER_DEPOSITS)
				label.text = "Percent of Deposit Held";
			else if(this.vis.filter == this.vis.FILTER_LOANS)
				label.text = "Percent of Loans Originated";
			
			if(this.vis.mode == this.vis.MODE_TARP)
			{
				var colors:Array = [0xFFFFFF, 0x005395];
				label.text += "\nby TARP CPP Recipients";
			}
			else if(this.vis.mode == this.vis.MODE_BANK)
			{
				var colors:Array = [0xFFFFFF, 0x7B0094];
				label.text += "\nby " + this.vis.bankName;
			}
				
			label.setTextFormat(new TextFormat("Helvetica", 12, 0x000000, false));
			
			var fillType:String = GradientType.LINEAR;
			
			var alphas:Array = [1, 1];
			var ratios:Array = [0x00, 0xFF];
			var matr:Matrix = new Matrix();
			
			matr.createGradientBox(100, 20, 0, 25, 0);
			var spreadMethod:String = SpreadMethod.PAD;
			this.graphics.beginGradientFill(fillType, colors, alphas, ratios, matr, spreadMethod);
			this.graphics.lineStyle(1, 0xb0b0b0);
			this.graphics.drawRect(25,0,100,20);
			
			

		}
		
	}
}
package com.sunlightfoundation.gradientbox
{
	import flash.display.Graphics;
	import flash.display.SpreadMethod;
	import flash.geom.Matrix;

	import mx.collections.ArrayCollection;
	import mx.containers.Box;
	import mx.core.EdgeMetrics;
	import mx.utils.GraphicsUtil;

	public class GradientBox extends Box {
		/* ----------------------------- Variables ----------------------------- */
		private var _colors:Array; // maximum of 16 colors
		public function set colors(value:Array):void
		{
			_colors = value;
			invalidateDisplayList();
		}
		public function get colors():Array
		{
			return _colors;
		}
		
		private var _gradientDirection:String = "vertical";
		[Inspectable(category="General",
			enumeration="vertical,horizontal,rotated",
			defaultValue="vertical")]
		public function set gradientDirection(value:String):void
		{
			_gradientDirection = value;
			invalidateDisplayList();
		}
		public function get gradientDirection():String
		{
			return _gradientDirection;
		}
		
		private var _gradientType:String = "linear";
		[Inspectable(category="General", enumeration="linear,radial", 
			defaultValue="linear")]
		public function set gradientType(value:String):void
		{
			_gradientType = value;
			invalidateDisplayList();
		}
		public function get gradientType():String
		{
			return _gradientType;
		}
		
		private var _r:Number = 0;
		public function set r(value:Number):void
		{
			_r = value;
			invalidateDisplayList();
		}
		public function get r():Number
		{
			return _r;
		}
		
		private var _interpolationMethod:String = "linearRGB";
		[Inspectable(category="General",
			enumeration="linearRGB,rgb",
			defaultValue="linearRGB")]
		public function set interpolationMethod(value:String):void
		{
			_interpolationMethod = value;
			invalidateDisplayList();
		}
		public function get interpolationMethod():String
		{
			return _interpolationMethod;
		}
		/* ----------------------------- Variables ----------------------------- */
	
		public function GradientBox() 
		{
			super();
			setStyle("borderStyle","solid");
			setStyle("borderThickness",0);
		}
	
	        override protected function updateDisplayList(unscaledWidth:Number, 
	            unscaledHeight:Number):void 
	        {
	            super.updateDisplayList(unscaledWidth, unscaledHeight);    
	    
	            var g:Graphics = graphics;
	            var b:EdgeMetrics = borderMetrics;
	            var w:Number = unscaledWidth - b.left - b.right;
	            var h:Number = unscaledHeight - b.top - b.bottom;
	            var m:Matrix;
	        
	            if(_gradientDirection == "vertical")
	        	m = verticalGradientMatrix(0, 0, w, h);
	            else if(_gradientDirection == "horizontal")
	        	m = horizontalGradientMatrix(0, 0, w, h);
	            else
	        	m = rotatedGradientMatrix(0,0,w,h,r);
		    var alphaArray:Array = new Array();
		    var ratioArray:Array = new Array();
		    var x:Number;
		    for(x = 0; x < _colors.length; x++)
			alphaArray[x] = 1;
		    for(x = 0; x < _colors.length; x++)
			ratioArray[x] = Math.floor(255*(x/(_colors.length-1)));
	
		    g.clear();
	            g.beginGradientFill(_gradientType, _colors, alphaArray, ratioArray, m, 
	        	SpreadMethod.PAD, _interpolationMethod);
	    
	            var cn:uint = this.getStyle("cornerRadius");
	            GraphicsUtil.drawRoundRectComplex(g, b.left, b.top, w, h, cn, 
		    	cn, cn, cn);
	    
	            g.endFill();
	        }
	     
		private function rotatedGradientMatrix(x:Number, y:Number, 
			width:Number, height:Number, rotation:Number):Matrix
		{
			var tempMatrix:Matrix = new Matrix();
			tempMatrix.createGradientBox(width, height, rotation * Math.PI
				/ 180, x, y);
			return tempMatrix;
		}
	}
}
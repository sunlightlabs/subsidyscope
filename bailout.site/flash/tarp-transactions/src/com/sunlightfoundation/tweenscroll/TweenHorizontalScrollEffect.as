package com.sunlightfoundation.tweenscroll
{
	import mx.effects.IEffectInstance;
	import mx.effects.TweenEffect;

	public class TweenHorizontalScrollEffect extends TweenEffect
	{
		public var scrollTo:Number;
		public var currentScrollPosition:Number;
		
		public function TweenHorizontalScrollEffect(target:Object=null)
		{
			super(target);
			//define instanceClass  
			instanceClass = TweenHorizontalScrollEffectInstance; 
		}
		
		// override getAffectedProperties() method  
		override public function getAffectedProperties():Array{  
			// return an array of affected properties  
			return ["horizontalScrollPosition"];  
		}		
		   
		// override initInstance() accepting IEffectInstance paramater  
		override protected function initInstance(instance:IEffectInstance):void{  
			//call super.initInstance() and pass IEffectInstance paramater  
			super.initInstance(instance);  
			//set the initial properties of instanceClass if required  
			TweenHorizontalScrollEffectInstance(instance).scrollTo = scrollTo;  
		}
		
	}
}
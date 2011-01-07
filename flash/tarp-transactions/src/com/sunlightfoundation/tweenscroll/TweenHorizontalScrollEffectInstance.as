package com.sunlightfoundation.tweenscroll
{
	import mx.core.Container;
	import mx.effects.Tween;
	import mx.effects.effectClasses.TweenEffectInstance;

	public class TweenHorizontalScrollEffectInstance extends TweenEffectInstance
	{
		public var scrollTo:Number;		
		
		public function TweenHorizontalScrollEffectInstance(target:mx.core.Container)
		{
			super(target);
		}
		
		//class should override play() method  
		override public function play():void{  
		    //overriden play() method should call super.play()  
		    super.play();  
		    //play() method should construct Tween object  
		    new Tween(this, target.horizontalScrollPosition , scrollTo, 800);  
		}

		//override onTweenUpate() method  
		override public function onTweenUpdate(value:Object):void{  
		    //call super.onTweenUpdate()  
		    super.onTweenUpdate(value);  
		    //update the properties  
		    target.horizontalScrollPosition = value;	
		    //trace('current tween: ' + value.to);
		    
		    var t:TweenHorizontalScrollEffect = this.effect as TweenHorizontalScrollEffect;
		    t.currentScrollPosition = Number(value);
		    
		    /*
		    var parentEffect:TweenHorizontalScrollEffect = this.effect as TweenHorizontalScrollEffect;	   
		    parentEffect.currentScrollPosition = Number(value);
		    */
		}
		
	}
}
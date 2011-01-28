package
{
	import flash.events.Event;

	public class LoaderEvent extends Event
	{
		public static const LOADER_STARTING:String = "starting";
		public static const LOADER_FINSHED:String = "finished";
		
		public function LoaderEvent(type:String, bubbles:Boolean=false, cancelable:Boolean=false)
		{
			super(type, bubbles, cancelable);
		}
		
	}
}


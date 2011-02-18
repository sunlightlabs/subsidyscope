package global {
	
	import elements.axis.AxisLabel;
	import elements.labels.XLegend;
	import elements.axis.XAxisLabels;
	import flash.external.ExternalInterface;
	public class Global {
		private static var instance:Global = null;
		private static var allowInstantiation:Boolean = false;
		
		public var x_labels:XAxisLabels;
		public var x_legend:XLegend;
		public var total_value:Number = 0; 
		public var radius_padding:Number = 0;
		private var tooltip:String;
		
		
		public function Global() {
		}
		
		public static function getInstance() : Global {
			if ( Global.instance == null ) {
				Global.allowInstantiation = true;
				Global.instance = new Global();
				Global.allowInstantiation = false;
			}
			return Global.instance;
		}
		
		public function get_x_label( pos:Number ):String {
			
			// PIE charts don't have X Labels
			
			tr.ace('xxx');
			tr.ace( this.x_labels == null )
			tr.ace(pos);
//			tr.ace( this.x_labels.get(pos))
			
			
			if ( this.x_labels == null )
				return null;
			else
				return this.x_labels.get(pos);
		}
		
		public function get_x_legend(): String {
			
			// PIE charts don't have X Legend
			if( this.x_legend == null )
				return null;
			else
				return this.x_legend.text;
		}
		
		public function set_tooltip_string( s:String ):void {
			tr.ace('@@@@@@@');
			tr.ace(s);
			this.tooltip = s;
		}
		
		public function get_tooltip_string():String {
			return this.tooltip;
		}
		
		public function get_total_value():Number {
		    return this.total_value;
		}
		
		public function set_total_value(the_total:Number):void {
		    this.total_value = the_total;
		}
		public function get_radius_padding():int {
		    return this.radius_padding;
		}
		public function set_radius_padding(padding:int):void {
		    this.radius_padding = padding;
		}
		    
	}
}
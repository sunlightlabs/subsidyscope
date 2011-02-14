// ActionScript file
import com.sunlightfoundation.gradientbox.GradientBox;

import flash.events.MouseEvent;
import flash.external.ExternalInterface;
import flash.system.Security;

import mx.controls.Label;
import mx.rpc.events.FaultEvent;
import mx.rpc.events.ResultEvent;

var boxes:Array = new Array();
var highlightedBoxes:Array = new Array();
var gradientColors:Array = new Array;

public function init():void
{
	// security setup		
	if(Application.application.parameters['policy_file']!=null)
	{
		trace(Application.application.parameters['policy_file']);		
		flash.system.Security.loadPolicyFile(Application.application.parameters['policy_file']);
	}
	flash.system.Security.allowDomain("*", "*.subsidyscope.com", "*.subsidyscope.net", "*.subsidyscope.org", "assets.subsidyscope.com");
	
	// basic setup
	this.width = parseInt(Application.application.parameters.width);
	this.height = parseInt(Application.application.parameters.height);
	this.main_canvas.height = this.height - 16;
	this.main_canvas.x = 0;
	this.main_canvas.y = 0;	
	for(var i:int=0;Application.application.parameters['bar_color_'+i]!=null;i++)	
		gradientColors.unshift(Number('0x' + Application.application.parameters['bar_color_' + i]));	
	
	// fetch XML
	this.tarpDataService.url = Application.application.parameters.data_url;
	this.tarpDataService.addEventListener(FaultEvent.FAULT, tarpDataFaultEventHandler);
	tarpDataService.send();	
	
	// JS hook
	try{
		ExternalInterface.addCallback('flexHighlightBar',highlightBar);
	}
	catch(e:SecurityError)
	{
		var l:Label = new Label();
		l.text = e.message.toString();
		this.main_canvas.addChild(l);
	}
}

private function tarpDataFaultEventHandler(event:mx.rpc.events.FaultEvent):void
{
	var l:Label = new Label();
	l.toolTip = event.message.toString();
	l.text = 'Failed to load data';
	l.y = 0;
	l.x = 0;
	this.main_canvas.addChild(l);
}

public function loadTarpData(event:ResultEvent):void
{	
	// let's get you out of that wet XML and into something a little more comfortable
	var tarpTransactions:Array = new Array();
	var max_value:Number = -1;
	var cumulative_total:Number = 0;
	for(var i:uint=0;i<event.result.transactions.transaction.length;i++)
	{
		var t:Array = new Array();
		t['id'] = event.result.transactions.transaction[i].id;
		t['price'] = parseInt(event.result.transactions.transaction[i].price);
		t['date'] = event.result.transactions.transaction[i].date;
		t['ordinal'] = i;
		tarpTransactions.push(t);
		
		cumulative_total += t['price'];
		max_value = Math.max(max_value, t['price']);
	}
	
	// set canvas width
	this.main_canvas.width = (Application.application.parameters.bar_margin + Application.application.parameters.bar_width) * tarpTransactions.length;
	
	drawLabels(cumulative_total);
	
	doDrawing(tarpTransactions, max_value, cumulative_total);
}

private function drawLabels(cumulative_total:Number):void
{	
	trace ('in drawlabels with param ' + cumulative_total);
	const LINE_SCALE:Number = 50000000000; // $50bn
	const ORDER_OF_MAGNITUDE:Number = 1000000000; // $1bn
	var num_lines:int = Math.floor(cumulative_total / LINE_SCALE);
	for(var i:uint=1;i<=num_lines;i++)
	{
		var line_y:uint = this.main_canvas.height - Math.floor((i/num_lines) * (this.main_canvas.height-16))
		
		// draw the label
		var l:mx.controls.Label = new Label();
		l.text = '$' + Math.floor(i * LINE_SCALE / ORDER_OF_MAGNITUDE) + 'b';
		l.setStyle('color','#AAAAAA');
		l.setStyle('fontSize',10);
		l.setStyle('textAlign','right');
		l.width = this.labelHolder.width;
		l.x = 0;
		l.y = Math.max(0,Math.floor(line_y - 6));		

		trace('drawing label at ' + l.text + ' (y:' + l.y + ')');
		
		this.labelHolder.addChild(l);		
		
		// draw the line
		this.axis_overlay.graphics.lineStyle(1, 0xaaaaaa);
		this.axis_overlay.graphics.moveTo(0,line_y);
		this.axis_overlay.graphics.lineTo(this.axis_overlay.width, line_y);
	}
	
}

private function doDrawing(tarpTransactions:Array, max_value:Number, total:Number):void
{
	trace('in doDrawing');

	var BAR_MARGIN:int = Application.application.parameters.bar_margin;
	var BAR_WIDTH:int = Application.application.parameters.bar_width;

	this.main_canvas.width = tarpTransactions.length * (BAR_MARGIN + BAR_WIDTH);

	var running_total:Number = 0;
	for(var i:uint=0;i<tarpTransactions.length;i++)
	{
		var box_height:uint = Math.floor(((tarpTransactions[i].price + running_total) / total) * this.main_canvas.height);
		var b:GradientBox = new GradientBox();
		b.gradientDirection = 'vertical';
		b.colors = gradientColors; //[0x0000FF, 0xFFFFFF];
		b.id = 'box_' + tarpTransactions[i].id;
		b.width = BAR_WIDTH;
		b.height = box_height;
		b.x = tarpTransactions[i].ordinal * (BAR_MARGIN + BAR_WIDTH);
		b.y = this.main_canvas.height - b.height;
		b.addEventListener(MouseEvent.MOUSE_OVER,box_mouseover);
		b.addEventListener(MouseEvent.MOUSE_OUT,box_mouseout);
		this.main_canvas.addChild(b);
		
		boxes[tarpTransactions[i].id] = b;
		
		running_total += tarpTransactions[i].price;
	}
	
	trace('leaving doDrawing');
}

private function _highlightBar(box:GradientBox):void
{
	box.setStyle("backgroundColor","yellow");	
	highlightedBoxes.push(box);
}

private function _dehighlightBars():void
{
	// turn off highlighted boxes
	var t:GradientBox = null;
	while(t = highlightedBoxes.pop())
	{
		t.setStyle("backgroundColor","none");
	}
}

public function highlightBar(bar_id:*):void
{
	trace('highlightBar(' + bar_id + ') + boxes.length=' + boxes.length);
	
	_dehighlightBars();

	var box:GradientBox = boxes[parseInt(bar_id)];
	_highlightBar(box);	

	if(!this.tweenScrollEff.isPlaying)
	{
		this.tweenScrollEff.scrollTo = Math.min(Math.max(0,(box.x - Math.floor(this.width / 2))),this.main_canvas.width);
		this.tweenScrollEff.play();
	}
	
	trace(boxes[parseInt(bar_id)].x);	
}

public function box_mouseover(event:MouseEvent):void
{
	_dehighlightBars();
	
	var box:GradientBox = GradientBox(event.currentTarget);
	_highlightBar(box);	
	
	var row_id:String = event.target.id.replace(/box_/, '');
	ExternalInterface.call('TARP_highlight_table_row',row_id,'false');	
}

public function box_mouseout(event:MouseEvent):void
{

}
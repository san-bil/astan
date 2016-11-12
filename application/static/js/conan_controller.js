buffer = [];
maxBufferSize = 15;

new_video_flag=0;

var rgbColors = function(t) {
  t = parseInt(t);
  if (t < 2)
    throw new Error("'t' must be greater than 1.");

  // distribute the colors evenly on
  // the hue range (the 'H' in HSV)
  var i = 360 / (t - 1);

  // hold the generated colors
  var r = [];
  var sv = 70;
  for (var x = 0; x < t; x++) {
    // alternate the s, v for more
    // contrast between the colors.
    sv = sv > 90 ? 70 : sv+10;
    r.push(GetColorCode([i * x, sv, sv]));
  }
  return r;
};

function GetColorCode(hsv) {
     var c = Color( {h:hsv[0],s:hsv[1],v:hsv[2]} ,'hsv');
     return c.toString();
}

function get_video_duration(){
  return $("video").get(0).duration*1000;
}

function get_video_duration_secs(){
  return $("video").get(0).duration;
}


function get_video_timepoint(){
  return $("video").get(0).currentTime;
}

function get_taskname(){
  var task_name = $("div[id^=tasknamehack_]").attr('id').substring(("tasknamehack_".length));
  return task_name;
}

function get_subject(){
  var subject = $("div[id^=subjecthack_]").attr('id').substring(("subjecthack_".length));
  return subject;
}

function get_video_selection(){
  var videoName = $('#videodropdown>option:selected').text();
  return videoName;
}

function get_annotations_push_endpoint(subject, videoName, task_name){
  var annotations_fetch_endpoint = "/push_csv_annos?subject=" + subject + "&video=" + videoName +"&task_name=" + task_name
  return annotations_fetch_endpoint
}

function get_annotations_fetch_endpoint(subject, videoName, task_name, annotation_variable){
  var annotations_fetch_endpoint = "/fetch_csv_annos?subject=" + subject + "&video=" + videoName + "&task_name=" + task_name + "&dimension=" + annotation_variable
  return annotations_fetch_endpoint
}

function get_variable_selection(){
  var variable = $('#variabledropdown>option:selected').text();
  return variable;
}

function zeroPad(num, places) {
  var zero = places - num.toString().length + 1;
  return Array(+(zero > 0 && zero)).join("0") + num;
}

function get_current_datetime(){
  var currentdate = new Date(); 
  var datetime = currentdate.getDate() + "-"
                + (currentdate.getMonth()+1)  + "-" 
                + currentdate.getFullYear() + "#"  
                + zeroPad(currentdate.getHours(),2) + ":"  
                + zeroPad(currentdate.getMinutes(),2) + ":" 
                + zeroPad(currentdate.getSeconds(),2);
  return datetime;
}


def_key_combos = function(e, ui) {
  var v;
  console.log(e.keyCode);
  if (e.keyCode === 13 || e.keyCode === 32 || e.keyCode === 115) {
    v = $("#video");
    v.get(0).pause();
  }
  if (e.keyCode === 32) {
    return !(e.keyCode === 32);
  }
  $("#slider").slider("disable");
  return $("#slider").slider("enable");
};

play_video = function(e, ui) {
  $("#video").get(0).play();
};

pause_video = function(e, ui) {
  $("#video").get(0).pause();
};

function change_variable() {
  var variable = get_variable_selection();
 
  $("#variabledropdown option").each(function()
  {
      $("#slider").removeClass($(this).val());
  });
  $("#dimension").empty();
  $("#slider").addClass(variable);
  $("#dimension").append(variable);
  $( "#slider" ).slider( "value", 0 );
}

function change_video() {
  $("#labels").width(600);
  var vidpane = $("#vidpane")
  var vid_path = $( "#videodropdown" ).val()
  $("video").remove()

  var video = $('<video id="video" width="600" height="600"></video>').attr("preload","auto").attr("controls","controls")
      .append('<source src="' + vid_path + '"/>')
      .appendTo($("#vidpane"));

  $('#playbackdropdown').val('1');
   
  new_video_flag=1;
  
  $("video").on("canplay",set_up_annotation_state);
  $( "#slider" ).slider( "value", 0 );
  setTimeout(function(){
    video_duration = $("#video").get(0).duration;
    $("#video").get(0).addEventListener("seeking",function(){
      set_graph_window($("#video").get(0).currentTime);
    });
    $("#video").get(0).addEventListener("play",function(){
      playing_sync_callback_id=setInterval(function(){set_graph_window(get_video_timepoint())},250);
      console.log("played");
    });
    $("#video").get(0).addEventListener("pause",function(){
      clearInterval(playing_sync_callback_id);
      console.log("paused");
    });
  },1000);
}

video_duration = null;

on_mouse_move = function(e, ui) {
  var h, s, val;
  s = $("#slider");
  h = $(".ui-slider-handle", s);
  if (h.hasClass("ui-state-focus")) {
    val = ((e.clientX - s.offset().left) / s.width()) * 2 - 1;
    if (val > 1) {
      val = 1;
    }
    if (val < -1) {
      val = -1;
    }
    return s.slider("option", "value", val);
  }
};


function set_up_annotation_state(){

  if(new_video_flag==1){
    $(window).keypress(def_key_combos)
  }
  new_video_flag=0;
}


send_buffer_to_server = function() {
  console.log('send_buffer_to_server');
  var tosend;
  tosend = buffer;
  buffer = [];
  var subject = get_subject();
  var task_name = get_taskname();
  var video_name = get_video_selection();
  var endpoint = get_annotations_push_endpoint(subject, video_name, task_name);
  var data_to_send = JSON.stringify({'buffer':tosend});
  outbound_request = $.ajax({
    type: 'post',
    url: endpoint,
    dataType: 'json',
    contentType: 'application/json',
    data: data_to_send,
  });

  outbound_request.fail(function( jqXHR, textStatus, errorThrown ) {
    if(jqXHR.status==200){
    }else{
      alert("Server is down. Stop annotating for now. Email the admin to ask what's wrong. Press Ctrl+Shift+J in chrome and attach a screenshot.");
    }
  });
};


fetch_annos_from_server = function() {
  var fetched_annotations=null;
  var annotation_variable = get_variable_selection();
  var subject = get_subject();
  var task_name = get_taskname();
  var video_name = get_video_selection();
  var endpoint = get_annotations_fetch_endpoint(subject, video_name, task_name,annotation_variable)

  outbound_request = $.ajax({
    type: 'post',
    url: endpoint,
    async: false,
    dataType: 'json',
    success: function(data) {
        fetched_annotations = data;
    }
    //dataType: 'json',
    //contentType: 'application/json',
    //data: JSON.stringify({buffer:tosend}),
  });

  outbound_request.fail(function( jqXHR, textStatus, errorThrown ) {
    console.log(errorThrown);
    if(jqXHR.status==200){
    }else{
      alert("Can't fetch annotations from server. Stop annotating for now. Email the admin to ask what's wrong. Press Ctrl+Shift+J in chrome and attach a screenshot.");
    }
  });
  return fetched_annotations;
};

last_point_added=null;
on_slider_change = function(e, ui) {
  add_to_buffer();
};

function add_to_buffer(){
  var dimension = get_variable_selection();
  var videoName = get_video_selection();
  var subject = get_subject();
  var videotime = $("#video").get(0).currentTime;
  var annotation_value = $("#slider").slider("option","value");
  update_anno_graph(videotime, annotation_value);
  buffer.push({
    interval_id: active_series_id,
    clienttime: Date.now(),
    subject: subject,
    video: videoName,
    dimension: dimension,
    time: videotime,
    value: annotation_value,
    playing: !($("#video").get(0).paused)
  });
  if (buffer.length >= maxBufferSize) {
    send_buffer_to_server();
  }
  last_point_added=Date.now()
}

active_series_id=null;
active_series=[];
seriesData = [];
interval_ids={};
interval_ids_reverse={};
dummy_data_callback_id=null;

interval_ids = {};
interval_ids_reverse = {};
interval_ids_ctr=0

function create_new_interval(interval_id){
  interval_ids[interval_id]=interval_ids_ctr;
  interval_ids_reverse[interval_ids_ctr] = interval_id;
  seriesData[interval_ids_ctr]=[];
  interval_ids_ctr=interval_ids_ctr+1;
}

function lerp(x1,y1,x2,y2,q){
  var ydiff=y2-y1;
  var xdiff=x2-x1;
  var slope=(ydiff*1.0)/xdiff;
  var q_rat=(q-x1);
  return y1+(q_rat*slope);
}

function interp_series(series,temporal_spacing){
  var new_series=[];
  //print("series");
  //print_series(series);
  for(var j=0;j<series.length;j++){
    if(j>0){
      while(true){
        var real_x_point=series[j].x;
        var real_y_point=series[j].y;
        var last_display_x=new_series[new_series.length-1].x;
        var last_display_y=new_series[new_series.length-1].y;
        if(temporal_spacing<(real_x_point - last_display_x)){
          var new_x=last_display_x+temporal_spacing;
          var new_y=lerp(last_display_x,last_display_y,real_x_point,real_y_point,new_x);
          new_series.push({ x: new_x, y: new_y });
        }else{
          new_series.push({ x: series[j].x, y: series[j].y });
          break;
        }
      }
    }else{
      new_series.push({ x: series[j].x, y: series[j].y });
    }
  }
  //print("new_series");
  //print_series(new_series);
  return new_series;
}

function print_series(series){
  series.forEach(function(foo){print(foo.x+" : "+foo.y)});
}

print=console.log
function annos_to_series(annos){
    var tmp_seriesData=[];
    for(var i=0;i<annos.length;i++){

      var interval_id = annos[i].interval_id;
      if(!(interval_id in interval_ids)){
        tmp_seriesData[interval_ids_ctr]=[];
        create_new_interval(interval_id);
      }
      interval_id_idx=interval_ids[interval_id];

      tmp_seriesData[interval_id_idx].push({ x: parseFloat(annos[i].time), y: parseFloat(annos[i].value) });  
    }

    for(var i=0;i<tmp_seriesData.length;i++){
      temporal_spacing=0.1;
      seriesData[i] = interp_series(tmp_seriesData[i],temporal_spacing);
      //seriesData[i] = tmp_seriesData[i];
    }

    // if(seriesData.length==0){
    //   seriesData.push([{x: 0, y: 0}]);
    // }
}

function add_dummy_annotation(){
    var videotime = $("#video").get(0).currentTime;
    var annotation_value = $( "#slider" ).slider( "value");
    
    update_anno_graph(videotime, annotation_value)
    set_graph_window(get_video_timepoint());
}

function add_annotation_event(){
  add_to_buffer();
}


function start_annotating(){
  var video_time=$("#video").get(0).currentTime;

  active_series_id=get_current_datetime()+"@"+video_time.toString();
  create_new_interval(active_series_id);
  active_series_idx=interval_ids[active_series_id];
  my_series.push({color:get_color(active_series_idx+1),data:seriesData[active_series_idx],name:active_series_id});

  play_video();
  dummy_data_callback_id = setInterval( add_dummy_annotation, 50 );
  add_annotation_event_callback_id = setInterval( add_annotation_event, 500 );
  graph_window_callback_id = setInterval( function(){set_graph_window(get_video_timepoint());}, 1000 );
  redraw_legend();
}

window_width=10;
function set_graph_window(videotime){

  if($("#view_whole_timeline").get(0).checked){
    graph.render();
  }else{
    var lb=Math.max(0,videotime-(window_width/2));
    var lb_diff=(0-(videotime-(window_width/2)));
    if(lb_diff<0){
      lb_diff=0;
    }

    var ub=Math.min(video_duration,videotime+(window_width/2)+Math.abs(lb_diff));

    graph.window.xMin = lb;
    graph.window.xMax = ub;
    graph.update();
  }
}

function update_anno_graph(videotime, annotation_value){
  seriesData[seriesData.length-1].push({ x: videotime, y: annotation_value });
}


graph=0;
numColours=15;
my_colours = rgbColors(numColours);

function clear_chart_state(){
  $('#chart').empty();
  graph=0;
  active_series_id=null;
  active_series=[];
  seriesData = [];
  interval_ids={};
  interval_ids_reverse={};
  dummy_data_callback_id=null;

  interval_ids = {};
  interval_ids_reverse = {};
  interval_ids_ctr=0

}

function get_color(idx){
  var color_idx = (numColours % idx);
  return my_colours[color_idx];
}

function add_anno_graph(){
  clear_chart_state();
  annos = fetch_annos_from_server();
  annos_to_series(annos);

  var palette = new Rickshaw.Color.Palette( { scheme: 'classic9' } );

  my_series = [];
  
  for(var j=0;j<seriesData.length;j++){
    my_series.push({color:get_color(j+1),data:seriesData[j],name:interval_ids_reverse[j]});
  }

  dummy_data = interp_series([{x:0,y:0},{x:get_video_duration_secs(),y:0}],0.05);

  my_series.push({color:"#000000",data:dummy_data,name:'placeholder (ignore)'});

  graph = new Rickshaw.Graph( {
    element: document.getElementById("chart"),
    width: 500,
    height: 350,
    stroke: true,
    preserve: true,
    min: -1,
    max: 1,
    stack: false,
    renderer: 'line',
    series: my_series,
  } );

  graph.render();

  // var preview = new Rickshaw.Graph.RangeSlider( {
  //   graph: graph,
  //   element: document.getElementById('preview'),
  // } );

  var hoverDetail = new Rickshaw.Graph.HoverDetail( {
    graph: graph,
    xFormatter: function(x) {
      return x.toString().slice(0,4)+"s";
    }
  } );

  // var annotator = new Rickshaw.Graph.Annotate( {
  //   graph: graph,
  //   element: document.getElementById('timeline')
  // } );

  legend = new Rickshaw.Graph.Legend( {
    graph: graph,
    element: document.getElementById('legend')

  } );

  var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
    graph: graph,
    legend: legend
  } );

  var order = new Rickshaw.Graph.Behavior.Series.Order( {
    graph: graph,
    legend: legend
  } );

  var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight( {
    graph: graph,
    legend: legend
  } );

  var ticksTreatment = 'glow';

  var xAxis = new Rickshaw.Graph.Axis.Time( {
    graph: graph,
    ticksTreatment: ticksTreatment,
    pixelsPerTick:25,
    timeFixture: new Rickshaw.Fixtures.Time.Local()
  } );

  xAxis.render();

  var yAxis = new Rickshaw.Graph.Axis.Y( {
    graph: graph,
    tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
    ticksTreatment: ticksTreatment
  } );

  yAxis.render();


  // var controls = new RenderControls( {
  //   element: document.querySelector('form'),
  //   graph: graph
  // } );

  // add some data every so often


  // function addAnnotation(force) {
  //  if (messages.length > 0 && (force || Math.random() >= 0.95)) {
  //    annotator.add(seriesData[2][seriesData[2].length-1].x, messages.shift());
  //    annotator.update();
  //  }
  // }

  // addAnnotation(true);
  // setTimeout( function() { setInterval( addAnnotation, 6000 ) }, 6000 );

  var previewXAxis = new Rickshaw.Graph.Axis.Time({
    graph: graph,
    timeFixture: new Rickshaw.Fixtures.Time.Local(),
    ticksTreatment: ticksTreatment
  });

  previewXAxis.render();

  setTimeout(function(){set_graph_window(0);},1500);
}

function redraw_legend(){
  $('div#legend').empty();
  legend = new Rickshaw.Graph.Legend({
      graph: graph,
      element: document.getElementById('legend')
  });

}


$(function(){


  $( "#videodropdown" ).change(change_video);
  change_video();

  $( "#variabledropdown" ).change(change_variable);
  change_variable();

  $( "#variabledropdown" ).change(add_anno_graph);
  // $( "#videodropdown" ).change(add_anno_graph);
  // add_anno_graph();
  
  $("#video").get(0).addEventListener("canplay",function() {
    add_anno_graph();
  });



  $(window).keypress(def_key_combos);

  $("#labels").click(pause_video);
  $("#labels").width(600);

  $("#labels").click(function(){
      clearInterval(dummy_data_callback_id);
      clearInterval(graph_window_callback_id);
      clearInterval(add_annotation_event_callback_id);
  });

  $(document).mousemove(on_mouse_move);

  $("#slider").slider({
    orientation: 'horizontal',
    min: -1,
    max: 1,
    value: 0,
    step: 0.01,
    slide: on_slider_change,
    change: on_slider_change,
    start: start_annotating,
    width: 600,

  });


  $("#view_whole_timeline").change(function() {
    if ($(this).is(':checked')) {
      console.log('check on');
      graph.window.xMin = 0;
      graph.window.xMax = get_video_duration();
      graph.render();
    }else{
      console.log('check off');
      set_graph_window(get_video_timepoint());
    }
  });

  

  $("#video").bind("ended", function() {
    var is_seeking = $("#video").get(0).seeking;
    clearInterval(dummy_data_callback_id);
    if(!is_seeking){
      send_buffer_to_server();
    }
  });

});
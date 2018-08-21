function cartanim_init(a_d) {

    window.cartanim = {
        animdir: a_d,
        in_loading_state: false,
        frames: null,
        current_frame: -1,
        conventional_map: null,
        colors: null,
        labels: null,
        map_width: 0,
        map_height: 0,
        frame_hold_time: 2,
        frame_transition_time: 1,
        paused: true,
        current_interval: null,
        enter_loading_state: function() {
            this.in_loading_state = true;

            document.getElementById('player').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
        },
        exit_loading_state: function() {
            this.in_loading_state = false;

            document.getElementById('loading').style.display = 'none';
        },
        do_fatal_error: function(message) {
            this.in_loading_state = true; // Lock the UI but don't display loading screen

            document.getElementById('fatal-error-message').innerText = message;

            document.getElementById('player').style.display = 'none';
            document.getElementById('loading').style.display = 'none';

            document.getElementById('fatal-error').style.display = 'block';
        },
        http_get: function(url, timeout=15000) {

            return new Promise(function(resolve, reject){

                var xhttp = new XMLHttpRequest();

                xhttp.onreadystatechange = function() {
                    if(this.readyState == 4)
                    {
                        if(this.status == 200)
                        {
                            try
                            {
                                resolve(JSON.parse(this.responseText));
                            }
                            catch(e)
                            {
                                console.log(e);
                                console.log(this.responseText);
                                reject('Unable to parse output.');
                            }
                        }
                        else
                        {
                            console.log(url);
                            reject('Unable to fetch data from the server.');
                        }
                    }
                };

                xhttp.ontimeout = function(e) {
                    reject('The request has timed out.');
                }

                xhttp.open("GET", url, true);
                xhttp.timeout = timeout;
                xhttp.send();

            });
        },
        load_animation_frame: function(animation, frame) {

            return new Promise(function(resolve, reject){

                window.cartanim.http_get(window.cartanim.animdir + "/" + animation + "/" + frame.file).then(function(d){

                    resolve({
                        'label': frame.label,
                        'cartogram': d
                    });

                }, reject);

            });

        },
        load_animation_ancillary: function(animation) {

            return new Promise(function(resolve,reject){

                var conventional_map = window.cartanim.http_get(window.cartanim.animdir + "/" + animation + "/conventional.json");
                var labels = window.cartanim.http_get(window.cartanim.animdir + "/" + animation + "/labels.json");
                var colors = window.cartanim.http_get(window.cartanim.animdir + "/" + animation + "/colors.json");

                Promise.all([conventional_map, colors, labels]).then(function(values){

                    resolve({
                        'conventional_map': values[0],
                        'colors': values[1],
                        'labels': values[2]
                    });

                }, reject);

            });

        },
        scale_maps: function() {

            var maps = [this.conventional_map];

            this.frames.forEach(function(frame){
                maps.push(frame.cartogram);
            }, this);

            var map_widths = [];
            var map_heights = [];

            maps.forEach(function(map){

                map_widths.push(map.extrema.max_x - map.extrema.min_x);
                map_heights.push(map.extrema.max_y - map.extrema.min_y);

            });

            this.map_width = map_widths.reduce(function(a, b){

                return Math.max(a, b);

            });

            this.map_height = map_heights.reduce(function(a, b){

                return Math.max(a, b);
            });

            maps.forEach(function(value, index){

                maps[index].scale_x = this.map_width/(maps[index].extrema.max_x-maps[index].extrema.min_x);
                maps[index].scale_y = this.map_height/(maps[index].extrema.max_y-maps[index].extrema.min_y);

            }, this);

        },
        scale_labels: function() {

            var label_points_x = [];
            var label_points_y = [];

            this.labels.labels.forEach(function(label){
                label_points_x.push(label.x);
                label_points_y.push(label.y);
            })

            this.labels.lines.forEach(function(line){

                label_points_x.push(line.x1);
                label_points_x.push(line.x2);
                label_points_y.push(line.y1);
                label_points_y.push(line.y2);

            });

            var labels_width = label_points_x.reduce(function(a,b){ return Math.max(a,b); }) - label_points_x.reduce(function(a,b){ return Math.min(a,b); });
            var labels_height = label_points_y.reduce(function(a,b){ return Math.max(a,b); }) - label_points_y.reduce(function(a,b){ return Math.min(a,b); });

            /*this.labels.extrema = {
                'max_x': label_points_x.reduce(function(a,b){ return Math.max(a,b); }),
                'min_x': label_points_x.reduce(function(a,b){ return Math.min(a,b); }),
                'max_y': label_points_y.reduce(function(a,b){ return Math.max(a,b); }),
                'min_y': label_points_y.reduce(function(a,b){ return Math.min(a,b); })
            };*/

            this.labels.scale_x = Math.sqrt(this.conventional_map.scale_x * (labels_width/(this.conventional_map.extrema.max_x - this.conventional_map.extrema.min_x)));
            this.labels.scale_y = Math.sqrt(this.conventional_map.scale_y * (labels_height/(this.conventional_map.extrema.max_y - this.conventional_map.extrema.min_y)));

        },
        frame_line_functions: function(data){

            var a = data.extrema.min_x;

          	var b = data.extrema.max_y;

            var lineFunction = d3.svg.line()
                                     .x(function(d) { return data.scale_x * (-1*a + d[0]) })
                                     .y(function(d) { return data.scale_y * (b - d[1]) })
                                     .interpolate("linear");
            
            var lfs = [];
            
            data.features.forEach(function(feature){

                lfs.push({id: feature.properties.polygon_id, path: lineFunction(feature.coordinates)})

            });

            return lfs;

        },
        frame_fill_color: function(data){

            data.features.forEach(function(v, i){

                data.features[i].properties.color = window.cartanim.colors['id_' + data.features[i].id];

            });

        },
        draw_d3_graphic: function(this_map, data, element_id, labels=null) {

            console.log(this_map);

            var a = data.extrema.min_x;

          	var b = data.extrema.max_y;

            var lineFunction = d3.svg.line()
                                     .x(function(d) { return data.scale_x * (-1*a + d[0]) })
                                     .y(function(d) { return data.scale_y * (b - d[1]) })
                                     .interpolate("linear");
                                     
            var canvas = d3.select("#" + element_id).append("svg")
            .attr("width", this.map_width)
            .attr("height", this.map_height);

            var group = canvas.selectAll()
              .data(data.features)
              .enter()
              .append("path")
            
              console.log(this_map);
            
            var polygon_paths = new Array();

            var areas = group.attr("d",function(d) { 
                var l = lineFunction(d.coordinates);

                polygon_paths.push({id: d.properties.polygon_id, path: l})
                return l;

            }).attr("id", function(d){ return "path-" + this_map + "-" + d.properties.polygon_id; })
              .attr("class", function(d){ return "area" + " path-" + this_map + "-" + d.id;})
              .attr("fill", function(d) {return d.properties.color})
              .attr("stroke", "#000")
              .attr("stroke-width", "0.5")
              /*.on('mouseover', function(d, i) {
                             window.cartogram.highlight_by_id(maps, d.id, 0.6);

                             window.cartogram.tooltip_show(d.id);

                             })
              .on('mouseout', function(d, i) {
                             window.cartogram.highlight_by_id(maps, d.id, 1);
                              });*/
            
            if(labels != null)
            {
                /* First draw the text */

                var text = canvas.selectAll("text")
                                    .data(labels.labels)
                                    .enter()
                                    .append("text");
                
                var textLabels = text.attr('x', function(d) { return labels.scale_x * d.x; })
                                    .attr('y', function(d) { return labels.scale_y * d.y; })
                                    .attr('font-family', 'sans-serif')
                                    .attr('font-size', '7.5px')
                                    .attr('fill', '#000')
                                    .text(function(d) { return d.text; });
                
                var lines = canvas.selectAll("line")
                                    .data(labels.lines)
                                    .enter()
                                    .append("line");
                
                var labelLines = lines.attr('x1', function(d) { return d.x1 * labels.scale_x; })
                                    .attr('x2', function(d) { return d.x2 * labels.scale_x; })
                                    .attr('y1', function(d) { return d.y1 * labels.scale_y; })
                                    .attr('y2', function(d) { return d.y2 * labels.scale_y; })
                                    .attr('stroke-width', 1)
                                    .attr('stroke', '#000');
            }
            
            return polygon_paths;
        },
        change_frame: function(old_frame, new_frame) {
            if(this.in_loading_state)
                return;
            
            this.frames[old_frame].cartogram.d3lf.forEach(function(v, i){

                var new_path = null;

                this.frames[new_frame].cartogram.d3lf.forEach(function(w,j){

                    if(w.id == v.id)
                        new_path = w.path;

                }, this);

                if(new_path != null)
                {
                    d3.select('#path-frame-' + v.id)
                    .attr('d', v.path)
                    .transition()
                    .ease(d3.easeCubic)
                    .duration(1000)
                    .attr('d', new_path);
                }

            }, this);

            setTimeout((function(f){
                
                return function(){
                    document.getElementById('frame-label').innerText = window.cartanim.frames[f].label;

                    window.cartanim.frames.forEach(function(frame, i){

                        if(i == f)
                            document.getElementById('frame-control-' + i).classList.add('active');
                        else
                            document.getElementById('frame-control-' + i).classList.remove('active');

                    });
                };

            }(new_frame)), 1000);
            
            
        },
        next_frame: function() {
            if(this.in_loading_state)
                return;
            
            var old_frame = this.current_frame;
            
            if(this.current_frame == (this.frames.length - 1))
                this.current_frame = 0
            else
                this.current_frame += 1
            
            this.change_frame(old_frame, this.current_frame);
        },
        play_animation: function()
        {
            this.current_interval = setInterval(function(){
                window.cartanim.next_frame();
            }, 3000);
        },
        toggle_play: function()
        {
            if(this.current_interval != null)
                clearInterval(this.current_interval);
            
            if(this.paused)
            {
                this.play_animation();
            }

            this.paused = !this.paused;

            document.getElementById('play-pause').innerText = this.paused ? "Play" : "Pause";
        },
        populate_frame_controls: function() {

            this.frames.forEach(function(frame, id){

                var button = document.createElement('button');
                button.type = "button";
                button.className = "btn btn-secondary";

                button.onclick = (function(i){

                    return function(){

                        console.log(i);

                        if(window.cartanim.current_frame == i)
                            return;

                        if(window.cartanim.current_interval != null)
                            clearInterval(window.cartanim.current_interval);
                        
                        window.cartanim.change_frame(window.cartanim.current_frame, i);
                        window.cartanim.current_frame = i;

                        if(!window.cartanim.paused)
                            window.cartanim.play_animation();
                    
                    };

                }(id));

                button.innerText = frame.label;
                button.id = 'frame-control-' + id;

                if(id == 0)
                    button.className = "btn btn-secondary active";

                document.getElementById('frame-controls').appendChild(button);

            });

        },
        load_animation: function(animation) {

            if(this.in_loading_state)
                return;
            
            this.frames = [];
            this.current_frame = 0;
            this.conventional_map = null;
            this.colors = null;
            this.labels = null;
            
            this.enter_loading_state();

            document.getElementById('frame-controls').innerHTML = "";

            this.http_get(this.animdir + "/" + animation + "/frames.json").then(function(frames){

                var frame_promises = [];

                frames.frames.forEach(function(frame){

                    frame_promises.push(window.cartanim.load_animation_frame(animation, frame));

                });

                Promise.all([window.cartanim.load_animation_ancillary(animation), Promise.all(frame_promises)]).then(function(values){

                    window.cartanim.conventional_map = values[0].conventional_map;
                    window.cartanim.colors = values[0].colors;
                    window.cartanim.labels = values[0].labels;

                    values[1].forEach(function(frame){

                        window.cartanim.frames.push(frame);

                    });

                    window.cartanim.scale_maps();
                    window.cartanim.scale_labels();

                    window.cartanim.frame_fill_color(window.cartanim.conventional_map);

                    window.cartanim.frames.forEach(function(frame){

                        window.cartanim.frame_fill_color(frame.cartogram);

                    });

                    for(let i = 1; i < window.cartanim.frames.length; i++)
                    {
                        /* All but the first frame need their paths precomputed */

                        window.cartanim.frames[i].cartogram.d3lf = window.cartanim.frame_line_functions(window.cartanim.frames[i].cartogram);
                    }

                    /* Now draw the conventional map and the first frame */

                    window.cartanim.conventional_map.d3lf = window.cartanim.draw_d3_graphic('conventional', window.cartanim.conventional_map, 'conventional-map', window.cartanim.labels);

                    window.cartanim.frames[0].cartogram.d3lf = window.cartanim.draw_d3_graphic('frame', window.cartanim.frames[0].cartogram, 'frame-map', null);

                    document.getElementById('frame-label').innerText = window.cartanim.frames[0].label;

                    window.cartanim.populate_frame_controls();

                    window.cartanim.exit_loading_state();
                    document.getElementById('player').style.display = "block";

                }, window.cartanim.do_fatal_error);

            });
        }
    }

}
function clearFileInput(ctrl) {
    try {
      ctrl.value = null;
    } catch(ex) { }
    if (ctrl.value) {
      ctrl.parentNode.replaceChild(ctrl.cloneNode(true), ctrl);
    }
  }

function cartogram_init(c_u, cui_u, c_d, g_u)
{
    window.cartogram = {

        in_loading_state: false,
        cartogram_url: c_u,
        cartogramui_url: cui_u,
        cartogram_data_dir: c_d,
        gridedit_url: g_u,
        color_data: null,
        map_alternates: {
            map1: null,
            map2: null,
            map3: null,
            map_selected: '',
            maps_possible: []
        },
        map_config: {},
        abbreviations: {},
        scaling_factor: 1,
        enable_highlight: true,
        enable_tooltip: true,
        enable_switching: true,
        enable_toplabel: false,
        hide_maps_by_id: [],
        animation_duration: 1000,
        grid_document: null,
        gridedit_window: null,
        tooltip: new Array(0),
        loading_state: null,
        fatal_error_extended_info: null,
        launch_gridedit: function() {

            if(this.grid_document === null || this.in_loading_state)
                return;
            
            if(this.gridedit_window === null || this.gridedit_window.closed)
            {
                this.gridedit_window = window.open(this.gridedit_url, "gridedit_" + new Date().getTime(), 'width=550,height=650,resizable,scrollbars');

                this.gridedit_window.addEventListener("load", (function(gd){

                    return function(e) {
                        window.cartogram.gridedit_window.gridedit_init();

                        window.cartogram.gridedit_window.gridedit.on_update = function(gd) {

                            window.cartogram.on_gridedit_update(gd);

                        };

                        window.cartogram.gridedit_window.gridedit.set_allow_update(!this.in_loading_state);

                        window.cartogram.gridedit_window.gridedit.load_document(gd);
                    };

                }(this.grid_document)));
            }
            else
            {
                this.gridedit_window.gridedit.load_document(this.grid_document);
                this.gridedit_window.focus();
            }           

        },
        edit_button_enabled: function() {
            return (this.grid_document === null);
        },
        update_grid_document: function(new_gd) {

            this.grid_document = new_gd;

            if(this.grid_document !== null)
            {
                if(!this.in_loading_state)
                    document.getElementById('edit-button').disabled = false;

                if(this.gridedit_window !== null && !this.gridedit_window.closed)
                    this.gridedit_window.gridedit.load_document(this.grid_document);
            }
            else
            {
                document.getElementById('edit-button').disabled = true;
            }

        },
        grid_document_to_csv: function(gd){

            var csv = "";

            for(let row = 0; row < gd.height; row++)
            {
                for(let col = 0; col < gd.width; col++)
                {
                    /* We use Excel style CSV escaping */
                    csv += '"' + gd.contents[(row * gd.width) + col].replace(/"/gm, '""') + '"';

                    if(col < (gd.width - 1))
                    {
                        csv += ",";
                    }
                }

                if(row < (gd.height - 1))
                {
                    csv += "\n";
                }
            }

            return csv;

        },
        generate_mime_boundary: function() {

            var text = "---------";
            var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

            for (var i = 0; i < 25; i++)
                text += possible.charAt(Math.floor(Math.random() * possible.length));

            return text;

        },
        gen_cartogramui_req_body_from_grid_document: function(handler, gd)
        {

            var mime_boundary = this.generate_mime_boundary();
            var csv = this.grid_document_to_csv(gd);

            while(true)
            {
                var search_string = csv + "csv" + "handler" + handler;
                if(search_string.search(mime_boundary) === -1)
                    break;
                
                mime_boundary = this.generate_mime_boundary();
            }

            var req_body = "";

            req_body += "--" + mime_boundary + "\n";
            req_body += 'Content-Disposition: form-data; name="handler"\n\n'
            req_body += handler + "\n";

            req_body += "--" + mime_boundary + "\n";
            req_body += 'Content-Disposition: form-data; name="csv"; filename="data.csv"\n';
            req_body += 'Content-Type: text/csv\n\n';
            req_body += csv + "\n";
            req_body += "--" + mime_boundary + "--";

            return [mime_boundary, req_body];

        },
        tooltip_clear: function() {
            if(this.enable_tooltip)
                document.getElementById('tooltip').innerHTML = "<b>Hover over map regions to see more information.</b>";
            else
                document.getElementById('tooltip').innerHTML = "&nbsp;";
        },
        tooltip_initialize: function() {
            this.tooltip = new Array(0);
        },
        tooltip_show: function(id) {

            if(this.tooltip.length > 0 && this.enable_tooltip)
            {
                document.getElementById('tooltip').innerHTML = "<b>" + this.tooltip[0].data["id_" + id].name + " (" + this.abbreviations[ this.tooltip[0].data["id_" + id].name ] + ")</b>";

                this.tooltip.forEach(function(v, i){

                    document.getElementById('tooltip').innerHTML += "<br/><i>" + window.cartogram.tooltip[i].label + ":</i> " + window.cartogram.tooltip[i].data["id_" + id].value.toLocaleString() + " " + window.cartogram.tooltip[i].unit;

                });
            }

        },
        draw_bar_chart_from_tooltip(container, tooltip) {

            var margin = {top: 5, right: 5, bottom: 5, left: 5},
                width = 800 - margin.left - margin.right,
                height = 400 - margin.top - margin.bottom;
            
            // ranges
            var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

            var y = d3.scale.linear().range([height, 0]);

            // axes
            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")


            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .ticks(10);
            
            // SVG element
            var svg = d3.select("#" + container).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", 
                "translate(" + margin.left + "," + margin.top + ")");

            // Data formatting
            var data = new Array();

            Object.keys(tooltip.data).forEach(function(key, index){

                data.push(tooltip.data[key]);

            });

            /* Display in alphabetical order */
            data.sort(function(a,b){

                if(a.name<b.name)
                    return -1;
                else if(a.name>b.name)
                    return 1;
                else
                    return 0;

            });
            
            // scale the range of the data
            x.domain(data.map(function(d) { return d.name; }));
            y.domain([0, d3.max(data, function(d) { return d.value; }) + 5]);

            // add axes
            svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", "-.55em")
            .attr("transform", "rotate(-90)" );

            svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 5)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("User Data");

            // add the bar chart
            svg.selectAll("bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.name); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height - y(d.value); });

            /*svg.selectAll(".text")        
            .data(data)
            .enter()
            .append("text")
            .attr("class","label")
            .attr("x", (function(d) { return x(d.name); }  ))
            .attr("y", function(d) { return y(d.value) - 10; })
            .text(function(d) { return d.value; });*/

        },
        do_nonfatal_error: function(message) {
            document.getElementById('non-fatal-error').innerHTML = message;
        },
        clear_nonfatal_error: function() {
            document.getElementById('non-fatal-error').innerHTML = "";
        },
        do_fatal_error: function(message) {
            document.getElementById('error-message').innerHTML = message;

            document.getElementById('loading').style.display = 'none';
            document.getElementById('cartogram').style.display = 'none';

            document.getElementById('error').style.display = 'block';

            if(window.cartogram.fatal_error_extended_info !== null)
            {
                document.getElementById('error-extended-content').innerHTML = window.cartogram.fatal_error_extended_info;
                document.getElementById('error-extended').style.display = 'block';
            }
        },
        enter_loading_state: function() {
            /* We set the height of the loading div to the height of the previously displayed blocks */
            /* This makes transition to the loading state seem less jarring */

            var loading_height = 0;

            if(document.getElementById('cartogram').style.display !== "none")
            {
                loading_height += document.getElementById('cartogram').clientHeight;
            }

            if(document.getElementById('error').style.display !== "none")
            {
                loading_height += document.getElementById('error').clientHeight;
            }

            console.log(loading_height);

            /* The loading div will be at least 100px tall */
            if(loading_height > 100)
            {
                document.getElementById('loading').style.height = loading_height + "px";
            }
            else
            {
                document.getElementById('loading').style.height = "auto";
            }

            document.getElementById('loading').style.display = 'block';
            document.getElementById('cartogram').style.display = 'none';
            document.getElementById('error').style.display = 'none';

            /* Disable interaction with the upload form */
            document.getElementById('upload-button').disabled = true;
            document.getElementById('edit-button').disabled = true;
            document.getElementById('handler').disabled = true;

            /* If GridEdit is open, disable updating */
            if(this.gridedit_window !== null && !this.gridedit_window.closed && typeof(this.gridedit_window.gridedit) === "object")
            {
                this.gridedit_window.gridedit.set_allow_update(false);
            }

            document.getElementById('loading-progress-container').style.display = 'none';

            this.in_loading_state = true;
            this.loading_state = null;
        },
        show_progress_bar: function() {
            document.getElementById('loading-progress-container').style.display = 'block';
            document.getElementById('loading-progress').style.width = "0%";
        },
        update_progress_bar: function(min, max, value) {

            if(value < max)
                value = Math.max(min, value);
            else
                value = Math.min(max, value);

            document.getElementById('loading-progress').style.width = value + "%";
        },
        exit_loading_state: function() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('upload-button').disabled = false;
            document.getElementById('edit-button').disabled = this.edit_button_enabled();
            document.getElementById('handler').disabled = false;

            /* If GridEdit is open, enable updating */
            if(this.gridedit_window !== null && !this.gridedit_window.closed && typeof(this.gridedit_window.gridedit) === "object")
            {
                this.gridedit_window.gridedit.set_allow_update(true);
            }

            this.in_loading_state = false;
        },
        serialize_post_variables: function(vars) {

            var post_string = "";
            var first_entry = true;

            Object.keys(vars).forEach(function(key, index) {

                post_string += (first_entry ? "" : "&" ) + key + "=" + encodeURIComponent(vars[key]);
                first_entry = false;
                
            });

            return post_string;

        },
        /* From Stack Overflow: https://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color-or-rgb-and-blend-colors
        */
        shadeColor2: function(color, percent) {   
            var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
            return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
        },
        highlight_by_id: function(maps, id, value) {

            maps.forEach(function(v){

                elements = document.getElementsByClassName('path-' + v + '-' + id);

                for(i = 0; i < elements.length; i++)
                {
                    //elements[i].setAttribute('fill-opacity', value);
                    elements[i].setAttribute('fill', this.shadeColor2(this.color_data['id_' + id], value));
                    //elements[i].setAttribute('fill', this.shadeColor2(elements[i].getAttribute('fill'), value));
                }

            }, this);

        },
        generate_svg_download_links: function(map1_container, map2_container, map1_link, map2_link, map1_name, map2_name)
        {
            var svg_header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>';

            document.getElementById(map1_link).href = "data:image/svg+xml;base64," + window.btoa(svg_header + document.getElementById(map1_container).innerHTML);
            document.getElementById(map1_link).download = map1_name + ".svg";

            document.getElementById(map2_link).href = "data:image/svg+xml;base64," + window.btoa(svg_header + document.getElementById(map2_container).innerHTML);
            document.getElementById(map2_link).download = map2_name + ".svg";
        },
        generate_social_media_links: function(url)
        {
            document.getElementById('facebook-share').href = "https://www.facebook.com/sharer/sharer.php?u=" + window.encodeURIComponent(url);

            document.getElementById('linkedin-share').href = "https://www.linkedin.com/shareArticle?url=" + window.encodeURIComponent(url) + "&mini=true&title=Cartogram&summary=Create%20cartograms%20with%20go-cart.io&source=go-cart.io";

            document.getElementById('twitter-share').href = "https://twitter.com/share?url=" + window.encodeURIComponent(url);

        },
        scale_labels: function(map, labels) {
            labels.scale_x =  this.scaling_factor * (map.scaled_width/(map.width * labels.scale_x));
            labels.scale_y = this.scaling_factor * (map.scaled_height/(map.height * labels.scale_y));

        },
        draw_d3_graphic: function(this_map, maps, data, element_id, width, height, scale_x, scale_y, labels=null) {

            console.log("Drawing " + this_map + " at scale " + scale_x + " x " + scale_y);

            var a = data.extrema.min_x;

          	var b = data.extrema.max_y;

            var lineFunction = d3.svg.line()
                                     .x(function(d) { return window.cartogram.scaling_factor * (scale_x * (-1*a + d[0])) })
                                     .y(function(d) { return window.cartogram.scaling_factor * (scale_y * (b - d[1])) })
                                     .interpolate("linear");
                                     
            var canvas = d3.select(element_id).append("svg")
            .attr("width", window.cartogram.scaling_factor*width)
            .attr("height", window.cartogram.scaling_factor*height);

            /* Exclude polygons that we're not supposed to draw */

            var processed_features = [];

            data.features.forEach(function(feature, id){

                if(!this.map_config.dont_draw.includes(feature.properties.polygon_id) && !this.map_config.elevate.includes(feature.properties.polygon_id))
                    processed_features.push(feature);

            }, this);

            /* Items which are elevated are drawn at the end */
            this.map_config.elevate.forEach(function(polygon_id){

                for(let i = 0; i < data.features.length; i++)
                {
                    if(data.features[i].properties.polygon_id == polygon_id)
                    {
                        processed_features.push(data.features[i]);
                        break;
                    }
                }

            }, this);

            var group = canvas.selectAll()
              .data(processed_features)
              .enter()
              .append("path")
            
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
              .on('mouseenter', function(d, i) {

                             if(window.cartogram.enable_highlight)
                                window.cartogram.highlight_by_id(maps, d.id, 0.4);
                             if(window.cartogram.enable_tooltip)
                                window.cartogram.tooltip_show(d.id);

                             })
              .on('mouseleave', function(d, i) {
                             if(window.cartogram.enable_highlight)
                                window.cartogram.highlight_by_id(maps, d.id, 0);
                              });
            
            if(labels != null)
            {
                /* First draw the text */

                var text = canvas.selectAll("text")
                                    .data(labels.labels)
                                    .enter()
                                    .append("text");
                
                var textLabels = text.attr('x', function(d) { return labels.scale_x*d.x; })
                                    .attr('y', function(d) { return labels.scale_y*d.y; })
                                    .attr('font-family', 'sans-serif')
                                    .attr('font-size', '8.5px')
                                    .attr('fill', '#000')
                                    .attr('class', 'cartogram-label')
                                    .text(function(d) { return d.text; });
                
                var lines = canvas.selectAll("line")
                                    .data(labels.lines)
                                    .enter()
                                    .append("line");
                
                var labelLines = lines.attr('x1', function(d) { return  labels.scale_x*d.x1; })
                                    .attr('x2', function(d) { return  labels.scale_x*d.x2; })
                                    .attr('y1', function(d) { return labels.scale_y*d.y1; })
                                    .attr('y2', function(d) { return labels.scale_y*d.y2; })
                                    .attr('stroke-width', 1)
                                    .attr('class', 'cartogram-label')
                                    .attr('stroke', '#000');
            }
            
            return polygon_paths;
        },
        get_generated_cartogram: function(areas_string, handler, unique_sharing_key) {

            return new Promise(function(resolve,reject){

                window.cartogram.fatal_error_extended_info = "";

                oboe({
                    url: window.cartogram.cartogram_url,
                    method: "POST",
                    headers: {'Content-type': 'application/x-www-form-urlencoded'},
                    body: window.cartogram.serialize_post_variables({
                    handler: handler,
                    values: areas_string,
                    unique_sharing_key: unique_sharing_key
                    }),
                }).node('loading_progress_points.*', function(loading_progress_point){

                    if(loading_progress_point.loading_point !== null)
                    {
                        if(window.cartogram.loading_state === null)
                        {
                            window.cartogram.loading_state = loading_progress_point.loading_point;
                            window.cartogram.update_progress_bar(0,100,20);
                        }
                        else
                        {
                            if(loading_progress_point.loading_point < 0.01)
                                loading_progress_point.loading_point = 0.01;
                            
                            var percentage = Math.floor(((window.cartogram.loading_state - loading_progress_point.loading_point) / (window.cartogram.loading_state - 0.01))*95);

                            /* It's unlikely to happen, but we don't want the progress bar to go in reverse */
                            window.cartogram.update_progress_bar(20,100,percentage);
                        }
                    }

                    console.log(loading_progress_point.stderr_line);

                    window.cartogram.fatal_error_extended_info += loading_progress_point.stderr_line;

                }).done(function(result){

                    window.cartogram.fatal_error_extended_info = null;

                    window.cartogram.update_progress_bar(0,100,100);

                    resolve(result.cartogram_data);

                }).fail(function(){

                    reject('There was an error retrieving the cartogram from the server.');

                });

            });

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
        http_post: function(url, form_data, headers={}, timeout=15000) {

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

                xhttp.open("POST", url, true);
                xhttp.timeout = timeout;

                Object.keys(headers).forEach(function(key, index) {
                    xhttp.setRequestHeader(key, headers[key]);
                });

                xhttp.send(form_data);

            });

        },
        get_pregenerated_map: function(handler, map_name) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/" + map_name + ".json");
        },
        get_default_colors: function(handler) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/colors.json");
        },
        get_grid_document_template: function(handler) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/griddocument.json");
        },
        get_labels: function(handler) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/labels.json");
        },
        get_abbreviations: function(handler) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/abbreviations.json");
        },
        get_config: function(handler) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/config.json");
        },
        switch_displayed_map: function(map_container, new_map_name){

            if(this.in_loading_state)
                return;
            
            this.in_loading_state = true; // Lock the UI but don't display loading block

            var old_map = this.map_alternates[this.map_alternates.map_selected];
            var new_map = this.map_alternates[new_map_name];
            
            old_map.forEach(function(v, i){

                    var new_path = null;

                    new_map.forEach(function(w,j){

                        if(w.id == v.id)
                            new_path = w.path;

                    });

                    if(new_path != null)
                    {
                        if(this.animation_duration > 0)
                        {
                            d3.select('#path-' + map_container + '-' + v.id)
                            .attr('d', v.path)
                            .transition()
                            .ease(d3.easeCubic)
                            .duration(this.animation_duration)
                            .attr('d', new_path);
                        }
                        else
                        {
                            /* Having a 0 ms duration for the transition causes problems */
                            d3.select('#path-' + map_container + '-' + v.id)
                            .attr('d', new_path);
                        }
                        
                    }

            }, this);

            this.map_alternates.map_selected = new_map_name;

            this.map_alternates.maps_possible.forEach(function(v){

                if(document.getElementById(v + '-selector') === null)
                    return;

                if(v == new_map_name)
                {
                    document.getElementById(v + '-selector').setAttribute('onclick', '');
                    document.getElementById(v + '-selector').classList.add('active');
                }
                else
                {
                    document.getElementById(v + '-selector').setAttribute('onclick', "window.cartogram.switch_displayed_map('" + map_container + "', '" + v + "')");
                    document.getElementById(v + '-selector').classList.remove('active');
                }

            });

            window.setTimeout(function(){window.cartogram.generate_svg_download_links('map-area', 'cartogram-area', 'map-download', 'cartogram-download', 'map', 'cartogram');}, this.animation_duration + 100);

            this.in_loading_state = false;

        },
        create_map_switch_button: function(map, map_container, title, active){

            var button = document.createElement('button');
            button.innerText = title;
            button.id = map + "-selector";

            if(active)
            {
                button.className = "btn btn-secondary active";
            }
            else
            {
                button.className = "btn btn-secondary";
                button.setAttribute('onclick', "window.cartogram.switch_displayed_map('" + map_container + "', '" + map + "');");
            }

            return button;

        },
        draw_three_maps: function(map1, map2, map3, map1_container, map2_3_container, map1_name, map2_name, map3_name, map1_labels=null){

            return new Promise(function(resolve, reject){

                Promise.all([map1, map2, map3]).then(function(values){

                /* Clean up the map containers */

                document.getElementById(map1_container).innerHTML = "";
                document.getElementById(map2_3_container).innerHTML = "";

                document.getElementById('map2-switch-buttons').innerHTML = "";

                /* Now we fill the color information into each map */

                values.forEach(function(value, index){

                    values[index].features.forEach(function(v, i){

                        values[index].features[i].properties.color = window.cartogram.color_data['id_' + values[index].features[i].id];

                    });

                });

                var map_width = Math.max((values[0].extrema.max_x-values[0].extrema.min_x), (values[1].extrema.max_x-values[1].extrema.min_x), (values[2].extrema.max_x-values[2].extrema.min_x));
                var map_height = Math.max((values[0].extrema.max_y-values[0].extrema.min_y), (values[1].extrema.max_y-values[1].extrema.min_y), (values[2].extrema.max_y-values[2].extrema.min_y));

                /* Now we want to make sure that all three maps are displayed with equal area */

                values.forEach(function(value, index){

                    values[index].width = values[index].extrema.max_x-values[index].extrema.min_x;
                    values[index].height = values[index].extrema.max_y-values[index].extrema.min_y;
                    values[index].scaled_width = map_width;
                    values[index].scaled_height = map_height;
                    values[index].scale_x = map_width/(values[index].extrema.max_x-values[index].extrema.min_x);
                    values[index].scale_y = map_height/(values[index].extrema.max_y-values[index].extrema.min_y);

                });

                if(map1_labels !== null)
                {
                    window.cartogram.scale_labels(values[0], map1_labels);
                }
                
                window.cartogram.draw_d3_graphic("map1", ['map1', 'map2'], values[0], "#" + map1_container, map_width, map_height, values[0].scale_x, values[0].scale_y, map1_labels);
                
                window.cartogram.map_alternates.map2 = window.cartogram.draw_d3_graphic("map2", ['map1', 'map2'], values[1], "#" + map2_3_container, map_width, map_height, values[1].scale_x, values[1].scale_y);

                var lineFunction_map1 = d3.svg.line()
                    .x(function(d) { return window.cartogram.scaling_factor * (values[0].scale_x * (-1*(values[0].extrema.min_x) + d[0])) })
                    .y(function(d) { return window.cartogram.scaling_factor * (values[0].scale_y * ((values[0].extrema.max_y) - d[1])) })
                    .interpolate("linear");
                
                var lineFunction_map3 = d3.svg.line()
                    .x(function(d) { return window.cartogram.scaling_factor * (values[2].scale_x * (-1*(values[2].extrema.min_x) + d[0])) })
                    .y(function(d) { return window.cartogram.scaling_factor * (values[2].scale_y * ((values[2].extrema.max_y) - d[1])) })
                    .interpolate("linear");

                window.cartogram.map_alternates.map1 = new Array();
                window.cartogram.map_alternates.map3 = new Array();

                values[0].features.forEach(function(feature){

                    window.cartogram.map_alternates.map1.push({id: feature.properties.polygon_id, path: lineFunction_map1(feature.coordinates)})

                });

                values[2].features.forEach(function(feature){

                    window.cartogram.map_alternates.map3.push({id: feature.properties.polygon_id, path: lineFunction_map3(feature.coordinates)})

                });

                window.cartogram.map_alternates.maps_possible = ['map1', 'map2', 'map3'];
                window.cartogram.map_alternates.map_selected = "map2";

                if(window.cartogram.enable_switching)
                {
                    document.getElementById('map1-switch').style.display = 'block';
                    document.getElementById('map2-switch').style.display = 'block';
                }
                else
                {
                    document.getElementById('map1-switch').style.display = 'none';
                    document.getElementById('map2-switch').style.display = 'none';
                }
                
                if(window.cartogram.enable_toplabel)
                {
                    document.getElementById('map1-toplabel').style.display = 'block';
                    document.getElementById('map2-toplabel').style.display = 'block';
                }
                else
                {
                    document.getElementById('map1-toplabel').style.display = 'none';
                    document.getElementById('map2-toplabel').style.display = 'none';
                }

                document.getElementById('map1-toplabel').innerText = map1_name;
                document.getElementById('map2-toplabel').innerText = map2_name;

                if(!window.cartogram.hide_maps_by_id.includes(2))
                {
                    document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map2', 'map2', map2_name, true));
                }

                if(!window.cartogram.hide_maps_by_id.includes(3))
                {
                    document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map3', 'map2', map3_name, false));
                }

                if(!window.cartogram.hide_maps_by_id.includes(1))
                {
                    document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map1', 'map2', map1_name, false));
                }               
                
                resolve(values);

                },reject);

            });
            

        },
        draw_two_maps: function(map1, map2, map1_container, map2_container, map1_name, map2_name, map1_labels=null) {

            this.tooltip_clear();

            return new Promise(function(resolve, reject){

                Promise.all([map1, map2]).then(function(values){

                /* Clean up the map containers */

                document.getElementById(map1_container).innerHTML = "";
                document.getElementById(map2_container).innerHTML = "";

                document.getElementById('map2-switch-buttons').innerHTML = "";

                document.getElementById('map1-switch').style.display = 'none';
                document.getElementById('map2-switch').style.display = 'none';

                /* Now we fill the color information into both maps */

                values.forEach(function(value, index){

                    values[index].features.forEach(function(v, i){

                        values[index].features[i].properties.color = window.cartogram.color_data['id_' + values[index].features[i].id];

                    });

                });



                /* Now we want to make sure that both maps are displayed with an equal area. */

                var map_width = Math.max((values[0].extrema.max_x-values[0].extrema.min_x), (values[1].extrema.max_x-values[1].extrema.min_x));
                var map_height = Math.max((values[0].extrema.max_y-values[0].extrema.min_y), (values[1].extrema.max_y-values[1].extrema.min_y));

                values.forEach(function(value, index){

                    values[index].width = values[index].extrema.max_x-values[index].extrema.min_x;
                    values[index].height = values[index].extrema.max_y-values[index].extrema.min_y;
                    values[index].scaled_width = map_width;
                    values[index].scaled_height = map_height;
                    values[index].scale_x = map_width/(values[index].extrema.max_x-values[index].extrema.min_x);
                    values[index].scale_y = map_height/(values[index].extrema.max_y-values[index].extrema.min_y);

                });

                if(map1_labels !== null)
                {
                    window.cartogram.scale_labels(values[0], map1_labels);
                }

                window.cartogram.map_alternates.map1 = window.cartogram.draw_d3_graphic("map1", ['map2', 'map1'], values[0], "#" + map1_container, map_width, map_height, values[0].scale_x, values[0].scale_y, map1_labels);

                window.cartogram.map_alternates.map2 = window.cartogram.draw_d3_graphic("map2", ['map2', 'map1'], values[1], "#" + map2_container, map_width, map_height, values[1].scale_x, values[1].scale_y);

                window.cartogram.map_alternates.maps_possible = ['map1', 'map2'];
                window.cartogram.map_alternates.map_selected = "map2";

                if(window.cartogram.enable_switching)
                {
                    document.getElementById('map1-switch').style.display = 'block';
                    document.getElementById('map2-switch').style.display = 'block';
                }
                else
                {
                    document.getElementById('map1-switch').style.display = 'none';
                    document.getElementById('map2-switch').style.display = 'none';
                }

                if(window.cartogram.enable_toplabel)
                {
                    document.getElementById('map1-toplabel').style.display = 'block';
                    document.getElementById('map2-toplabel').style.display = 'block';
                }
                else
                {
                    document.getElementById('map1-toplabel').style.display = 'none';
                    document.getElementById('map2-toplabel').style.display = 'none';
                }

                document.getElementById('map1-toplabel').innerText = map1_name;
                document.getElementById('map2-toplabel').innerText = map2_name;

                if(!window.cartogram.hide_maps_by_id.includes(2))
                {
                    document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map2', 'map2', map2_name, true));
                }

                if(!window.cartogram.hide_maps_by_id.includes(1))
                {
                    document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map1', 'map2', map1_name, false));
                }

                resolve(values);

            }, reject);

            });

        },
        on_gridedit_update: function(gd)
        {
            if(this.in_loading_state)
                return;
            
            this.request_and_draw_cartogram(gd, null, false);
        },
        request_and_draw_cartogram: function(gd=null,handler=null,update_grid_document=true){

            if(this.in_loading_state)
                return false;
            
            this.clear_nonfatal_error();

            /* Do some validation */

            if(gd === null)
            {
                if(document.getElementById('csv').files.length < 1)
                {
                    this.do_nonfatal_error('You must upload CSV data.');
                    return false;
                }
            }
            

            this.tooltip_clear();
            this.tooltip_initialize();
            this.enter_loading_state();
            this.show_progress_bar();

            if(handler === null)
            {
                handler = document.getElementById('handler').value;
            }

            var cartogramui_promise = null;
            
            if(gd === null)
            {
                var form_data = new FormData();

                form_data.append("handler", handler);
                form_data.append("csv", document.getElementById('csv').files[0]);

                cartogramui_promise = this.http_post(this.cartogramui_url, form_data);
            }
            else
            {
                var cartogramui_req_body = this.gen_cartogramui_req_body_from_grid_document(handler, gd);

                cartogramui_promise = this.http_post(this.cartogramui_url, cartogramui_req_body[1], {
                    'Content-Type': 'multipart/form-data; boundary=' + cartogramui_req_body[0]
                });
            }            
            
            Promise.all([cartogramui_promise, this.get_labels(handler)]).then(function(responses){

                if(responses[0].error == "none")
                {
                    window.cartogram.color_data = responses[0].color_data;

                    window.cartogram.draw_three_maps(window.cartogram.get_pregenerated_map(handler, "original"), window.cartogram.get_generated_cartogram(responses[0].areas_string, handler, responses[0].unique_sharing_key), window.cartogram.get_pregenerated_map(handler, "population"), "map-area", "cartogram-area", "Land Area", responses[0].tooltip.label, "Population", responses[1]).then(function(v){

                        window.cartogram.tooltip.push(v[0].tooltip);
                        window.cartogram.tooltip.push(v[2].tooltip);
                        window.cartogram.tooltip.push(responses[0].tooltip);

                        window.cartogram.generate_svg_download_links('map-area', 'cartogram-area', 'map-download', 'cartogram-download', 'map', 'cartogram');

                        window.cartogram.generate_social_media_links("https://go-cart.io/cart/" + v[1].unique_sharing_key);

                        if(update_grid_document)
                            window.cartogram.update_grid_document(responses[0].grid_document);
                        
                        window.cartogram.exit_loading_state();
                        document.getElementById('cartogram').style.display = "block"; //Bootstrap rows use blockbox

                    }, function(e){
                        window.cartogram.do_fatal_error(e);

                        window.cartogram.draw_bar_chart_from_tooltip('barchart', responses[0].tooltip);
                        document.getElementById('barchart-container').style.display = "block";
                    });
                }
                else
                {
                    window.cartogram.exit_loading_state();
                    document.getElementById('cartogram').style.display = "block"; //Bootstrap rows use blockbox
                    window.cartogram.do_nonfatal_error(responses[0].error);
                }

            }, this.do_fatal_error);

            return false; // We don't want to submit the form

        },
        switch_cartogram_type: function(type, colors=null) {

            if(this.in_loading_state)
                return;
            
            this.enter_loading_state();

            this.tooltip_clear();
            this.tooltip_initialize();

            if(colors === null)
                colors = this.get_default_colors(type);

            Promise.all([colors, this.get_grid_document_template(type), this.get_labels(type), this.get_config(type), this.get_abbreviations(type)]).then(function(values){

              window.cartogram.color_data = values[0];
              window.cartogram.map_config = values[3];
              window.cartogram.abbreviations = values[4];
              

              window.cartogram.draw_two_maps(window.cartogram.get_pregenerated_map(type, "original"), window.cartogram.get_pregenerated_map(type, "population"), "map-area", "cartogram-area", "Land Area", "Human Population", values[2]).then(function(v){

                window.cartogram.tooltip.push(v[0].tooltip);
                window.cartogram.tooltip.push(v[1].tooltip);

                window.cartogram.generate_svg_download_links('map-area', 'cartogram-area', 'map-download', 'cartogram-download', 'map', 'cartogram');

                document.getElementById('template-link').href = window.cartogram.cartogram_data_dir+ "/" + type + "/template.csv";

                window.cartogram.update_grid_document(values[1]);
                
                window.cartogram.exit_loading_state();
                document.getElementById('cartogram').style.display = 'block'; // Bootstrap rows use blockbox
              }, window.cartogram.do_fatal_error); 

            }, this.do_fatal_error);
        }

    };

    window.onbeforeunload = function() {
        if(window.cartogram.gridedit_window !== null && !window.cartogram.gridedit_window.closed)
        {
            window.cartogram.gridedit_window.close();
        }
    }
}

function clearFileInput(ctrl) {
    try {
      ctrl.value = null;
    } catch(ex) { }
    if (ctrl.value) {
      ctrl.parentNode.replaceChild(ctrl.cloneNode(true), ctrl);
    }
  }

function cartogram_init(c_u, cui_u, c_d)
{
    window.cartogram = {

        in_loading_state: false,
        cartogram_url: c_u,
        cartogramui_url: cui_u,
        cartogram_data_dir: c_d,
        color_data: null,
        map_alternates: {
            map1: null,
            map2: null,
            map3: null,
            map_selected: '',
            maps_possible: []
        },
        tooltip: new Array(0),
        loading_state: null,
        fatal_error_extended_info: null,
        tooltip_clear: function() {
            document.getElementById('tooltip').innerHTML = "<b>Hover over map regions to see more information.</b>";
        },
        tooltip_initialize: function() {
            this.tooltip = new Array(0);
        },
        tooltip_show: function(id) {

            if(this.tooltip.length > 0)
            {
                document.getElementById('tooltip').innerHTML = "<b>" + this.tooltip[0].data["id_" + id].name + "</b>";

                this.tooltip.forEach(function(v, i){

                    document.getElementById('tooltip').innerHTML += "<br/><i>" + window.cartogram.tooltip[i].label + ":</i> " + window.cartogram.tooltip[i].data["id_" + id].value.toLocaleString() + " " + window.cartogram.tooltip[i].unit;

                });
            }

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
            document.getElementById('handler').disabled = true;

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
            document.getElementById('handler').disabled = false;
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
        highlight_by_id: function(maps, id, value) {

            maps.forEach(function(v){

                elements = document.getElementsByClassName('path-' + v + '-' + id);

                for(i = 0; i < elements.length; i++)
                {
                    elements[i].setAttribute('fill-opacity', value);
                }

            });

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
        draw_d3_graphic: function(this_map, maps, data, element_id, width, height, scale_x, scale_y) {

            var a = data.extrema.min_x;

          	var b = data.extrema.max_y;

            var lineFunction = d3.svg.line()
                                     .x(function(d) { return scale_x * (-1*a + d[0]) })
                                     .y(function(d) { return scale_y * (b - d[1]) })
                                     .interpolate("linear");
                                     
            var canvas = d3.select(element_id).append("svg")
            .attr("width", width)
            .attr("height", height);

            var group = canvas.selectAll()
              .data(data.features)
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
              .on('mouseover', function(d, i) {
                             window.cartogram.highlight_by_id(maps, d.id, 0.6);

                             window.cartogram.tooltip_show(d.id);

                             })
              .on('mouseout', function(d, i) {
                             window.cartogram.highlight_by_id(maps, d.id, 1);
                              });
            
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
        http_get: function(url) {

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

                xhttp.open("GET", url, true);
                xhttp.send();

            });

        },
        http_post: function(url, form_data) {

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

                xhttp.open("POST", url, true);
                xhttp.send(form_data);

            });

        },
        get_pregenerated_map: function(handler, map_name) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/" + map_name + ".json");
        },
        get_default_colors: function(handler) {
            return this.http_get(this.cartogram_data_dir + "/" + handler + "/colors.json");
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
                        d3.select('#path-' + map_container + '-' + v.id)
                        .attr('d', v.path)
                        .transition()
                        .ease(d3.easeCubic)
                        .duration(1000)
                        .attr('d', new_path);
                    }

                });

            this.map_alternates.map_selected = new_map_name;

            this.map_alternates.maps_possible.forEach(function(v){

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

            window.setTimeout(function(){window.cartogram.generate_svg_download_links('map-area', 'cartogram-area', 'map-download', 'cartogram-download', 'map', 'cartogram');}, 1100);

            this.in_loading_state = false;

        },
        create_map_switch_button: function(map, map_container, title, active){

            var button = document.createElement('button');
            button.innerText = title;
            button.id = map + "-selector";

            if(active)
            {
                button.className = "btn btn-secondary btn-sm active";
            }
            else
            {
                button.className = "btn btn-secondary btn-sm";
                button.setAttribute('onclick', "window.cartogram.switch_displayed_map('" + map_container + "', '" + map + "');");
            }

            return button;

        },
        draw_three_maps: function(map1, map2, map3, map1_container, map2_3_container, map1_name, map2_name, map3_name){

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

                    values[index].scale_x = map_width/(values[index].extrema.max_x-values[index].extrema.min_x);
                    values[index].scale_y = map_height/(values[index].extrema.max_y-values[index].extrema.min_y);

                });
                
                window.cartogram.draw_d3_graphic("map1", ['map1', 'map2'], values[0], "#" + map1_container, map_width, map_height, values[0].scale_x, values[0].scale_y);
                
                window.cartogram.map_alternates.map2 = window.cartogram.draw_d3_graphic("map2", ['map1', 'map2'], values[1], "#" + map2_3_container, map_width, map_height, values[1].scale_x, values[1].scale_y);

                var lineFunction_map1 = d3.svg.line()
                    .x(function(d) { return values[0].scale_x * (-1*(values[0].extrema.min_x) + d[0]) })
                    .y(function(d) { return values[0].scale_y * ((values[0].extrema.max_y) - d[1]) })
                    .interpolate("linear");
                
                var lineFunction_map3 = d3.svg.line()
                    .x(function(d) { return values[2].scale_x * (-1*(values[2].extrema.min_x) + d[0]) })
                    .y(function(d) { return values[2].scale_y * ((values[2].extrema.max_y) - d[1]) })
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

                document.getElementById('map1-switch').style.display = 'block';
                document.getElementById('map2-switch').style.display = 'block';

                document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map2', 'map2', map2_name, true));
                document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map3', 'map2', map3_name, false));
                document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map1', 'map2', map1_name, false));
                
                resolve(values);

                },reject);

            });
            

        },
        draw_two_maps: function(map1, map2, map1_container, map2_container, map1_name, map2_name) {

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

                    values[index].scale_x = map_width/(values[index].extrema.max_x-values[index].extrema.min_x);
                    values[index].scale_y = map_height/(values[index].extrema.max_y-values[index].extrema.min_y);

                });

                window.cartogram.map_alternates.map1 = window.cartogram.draw_d3_graphic("map1", ['map2', 'map1'], values[0], "#" + map1_container, map_width, map_height, values[0].scale_x, values[0].scale_y);

                window.cartogram.map_alternates.map2 = window.cartogram.draw_d3_graphic("map2", ['map2', 'map1'], values[1], "#" + map2_container, map_width, map_height, values[1].scale_x, values[1].scale_y);

                window.cartogram.map_alternates.maps_possible = ['map1', 'map2'];
                window.cartogram.map_alternates.map_selected = "map2";

                document.getElementById('map1-switch').style.display = 'block';
                document.getElementById('map2-switch').style.display = 'block';

                document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map2', 'map2', map2_name, true));
                document.getElementById('map2-switch-buttons').appendChild(window.cartogram.create_map_switch_button('map1', 'map2', map1_name, false));

                resolve(values);

            }, reject);

            });

        },
        request_and_draw_cartogram: function(){

            if(this.in_loading_state)
                return false;
            
            this.clear_nonfatal_error();

            /* Do some validation */

            if(document.getElementById('csv').files.length < 1)
            {
                this.do_nonfatal_error('You must upload CSV data.');
                return false;
            }

            this.tooltip_clear();
            this.tooltip_initialize();
            this.enter_loading_state();
            this.show_progress_bar();
            
            var handler = document.getElementById('handler').value;

            var form_data = new FormData();

            form_data.append("handler", handler);
            form_data.append("csv", document.getElementById('csv').files[0]);
            
            this.http_post(this.cartogramui_url, form_data).then(function(response){

                if(response.error == "none")
                {
                    window.cartogram.color_data = response.color_data;

                    window.cartogram.draw_three_maps(window.cartogram.get_pregenerated_map(handler, "original"), window.cartogram.get_generated_cartogram(response.areas_string, handler, response.unique_sharing_key), window.cartogram.get_pregenerated_map(handler, "population"), "map-area", "cartogram-area", "Land Area", "User Data", "Population").then(function(v){

                        window.cartogram.tooltip.push(v[0].tooltip);
                        window.cartogram.tooltip.push(v[2].tooltip);
                        window.cartogram.tooltip.push(response.tooltip);

                        window.cartogram.generate_svg_download_links('map-area', 'cartogram-area', 'map-download', 'cartogram-download', 'map', 'cartogram');

                        window.cartogram.generate_social_media_links("https://go-cart.io/cart/" + v[1].unique_sharing_key);
                        
                        window.cartogram.exit_loading_state();
                        document.getElementById('cartogram').style.display = "flex"; //Bootstrap rows use flexbox

                    }, window.cartogram.do_fatal_error);
                }
                else
                {
                    window.cartogram.exit_loading_state();
                    document.getElementById('cartogram').style.display = "flex"; //Bootstrap rows use flexbox
                    window.cartogram.do_nonfatal_error(response.error);
                }

            }, this.do_fatal_error);

            return false; // We don't want to submit the form

        },
        switch_cartogram_type: function(type) {

            if(this.in_loading_state)
                return;
            
            this.enter_loading_state();

            this.tooltip_clear();
            this.tooltip_initialize();

            this.get_default_colors(type).then(function(colors){

              window.cartogram.color_data = colors;

              window.cartogram.draw_two_maps(window.cartogram.get_pregenerated_map(type, "original"), window.cartogram.get_pregenerated_map(type, "population"), "map-area", "cartogram-area", "Land Area", "Population").then(function(v){

                window.cartogram.tooltip.push(v[0].tooltip);
                window.cartogram.tooltip.push(v[1].tooltip);

                window.cartogram.generate_svg_download_links('map-area', 'cartogram-area', 'map-download', 'cartogram-download', 'map', 'cartogram');

                document.getElementById('template-link').href = window.cartogram.cartogram_data_dir+ "/" + type + "/template.csv";
                
                window.cartogram.exit_loading_state();
                document.getElementById('cartogram').style.display = 'flex'; // Bootstrap rows use flexbox
              }, window.cartogram.do_fatal_error); 

            }, this.do_fatal_error);
        }

    };
}

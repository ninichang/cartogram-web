function cartogram_init(c_u, c_d, c)
{
    window.cartogram = {

        in_loading_state: false,
        cartogram_url: c_u,
        cartogram_data_dir: c_d,
        color_data: c,
        do_fatal_error: function(message) {
            document.getElementById('error-message').innerHTML = message;

            document.getElementById('loading').style.display = 'none';
            document.getElementById('cartogram').style.display = 'none';

            document.getElementById('error').style.display = 'block';
        },
        enter_loading_state: function() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('cartogram').style.display = 'none';
            document.getElementById('error').style.display = 'none';

            this.in_loading_state = true;
        },
        exit_loading_state: function() {
            document.getElementById('loading').style.display = 'none';
            in_loading_state = false;
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

            var areas = group.attr("d",function(d) {return lineFunction(d.coordinates);})
                       .attr("class", function(d){ return "area" + " path-" + this_map + "-" + d.id;})
                     .attr("fill", function(d) {return d.properties.color})
                     .on('mouseover', function(d, i) {
                             window.cartogram.highlight_by_id(maps, d.id, 0.6);
                             })
                   	 .on('mouseout', function(d, i) {
                             window.cartogram.highlight_by_id(maps, d.id, 1);
                              });
        },
        get_generated_cartogram: function(areas_string, handler) {

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
                                reject('Input string does not have a proper JSON format.');
                            }
                        }
                        else
                        {
                            reject('Unable to fetch the cartogram from the server.');
                        }
                    }
                    
                };

                xhttp.open("POST", window.cartogram.cartogram_url, true);
                xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                xhttp.send(window.cartogram.serialize_post_variables({
                    handler: handler,
                    values: areas_string
                }));

            });

        },
        get_pregenerated_map: function(handler, map_name) {

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
                                reject('Input string does not have a proper JSON format.');
                            }
                        }
                        else
                        {
                            reject('Unable to fetch the cartogram from the server.');
                        }
                    }
                };

                xhttp.open("GET", window.cartogram.cartogram_data_dir + "/" + handler + "/" + map_name + ".json", true);
                xhttp.send();

            });

        },
        draw_cartogram: function(areas_string, handler) {

            if(this.in_loading_state)
                return;
            
            this.enter_loading_state();

            Promise.all([this.get_generated_cartogram(areas_string, handler), this.get_pregenerated_map(handler, "original")]).then(function(values){

                /* Now we fill the color information into both maps */

                values.forEach(function(value, index){

                    values[index].features.forEach(function(v, i){

                        values[index].features[i].properties.color = window.cartogram.color_data['id_' + values[index].features[i].id];

                    });

                });

                /* Now we want to make sure that both maps are displayed with an equal area. */

                var map_width = Math.max((values[0].extrema.max_x-values[0].extrema.min_x), (values[1].extrema.max_x-values[1].extrema.min_x));
                var map_height = Math.max((values[0].extrema.max_y-values[0].extrema.min_y), (values[1].extrema.max_y-values[1].extrema.min_y));

                var scale_original_x = 1;
                var scale_original_y = 1;                
                var scale_cartogram_x = 1;
                var scale_cartogram_y = 1;

                if((values[0].extrema.max_x - values[0].extrema.min_x) > (values[1].extrema.max_x - values[1].extrema.min_x))
                {
                    /* The original map is wider than the cartogram */

                    scale_original_x = (values[0].extrema.max_x - values[0].extrema.min_x)/(values[1].extrema.max_x - values[1].extrema.min_x);
                }
                else
                {
                    /* The cartogram is wider than the original map */

                    scale_cartogram_x = (values[1].extrema.max_x - values[1].extrema.min_x)/(values[0].extrema.max_x - values[0].extrema.min_x);
                }

                if((values[0].extrema.max_y - values[0].extrema.min_y) > (values[1].extrema.max_y - values[1].extrema.min_y))
                {
                    /* The original map is taller than the cartogram */

                    scale_original_y = (values[0].extrema.max_y - values[0].extrema.min_y)/(values[1].extrema.max_y - values[1].extrema.min_y);
                }
                else
                {
                    /* The cartogram is taller than the original map */

                    scale_cartogram_y = (values[1].extrema.max_y - values[1].extrema.min_y)/(values[0].extrema.max_y - values[0].extrema.min_y);
                }

                console.log(map_width);
                console.log(map_height);

                console.log(scale_original_x);
                console.log(scale_original_y);

                console.log(scale_cartogram_x);
                console.log(scale_cartogram_y);



                window.cartogram.draw_d3_graphic("cartogram", ['cartogram', 'original'], values[0], "#cartogram-area", map_width, map_height, scale_cartogram_x, scale_cartogram_y);
                window.cartogram.draw_d3_graphic("original", ['cartogram', 'original'], values[1], "#map-area", map_width, map_height, scale_original_x, scale_original_y);

                window.cartogram.exit_loading_state();

                document.getElementById('cartogram').style.display = 'flex'; //Bootstrap rows use flexbox

            }, this.do_fatal_error);

        }

    };
}
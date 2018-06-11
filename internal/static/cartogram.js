function cartogram_init(c_u)
{
    window.cartogram = {

        in_loading_state: false,
        cartogram_url: c_u,
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
        draw_cartogram: function(areas_string, handler) {

            if(this.in_loading_state)
                return;
            
            this.enter_loading_state();

            var xhttp = new XMLHttpRequest();

            xhttp.onreadystatechange = function() {
                if(this.readyState == 4)
                {
                    if(this.status == 200)
                    {
                        try {
                        data = JSON.parse(this.responseText);
                        } catch (e) {	
                        window.cartogram.do_fatal_error('Input string does not have a proper JSON format.');
                        return;
                        }
                        
                        var a = 0;
                        var b = 600;
                        var k = 1;

                        var lineFunction = d3.svg.line()
                                                .x(function(d) { return a + k * d[0]; })
                                                .y(function(d) { return b - k * d[1]; })
                                                .interpolate("linear");
                                                
                        var canvas = d3.select("#cartogram").append("svg")
                        .attr("width", 1000)
                        .attr("height", 1000);

                        var group = canvas.selectAll()
                        .data(data.features)
                        .enter()
                        .append("path");

                        var areas = group.attr("d",function(d) {return lineFunction(d.coordinates);})
                                        .attr("class", "area")
                                        .attr("fill", function(d) {return d.properties.color})
                                        .on('mouseover', function(d, i) {
                                            var currentState = this;
                                            d3.select(this).style('fill-opacity', 0.6);
                                            })
                                            .on('mouseout', function(d, i) {
                                            var currentState = this;
                                            d3.select(this).style('fill', function(d) {return d.properties.color})
                                                            .style('fill-opacity', 1);
                                            });
                        
                        window.cartogram.exit_loading_state();
                        document.getElementById('cartogram').style.display = 'block';
                    }
                    else
                    {
                        window.cartogram.do_fatal_error('Unable to fetch the cartogram from the server.');
                    }
                }
            };

            xhttp.open("POST", this.cartogram_url, true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send(this.serialize_post_variables({
                handler: 'usa',
                values: areas_string
            }));


        }

    };
}
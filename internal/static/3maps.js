function interactivity_message(all_features, deactivations){

    var enabled_feautures = [];

    all_features.forEach(function(feature){

        if(!deactivations.includes(feature.name))
            enabled_feautures.push(feature.description);

    });

    if(enabled_feautures.length == 0)
        return "You have access to no interactive features.";
    
    if(enabled_feautures.length == 1)
        return "You have access to the " + enabled_feautures[0] + " feature.";
    
    var msg = "You have access to the ";

    for(let i = 0; i < enabled_feautures.length; i++)
    {
        if(i == (enabled_feautures.length - 1))
            msg += " and";
        
        msg += " " + enabled_feautures[i];

        if(i != (enabled_feautures.length - 1) && enabled_feautures.length != 2)
            msg += ",";     
    }

    msg += " features.";

    return msg;

}

function draw_3maps(data_base_url, handler, maps, deactivations, hide)
{
    if(window.cartogram.in_loading_state || maps.length != 3)
        return;
    
    window.cartogram.scaling_factor = 1.5;

    deactivations = deactivations.split(",");

    if(hide.trim() === "")
    {
        hide = [];
    }
    else
    {
        hide = hide.split(",");
        
        hide.forEach(function(h,i){
            hide[i] = parseInt(h);
        });
    }

    

    if(hide.length > 0)
    {
        window.cartogram.scaling_factor = 1.7;

        var col_width = 6;

        if(hide.length > 1)
        {
            col_width = 12;
        }

        (function(h){
            [1,2,3].forEach(function(map_id){

                console.log(h);

                if(h.includes(map_id))
                {
                    document.getElementById('map' + map_id + '-container').style.display = 'none';
                }
                
                document.getElementById('map' + map_id + '-container').className = 'col-md-' + col_width;
    
            });
        }(hide));
        


    }

    window.cartogram.enable_highlight = !(deactivations.includes('highlight'));
    window.cartogram.enable_tooltip = !(deactivations.includes('tooltip'));

    window.cartogram.get_config(handler).then(function(config){

        window.cartogram.get_abbreviations(handler).then(function(abbreviations){

            window.cartogram.map_config = config;
            window.cartogram.abbreviations = abbreviations;

        maps.forEach(function(map, index){

            if(map.type === "pregen")
            {
                var promise_array = [
                    window.cartogram.get_pregenerated_map(handler, map.name),
                    window.cartogram.get_default_colors(handler)
                ];
    
                if(map.name === "original")
                    promise_array.push(window.cartogram.get_labels(handler));
    
                maps[index].promise = Promise.all(promise_array);
    
            }
            else
            {
                var promise_array = [
                    window.cartogram.http_get(data_base_url + "/" + map.name + "_cartogram.json"),
                    window.cartogram.http_get(data_base_url + "/" + map.name + "_cartogramui.json")
                ];
    
                maps[index].promise = Promise.all(promise_array);
            }
        });
    
        Promise.all(maps.map(map => map.promise)).then(function(mps){
    
            mps.forEach(function(mp, index){
    
                maps[index].map = mp[0];
    
                if(maps[index].type == "pregen")
                {
                    maps[index].colors = mp[1];
                    maps[index].tooltip = mp[0].tooltip;
    
                    if(maps[index].name === "original")
                        maps[index].labels = mp[2];
                }
                else
                {
                    maps[index].colors = mp[1].color_data;
                    maps[index].tooltip = mp[1].tooltip;
                }
    
            });
    
            /* Fill in the color information */
            maps.forEach(function(map, index){
    
                map.map.features.forEach(function(feature, i){
    
                    maps[index].map.features[i].properties.color = maps[1].colors['id_' + maps[index].map.features[i].id];
    
                });
    
            });

            window.cartogram.color_data = maps[1].colors;
    
            /* Resize the maps, and the labels if necessary. Then, draw the map */
            var map_width = Math.max((maps[0].map.extrema.max_x - maps[0].map.extrema.min_x), (maps[1].map.extrema.max_x - maps[1].map.extrema.min_x), (maps[2].map.extrema.max_x - maps[2].map.extrema.min_x));
            var map_height = Math.max((maps[0].map.extrema.max_y - maps[0].map.extrema.min_y),(maps[1].map.extrema.max_y - maps[1].map.extrema.min_y), (maps[2].map.extrema.max_y - maps[2].map.extrema.min_y));
    
            var map_ids = [];
    
            maps.forEach(function(map, index){
                map_ids.push("map" + (index + 1));
            });
    
            window.cartogram.tooltip_clear();
            window.cartogram.tooltip_initialize();
    
            maps.forEach(function(map, index){
    
                maps[index].map.width = maps[index].map.extrema.max_x-maps[index].map.extrema.min_x;
                maps[index].map.height = maps[index].map.extrema.max_y-maps[index].map.extrema.min_y;
                maps[index].map.scaled_width = map_width;
                maps[index].map.scaled_height = map_height;
                maps[index].map.scale_x = map_width/(maps[index].map.extrema.max_x-maps[index].map.extrema.min_x);
                maps[index].map.scale_y = map_height/(maps[index].map.extrema.max_y-maps[index].map.extrema.min_y);
    
                if(maps[index].hasOwnProperty('labels'))
                {
                    window.cartogram.scale_labels(maps[index].map, maps[index].labels);
                }
    
                window.cartogram.draw_d3_graphic(map_ids[index], map_ids, maps[index].map, '#' + map_ids[index], map_width, map_height, maps[index].map.scale_x, maps[index].map.scale_y, (maps[index].hasOwnProperty('labels') ? maps[index].labels : null));
    
                window.cartogram.tooltip.push(maps[index].tooltip);
                
                document.getElementById(map_ids[index] + '-name').innerText = maps[index].tooltip.label;
    
            });

            document.getElementById('interactivity-message').innerText = interactivity_message([
                {'name': 'tooltip', 'description': 'infotips'},
                {'name': 'highlight', 'description': 'parallel highlighting'}
            ], deactivations);
    
            document.getElementById('loading').style.display = "none";
            document.getElementById('cartogram').style.display = "block";
            
        }, function(e){
            console.log(e);
        });

    }, function(e){
        console.log(e);
    });
}, function(e){
    console.log(e);
});
    
    
}
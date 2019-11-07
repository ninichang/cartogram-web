/**
 * @fileOverview This file contains the frontend UI for the go-cart.io web application
 * @author Ian Duncan
 * @version 2.0.0
 */

 /**
  * Extrema for a map
  * @typedef {Object} Extrema
  * @property {number} min_x
  * @property {number} max_x
  * @property {number} min_y
  * @property {number} max_y
  */

/**
 * Configuration for a map. Some maps do not display properly without modification. This configuration information
 * allows us to draw maps properly by hiding certain polygons, and changing the order in which they are drawn.
 * @typedef {Object} MapConfig
 * @property {Array} dont_draw A list of polygon IDs not to draw
 * @property {Array} elevate A list of polygon IDs to draw after all others
 */

/**
 * Labels for a map version
 * @typedef {Object} Labels
 * @property {number} scale_x Horizontal scaling factor for all label coordinates
 * @property {number} scale_y Vertical scaling factor for all label coordinates
 * @property {Array<{x: number, y: number, text: string}>} labels Text labels
 * @property {Array<{x1: number, y1: number, x2: number, y2: number}>} lines Line labels
 */

function clearFileInput(ctrl) {
    try {
      ctrl.value = null;
    } catch(ex) { }
    if (ctrl.value) {
      ctrl.parentNode.replaceChild(ctrl.cloneNode(true), ctrl);
    }
  }

/**
 * HTTP contains some helper methods for making AJAX requests
 */
class HTTP {

    /**
     * Performs an HTTP GET request and returns a promise with the JSON value of the response
     * @param {string} url The URL of the GET request 
     * @param {number} timeout The timeout, in seconds, of the GET request
     * @param {function} onprogress A function to be called when the request progress information is updated
     * @returns {Promise} A promise to the HTTP response
     */
    static get(url, timeout=null, onprogress=null) {
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
                            reject(Error('Unable to parse output.'));
                        }
                    }
                    else
                    {
                        console.log(url);
                        reject(Error('Unable to fetch data from the server.'));
                    }
                }
            };

            if(onprogress !== null) {
                xhttp.onprogress = onprogress;
            }

            xhttp.ontimeout = function(e) {
                reject(Error('The request has timed out.'));
            }

            if(timeout !== null) {
                xhttp.timeout = timeout;
            }

            xhttp.open("GET", url, true);
            xhttp.send();

        });
    }

    /**
     * Performs an HTTP POST request and returns a promise with the JSON value of the response
     * @param {string} url The URL of the POST request
     * @param {any} form_data The body or form data of the POST request
     * @param {Object} headers The headers of the POST request
     * @param {number} timeout The timeout, in seconds, of the GET request
     * @returns {Promise<Object|string>} A promise to the HTTP response
     */
    static post(url, form_data, headers={}, timeout=15000) {

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
                            reject(Error('Unable to parse output.'));
                        }
                    }
                    else
                    {
                        console.log(url);
                        reject(Error('Unable to fetch data from the server.'));
                    }
                }
            };

            xhttp.ontimeout = function(e) {
                reject(Error('The request has timed out.'));
            }

            xhttp.open("POST", url, true);
            xhttp.timeout = timeout;

            Object.keys(headers).forEach(function(key, index) {
                xhttp.setRequestHeader(key, headers[key]);
            });

            xhttp.send(form_data);

        });
        
    }

    /**
     * Performs an HTTP request when a streaming response is expected.
     * @param {string} url The URL of the request
     * @param {string} method The HTTP method of the request
     * @param {Object.<string,string>} headers The HTTP headers of the request
     * @param {string} body The body of the request
     * @param {Object.<string,Function>} nodes A map of JSON nodes to event handlers that will be called when a new JSON
     * element matching the node description is detected.
     * @returns {Promise}
     */
    static streaming(url, method, headers, body, nodes) {

        return new Promise(function(resolve,reject){

            var oboe_request = oboe({
                url: url,
                method: method,
                headers: headers,
                body: body,
            });
    
            Object.keys(nodes).forEach(function(node){
    
                oboe_request = oboe_request.node(node, nodes[node]);
    
            });
    
            oboe_request = oboe_request.done(result => resolve(result));
            oboe_request = oboe_request.fail(() => reject(Error('Unable to fetch data from the server.')));

        });        

    }

    /**
     * serializePostVariables produces a www-form-urlencoded POST body from the given variables.
     * @param {Object.<string,string>} vars The variables to encode in the body
     * @returns {string}
     */
    static serializePostVariables(vars) {

        var post_string = "";
        var first_entry = true;

        Object.keys(vars).forEach(function(key, index) {

            post_string += (first_entry ? "" : "&" ) + key + "=" + encodeURIComponent(vars[key]);
            first_entry = false;
            
        });

        return post_string;

    }

    /**
     * generateMIMEBoundary generates a random string that can be used as a boundary in a multipart MIME post body.
     * @returns {string}
     */
    static generateMIMEBoundary() {

        var text = "---------";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 25; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;

    }
}

/**
 * SVG contains helper methods for drawing SVG objects
 */
class SVG {

    /**
     * lineFunction returns a string of SVG path commands for a polygon with holes
     * @param {Function} scaleX A function to scale X coordinates
     * @param {Function} scaleY A function to scale Y coordinates
     * @param {Array} coordinates An array of coordinates for the polygon
     * @param {Array} holes An array of arrays of coordinates for the holes of the polygon
     * @returns {string} The SVG path
     */
    static lineFunction(scaleX, scaleY, coordinates, holes) {

        var path = "";

        for(let i = 0; i < coordinates.length; i++) {

            if(i == 0) {
                path += "M " + scaleX(coordinates[i]).toString() + "," + scaleY(coordinates[i]).toString() + " ";
            } else {
                path += "L " + scaleX(coordinates[i]).toString() + "," + scaleY(coordinates[i]).toString() + " ";
            }

        }

        path += "z ";

        holes.forEach(function(hole_coords){

            for(let i = 0; i < hole_coords.length; i++) {
                if(i == 0) {
                    path += "M " + scaleX(hole_coords[i]).toString() + "," + scaleY(hole_coords[i]).toString() + " ";
                } else {
                    path += "L " + scaleX(hole_coords[i]).toString() + "," + scaleY(hole_coords[i]).toString() + " ";
                }
            }

            path += "z ";

        });

        return path;

    }

}

/**
 * Polygon contains data for one D3 polygon
 */
class Polygon {

    /**
     * constructor creates a new instance of the Polygon class
     * @param {string} id The id of the Path
     * @param {Object} path The D3 line function of the Polygon
     * @param {Array<Array<number,number>>} coordinates The raw coordinates of the Polygon, to be used to rescale the polygon for area equalization
     * @param {Array<Array<Array<number,number>>>} holes The raw holes of the Polygon, to be used to rescale the polygon for area equalization
     */
    constructor(id, path, coordinates, holes=[]) {
        /**
         * The Polygon ID
         * @type {string}
         */
        this.id = id;

        /**
         * The Polygon D3 line function
         * @type {Object}
         */
        this.path = path;

        this.coordinates = coordinates;

        this.holes = holes;
    }
}

/**
 * RegionVersion contains data for a version of a map region
 */
class RegionVersion {

    /**
     * constructor creates a new instance of the RegionVersion class
     * @param {string} name The human-readable name of the version
     * @param {string} unit The unit of the version
     * @param {number} value The value of the version
     * @param {Array<Polygon>} polygons The polygons of the version
     */
    constructor(name, unit, value, polygons) {
        this.name = name;
        this.unit = unit;
        this.value = value;
        this.polygons = polygons;
    }
}

/**
 * Region contains map data for a region of a conventional map or cartogram
 */
class Region {

    /**
     * constructor creates a new instance of the Region class
     * @param {string} name The name of the region
     * @param {string} abbreviation The abbreviation of the region
     */
    constructor(name, abbreviation) {
        this.name = name;
        this.abbreviation = abbreviation;

        /**
         * The versions of the region
         * @type {Object.<string, RegionVersion>}
         */
        this.versions = {};
    }

    /**
     * Adds a new version to the region
     * @param {string} sysname The unique system identifier of the version (not necessarily human readable or friendly)
     * @param {RegionVersion} version The new region version
     */
    addVersion(sysname, version) {
        this.versions[sysname] = version;
    }

    /**
     * Returns the region version with sysname
     * @param {string} sysname The sysname of the region version
     * @returns {RegionVersion}
     */
    getVersion(sysname) {
        return this.versions[sysname];
    }


}

/**
 * MapVersion contains map data for a version of a conventional map or cartogram
 */
class MapVersion {

    /**
     * constructor creates an instance of the MapVersion class
     * @param {string} name The human-readable name of the map version
     * @param {Extrema} extrema Extrema for this map version
     * @param {Labels} labels The labels of the map version. Optional.
     */
    constructor(name, extrema, labels=null) {
        this.name = name;
        this.extrema = extrema;
        this.labels = labels;
    }
}

/**
 * An enum of the supported map data formats.
 * @constant 
 * @type {Object<string,number>}
 * @default
 */
const MapDataFormat = {
    GOCARTJSON: 1,
    GEOJSON: 2
};

/**
 * MapVersionData contains data used to construct a map from raw JSON data
 */
class MapVersionData {

    /**
     * constructor creates an instance of the MapVersionData class from raw map data in JSON
     * @param {Array<{id: string, polygon_id: number, coordinates: Array<Array<number,number>>}>} features
     * @param {Extrema} extrema Extrema for the map version
     * @param {Object} tooltip Tooltip data for the map version
     * @param {string} tooltip.unit
     * @param {string} tooltip.label
     * @param {Object.<string,{name: string, value: number}>} tooltip.data
     * @param {Object.<string,string>} abbreviations A map of region names to abbreviations. Only needs to be specified once per map.
     * @param {Labels} labels Labels for the map version
     * @param {number} format The format of the given map data.
     */
    constructor(features, extrema, tooltip, abbreviations=null, labels=null, format=MapDataFormat.GOCARTJSON) {

        /**
         * @type {Object.<string,{polygons: Array<{id: string, coordinates: Array<Array<number,number>>}>, name: string, value: string}}
         */
        this.regions = {};

        switch(format) {
        case MapDataFormat.GOCARTJSON:
            features.forEach(function(feature){

                if(this.regions.hasOwnProperty(feature.id)) {

                    this.regions[feature.id].polygons.push({
                        id: feature.properties.polygon_id.toString(),
                        coordinates: feature.coordinates,
                        holes: feature.hasOwnProperty("holes") ? feature.holes : []
                    })

                } else {

                    this.regions[feature.id] = {
                        polygons: [
                            {
                                id: feature.properties.polygon_id.toString(),
                                coordinates: feature.coordinates,
                                holes: feature.hasOwnProperty("holes") ? feature.holes : []
                            }
                        ],
                        name: tooltip.data["id_" + feature.id]["name"],
                        value: tooltip.data["id_" + feature.id]["value"],
                        abbreviation: abbreviations !== null ? abbreviations[tooltip.data["id_" + feature.id]["name"]] : ""
                    }

                }

            }, this);

            break;
        case MapDataFormat.GEOJSON:

            var next_polygon_id = 1;

            features.forEach(function(feature){

                switch(feature.geometry.type) {
                case "Polygon":
                    
                    var polygon_coords;
                    var polygon_holes = [];

                    var polygon_id = next_polygon_id.toString();

                    for(let i = 0; i < feature.geometry.coordinates.length; i++) {

                        /* The first array of coordinates is the outer ring. The rest are holes */
                        if(i == 0) {
                            polygon_coords = feature.geometry.coordinates[0];
                            next_polygon_id++;
                            continue;
                        }

                        polygon_holes.push(feature.geometry.coordinates[i]);

                        /* We increase the polygon ID for holes for compatibility reasons. This is what the gen2json
                           Python script does.
                        */
                        next_polygon_id++;
                    }

                    this.regions[feature.properties.cartogram_id] = {
                        polygons: [
                            {
                                id: polygon_id,
                                coordinates: polygon_coords,
                                holes: polygon_holes
                            }
                        ],
                        name: tooltip.data["id_" + feature.properties.cartogram_id]["name"],
                        value: tooltip.data["id_" + feature.properties.cartogram_id]["value"],
                        abbreviation: abbreviations !== null ? abbreviations[tooltip.data["id_" + feature.properties.cartogram_id]["name"]] : ""
                    }

                    break;
                case "MultiPolygon":
                    
                    var polygons = [];

                    feature.geometry.coordinates.forEach(function(polygon){

                        var polygon_coords;
                        var polygon_holes = [];
                        var polygon_id = next_polygon_id.toString();

                        for(let i = 0; i < polygon.length; i++) {

                            /* The first array of coordinates is the outer ring. The rest are holes */
                            if(i == 0) {
                                polygon_coords = polygon[0];
                                next_polygon_id++;
                                continue;
                            }

                            polygon_holes.push(polygon[i]);

                            /* We increase the polygon ID for holes for compatibility reasons. This is what the gen2json
                            Python script does.
                            */
                            next_polygon_id++;
                        }

                        polygons.push({
                            id: polygon_id,
                            coordinates: polygon_coords,
                            holes: polygon_holes
                        });

                    }, this);

                    this.regions[feature.properties.cartogram_id] = {
                        polygons: polygons,
                        name: tooltip.data["id_" + feature.properties.cartogram_id]["name"],
                        value: tooltip.data["id_" + feature.properties.cartogram_id]["value"],
                        abbreviation: abbreviations !== null ? abbreviations[tooltip.data["id_" + feature.properties.cartogram_id]["name"]] : ""
                    }
                    
                    break;
                default:
                    throw ("Feature type '" + feature.geometry.type + "' not supported");

                }

            }, this);
            break;
        default:
            throw "Unsupported map format";
        }        

        /**
         * @type {Extrema}
         */
        this.extrema = extrema;

        /**
         * @type {string}
         */
        this.name = tooltip.label;

        /**
         * @type {string}
         */
        this.unit = tooltip.unit;

        /**
         * @type {Labels}
         */
        this.labels = labels;
        
    }

}

/**
 * CartMap contains map data for a conventional map or cartogram. One map can contain several versions. In a map version,
 * the map geography is used to represent a different dataset (e.g. land area in a conventional map version, or GDP or
 * population in a cartogram map version).
 */
class CartMap {

    /**
     * constructor creates a new instance of the Map class
     * @param {string} name The name of the map or cartogram
     * @param {MapConfig} config The configuration of the map or cartogram
     */
    constructor(name, config) {

        this.name = name;

        /**
         * The map configuration information.
         * @type {MapConfig}
         */
        this.config = {
            dont_draw: config.dont_draw.map(id => id.toString()),
            elevate: config.elevate.map(id => id.toString()),
            scale: 1.3
        }

        /**
         * The map colors. The keys are region IDs.
         * @type {Object.<string,string>}
         */
        this.colors = {};

        /**
         * The map versions. The keys are version sysnames.
         * @type {Object.<string,MapVersion>}
         */
        this.versions = {};

        /**
         * The map regions. The keys are region IDs.
         * @type {Object.<string,Region>}
         */
        this.regions = {};

        /**
         * The width of the map.
         * @type {number}
         */
        this.width = 0.0;

        /**
         * The height of the map.
         * @type {number}
         */
        this.height = 0.0;
        
    }

    /**
     * getConvenLegendUnit returns the a legend unit of the conventional map
     * @param {string} sysname The sysname of the map version
     * @returns {string} The legend unit of the map
     */
    getLegendUnit(sysname){
        var unit = "";
        Object.keys(this.regions).forEach(function(region_id){
            unit = this.regions[region_id].getVersion(sysname).unit;
        }, this);
        return unit;
    }


    /**
     * The following returns the scaling factors (x and y) of map of specified version.
     * @param {string} sysname The sysname of the map version
     * @returns {number[]} The total polygon area of the specified map version
     */
    getVersionPolygonScale(sysname) {

        const version_width = this.versions[sysname].extrema.max_x - this.versions[sysname].extrema.min_x;
        const version_height = this.versions[sysname].extrema.max_y - this.versions[sysname].extrema.min_y;

        const scale_x = this.width / version_width;
        const scale_y = this.height / version_height;

        return [scale_x, scale_y];
    }

    /**
     * getTotalAreasAndValuesForVersion returns the sum of all region values and area for the specified map version.
     * @param {string} sysname The sysname of the map version
     * @returns {number[]} The total value and area of the specified map version
     */
    getTotalAreasAndValuesForVersion(sysname) {

        var area = 0;
        var sum = 0;
        const na_regions = [];
        Object.keys(this.regions).forEach(function(region_id){
            var areaValue = 0;
            this.regions[region_id].getVersion(sysname).polygons.forEach(function(polygon){
                const coordinates = polygon.coordinates;

                areaValue += d3.polygonArea(coordinates);

                polygon.holes.forEach(function(hole){

                    areaValue -= d3.polygonArea(hole);

                }, this);

            }, this);



            const regionValue = this.regions[region_id].getVersion(sysname).value;

            if(regionValue !== 'NA') {
                sum += regionValue;
            } else {

                na_regions.push({id: region_id, area: areaValue});
            }

            area += areaValue;
        }, this);

        const avg_density = sum/area;

        na_regions.forEach(function(na_region){


            sum += avg_density * na_region.area;

        }, this);

        return [area, sum];
    }

    /**
     * getTotalValuesForVersion returns the sum of all region values for the specified map version.
     * @param {string} sysname The sysname of the map version
     * @returns {number} The total value of the specified map version
     */
    getTotalValuesForVersion(sysname) {
        
        var sum = 0;        
        Object.keys(this.regions).forEach(function(region_id){
            const regionValue = this.regions[region_id].getVersion(sysname).value;
           
            if(regionValue != 'NA') {
                sum += regionValue;
            }
        }, this);

        return sum;
    }

    /**
     * The following returns the sum of all region polygon area values for the specified map version.
     * @param {string} sysname The sysname of the map version
     * @returns {number} The total value of the specified map version
     */
    getTotalAreaForVersion(sysname) {
        var area = 0;        
        Object.keys(this.regions).forEach(function(region_id){
            this.regions[region_id].getVersion(sysname).polygons.forEach(function(polygon){
                const coordinates = polygon.coordinates;
                
                const areaValue = d3.polygonArea(coordinates);

                area += areaValue;

            })
        }, this);
        return area;
    }

    /**
     * Determines if the computed legend area and value is correct
     * @param sysname
     * @param width
     * @param value
     */
    verifyLegend(sysname, width, value) {

        const [scale_x, scale_y] = this.getVersionPolygonScale(sysname);
        const [version_area, version_values] = this.getTotalAreasAndValuesForVersion(sysname);
        const tolerance = 0.001;

        const legendTotalValue = (version_area * scale_x * scale_y / (width * width)) * value;

        if(!(Math.abs(version_values - legendTotalValue) < tolerance)) {
            console.warn(`The legend value (${value}) and width (${width}px) for ${sysname} is not correct. Calculating the total value from the legend yields ${legendTotalValue}, but it should be ${version_values}`);
        } else {
            console.log(`The legend value (${value}) and width (${width}px) for ${sysname} is correct (calculated total value=${legendTotalValue}, actual total value=${version_values})`);
        }

    }

    /**
     * The following draws the legend for each map
     * @param {string} sysname The sysname of the map version
     */

    drawLegend(sysname, legend_square_id, legend_text_id, legend_superscript_id, legend_superscript_unit_id){
        
        var legend_square = document.getElementById(legend_square_id);
        var legend_text = document.getElementById(legend_text_id);
        var legend_superscript = document.getElementById(legend_superscript_id);
        var legend_superscript_unit_id = document.getElementById(legend_superscript_unit_id);

        // Get unit for the map that we wish to draw legend for.
        const unit = this.getLegendUnit(sysname);

        // Obtain the scaling factors for this map.
        const [scale_x, scale_y]= this.getVersionPolygonScale(sysname);
        const [version_area, version_values] = this.getTotalAreasAndValuesForVersion(sysname);
        const legend = version_values/(version_area*scale_x*scale_y);

        // square default is 30 by 30 px
        var ratio = legend*900 >= 1 ? legend*900: 1;

        
        // If the legend ratio is smaller than 1, set to 1 in case the legend square becomes too big.
        if(ratio == 1){
            var exp_num = (legend*900).toExponential().split("e");
            var first_num = exp_num[0];
            if(Math.abs(first_num - 10) < Math.abs(first_num - 5) && Math.abs(first_num - 10) < Math.abs(first_num - 2)){
                first_num = 10;
            } else if (Math.abs(first_num - 5) < Math.abs(first_num - 2)){
                first_num = 5;
            } else {
                first_num = 2;
            }
            legend_text.innerHTML = "= " + first_num * Math.pow(10, parseInt(exp_num[1])) + unit;
            const width = Math.sqrt(first_num * Math.pow(10, parseInt(exp_num[1]))*900/(legend*900).toExponential());
  
            if(exp_num[1] >= -4){
                legend_square.setAttribute("width", width.toString() +"px");
                legend_square.setAttribute("height", width.toString() +"px");
                console.log(`original: ${exp_num}; new : ${width}`);
                
            } else{
                legend_square.setAttribute("width", width +"px");
                legend_square.setAttribute("height", width +"px");
                legend_superscript.style.display = "inline-block";
                legend_superscript_unit_id.style.display = "inline-block";
                legend_superscript.innerHTML = exp_num[1];
                legend_text.innerHTML = "= " + first_num + " x 10 "
                legend_superscript_unit_id.innerHTML = unit;
            }
            this.verifyLegend(sysname, width, first_num * Math.pow(10, parseInt(exp_num[1])));

        }
        else{
            legend_superscript_unit_id.style.display = "none";
            legend_superscript.style.display = "none";
            var round_ratio = Math.pow(10, (Math.round(ratio).toString().length-1));            
            if(round_ratio.length === 2){
                round_ratio = 100
            } else if(round_ratio === 1){
                round_ratio = 10
            }

            const r = ratio/round_ratio;
            var final_ratio = 0;
            if(Math.abs(r - 1) < Math.abs(r - 5) && Math.abs(r - 1) < Math.abs(r - 2)){
                final_ratio = 1;
            } else if (Math.abs(r - 5) < Math.abs(r - 2)){
                final_ratio = 5;
            } else {
                final_ratio = 2;
            }

            const width = Math.sqrt(final_ratio*round_ratio*900/ratio);
            var scale_word = (round_ratio > 999999) ? " million" : round_ratio.toString().substr(1);
            if(scale_word == " million" && round_ratio >= 10000000){
                if(round_ratio >= 10000000000000){
                    scale_word = round_ratio / 10000000000000 + " billion"
                }
                scale_word = round_ratio/10000000 + " million"
            } else if(scale_word !== " million" && scale_word.length >= 3){
                const set_of_zeros = Math.floor(scale_word.length/3)
                const remaining_zeros = scale_word.length%3
                if(set_of_zeros === 1 && remaining_zeros === 0){
                    scale_word = "000".repeat(set_of_zeros);
                } else{
                    scale_word = "0".repeat(remaining_zeros) + " 000".repeat(set_of_zeros);
                }
            }

            this.verifyLegend(sysname, width, final_ratio*round_ratio);

            legend_square.setAttribute("width", width.toString() +"px");
            legend_square.setAttribute("height", width.toString() +"px");
            legend_text.setAttribute("x", (width+10).toString() + "px");

            if(scale_word.length === 1){
                legend_text.innerHTML = "= " + final_ratio + scale_word + " " + unit
            } else {
                legend_text.innerHTML = "= " + final_ratio + scale_word + " " + unit
            }
        }
    }


    /**
     * addVersion adds a new version to the map. If a version with the specified sysname already exists, it will be overwritten.
     * @param {string} sysname A unique system identifier for the version
     * @param {MapVersionData} data Data for the new map version.
     */
    addVersion(sysname, data) {

        if(this.versions.hasOwnProperty(sysname)) {
            delete this.versions[sysname];
        }

        // Here we perform the area equalization.
        // We take the largest map version, and scale all others to have the same dimensions.

        /**
         * @type {Object.<string, {x: number, y: number}>}
         */
        var scale_factors = {};

        var max_height = 0.0;
        var max_width = 0.0;

        Object.keys(this.versions).forEach(function(version_sysname){

            var width = this.versions[version_sysname].extrema.max_x - this.versions[version_sysname].extrema.min_x;
            var height = this.versions[version_sysname].extrema.max_y - this.versions[version_sysname].extrema.min_y;

            if(width > max_width) {
                max_width = width;
            }

            if(height > max_height) {
                max_height = height;
            }

        }, this);

        var new_version_width = data.extrema.max_x - data.extrema.min_x;
        var new_version_height = data.extrema.max_y - data.extrema.min_y;

        if(new_version_width > max_width) {
            max_width = new_version_width;
        }

        if(new_version_height > max_height) {
            max_height = new_version_height;
        }

        if(max_width > 400.0) {
            var max_width_old = max_width;
            max_width = 400.0;
            max_height = (max_width / max_width_old) * max_height;
        }

        if(max_height > 500.0) {
            var max_height_old = max_height;
            max_height = 500.0;
            max_width = (max_height / max_height_old) * max_width;
        }

        this.width = max_width * this.config.scale;
        this.height = max_height * this.config.scale;

        Object.keys(this.versions).forEach(function(version_sysname){

            var width = this.versions[version_sysname].extrema.max_x - this.versions[version_sysname].extrema.min_x;
            var height = this.versions[version_sysname].extrema.max_y - this.versions[version_sysname].extrema.min_y;

            scale_factors[version_sysname] = {x: max_width / width * this.config.scale, y: max_height / height * this.config.scale};

        }, this);

        scale_factors[sysname] = {x: max_width / new_version_width * this.config.scale, y: max_height / new_version_height * this.config.scale};

        Object.keys(data.regions).forEach(function(region_id){

            var region = data.regions[region_id];

            var polygons = region.polygons.map(polygon =>
                new Polygon(
                    polygon.id,
                    /*d3.svg.line()
                        .x(d => scale_factors[sysname].x * (-1*(data.extrema.min_x) + d[0]))
                        .y(d => scale_factors[sysname].y * ((data.extrema.max_y) - d[1]))
                        .interpolate("linear")(polygon.coordinates),*/
                    SVG.lineFunction(
                        d => scale_factors[sysname].x * (-1*(data.extrema.min_x) + d[0]),
                        d => scale_factors[sysname].y * ((data.extrema.max_y) - d[1]),
                        polygon.coordinates,
                        polygon.holes
                    ),
                    polygon.coordinates,
                    polygon.holes

                )
            );

            // Create the region if it doesn't exist.
            // This should only happen when adding the first map version.
            if(!this.regions.hasOwnProperty(region_id)) {

                this.regions[region_id] = new Region(region.name, region.abbreviation);

            }

            this.regions[region_id].addVersion(
                sysname,
                new RegionVersion(
                    data.name,
                    data.unit,
                    region.value,
                    polygons
                )
            );


        }, this);

        // Now we need to recompute the D3 line functions of all other map versions to ensure area equalization.
        Object.keys(this.versions).forEach(function(version_sysname){

            Object.keys(this.regions).forEach(function(region_id){

                var polygons = this.regions[region_id].versions[version_sysname].polygons.map(polygon =>
                    new Polygon(
                        polygon.id,
                        /*d3.svg.line()
                            .x(d => scale_factors[version_sysname].x * (-1*(this.versions[version_sysname].extrema.min_x) + d[0]))
                            .y(d => scale_factors[version_sysname].y * ((this.versions[version_sysname].extrema.max_y) - d[1]))
                            .interpolate("linear")(polygon.coordinates),*/
                        SVG.lineFunction(
                            d => scale_factors[version_sysname].x * (-1*(this.versions[version_sysname].extrema.min_x) + d[0]),
                            d => scale_factors[version_sysname].y * ((this.versions[version_sysname].extrema.max_y) - d[1]),
                            polygon.coordinates,
                            polygon.holes
                        ),
                        polygon.coordinates,
                        polygon.holes
                    )
                )

                this.regions[region_id].versions[version_sysname].polygons = polygons;

            }, this);

        },this);

        this.versions[sysname] = new MapVersion(
            data.name,
            data.extrema,
            data.labels,
        );
    }

    /**
     * highlightByID highlights or unhighlights a region depending on the given opacity value.
     * @param {string} region_id The ID of the region to highlight
     * @param {string} color The original color of the region
     * @param {boolean} highlight Whether to highlight or unhighlight the region
     */
    static highlightByID(where_drawn, region_id, color, highlight) {

        where_drawn.forEach(function(element_id){

            var polygons = document.getElementsByClassName("path-" + element_id + "-" + region_id);

            for(let i = 0; i < polygons.length; i++) {
                if(highlight) {
                    polygons[i].setAttribute('fill', tinycolor(color).brighten(20));
                } else {
                    polygons[i].setAttribute('fill', color);
                }
                
            }

        });

    }

    /**
     * drawTooltip draws the tooltip for the currently highlighted region.
     * @param {MouseEvent} event Mouse event. Used to place the tooltip next to the cursor
     * @param {string} region_id The ID of the region currently highlighted
     */
    drawTooltip(event, region_id) {

        document.getElementById('tooltip').innerHTML = "<b>" + this.regions[region_id].name + " (" + this.regions[region_id].abbreviation + ")</b>";

        Object.keys(this.regions[region_id].versions).forEach(function(sysname){

            document.getElementById('tooltip').innerHTML += "<br/><i>" + this.regions[region_id].versions[sysname].name + ":</i> " + this.regions[region_id].versions[sysname].value.toLocaleString() + " " + this.regions[region_id].versions[sysname].unit;

        }, this);

        document.getElementById('tooltip').style.display = 'inline-block';
               
        document.getElementById('tooltip').style.left = (event.pageX - 50) + 'px';    

        document.getElementById('tooltip').style.top = (event.pageY + 15) + 'px';

    }

    static hideTooltip() {
        document.getElementById('tooltip').style.display = 'none';
    }

    /**
     * drawVersion draws a map version in the element with the given ID. You must add colors to the map before attempting to draw a version.
     * Note that version switching is not supported if you draw a version of a map with labels as the initial version.
     * @param {string} sysname The sysname of the map version
     * @param {string} element_id The element of the ID to place the map
     * @param {Array<string>} where_drawn The elements of the IDs where versions of this map are and will be drawn (including the current element_id). Used for parallel highlighting
     */
    drawVersion(sysname, element_id, where_drawn) {

        var map_container = document.getElementById(element_id);
        var version = this.versions[sysname];

        // Empty the map container element
        while(map_container.firstChild) {
            map_container.removeChild(map_container.firstChild);
        }

        var canvas = d3.select('#' + element_id).append("svg")
            .attr("width", this.width)
            .attr("height", this.height);
        
        var polygons_to_draw = [];

        // First we collect the information for each polygon to make using D3 easier.
        Object.keys(this.regions).forEach(function(region_id){

            this.regions[region_id].getVersion(sysname).polygons.forEach(function(polygon){

                if(!this.config.dont_draw.includes(polygon.id)) {

                    polygons_to_draw.push({
                        region_id: region_id,
                        polygon_id: polygon.id,
                        path: polygon.path,
                        color: this.colors[region_id],
                        elevated: this.config.elevate.includes(polygon.id),
                        value: this.regions[region_id].getVersion(sysname).value
                    });
                }

                

            }, this);

        }, this);

        /* To elevate polygons, we draw the elevated ones last */
        polygons_to_draw.sort(function(p1, p2){

            if(p1.elevated && !p2.elevated) {
                return 1;
            }

            if(p1.elevated && p2.elevated) {
                return 0;
            }

            if(!p1.elevated && p2.elevated) {
                return -1;
            }

            if(!p1.elevated && !p2.elevated) {
                return 0;
            }

        });

        var group = canvas.selectAll()
              .data(polygons_to_draw)
              .enter()
              .append("path");
            
        var areas = group.attr("d", d => d.path
        ).attr("id", d => "path-" + element_id + "-" + d.polygon_id)
          /* Giving NA regions a different class prevents them from being highlighted, preserving
             their white fill color.
          */
          .attr("class", d => "area" + " path-" + element_id + "-" + d.region_id + (d.value === "NA" ? "-na" : ""))
          /* NA regions are filled with white */
          .attr("fill", d => d.value === "NA" ? "#CCCCCC" : d.color)
          .attr("stroke", "#000")
          .attr("stroke-width", "0.5")
          .on('mouseenter', (function(map, where_drawn){
                return function(d, i){

                        CartMap.highlightByID(where_drawn, d.region_id, d.color, true);

                        map.drawTooltip(d3.event, d.region_id);

                    };
          }(this, where_drawn)))
          .on('mousemove', (function(map){
                return function(d, i){

                    map.drawTooltip(d3.event, d.region_id);
            };}(this)))
          .on('mouseleave', (function(map, where_drawn){
                return function(d, i){

                    CartMap.highlightByID(where_drawn, d.region_id, d.color, false);

                    CartMap.hideTooltip();
            };}(this, where_drawn)));
        
        if(version.labels !== null) {

            /* First draw the text */

            var labels = version.labels;

            /*
            I created labels using Inkscape with the maps that were scaled for the purposes of area equalization.
            Scaling the labels like this ensures that they are displayed properly.
            */
            var scale_x = this.width / ((version.extrema.max_x - version.extrema.min_x) * labels.scale_x);
            var scale_y = this.height / ((version.extrema.max_y - version.extrema.min_y) * labels.scale_y);

            var text = canvas.selectAll("text")
                        .data(labels.labels)
                        .enter()
                        .append("text");

            var textLabels = text.attr('x', d => d.x * scale_x)
                        .attr('y', d => d.y * scale_y)
                        .attr('font-family', 'sans-serif')
                        .attr('font-size', '7.5px')
                        .attr('fill', '#000')
                        .text(d => d.text)

            var lines = canvas.selectAll("line")
                        .data(labels.lines)
                        .enter()
                        .append("line");

            var labelLines = lines.attr('x1', d => d.x1 * scale_x)
                        .attr('x2', d => d.x2 * scale_x)
                        .attr('y1', d => d.y1 * scale_y)
                        .attr('y2', d => d.y2 * scale_y)
                        .attr('stroke-width', 1)
                        .attr('stroke', '#000');

        }

    }




    /**
     * switchVersion switches the map version displayed in the element with the given ID with an animation.
     * @param {string} current_sysname The sysname of the currently displayed version
     * @param {string} new_sysname The sysname of the version to be displayed
     * @param {string} element_id The ID of the element containing the map
     */
    switchVersion(current_sysname, new_sysname, element_id) {

        Object.keys(this.regions).forEach(function(region_id){

            var region = this.regions[region_id];

            this.regions[region_id].versions[current_sysname].polygons.forEach(function(polygon){

                d3.select('#path-' + element_id + '-' + polygon.id)
                    .attr('d', polygon.path)
                    .transition()
                    .ease(d3.easeCubic)
                    .duration(1000)
                    .attr('d', this.regions[region_id].versions[new_sysname].polygons.find(poly => poly.id == polygon.id).path
                    );
                
                /* Change the color and ensure correct highlighting behavior after animation
                   is complete
                */
                window.setTimeout(function(){
                    if(this.regions[region_id].versions[new_sysname].value === "NA") {
                        document.getElementById('path-' + element_id + '-' + polygon.id).setAttribute('fill', '#CCCCCC');

                        document.getElementById('path-' + element_id + '-' + polygon.id).classList.remove('path-' + element_id + '-' + region_id);
                        document.getElementById('path-' + element_id + '-' + polygon.id).classList.add('path-' + element_id + '-' + region_id + '-na');

                    } else {
                        document.getElementById('path-' + element_id + '-' + polygon.id).setAttribute('fill', this.colors[region_id]);
                        document.getElementById('path-' + element_id + '-' + polygon.id).classList.add('path-' + element_id + '-' + region_id);
                        document.getElementById('path-' + element_id + '-' + polygon.id).classList.remove('path-' + element_id + '-' + region_id + '-na');
                    }
                }.bind(this), 800);
                

            }, this);
            

        }, this);        

        this.drawLegend(new_sysname, "legend-square-" + element_id, "legend-text-" + element_id, "legend-superscript-" + element_id, "legend-superscript-unit-" + element_id);
    }
}

/**
 * Cartogram contains the main frontend logic for the go-cart web application.
 */
class Cartogram {

    /**
     * constructor creates an instance of the Cartogram class
     * @param {string} c_u The URL of the cartogram generator
     * @param {string} cui_u The cartogramui URL 
     * @param {string} c_d  The URL of the cartogram data directory
     * @param {string} g_u The URL of the gridedit page
     * @param {srinng} gp_u The URL to retrieve progress information
     * @param {string} version The version string used to prevent improper caching of map assets
     */

    constructor(c_u, cui_u, c_d, g_u, gp_u, version) {

        this.config = {
            cartogram_url: c_u,
            cartogramui_url: cui_u,
            cartogram_data_dir: c_d,
            gridedit_url: g_u,
            getprogress_url: gp_u,
            version: version
        };

        /**
         * The cartogram model
         * @property {CartMap|null} map The current map
         * @property {string} current_sysname The sysname of the map version selected for viewing on the right
         * @property {string} map_sysname The sysname of the currently selected map
         * @property {boolean} in_loading_state Whether or not we're in a loading state
         * @property {Object|null} loading_state The current loading state
         * @property {Object|null} grid_document The current grid document
         * @property {Window|null} gridedit_window The {@link Window} of the gridedit interface
         */
        this.model = {
            map: null,
            current_sysname: '',
            map_sysname: '',
            in_loading_state: false,
            loading_state: null,
            grid_document: null,
            gridedit_window: null,
        };

        /**
         * Contains extended information about a fatal error. Used to produce a meaningful error report when cartogram
         * generation fails
         * @type {string|null}
         */
        this.extended_error_info = null;

        // Close the gridedit window upon navigating away from the page if it's open
        window.onbeforeunload = function() {
            if(this.model.gridedit_window !== null && !this.model.gridedit_window.closed)
            {
                this.model.gridedit_window.close();
            }
        }.bind(this);

    }
    
    /**
     * setExtendedErrorInfo sets the extended error information. You must call this function before doFatalError to
     * display this information.
     * @param {string} info The extended error information, in plaintext 
     */
    setExtendedErrorInfo(info) {

        this.extended_error_info = info;

    }

    /**
     * appendToExtendedErrorInfo appends new text to the existing extended error information.
     * @param {string} info The additional extended error information, in plaintext
     */
    appendToExtendedErrorInfo(info) {

        this.extended_error_info += info;
        
    }

    /**
     * clearExtendedErrorInfo clears the existing extended error information.
     */
    clearExtendedErrorInfo() {

        this.extended_error_info = null;

    }

    /**
     * launchGridEdit opens the gridedit window if possible.
     */
    launchGridEdit() {

        if(this.model.grid_document === null || this.model.in_loading_state)
            return;
        
        if(this.model.gridedit_window === null || this.model.gridedit_window.closed)
        {
            this.model.gridedit_window = window.open(this.config.gridedit_url, "gridedit_" + new Date().getTime(), 'width=550,height=650,resizable,scrollbars');

            this.model.gridedit_window.addEventListener("load", (function(gd){

                return function(e) {
                    this.model.gridedit_window.gridedit_init();

                    this.model.gridedit_window.gridedit.on_update = function(gd) {

                        this.onGridEditUpdate(gd);

                    }.bind(this);

                    /*
                    This sets whether or not the Update button is clickable in the gridedit document
                    */
                    this.model.gridedit_window.gridedit.set_allow_update(!this.model.in_loading_state);

                    this.model.gridedit_window.gridedit.load_document(gd);
                }.bind(this);

            }.bind(this)(this.model.grid_document)));
        }
        else
        {
            this.gridedit_window.gridedit.load_document(this.grid_document);
            this.gridedit_window.focus();
        }

    }

    /**
     * onGridEditUpdate generates and displays a cartogram using the dataset in the current grid document when the
     * update button is clicked in the gridedit interface.
     * @param {Object} gd The updated grid document
     */
    onGridEditUpdate(gd) {

        if(this.model.in_loading_state)
            return;
        
        /*
        The user may make changes to the grid document while the cartogram loads. As a result, we don't want to update
        the grid document with the one returned by CartogramUI.
        */
        this.requestAndDrawCartogram(gd, null, false);

    }

    /**
     * editButtonDisabled returns whether the edit button to launch the gridedit window should be disabled.
     * @returns {boolean}
     */
    editButtonDisabled() {
        return this.grid_document === null;
    }

    /**
     * updateGridDocument updates the current grid document.
     * @param {Object} new_gd The new grid document
     */
    updateGridDocument(new_gd) {

        this.model.grid_document = new_gd;

        if(this.model.grid_document !== null)
        {
            if(!this.model.in_loading_state)
                document.getElementById('edit-button').disabled = false;

            /*
            If the gridedit window is open, push the new grid document to it
            */
            if(this.model.gridedit_window !== null && !this.model.gridedit_window.closed)
                this.model.gridedit_window.gridedit.load_document(this.model.grid_document);
        }
        else
        {
            document.getElementById('edit-button').disabled = true;
        }

    }

    /**
     * gridDocumentToCSV takes a grid document and converts it to CSV format with Excel-style quote escaping.
     * @param {Object} gd The grid document to convert
     */
    gridDocumentToCSV(gd) {

        var csv = "";

        for(let row = 0; row < gd.height; row++)
        {
            for(let col = 0; col < gd.width; col++)
            {
                /*
                We use Excel-style quote escaping. All values are placed within double quotes, and a double quote
                literal is represented by "".
                */
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

    }

    /**
     * @typedef {Object} RequestBody An HTTP POST multipart request body
     * @property {string} mime_boundary The MIME boundary for the request, which must be sent as a header
     * @property {string} req_body The request body text
     */

    /**
     * generateCartogramUIRequestBodyFromGridDocument generates a POST request body for CartogramUI from a grid
     * document. To do this, we convert the grid document to CSV format and pretend we're uploading it as a file. This
     * simplifies the backend code.
     * @param {string} sysname The sysname of the map.
     * @param {Object} gd The grid document
     * @returns {RequestBody}
     */
    generateCartogramUIRequestBodyFromGridDocument(sysname, gd) {

        var mime_boundary = HTTP.generateMIMEBoundary();
        var csv = this.gridDocumentToCSV(gd);

        // The MIME boundary can't be contained in the request body text
        while(true)
        {
            var search_string = csv + "csv" + "handler" + handler;
            if(search_string.search(mime_boundary) === -1)
                break;
            
            mime_boundary = HTTP.generateMIMEBoundary();
        }

        var req_body = "";

        req_body += "--" + mime_boundary + "\n";
        req_body += 'Content-Disposition: form-data; name="handler"\n\n'
        req_body += sysname + "\n";

        req_body += "--" + mime_boundary + "\n";
        req_body += 'Content-Disposition: form-data; name="csv"; filename="data.csv"\n';
        req_body += 'Content-Type: text/csv\n\n';
        req_body += csv + "\n";
        req_body += "--" + mime_boundary + "--";

        return {
            mime_boundary: mime_boundary,
            req_body: req_body
        };

    }

    /**
     * drawChartFromTooltip draws a barchart of the uploaded dataset, which can be found in the tooltip of the
     * CartogramUI response. We use this when CartogramUI returns a success response, but cartogram generation fails.
     * @param {string} container The ID of the element to draw the barchart in
     * @param {Object} tooltip The tooltip to retrieve the data from
     */
    drawBarChartFromTooltip(container, tooltip) {

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

    }

    /**
     * doNonFatalError informs the user of a non-critical error.
     * @param {Error} err 
     */
    doNonFatalError(err) {

        document.getElementById('non-fatal-error').innerHTML = err.message;

    }

    /**
     * clearNonFatalError clears the non-fatal error message currently being displayed.
     */
    clearNonFatalError() {

        document.getElementById('non-fatal-error').innerHTML = "";
        
    }
    
    /**
     * doFatalError locks the user interface and informs the user that there has been an unrecoverable error.
     * @param {Error} err 
     */
    doFatalError(err) {

        document.getElementById('error-message').innerHTML = err.message;

        document.getElementById('loading').style.display = 'none';
        document.getElementById('cartogram').style.display = 'none';

        document.getElementById('error').style.display = 'block';

        if(this.extended_error_info !== null)
        {
            document.getElementById('error-extended-content').innerHTML = this.extended_error_info;
            document.getElementById('error-extended').style.display = 'block';
        }

    }

    /**
     * enterLoadingState locks the user interface and informs the user that a blocking operation is taking place.
     * The progress bar is hidden by default. To show it, you must call {@link Cartogram.showProgressBar} after 
     * entering the loading state.
     */
    enterLoadingState() {

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

        // console.log(loading_height);

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
        if(this.model.gridedit_window !== null && !this.model.gridedit_window.closed && typeof(this.model.gridedit_window.gridedit) === "object")
        {
            this.model.gridedit_window.gridedit.set_allow_update(false);
        }

        document.getElementById('loading-progress-container').style.display = 'none';

        this.model.in_loading_state = true;
        this.model.loading_state = null;

    }

    /**
     * showProgressBar resets the progress bar and shows it to the user when in the loading state.
     */
    showProgressBar() {

        document.getElementById('loading-progress-container').style.display = 'block';
        document.getElementById('loading-progress').style.width = "0%";

    }

    /**
     * updateProgressBar updates the value of the progress bar.
     * @param {number} min The minimum percentage value
     * @param {number} max The maximum percentage value
     * @param {number} value The current percentage value (e.g. 50)
     */
    updateProgressBar(min, max, value) {

        if(value < max)
            value = Math.max(min, value);
        else
            value = Math.min(max, value);

        document.getElementById('loading-progress').style.width = value + "%";
        
    }

    /**
     * exitLoadingState exits the loading state. Note that while {@link Cartogram.enterLoadingState} hides the cartogram
     * element, exitLoadingState does not unhide it. You must do this yourself.
     */
    exitLoadingState() {

        document.getElementById('loading').style.display = 'none';
        document.getElementById('upload-button').disabled = false;
        document.getElementById('edit-button').disabled = this.editButtonDisabled();
        document.getElementById('handler').disabled = false;

        /* If GridEdit is open, enable updating */
        if(this.model.gridedit_window !== null && !this.model.gridedit_window.closed && typeof(this.model.gridedit_window.gridedit) === "object")
        {
            this.model.gridedit_window.gridedit.set_allow_update(true);
        }

        this.model.in_loading_state = false;
        
    }

    /**
     * generateSVGDownloadLinks generates download links for the map(s) and/or cartogram(s) displayed on the left and
     * right. We do this by taking advantage of the fact that D3 generates SVG markup. We convert the SVG markup into a
     * blob URL.
     */
    generateSVGDownloadLinks() {

        var svg_header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>';

        document.getElementById('map-download').onclick = (function(){

            return function(e) {

                e.preventDefault();

                document.getElementById('download-modal-link').href = "data:image/svg+xml;base64," + window.btoa(svg_header + document.getElementById('map-area').innerHTML);
                document.getElementById('download-modal-link').download = "equal-area-map.svg";

                $('#download-modal').modal();

            };

        }());

        document.getElementById('cartogram-download').onclick = (function(){

            return function(e) {

                e.preventDefault();

                document.getElementById('download-modal-link').href = "data:image/svg+xml;base64," + window.btoa(svg_header + document.getElementById('cartogram-area').innerHTML);
                document.getElementById('download-modal-link').download = "cartogram.svg";

                $('#download-modal').modal();

            };

        }());

        /*document.getElementById('map-download').href = "data:image/svg+xml;base64," + window.btoa(svg_header + document.getElementById('map-area').innerHTML);
        document.getElementById('map-download').download = "map.svg";*/

        /*document.getElementById('cartogram-download').href = "data:image/svg+xml;base64," + window.btoa(svg_header + document.getElementById('cartogram-area').innerHTML);
        document.getElementById('cartogram-download').download = "cartogram.svg";*/
        
    }

    /**
     * generateSocialMediaLinks generates social media sharing links for the given URL
     * @param {string} url The URL to generate social media sharing links for
     */
    generateSocialMediaLinks(url) {

        document.getElementById('facebook-share').href = "https://www.facebook.com/sharer/sharer.php?u=" + window.encodeURIComponent(url);

        document.getElementById('linkedin-share').href = "https://www.linkedin.com/shareArticle?url=" + window.encodeURIComponent(url) + "&mini=true&title=Cartogram&summary=Create%20cartograms%20with%20go-cart.io&source=go-cart.io";

        document.getElementById('twitter-share').href = "https://twitter.com/share?url=" + window.encodeURIComponent(url);

        document.getElementById('email-share').href = "mailto:?body=" + window.encodeURIComponent(url);

    }

    /**
     * getGeneratedCartogram generates a cartogram with the given dataset, and updates the progress bar with progress
     * information from the backend.
     * @param {string} sysname The sysname of the map
     * @param {string} areas_string The areas string of the dataset
     * @param {string} unique_sharing_key The unique sharing key returned by CartogramUI
     */
    getGeneratedCartogram(sysname, areas_string, unique_sharing_key) {

        return new Promise(function(resolve, reject){

            var req_body = HTTP.serializePostVariables({
                handler: sysname,
                values: areas_string,
                unique_sharing_key: unique_sharing_key
            });

            this.setExtendedErrorInfo("");

            var progressUpdater = window.setInterval(function(cartogram_inst, key){

                return function(){

                    HTTP.get(cartogram_inst.config.getprogress_url + "?key=" + encodeURIComponent(key) + "&time=" + Date.now()).then(function(progress){

                        if(progress.progress === null)
                        {
                            return;
                        }

                        if(cartogram_inst.model.loading_state === null) {

                            cartogram_inst.model.loading_state = Math.log10(progress.progress);
                            cartogram_inst.updateProgressBar(0, 100, 5);

                        } else {

                            if(progress.progress < 0.01) {
                                progress.progress = 0.01
                            }

                            if(progress.progress > cartogram_inst.model.loading_state) {
                                progress.progress = cartogram_inst.model.loading_state;
                            }

                            /*console.log("progress: " + progress.progress);
                            console.log("distance: " + Math.abs(cartogram_inst.model.loading_state - Math.log10(progress.progress)));
                            console.log("area: " + Math.abs(cartogram_inst.model.loading_state - (-2)));*/
                        

                            var percentage = Math.floor(Math.abs(cartogram_inst.model.loading_state - Math.log10(progress.progress)) / Math.abs(cartogram_inst.model.loading_state - (-2))*100);

                            /*console.log("percentage: " + percentage);
                            console.log("");*/

                            cartogram_inst.updateProgressBar(5, 100, percentage);

                            cartogram_inst.setExtendedErrorInfo(progress.stderr);
                        }

                    });

                };

            }(this, unique_sharing_key), 500);

            HTTP.streaming(
                this.config.cartogram_url,
                "POST",
                {'Content-type': 'application/x-www-form-urlencoded'},
                req_body,
                {}
            ).then(function(response){

                this.clearExtendedErrorInfo();

                this.updateProgressBar(0,100,100);

                window.clearInterval(progressUpdater);

                resolve(response.cartogram_data);
                
            }.bind(this), function(){
                window.clearInterval(progressUpdater);
                reject(Error("There was an error retrieving the cartogram from the server."));
            });

        }.bind(this));

    }

    /**
     * displayVersionSwitchButtons displays the buttons the user can use to switch between different map versions on the
     * right.
     */
    displayVersionSwitchButtons() {

        var buttons_container = document.getElementById('map2-switch-buttons');

        // Empty the buttons container
        while(buttons_container.firstChild){
            buttons_container.removeChild(buttons_container.firstChild);
        }

        var select = document.createElement("select")
        select.className = "form-control bg-primary text-light border-primary";
        select.value = this.model.current_sysname;

        // Sorting keeps the ordering of versions consistent
        Object.keys(this.model.map.versions).sort().forEach(function(sysname){

            /*var button = document.createElement('button');
            button.innerText = this.model.map.versions[sysname].name;

            if(sysname == this.model.current_sysname)
            {
                button.className = "btn btn-secondary btn-sm active";
            }
            else
            {
                button.className = "btn btn-secondary btn-sm";
                button.onclick = (function(sn){

                    return function(e){
                        this.switchVersion(sn);
                    }.bind(this);

                }.bind(this)(sysname));
            }*/

            var option = document.createElement('option');
            option.innerText = this.model.map.versions[sysname].name;
            option.value = sysname;
            option.selected = (sysname === this.model.current_sysname);

            select.appendChild(option);

        }, this);

        select.onchange = (function(cartogram_inst){

            return function(_e) {
                cartogram_inst.switchVersion(this.value);
            };

        }(this));

        buttons_container.appendChild(select);

        document.getElementById('map1-switch').style.display = 'block';
        document.getElementById('map2-switch').style.display = 'block';

    }

    /**
     * switchVersion switches the map version displayed in the element with the given ID
     * @param {string} sysname The sysname of the new version to be displayed
     */
    switchVersion(sysname) {

        this.model.map.switchVersion(this.model.current_sysname, sysname, 'cartogram-area');

        this.model.current_sysname = sysname;

        this.displayVersionSwitchButtons();
    }

    /**
     * requestAndDrawCartogram generates and displays a cartogram with a user-provided dataset. Always returns false to 
     * prevent form submission.
     * 
     * This is a two step process. First, we make a request to CartogramUI. This generates color and tooltip information
     * from the uploaded dataset, as well as the areas string that needs to be given to the cartogram generator to
     * actually generate the cartogram with the given dataset.
     * 
     * Once it receives the areas string, the cartogram generator produces a streaming HTTP response with information on
     * the progress of cartogram generation, and the cartogram points in JSON format. The information from CartogramUI
     * and the cartogram generator is then combined to draw the cartogram with the correct colors and tooltip
     * information.
     * @param {Object} gd The grid document to retrieve the dataset from. If null, the dataset is taken from the
     * uploaded CSV file
     * @param {string} sysname The sysname of the map. If null, it is taken from the map selection form control. 
     * @param {boolean} update_grid_document Wether to update the grid document with the grid document returned from
     * CartogramUI
     * @returns {boolean}
     */
    requestAndDrawCartogram(gd=null,sysname=null,update_grid_document=true) {

        if(this.model.in_loading_state)
            return false;
        
        this.clearNonFatalError();

        /* Do some validation */

        if(gd === null)
        {
            if(document.getElementById('csv').files.length < 1)
            {
                this.doNonFatalError(Error('You must upload CSV data.'));
                return false;
            }
        }

        this.enterLoadingState();
        this.showProgressBar();

        if(sysname === null)
        {
            sysname = document.getElementById('handler').value;
        }

        var cartogramui_promise;

        /*
        If we're submitting a grid document, convert it and pretend to upload a CSV file. Otherwise, actually upload the
        CSV file the user specified.
        */
        if(gd === null)
        {
            var form_data = new FormData();

            form_data.append("handler", sysname);
            form_data.append("csv", document.getElementById('csv').files[0]);

            cartogramui_promise = HTTP.post(this.config.cartogramui_url, form_data);
        }
        else
        {
            var cartogramui_req_body = this.generateCartogramUIRequestBodyFromGridDocument(sysname, gd);

            cartogramui_promise = HTTP.post(this.config.cartogramui_url, cartogramui_req_body.req_body, {
                'Content-Type': 'multipart/form-data; boundary=' + cartogramui_req_body.mime_boundary
            });
        }

        cartogramui_promise.then(function(response){

            if(response.error == "none") {

                /*
                The keys in the CartogramUI color_data are prefixed with id_. We iterate through the regions and extract
                the color information from color_data to produce a color map where the IDs are plain region IDs, as
                required by CartMap.
                */
                var colors = {};

                Object.keys(this.model.map.regions).forEach(function(region_id){

                    colors[region_id] = response.color_data["id_" + region_id];

                }, this);

                this.model.map.colors = colors;

                this.getGeneratedCartogram(sysname, response.areas_string, response.unique_sharing_key).then(function(cartogram){

                    /* We need to find out the map format. If the extrema is located in the bbox property, then we have
                       GeoJSON. Otherwise, we have the old JSON format.
                    */

                    if(cartogram.hasOwnProperty("bbox")) {

                        var extrema = {
                            min_x: cartogram.bbox[0],
                            min_y: cartogram.bbox[1],
                            max_x: cartogram.bbox[2],
                            max_y: cartogram.bbox[3]
                        };

                        this.model.map.addVersion("3-cartogram", new MapVersionData(cartogram.features, extrema, response.tooltip, null, null, MapDataFormat.GEOJSON));


                    } else {
                        this.model.map.addVersion("3-cartogram", new MapVersionData(cartogram.features, cartogram.extrema, response.tooltip,null, null,  MapDataFormat.GOCARTJSON));
                    }

                    

                    this.model.map.drawVersion("1-conventional", "map-area", ["map-area", "cartogram-area"]);
                    this.model.map.drawVersion("3-cartogram", "cartogram-area", ["map-area", "cartogram-area"]);
                    
                    

                    this.model.current_sysname = "3-cartogram";

                    this.generateSocialMediaLinks("https://go-cart.io/cart/" + response.unique_sharing_key);
                    this.generateSVGDownloadLinks();
                    this.displayVersionSwitchButtons();

                    if(update_grid_document) {
                        this.updateGridDocument(response.grid_document);
                    }

                    this.model.map.drawLegend(this.model.current_sysname, "legend-square-cartogram-area", "legend-text-cartogram-area", "legend-superscript-cartogram-area", "legend-superscript-unit-cartogram-area");

                    // The following line draws the conventional legend when the page first loads.
                    this.model.map.drawLegend("1-conventional", "legend-square-map-area", "legend-text-map-area", "legend-superscript-map-area", "legend-superscript-unit-map-area");

                    this.exitLoadingState();
                    document.getElementById('cartogram').style.display = "block";

                }.bind(this), function(err){
                    this.doFatalError(err);

                    this.drawBarChartFromTooltip('barchart', response.tooltip);
                    document.getElementById('barchart-container').style.display = "block";
                }.bind(this))

            } else {

                this.exitLoadingState();
                document.getElementById('cartogram').style.display = "block";
                this.doNonFatalError(Error(response.error));

            }

        }.bind(this), this.doFatalError);

        return false;

    }

    /**
     * getPregeneratedVersion returns an HTTP get request for a pregenerated map version.
     * @param {string} sysname The sysname of the map
     * @param {string} version The sysname of the map version
     * @returns {Promise}
     */
    getPregeneratedVersion(sysname, version) {
        return HTTP.get(this.config.cartogram_data_dir + "/" + sysname + "/" + version + ".json");
    }

    /**
     * getDefaultColors returns an HTTP get request for the default color scheme for a map.
     * @param {string} sysname The sysname of the map
     * @returns {Promise}
     */
    getDefaultColors(sysname) {
        return HTTP.get(this.config.cartogram_data_dir + "/" + sysname + "/colors.json");
    }

    /**
     * getGridDocumentTemplate returns a HTTP get request for a map's grid document template.
     * @param {string} sysname The sysname of the map
     * @returns {Promise}
     */
    getGridDocumentTemplate(sysname) {
        return HTTP.get(this.config.cartogram_data_dir + "/" + sysname + "/griddocument.json");
    }

    /**
     * getLabels returns an HTTP get request for the labels for the land area version of a map.
     * @param {string} sysname The sysname of the map
     * @returns {Promise}
     */
    getLabels(sysname) {
        return HTTP.get(this.config.cartogram_data_dir + "/" + sysname + "/labels.json");
    }

    /**
     * getAbbreviations returns an HTTP get request for the region abbreviations of a map.
     * @param {string} sysname The sysname of the map
     * @returns {Promise}
     */
    getAbbreviations(sysname) {
        return HTTP.get(this.config.cartogram_data_dir + "/" + sysname + "/abbreviations.json");
    }

    /**
     * getConfig returns an HTTP get request for the configuration information of a map.
     * @param {string} sysname The sysname of the map
     * @returns {Promise}
     */
    getConfig(sysname) {
        return HTTP.get(this.config.cartogram_data_dir + "/" + sysname + "/config.json");
    }

    /**
     * getMapMap returns an HTTP get request for all of the static data (abbreviations, original and population map
     * geometries, etc.) for a map. The progress bar is automatically updated with the download progress.
     * 
     * A map pack is a JSON object containing all of this information, which used to be located in separate JSON files.
     * Combining all of this information into one file increases download speed, especially for users on mobile devices,
     * and makes it easier to display a progress bar of map information download progress, which is useful for users
     * with slow Internet connections.
     * @param {string} sysname The sysname of the map
     * @returns {Promise}
     */
    getMapPack(sysname) {
        return HTTP.get(this.config.cartogram_data_dir + "/" + sysname + "/mappack.json?v=" + this.config.version, null, function(e){

            this.updateProgressBar(0, 100, Math.floor(e.loaded / e.total * 100));

        }.bind(this));
    }

    /**
     * switchMap loads a new map with the given sysname, and displays the conventional and population versions, as well
     * as an optional extra cartogram.
     * @param {string} sysname The sysname of the new map to load
     * @param {string} hrname The human-readable name of the new map to load
     * @param {MapVersionData} cartogram An optional, extra cartogram to display
     * @param {Object.<string,string>} colors A color palette to use instead of the default one
     */
    switchMap(sysname, hrname, cartogram=null,colors=null) {
        if(this.model.in_loading_state)
            return;
        
        this.enterLoadingState();
        this.showProgressBar();
        
        this.getMapPack(sysname).then(function(mappack){

            var map = new CartMap(hrname, mappack.config);

            /* We need to find out the map format. If the extrema is located in the bbox property, then we have
               GeoJSON. Otherwise, we have the old JSON format.
            */

            if(mappack.original.hasOwnProperty("bbox")) {

                var extrema = {
                    min_x: mappack.original.bbox[0],
                    min_y: mappack.original.bbox[1],
                    max_x: mappack.original.bbox[2],
                    max_y: mappack.original.bbox[3]
                };

                map.addVersion("1-conventional", new MapVersionData(mappack.original.features, extrema, mappack.original.tooltip, mappack.abbreviations, mappack.labels, MapDataFormat.GEOJSON));

            } else {
                map.addVersion("1-conventional", new MapVersionData(mappack.original.features, mappack.original.extrema, mappack.original.tooltip, mappack.abbreviations, mappack.labels, MapDataFormat.GOCARTJSON));
            }

            if(mappack.population.hasOwnProperty("bbox")) {

                var extrema = {
                    min_x: mappack.population.bbox[0],
                    min_y: mappack.population.bbox[1],
                    max_x: mappack.population.bbox[2],
                    max_y: mappack.population.bbox[3]
                };

                map.addVersion("2-population", new MapVersionData(mappack.population.features, extrema, mappack.population.tooltip, null, null, MapDataFormat.GEOJSON));

            } else {
                map.addVersion("2-population", new MapVersionData(mappack.population.features, mappack.population.extrema, mappack.population.tooltip, null, null, MapDataFormat.GOCARTJSON));
            }            

            if(cartogram !== null) {
                map.addVersion("3-cartogram", cartogram);
            }

            /*
            The keys in the colors.json file are prefixed with id_. We iterate through the regions and extract the color
            information from colors.json to produce a color map where the IDs are plain region IDs, as required by
            CartMap.
            */
            var colors = {};

            Object.keys(map.regions).forEach(function(region_id){

                colors[region_id] = mappack.colors["id_" + region_id];

            }, this);

            map.colors = colors;

            map.drawVersion("1-conventional", "map-area", ["map-area", "cartogram-area"]);

            if(cartogram !== null) {
                map.drawVersion("3-cartogram", "cartogram-area", ["map-area", "cartogram-area"]);
                this.model.current_sysname = "1-cartogram";
            } else {
                map.drawVersion("2-population", "cartogram-area", ["map-area", "cartogram-area"]);
                this.model.current_sysname = "2-population";
            }           

            this.model.map = map;           

            this.exitLoadingState();

            this.generateSocialMediaLinks(window.location.href);
            this.generateSVGDownloadLinks();
            this.displayVersionSwitchButtons();
            this.updateGridDocument(mappack.griddocument);

            this.model.map.drawLegend(this.model.current_sysname, "legend-square-cartogram-area", "legend-text-cartogram-area", "legend-superscript-cartogram-area", "legend-superscript-unit-cartogram-area");
            
            // The following line draws the conventional legend when the page first loads.
            this.model.map.drawLegend("1-conventional", "legend-square-map-area", "legend-text-map-area", "legend-superscript-map-area", "legend-superscript-unit-map-area");

            document.getElementById('template-link').href = this.config.cartogram_data_dir+ "/" + sysname + "/template.csv";
            document.getElementById('cartogram').style.display = 'block';

        }.bind(this));       

    }

}
<h1>Adding a Map</h1>

<p>This guide will help you add a new map to the go-cart.io website. This guide assumes that you have already set up the website code for local testing and development. If you have not done this, please read the setup guide in <code>docs/setup</code> before you continue.</p>

<h2>What You'll Need</h2>

<p>To add a map, you will need the following files, information, and software:</p>

<ul>
<li>Conventional map geography, in .gen format</li>
<li>Map region names and abbreviations</li>
<li>A sample dataset (e.g. GDP)</li>
<li>Population and land area (in km^2) for each map region</li>
<li>Inkscape, a free, open-source vector graphics editor for Windows, Mac, and Linux that can be downloaded at https://inkscape.org/. </li>
</ul>

<h2>Preparing Your Data</h2>

<p>The first step in adding a map is to prepare your data. First, you will need to copy the .gen file for the conventional map into <code>CARTOGRAM_DATA_DIR</code> (the folder where the C code lives). Then, you will need to create a .dat file for your map. This file will contain the names and abbreviations of your map, and your sample dataset. It is a text file that contains one entry per line. Each entry should look like (brackets should be omitted):</p>

<pre><code>[Region ID] [Sample Dataset Value] [Region Name] [Region Abbreviation]
</code></pre>

<p>The region IDs in the .dat file should correspond to the region IDs in your .gen file. For your reference, here is a .dat file for Germany:</p>

<pre><code>1 1787408 Hamburg HH
2 7926599 Niedersachsen NI
3 671489 Bremen HB
4 17865516 Nordrhein-Westfalen NW
5 6176172 Hessen HE
6 4052803 Rheinland-Pfalz RP
7 10879618 Baden-Wuerttemberg BW
8 12843514 Bayern BY
9 995597 Saarland SL
10 3520031 Berlin BE
11 2484826 Brandenburg BB
12 1612362 Mecklenburg-Vorpommern MV
13 4084851 Sachsen SN
14 2245470 Sachsen-Anhalt ST
15 2170714 Thueringen TH
16 2858714 Schleswig-Holstein SH
</code></pre>

<p>Some region names may contain accent marks or other unicode characters. Please use only ASCII characters in your .dat file. For example, in the .dat file above Thüringen is rendered as 'Theuringen'.</p>

<p>When you're finished creating your .dat file, you should save it in <code>CARTOGRAM_DATA_DIR</code>.</p>

<h2>Initializing Your Map</h2>

<p>Before creating a new map, you should create a Git branch to contain your work. Open a Terminal window and navigate to the <code>internal/</code> directory of the repository. Then, run</p>

<pre><code>$ git branch add-my-map-name
$ git checkout add-my-map-name
</code></pre>

<p>You should never add maps or make other changes on the default <code>master</code> branch!</p>

<p>From here on, you will be making use of the Add Map Wizard. Before you can use this wizard to initialize your new map, you must enter the Python virtual environment used by the go-cart.io website code. To do this, run</p>

<pre><code>$ source ./setupenv.sh
</code></pre>

<p>Your command prompt should change to indicate the you are in the virtual environment:</p>

<pre><code>(venv) $
</code></pre>

<p>Now you can run the Add Map Wizard. You will need to pick a name for your map to be used by the website code (this is different from the user-friendly name seen by website users). This name <strong>must not</strong> include spaces, hyphens, underscores, or any punctuation. Below are some example names for your reference:</p>

<pre><code>Map                     | Code Name
United States           | usa
Mainland China &amp; Taiwan | china
Germany                 | germany
</code></pre>

<p>This code name must be unique. The Add Map Wizard will let you know if your choice of code name has already been taken.</p>

<p>Once you have chosen a code name, you can run the Add Map Wizard:</p>

<pre><code>(venv) $ python addmap.py init your-code-name
</code></pre>

<p>The wizard will then ask you a series of questions about your map, and generate files needed to complete the map addition process.</p>

<pre><code>(venv) $ python addmap.py init france

Welcome to the Add Map Wizard!

Enter a user friendly name for this map: France

Now I need to know where the .gen and .dat files for this map are located. These files should be located in the CARTOGRAM_DATA_DIR directory. You should supply me with a path relative to CARTOGRAM_DATA_DIR.
E.G: The .gen file for this map is located at CARTOGRAM_DATA_DIR/map.gen. Enter "map.gen".

Enter the location of the .gen file for this map: france.gen
Enter the location of the .dat file for this map: france.dat
What are the regions of this map called (e.g. State, Province)? Department
What is the name of the dataset in the .dat file (e.g. GDP)? GDP

Writing handlers/france.py...
Writing static/cartdata/france/config.json...
Writing static/cartdata/france/abbreviations.json...
Writing static/cartdata/france/colors.json...
Writing static/cartdata/france/template.csv...

I will now create france.svg. You should edit this file to specify the default color and add labels for each region.
DO NOT RESIZE OR RESCALE THE CONTENTS OF THIS FILE! Accurate label placement depends on the scale calculated by this wizard.

Writing france.svg...
Writing static/cartdata/france/labels.json...

I will now create france-landarea.csv and france-population.csv. You should edit these files to specify the land area (in square kilometers) and population of each region.
DO NOT ALTER THE COLOR INFORMATION IN THESE FILES! You should specify the color for each region by editing france.svg

Writing france-landarea.csv...
Writing france-population.csv...

I will now modify web.py to add your new map. Before I do this, I will back up the current version of web.py to web.py.bak.

Backing up web.py...
Editing web.py...

All done!
</code></pre>

<p>If there is a problem, the wizard will print an error message, clean up, and exit. If an error occurs while the wizard is editing <code>web.py</code>, and this file becomes corrupted, you will need to restore the backup manually. You can do this by running:</p>

<pre><code>(venv) $ cp web.py.bak web.py
</code></pre>

<h2>Adding the Rest of Your Data</h2>

<p>At this point, the Add Map Wizard has produced several files in the <code>internal/</code> directory that you'll need to edit to complete the map addition process. First, you should edit <code>your-map-landarea.csv</code> and <code>your-map-population.csv</code> to add the population and land area information for each map region. You can edit these manually, using a text editor, or with a spreadsheet program like LibreOffice Calc or Microsoft Excel.</p>

<p>Now, by editing <code>your-map.svg</code> using Inkscape, you will set the default color for each map region and add labels for the conventional map. </p>

<h3>Adding Colors</h3>

<p>The go-cart.io website uses the same color scheme for all maps. The six colors you should use are listed below in Hex form, and can be seen by going to the <a href="http://colorbrewer2.org/#type=qualitative&amp;scheme=Dark2&amp;n=6">color scheme page</a> on ColorBrewer:</p>

<pre><code>#1b9e77
#d95f02
#7570b3
#e7298a
#66a61e
#e6ab02
</code></pre>

<p>Open <code>your-map.svg</code> in Inkscape. You should see a rendered version of your conventional map, with each region shaded with a light-gray:</p>

<p><img src="inkscape-colors1.png" alt="Inkscape 1" title="" /></p>

<p>To make adding colors easier, you will create a custom palette with the six colors in the ColorBrewer color scheme. To do this, click the left-pointing arrow at the bottom right corner of the Inkscape window. Then, select the 'Auto' palette. The color palette bar at the bottom of the window should then appear like in the screenshot above.</p>

<p>Now, right-click on a region you want to color, and select 'Fill and Stroke...'. A panel should open on the right-hand side of the Inkscape window:</p>

<p><img src="inkscape-colors2.png" alt="Inkscape 2" title="" /></p>

<p>Now, enter the Hex code for the color you want into the textbox labeled 'RGBA'. Add <code>ff</code> to the end for full opacity:</p>

<p><img src="inkscape-colors3.png" alt="Inkscape 3" title="" /></p>

<p>Now, click the swatch button (to the left of the question mark button in the Fill and Stroke panel). This will add the color to the palette bar:</p>

<p><img src="inkscape-colors4.png" alt="Inkscape 4" title="" /></p>

<p>Repeat this process for the remaining five colors. When you are finished, the palette bar should look something like:</p>

<p><img src="inkscape-colors5.png" alt="Inkscape 5" title="" /></p>

<p>Now the coloring process becomes significantly easier. Left click on each region you want to color, and then left click on the color in the palette bar you want to apply to that region. Color the map as you wish while keeping in mind the following constraints:</p>

<ul>
<li>Neighboring regions <strong>must not</strong> have the same color.</li>
<li>The distribution of colors throughout the map should be roughly equal. The default colors are not used to indicate data, but instead to allow users to clearly see the region boundaries.</li>
</ul>

<p>Some of your map regions may include many small polygons that are hard to spot in Inkscape. You don't have to color each one. The Add Map Wizard only requires that you color <strong>one</strong> polygon per map region (usually it is easiest if you color the largest one).</p>

<p>When you are done coloring each region, you should save your SVG file. Go to <code>File -&gt; Save As...</code> in the Inkscape menu. Don't change the filename, but ensure that the file type is <code>Plain SVG</code>, and <strong>not</strong> <code>Inkscape SVG</code>. When saving, Inkscape may ask you whether you want to overwrite your SVG file. You should accept overwriting this file. </p>

<h3>Adding Labels</h3>

<p>The go-cart.io website displays labels on the conventional map, which consist of text for region abbreviations, and lines. You can use Inkscape to add these labels. Open <code>your-map.svg</code> in Inkscape.</p>

<p>First, we'll add a text label. Click the text tool on the toolbar, left click on the map where you want to place the text label, and type the text you want to appear in the label.</p>

<p><img src="inkscape-labels1.png" alt="Inkscape 6" title="" /></p>

<p><img src="inkscape-labels2.png" alt="Inkscape 7" title="" /></p>

<p>Adjust the font size to 14 so that the label text appears as it would on the website. The font size of the labels in Inkscape does not affect their appearance on the website, but setting it appropriately will make it easier for you to place them correctly.</p>

<p>Now, go to <code>Object -&gt; Object Properties...</code>. Set the 'Label' field to <code>gocartlabel</code>, and click 'Set'. This will help the Add Map Wizard find your text labels in the SVG document.</p>

<p><img src="inkscape-labels3.png" alt="Inkscape 8" title="" /></p>

<p>If a region is too small to contain a text label, you can place the text label outside the map (but still within the bounding box), and include a line pointing from the label to the region. Click the line tool on the toolbar. Then, left click once on the image where you want the line to start. Left click again where you want the line to end, and right click to finish.</p>

<p><img src="inkscape-labels4.png" alt="Inkscape 9" title="" /></p>

<p><img src="inkscape-labels5.png" alt="Inkscape 10" title="" /></p>

<p>Again, go to <code>Object -&gt; Object Properties...</code>. Set the 'Label' field to <code>gocartlabel</code>, and click 'Set'.</p>

<p>Once you have finished adding all of your labels, you should save your SVG file. Go to <code>File -&gt; Save As...</code> in the Inkscape menu. Don't change the filename, but ensure that the file type is <code>Plain SVG</code>, and <strong>not</strong> <code>Inkscape SVG</code>. When saving, Inkscape may ask you whether you want to overwrite your SVG file. You should accept overwriting this file.</p>

<h3>Finishing Up</h3>

<p>At this point, you're now ready to finish the map addition process. Open a Terminal window and navigate to the <code>internal/</code> directory of the repository. Then, run</p>

<pre><code>$ source ./setupenv.sh
</code></pre>

<p>Your command prompt should change to indicate the you are in the virtual environment:</p>

<pre><code>(venv) $
</code></pre>

<p>Now you can run the Add Map Wizard again:</p>

<pre><code>(venv) $ python addmap.py data your-code-name
</code></pre>

<h2>Saving Your Changes</h2>

<p>You should commit your changes to your Git branch, and push these changes to GitHub.</p>

<pre><code>$ git add handlers
$ git add static
$ git commit -a -m "added map New Map Name"
$ git push origin add-my-map-name
</code></pre>

<p>Then, revert back to the master branch:</p>

<pre><code>$ git checkout master
</code></pre>

<p>You should also create a pull request on GitHub to let me know that you have finished adding the new map, so I can deploy it to the website. Navigate to https://github.com/jansky/cartogram-web/compare/, select your branch, and click 'Create pull request'.</p>

<p><img src="pull-request.png" alt="Pull Request" title="" /></p>

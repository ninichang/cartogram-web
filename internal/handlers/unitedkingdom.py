import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "United Kingdom"

    def get_gen_file(self):
        return "{}/unitedkingdom_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 999:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Aberdeen City
2 {} Aberdeenshire
3 {} Adur
4 {} Allerdale
5 {} Amber Valley
6 {} Angus
7 {} Argyll and Bute
8 {} Arun
9 {} Ashfield
10 {} Ashford
11 {} Aylesbury Vale
12 {} Babergh
13 {} Barking and Dagenham
14 {} Barnet
15 {} Barnsley
16 {} Barrow-in-Furness
17 {} Basildon
18 {} Basingstoke and Deane
19 {} Bassetlaw
20 {} Bath and North East Somerset
21 {} Bedford
22 {} Bexley
23 {} Birmingham
24 {} Blaby
25 {} Blackburn with Darwen
26 {} Blackpool
27 {} Blaenau Gwent
28 {} Bolsover
29 {} Bolton
30 {} Boston
31 {} Bournemouth
32 {} Bracknell Forest
33 {} Bradford
34 {} Braintree
35 {} Breckland
36 {} Brent
37 {} Brentwood
38 {} Bridgend
39 {} Brighton and Hove
40 {} Bristol, City of
41 {} Broadland
42 {} Bromley
43 {} Bromsgrove
44 {} Broxbourne
45 {} Broxtowe
46 {} Burnley
47 {} Bury
48 {} Caerphilly
49 {} Calderdale
50 {} Cambridge
51 {} Camden
52 {} Cannock Chase
53 {} Canterbury
54 {} Cardiff
55 {} Carlisle
56 {} Carmarthenshire
57 {} Castle Point
58 {} Central Bedfordshire
59 {} Ceredigion
60 {} Charnwood
61 {} Chelmsford
62 {} Cheltenham
63 {} Cherwell
64 {} Cheshire East
65 {} Cheshire West and Chester
66 {} Chesterfield
67 {} Chichester
68 {} Chiltern
69 {} Chorley
70 {} Christchurch
71 {} City of Edinburgh
72 {} City of London
73 {} Clackmannanshire
74 {} Colchester
75 {} Conwy
76 {} Copeland
77 {} Corby
78 {} Cornwall
79 {} Cotswold
80 {} County Durham
81 {} Coventry
82 {} Craven
83 {} Crawley
84 {} Croydon
85 {} Dacorum
86 {} Darlington
87 {} Dartford
88 {} Daventry
89 {} Denbighshire
90 {} Derby
91 {} Derbyshire Dales
92 {} Doncaster
93 {} Dover
94 {} Dudley
95 {} Dumfries and Galloway
96 {} Dundee City
97 {} Ealing
98 {} East Ayrshire
99 {} East Cambridgeshire
100 {} East Devon
101 {} East Dorset
102 {} East Dunbartonshire
103 {} East Hampshire
104 {} East Hertfordshire
105 {} East Lindsey
106 {} East Lothian
107 {} East Northamptonshire
108 {} East Renfrewshire
109 {} East Riding of Yorkshire
110 {} East Staffordshire
111 {} Eastbourne
112 {} Eastleigh
113 {} Eden
114 {} Elmbridge
115 {} Enfield
116 {} Epping Forest
117 {} Epsom and Ewell
118 {} Erewash
119 {} Exeter
120 {} Falkirk
121 {} Fareham
122 {} Fenland
123 {} Fife
124 {} Flintshire
125 {} Forest Heath
126 {} Forest of Dean
127 {} Fylde
128 {} Gateshead
129 {} Gedling
130 {} Glasgow City
131 {} Gloucester
132 {} Gosport
133 {} Gravesham
134 {} Great Yarmouth
135 {} Greenwich
136 {} Guildford
137 {} Gwynedd
138 {} Hackney
139 {} Halton
140 {} Hambleton
141 {} Hammersmith and Fulham
142 {} Harborough
143 {} Haringey
144 {} Harlow
145 {} Harrogate
146 {} Harrow
147 {} Hart
148 {} Hartlepool
149 {} Hastings
150 {} Havant
151 {} Havering
152 {} Herefordshire, County of
153 {} Hertsmere
154 {} High Peak
155 {} Highland
156 {} Hillingdon
157 {} Hinckley and Bosworth
158 {} Horsham
159 {} Hounslow
160 {} Huntingdonshire
161 {} Hyndburn
162 {} Inverclyde
163 {} Ipswich
164 {} Isle of Anglesey
165 {} Isle of Wight
166 {} Isles of Scilly
167 {} Islington
168 {} Kensington and Chelsea
169 {} Kettering
170 {} King's Lynn and West Norfolk
171 {} Kingston upon Hull, City of
172 {} Kingston upon Thames
173 {} Kirklees
174 {} Knowsley
175 {} Lambeth
176 {} Lancaster
177 {} Leeds
178 {} Leicester
179 {} Lewes
180 {} Lewisham
181 {} Lichfield
182 {} Lincoln
183 {} Liverpool
184 {} Luton
185 {} Maidstone
186 {} Maldon
187 {} Malvern Hills
188 {} Manchester
189 {} Mansfield
190 {} Medway
191 {} Melton
192 {} Mendip
193 {} Merthyr Tydfil
194 {} Merton
195 {} Mid Devon
196 {} Mid Suffolk
197 {} Mid Sussex
198 {} Middlesbrough
199 {} Midlothian
200 {} Milton Keynes
201 {} Mole Valley
202 {} Monmouthshire
203 {} Moray
204 {} Na h-Eileanan Siar
205 {} Neath Port Talbot
206 {} New Forest
207 {} Newark and Sherwood
208 {} Newcastle upon Tyne
209 {} Newcastle-under-Lyme
210 {} Newham
211 {} Newport
212 {} North Ayrshire
213 {} North Devon
214 {} North Dorset
215 {} North East Derbyshire
216 {} North East Lincolnshire
217 {} North Hertfordshire
218 {} North Kesteven
219 {} North Lanarkshire
220 {} North Lincolnshire
221 {} North Norfolk
222 {} North Somerset
223 {} North Tyneside
224 {} North Warwickshire
225 {} North West Leicestershire
226 {} Northampton
227 {} Northumberland
228 {} Norwich
229 {} Nottingham
230 {} Nuneaton and Bedworth
231 {} Oadby and Wigston
232 {} Oldham
233 {} Orkney Islands
234 {} Oxford
235 {} Pembrokeshire
236 {} Pendle
237 {} Perth and Kinross
238 {} Peterborough
239 {} Plymouth
240 {} Poole
241 {} Portsmouth
242 {} Powys
243 {} Preston
244 {} Purbeck
245 {} Reading
246 {} Redbridge
247 {} Redcar and Cleveland
248 {} Redditch
249 {} Reigate and Banstead
250 {} Renfrewshire
251 {} Rhondda Cynon Taf
252 {} Ribble Valley
253 {} Richmond upon Thames
254 {} Richmondshire
255 {} Rochdale
256 {} Rochford
257 {} Rossendale
258 {} Rother
259 {} Rotherham
260 {} Rugby
261 {} Runnymede
262 {} Rushcliffe
263 {} Rushmoor
264 {} Rutland
265 {} Ryedale
266 {} Salford
267 {} Sandwell
268 {} Scarborough
269 {} Scottish Borders
270 {} Sedgemoor
271 {} Sefton
272 {} Selby
273 {} Sevenoaks
274 {} Sheffield
275 {} Shepway
276 {} Shetland Islands
277 {} Shropshire
278 {} Slough
279 {} Solihull
280 {} South Ayrshire
281 {} South Bucks
282 {} South Cambridgeshire
283 {} South Derbyshire
284 {} South Gloucestershire
285 {} South Hams
286 {} South Holland
287 {} South Kesteven
288 {} South Lakeland
289 {} South Lanarkshire
290 {} South Norfolk
291 {} South Northamptonshire
292 {} South Oxfordshire
293 {} South Ribble
294 {} South Somerset
295 {} South Staffordshire
296 {} South Tyneside
297 {} Southampton
298 {} Southend-on-Sea
299 {} Southwark
300 {} Spelthorne
301 {} St Albans
302 {} St Edmundsbury
303 {} St. Helens
304 {} Stafford
305 {} Staffordshire Moorlands
306 {} Stevenage
307 {} Stirling
308 {} Stockport
309 {} Stockton-on-Tees
310 {} Stoke-on-Trent
311 {} Stratford-on-Avon
312 {} Stroud
313 {} Suffolk Coastal
314 {} Sunderland
315 {} Surrey Heath
316 {} Sutton
317 {} Swale
318 {} Swansea
319 {} Swindon
320 {} Tameside
321 {} Tamworth
322 {} Tandridge
323 {} Taunton Deane
324 {} Teignbridge
325 {} Telford and Wrekin
326 {} Tendring
327 {} Test Valley
328 {} Tewkesbury
329 {} Thanet
330 {} Three Rivers
331 {} Thurrock
332 {} Tonbridge and Malling
333 {} Torbay
334 {} Torfaen
335 {} Torridge
336 {} Tower Hamlets
337 {} Trafford
338 {} Tunbridge Wells
339 {} Uttlesford
340 {} Vale of Glamorgan
341 {} Vale of White Horse
342 {} Wakefield
343 {} Walsall
344 {} Waltham Forest
345 {} Wandsworth
346 {} Warrington
347 {} Warwick
348 {} Watford
349 {} Waveney
350 {} Waverley
351 {} Wealden
352 {} Wellingborough
353 {} Welwyn Hatfield
354 {} West Berkshire
355 {} West Devon
356 {} West Dorset
357 {} West Dunbartonshire
358 {} West Lancashire
359 {} West Lindsey
360 {} West Lothian
361 {} West Oxfordshire
362 {} West Somerset
363 {} Westminster
364 {} Weymouth and Portland
365 {} Wigan
366 {} Wiltshire
367 {} Winchester
368 {} Windsor and Maidenhead
369 {} Wirral
370 {} Woking
371 {} Wokingham
372 {} Wolverhampton
373 {} Worcester
374 {} Worthing
375 {} Wrexham
376 {} Wychavon
377 {} Wycombe
378 {} Wyre
379 {} Wyre Forest
380 {} York
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} 
 {} """.format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Aberdeen City","Aberdeenshire","Adur","Allerdale","Amber Valley","Angus","Argyll and Bute","Arun","Ashfield","Ashford","Aylesbury Vale","Babergh","Barking and Dagenham","Barnet","Barnsley","Barrow-in-Furness","Basildon","Basingstoke and Deane","Bassetlaw","Bath and North East Somerset","Bedford","Bexley","Birmingham","Blaby","Blackburn with Darwen","Blackpool","Blaenau Gwent","Bolsover","Bolton","Boston","Bournemouth","Bracknell Forest","Bradford","Braintree","Breckland","Brent","Brentwood","Bridgend","Brighton and Hove","Bristol, City of","Broadland","Bromley","Bromsgrove","Broxbourne","Broxtowe","Burnley","Bury","Caerphilly","Calderdale","Cambridge","Camden","Cannock Chase","Canterbury","Cardiff","Carlisle","Carmarthenshire","Castle Point","Central Bedfordshire","Ceredigion","Charnwood","Chelmsford","Cheltenham","Cherwell","Cheshire East","Cheshire West and Chester","Chesterfield","Chichester","Chiltern","Chorley","Christchurch","City of Edinburgh","City of London","Clackmannanshire","Colchester","Conwy","Copeland","Corby","Cornwall","Cotswold","County Durham","Coventry","Craven","Crawley","Croydon","Dacorum","Darlington","Dartford","Daventry","Denbighshire","Derby","Derbyshire Dales","Doncaster","Dover","Dudley","Dumfries and Galloway","Dundee City","Ealing","East Ayrshire","East Cambridgeshire","East Devon","East Dorset","East Dunbartonshire","East Hampshire","East Hertfordshire","East Lindsey","East Lothian","East Northamptonshire","East Renfrewshire","East Riding of Yorkshire","East Staffordshire","Eastbourne","Eastleigh","Eden","Elmbridge","Enfield","Epping Forest","Epsom and Ewell","Erewash","Exeter","Falkirk","Fareham","Fenland","Fife","Flintshire","Forest Heath","Forest of Dean","Fylde","Gateshead","Gedling","Glasgow City","Gloucester","Gosport","Gravesham","Great Yarmouth","Greenwich","Guildford","Gwynedd","Hackney","Halton","Hambleton","Hammersmith and Fulham","Harborough","Haringey","Harlow","Harrogate","Harrow","Hart","Hartlepool","Hastings","Havant","Havering","Herefordshire, County of","Hertsmere","High Peak","Highland","Hillingdon","Hinckley and Bosworth","Horsham","Hounslow","Huntingdonshire","Hyndburn","Inverclyde","Ipswich","Isle of Anglesey","Isle of Wight","Isles of Scilly","Islington","Kensington and Chelsea","Kettering","King's Lynn and West Norfolk","Kingston upon Hull, City of","Kingston upon Thames","Kirklees","Knowsley","Lambeth","Lancaster","Leeds","Leicester","Lewes","Lewisham","Lichfield","Lincoln","Liverpool","Luton","Maidstone","Maldon","Malvern Hills","Manchester","Mansfield","Medway","Melton","Mendip","Merthyr Tydfil","Merton","Mid Devon","Mid Suffolk","Mid Sussex","Middlesbrough","Midlothian","Milton Keynes","Mole Valley","Monmouthshire","Moray","Na h-Eileanan Siar","Neath Port Talbot","New Forest","Newark and Sherwood","Newcastle upon Tyne","Newcastle-under-Lyme","Newham","Newport","North Ayrshire","North Devon","North Dorset","North East Derbyshire","North East Lincolnshire","North Hertfordshire","North Kesteven","North Lanarkshire","North Lincolnshire","North Norfolk","North Somerset","North Tyneside","North Warwickshire","North West Leicestershire","Northampton","Northumberland","Norwich","Nottingham","Nuneaton and Bedworth","Oadby and Wigston","Oldham","Orkney Islands","Oxford","Pembrokeshire","Pendle","Perth and Kinross","Peterborough","Plymouth","Poole","Portsmouth","Powys","Preston","Purbeck","Reading","Redbridge","Redcar and Cleveland","Redditch","Reigate and Banstead","Renfrewshire","Rhondda Cynon Taf","Ribble Valley","Richmond upon Thames","Richmondshire","Rochdale","Rochford","Rossendale","Rother","Rotherham","Rugby","Runnymede","Rushcliffe","Rushmoor","Rutland","Ryedale","Salford","Sandwell","Scarborough","Scottish Borders","Sedgemoor","Sefton","Selby","Sevenoaks","Sheffield","Shepway","Shetland Islands","Shropshire","Slough","Solihull","South Ayrshire","South Bucks","South Cambridgeshire","South Derbyshire","South Gloucestershire","South Hams","South Holland","South Kesteven","South Lakeland","South Lanarkshire","South Norfolk","South Northamptonshire","South Oxfordshire","South Ribble","South Somerset","South Staffordshire","South Tyneside","Southampton","Southend-on-Sea","Southwark","Spelthorne","St Albans","St Edmundsbury","St. Helens","Stafford","Staffordshire Moorlands","Stevenage","Stirling","Stockport","Stockton-on-Tees","Stoke-on-Trent","Stratford-on-Avon","Stroud","Suffolk Coastal","Sunderland","Surrey Heath","Sutton","Swale","Swansea","Swindon","Tameside","Tamworth","Tandridge","Taunton Deane","Teignbridge","Telford and Wrekin","Tendring","Test Valley","Tewkesbury","Thanet","Three Rivers","Thurrock","Tonbridge and Malling","Torbay","Torfaen","Torridge","Tower Hamlets","Trafford","Tunbridge Wells","Uttlesford","Vale of Glamorgan","Vale of White Horse","Wakefield","Walsall","Waltham Forest","Wandsworth","Warrington","Warwick","Watford","Waveney","Waverley","Wealden","Wellingborough","Welwyn Hatfield","West Berkshire","West Devon","West Dorset","West Dunbartonshire","West Lancashire","West Lindsey","West Lothian","West Oxfordshire","West Somerset","Westminster","Weymouth and Portland","Wigan","Wiltshire","Winchester","Windsor and Maidenhead","Wirral","Woking","Wokingham","Wolverhampton","Worcester","Worthing","Wrexham","Wychavon","Wycombe","Wyre","Wyre Forest","York","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""], [0.0 for i in range(0,999)], {"Aberdeen City":"1","Aberdeenshire":"2","Adur":"3","Allerdale":"4","Amber Valley":"5","Angus":"6","Argyll and Bute":"7","Arun":"8","Ashfield":"9","Ashford":"10","Aylesbury Vale":"11","Babergh":"12","Barking and Dagenham":"13","Barnet":"14","Barnsley":"15","Barrow-in-Furness":"16","Basildon":"17","Basingstoke and Deane":"18","Bassetlaw":"19","Bath and North East Somerset":"20","Bedford":"21","Bexley":"22","Birmingham":"23","Blaby":"24","Blackburn with Darwen":"25","Blackpool":"26","Blaenau Gwent":"27","Bolsover":"28","Bolton":"29","Boston":"30","Bournemouth":"31","Bracknell Forest":"32","Bradford":"33","Braintree":"34","Breckland":"35","Brent":"36","Brentwood":"37","Bridgend":"38","Brighton and Hove":"39","Bristol, City of":"40","Broadland":"41","Bromley":"42","Bromsgrove":"43","Broxbourne":"44","Broxtowe":"45","Burnley":"46","Bury":"47","Caerphilly":"48","Calderdale":"49","Cambridge":"50","Camden":"51","Cannock Chase":"52","Canterbury":"53","Cardiff":"54","Carlisle":"55","Carmarthenshire":"56","Castle Point":"57","Central Bedfordshire":"58","Ceredigion":"59","Charnwood":"60","Chelmsford":"61","Cheltenham":"62","Cherwell":"63","Cheshire East":"64","Cheshire West and Chester":"65","Chesterfield":"66","Chichester":"67","Chiltern":"68","Chorley":"69","Christchurch":"70","City of Edinburgh":"71","City of London":"72","Clackmannanshire":"73","Colchester":"74","Conwy":"75","Copeland":"76","Corby":"77","Cornwall":"78","Cotswold":"79","County Durham":"80","Coventry":"81","Craven":"82","Crawley":"83","Croydon":"84","Dacorum":"85","Darlington":"86","Dartford":"87","Daventry":"88","Denbighshire":"89","Derby":"90","Derbyshire Dales":"91","Doncaster":"92","Dover":"93","Dudley":"94","Dumfries and Galloway":"95","Dundee City":"96","Ealing":"97","East Ayrshire":"98","East Cambridgeshire":"99","East Devon":"100","East Dorset":"101","East Dunbartonshire":"102","East Hampshire":"103","East Hertfordshire":"104","East Lindsey":"105","East Lothian":"106","East Northamptonshire":"107","East Renfrewshire":"108","East Riding of Yorkshire":"109","East Staffordshire":"110","Eastbourne":"111","Eastleigh":"112","Eden":"113","Elmbridge":"114","Enfield":"115","Epping Forest":"116","Epsom and Ewell":"117","Erewash":"118","Exeter":"119","Falkirk":"120","Fareham":"121","Fenland":"122","Fife":"123","Flintshire":"124","Forest Heath":"125","Forest of Dean":"126","Fylde":"127","Gateshead":"128","Gedling":"129","Glasgow City":"130","Gloucester":"131","Gosport":"132","Gravesham":"133","Great Yarmouth":"134","Greenwich":"135","Guildford":"136","Gwynedd":"137","Hackney":"138","Halton":"139","Hambleton":"140","Hammersmith and Fulham":"141","Harborough":"142","Haringey":"143","Harlow":"144","Harrogate":"145","Harrow":"146","Hart":"147","Hartlepool":"148","Hastings":"149","Havant":"150","Havering":"151","Herefordshire, County of":"152","Hertsmere":"153","High Peak":"154","Highland":"155","Hillingdon":"156","Hinckley and Bosworth":"157","Horsham":"158","Hounslow":"159","Huntingdonshire":"160","Hyndburn":"161","Inverclyde":"162","Ipswich":"163","Isle of Anglesey":"164","Isle of Wight":"165","Isles of Scilly":"166","Islington":"167","Kensington and Chelsea":"168","Kettering":"169","King's Lynn and West Norfolk":"170","Kingston upon Hull, City of":"171","Kingston upon Thames":"172","Kirklees":"173","Knowsley":"174","Lambeth":"175","Lancaster":"176","Leeds":"177","Leicester":"178","Lewes":"179","Lewisham":"180","Lichfield":"181","Lincoln":"182","Liverpool":"183","Luton":"184","Maidstone":"185","Maldon":"186","Malvern Hills":"187","Manchester":"188","Mansfield":"189","Medway":"190","Melton":"191","Mendip":"192","Merthyr Tydfil":"193","Merton":"194","Mid Devon":"195","Mid Suffolk":"196","Mid Sussex":"197","Middlesbrough":"198","Midlothian":"199","Milton Keynes":"200","Mole Valley":"201","Monmouthshire":"202","Moray":"203","Na h-Eileanan Siar":"204","Neath Port Talbot":"205","New Forest":"206","Newark and Sherwood":"207","Newcastle upon Tyne":"208","Newcastle-under-Lyme":"209","Newham":"210","Newport":"211","North Ayrshire":"212","North Devon":"213","North Dorset":"214","North East Derbyshire":"215","North East Lincolnshire":"216","North Hertfordshire":"217","North Kesteven":"218","North Lanarkshire":"219","North Lincolnshire":"220","North Norfolk":"221","North Somerset":"222","North Tyneside":"223","North Warwickshire":"224","North West Leicestershire":"225","Northampton":"226","Northumberland":"227","Norwich":"228","Nottingham":"229","Nuneaton and Bedworth":"230","Oadby and Wigston":"231","Oldham":"232","Orkney Islands":"233","Oxford":"234","Pembrokeshire":"235","Pendle":"236","Perth and Kinross":"237","Peterborough":"238","Plymouth":"239","Poole":"240","Portsmouth":"241","Powys":"242","Preston":"243","Purbeck":"244","Reading":"245","Redbridge":"246","Redcar and Cleveland":"247","Redditch":"248","Reigate and Banstead":"249","Renfrewshire":"250","Rhondda Cynon Taf":"251","Ribble Valley":"252","Richmond upon Thames":"253","Richmondshire":"254","Rochdale":"255","Rochford":"256","Rossendale":"257","Rother":"258","Rotherham":"259","Rugby":"260","Runnymede":"261","Rushcliffe":"262","Rushmoor":"263","Rutland":"264","Ryedale":"265","Salford":"266","Sandwell":"267","Scarborough":"268","Scottish Borders":"269","Sedgemoor":"270","Sefton":"271","Selby":"272","Sevenoaks":"273","Sheffield":"274","Shepway":"275","Shetland Islands":"276","Shropshire":"277","Slough":"278","Solihull":"279","South Ayrshire":"280","South Bucks":"281","South Cambridgeshire":"282","South Derbyshire":"283","South Gloucestershire":"284","South Hams":"285","South Holland":"286","South Kesteven":"287","South Lakeland":"288","South Lanarkshire":"289","South Norfolk":"290","South Northamptonshire":"291","South Oxfordshire":"292","South Ribble":"293","South Somerset":"294","South Staffordshire":"295","South Tyneside":"296","Southampton":"297","Southend-on-Sea":"298","Southwark":"299","Spelthorne":"300","St Albans":"301","St Edmundsbury":"302","St. Helens":"303","Stafford":"304","Staffordshire Moorlands":"305","Stevenage":"306","Stirling":"307","Stockport":"308","Stockton-on-Tees":"309","Stoke-on-Trent":"310","Stratford-on-Avon":"311","Stroud":"312","Suffolk Coastal":"313","Sunderland":"314","Surrey Heath":"315","Sutton":"316","Swale":"317","Swansea":"318","Swindon":"319","Tameside":"320","Tamworth":"321","Tandridge":"322","Taunton Deane":"323","Teignbridge":"324","Telford and Wrekin":"325","Tendring":"326","Test Valley":"327","Tewkesbury":"328","Thanet":"329","Three Rivers":"330","Thurrock":"331","Tonbridge and Malling":"332","Torbay":"333","Torfaen":"334","Torridge":"335","Tower Hamlets":"336","Trafford":"337","Tunbridge Wells":"338","Uttlesford":"339","Vale of Glamorgan":"340","Vale of White Horse":"341","Wakefield":"342","Walsall":"343","Waltham Forest":"344","Wandsworth":"345","Warrington":"346","Warwick":"347","Watford":"348","Waveney":"349","Waverley":"350","Wealden":"351","Wellingborough":"352","Welwyn Hatfield":"353","West Berkshire":"354","West Devon":"355","West Dorset":"356","West Dunbartonshire":"357","West Lancashire":"358","West Lindsey":"359","West Lothian":"360","West Oxfordshire":"361","West Somerset":"362","Westminster":"363","Weymouth and Portland":"364","Wigan":"365","Wiltshire":"366","Winchester":"367","Windsor and Maidenhead":"368","Wirral":"369","Woking":"370","Wokingham":"371","Wolverhampton":"372","Worcester":"373","Worthing":"374","Wrexham":"375","Wychavon":"376","Wycombe":"377","Wyre":"378","Wyre Forest":"379","York":"380","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":"","":""})

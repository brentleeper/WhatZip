# ZipFinder
ZipFinder locates zip codes in the US given coordinate data. Search types include coordinate, radius, and zip code. The result includes the zip code, county, state, and the GEO_JSON for the given zip code/s


Request format examples: GET
  General Format: http://127.0.0.1:5000/<user_token>/<search_type>/<response_format>?[lat=float]&[lon=float]&[radius=int]&[zipcode=xxxxx]
  
  Coordinate: http://127.0.0.1:5000/<user_token>/coordinate/<response_format>?lat=float&lon=float
  
  Radius: http://127.0.0.1:5000/<user_token>/radius/<response_format>?[lat=float]&[lon=float]&[radius=int]
  
  Zipcode: http://127.0.0.1:5000/<user_token>/zipcode/<response_format>?[zipcode=xxxxx]
  
  
Valid path param options:
  <user_token>      - Not currently implemented, pass any string
  <search_type>     - coordinate, radius, zipcode
  <response_format> - json, xml
  
<search_type> required params:
  coordinate:   -90 <= lat:float <= 90, -180 <= lon:float <= 180
  radius:       -90 <= lat:float <= 90, -180 <= lon:float <= 180, radius:int
  zipcode:      zipcode:int:5


Response Example:
 JSON:
 ```json
  {
  "message": "success",
  "request_ip": "127.0.0.1",
  "request_params": {
    "lat": "33.4792232",
    "lon": "-94.0782908",
    "radius": "2"
  },
  "response_code": 200,
  "result_ct": 2,
  "results": [
    {
      "county_name": "Bowie",
      "geo_json": {
        "coordinates": [
          [
            [
              [
                -94.061536,
                33.299821
              ],
              [
                -94.061591,
                33.299867
              ],
                ...
            ]
          ]],
        "type": "MultiPolygon"
      },
      "state_name": "Texas",
      "zipcode": "75501"
    },
    {
      "county_name": "Bowie",
      "geo_json": {
        "coordinates": [
          [
            [
              [
                -94.203221,
                33.474465
              ],
              [
                -94.203493,
                33.469714
              ],
              ...
           ]
        ]],
        "type": "MultiPolygon"
      },
      "state_name": "Texas",
      "zipcode": "75503"
    }
  ],
  "user_token": "asdflkdjsf"
}
```
XML:
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<root>
	<user_token type="str">asdflkdjsf</user_token>
	<response_code type="int">200</response_code>
	<message type="str">success</message>
	<request_ip type="str">127.0.0.1</request_ip>
	<request_params type="dict">
		<lat type="str">33.4792232</lat>
		<lon type="str">-94.0782908</lon>
		<radius type="str">2</radius>
	</request_params>
	<results type="list">
		<item type="dict">
			<zipcode type="str">75501</zipcode>
			<geo_json type="str">
				{&quot;type&quot;:&quot;MultiPolygon&quot;,&quot;coordinates&quot;:[[[[-94.061536,33.299821],[-94.061591,33.299867],...]]]]}
			</geo_json>
			<state_name type="str">Texas</state_name>
			<county_name type="str">Bowie</county_name>
		</item>
		<item type="dict">
			<zipcode type="str">75503</zipcode>
			<geo_json type="str">
				{&quot;type&quot;:&quot;MultiPolygon&quot;,&quot;coordinates&quot;:[[[[-94.203221,33.474465],[-94.203493,33.469714],...]]]]}
			</geo_json>
			<state_name type="str">Texas</state_name>
			<county_name type="str">Bowie</county_name>
		</item>
	</results>
	<result_ct type="int">2</result_ct>
</root>
```

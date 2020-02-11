# jbla
Json to BLender Animation

Example:

```javascript
{
	"Cube": { // name of the element in Blender (for example the default Cube)
		"tween": [ // we create a new tween
			{ // change x position from 0 to 5 in half a second
				"duration": 500,
				"type": "to",
				"props": {
					"x": 5
				}
			},
			{
				"duration": 500,
				"type": "to",
				"props": {
					"y": 5
				}
			},
			{
				"duration": 500,
				"type": "to",
				"props": {
					"z": 5
				}
			},
			{
				"duration": 1000,
				"type": "to",
				"props": {
					"x": 0,
					"y": 0,
					"z": 0
				}
			}
		]
	}
}
```

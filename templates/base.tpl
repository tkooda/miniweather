<!DOCTYPE html>
<html>
<head>
<title>MiniWeather.US{% if city and state and zip %}{{city}}, {{state}}  ({{zip}}){% endif %}</title>
<link rel="icon" href="data:;base64,iVBORw0KGgo=">
</head>
<body>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="/static/zip.js"></script>

<table width="100%">
 <tr>
  <td><a href="/">MiniWeather.US</a> : {% if city and state and zip %}{{city}}, {{state}}  ({{zip}}) : {% endif %}
  <input id="autocomplete" placeholder="Enter a city" onFocus="geolocate()" type="text"></input></td>
  <td align="right">{%if zip %}<a href="http://m.weather.com/weather/tenday/{{zip}}">Ten day forecast</a>{% else %}<a href="https://github.com/tkooda/miniweather">source</a>{% endif %}</td>
</tr>
</table>

{% if message %}
<br/>
  {{ message }}
<br/>
{% endif %}

{% if is_index %}
  {% include 'index_js.tpl' %}
{% endif %}

{% if img_url %}
  {% include 'zip.tpl' %}
{% endif %}

<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCILANmgIcwkai7OlOpUj03Jhp5yRXV48A&libraries=places&callback=initAutocomplete" async defer></script>

</body>
</html>

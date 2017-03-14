// zip.js

var key = 'AIzaSyCILANmgIcwkai7OlOpUj03Jhp5yRXV48A';


function isInteger(n) {
  return !isNaN(parseFloat(n)) && isFinite(n) && parseFloat(n) > 0;
}


// detect carriage return in input field.. -> redirect to /zip/$zip ..
window.onload = function () {
  document.getElementById("autocomplete").onkeydown = function (e) {
    if ( e.keyCode === 13 ) {
      console.log( "RETURN KEY: " + document.getElementById("autocomplete").value );
// FIXME: maybe check for zip here??
      redirect_to_zip_using_address( document.getElementById("autocomplete").value );
      return false;
    }
  }
}



// redirect to /zip/$zip using latitude + longitude ..
function redirect_to_zip_using_latlng( lat, lng ) {
  var url = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + key + '&latlng=' + lat + ',' + lng;
console.log( "url latlng: " + url );
  $.getJSON( url, function( data ) {
console.log( "status: " + data['status'] );
    var zip = 0;
    $.each( data[ 'results' ][ 0 ][ 'address_components' ] , function( key, val ) {
      if ( val[ 'types' ] == 'postal_code' ) {
        zip = val[ 'short_name' ];
        return false; // break
      }
    });
console.log( "latlng redir to zip: " + zip );
    if (zip != 0) {
//window.location.replace( "/zip/" + zip );
      window.location.href = "/zip/" + zip.toString();
      return false;
    } else console.log( "ERROR: zip is zero: " + lat + ", " + lng );
  });
}


// redirect to /zip/$zip using (e.g.) "city, state, country" ..
function redirect_to_zip_using_address( address ) {
  var url = 'https://maps.googleapis.com/maps/api/geocode/json?key=' + key + '&address=' + encodeURIComponent( address );
console.log( "url address: " + url );
  $.getJSON( url, function( data ) {
    console.log( "status: " + data['status'] );
    var lat = data[ 'results' ][ 0 ][ 'geometry' ][ 'location' ][ 'lat' ]; // just guess first response is good?
    var lng = data[ 'results' ][ 0 ][ 'geometry' ][ 'location' ][ 'lng' ];
    redirect_to_zip_using_latlng( lat, lng );
  });
}


// use Google Places API to provide autocomplete..

var placeSearch, autocomplete;
var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};

function initAutocomplete() {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
/** @type {!HTMLInputElement} */(document.getElementById('autocomplete')),
      {types: ['geocode']});
//      {types: ['(cities)']});

  // When the user selects an address from the dropdown, populate the address
  // fields in the form.
  autocomplete.addListener('place_changed', processAddress);
}


function processAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();
//console.log( "place.address_components: " + place.address_components );
  if ( ! place.address_components ) return;
  
  var city = "";
  var state = "";
  var country = "";
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
      var val = place.address_components[i][componentForm[addressType]];
//console.log( addressType + " : " + val );
      if ( addressType == 'locality' ) {
        city = val;
      } else if ( addressType == 'administrative_area_level_1' ) {
        state = val
      } else if ( addressType == 'country' ) {
        country = val
      }
    }
  }

//console.log( "citystatecountry:" + city + ", " + state + ", " + country );
  redirect_to_zip_using_address( city + ", " + state + ", " + country )
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}


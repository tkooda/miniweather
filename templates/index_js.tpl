<script>
   // attempt to get lat/lon from browser geocode, fetch likely zip, and attempt to redir to /zip/* from homepage (presume most visitors want to know about local weather) ..
   if (navigator.geolocation) {
     navigator.geolocation.getCurrentPosition(function(position) {
       redirect_to_zip_using_latlng( position.coords.latitude, position.coords.longitude );
     });
   }
</script>

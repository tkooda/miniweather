#!/usr/bin/python

from flask import Flask
from flask import render_template, request, redirect
import requests
import re
from google.appengine.ext import ndb
from urlparse import parse_qs, urlsplit, urlunsplit, SplitResult
from urllib import urlencode
from datetime import datetime


class Zip( ndb.Model ):
    """Caching for zip code data"""
    img_url = ndb.StringProperty()
    city = ndb.StringProperty()
    state = ndb.StringProperty()
    updated = ndb.DateTimeProperty( required = True, auto_now_add = True )


def hide_thunder( url ):
    ## tweak image display settings..
    url_parts = urlsplit( url ) # parse query from url
    url_query_args = parse_qs( url_parts.query ) # parse our query args
    pcmd_list = list( url_query_args[ "pcmd" ][0] ) # split into list for editing
    pcmd_list[ 9 ] = "0" # disable Thunder display
    url_query_args[ "pcmd" ] = "".join( pcmd_list ) # save it back
    fixed_url = urlunsplit( SplitResult( scheme="",
                                         netloc="",
                                         path = url_parts.path,
                                         query = urlencode( url_query_args, True ),
                                         fragment="" ) ) # re-join url parts
    return fixed_url


def show_snow( url ):
    ## tweak image display settings..
    url_parts = urlsplit( url ) # parse query from url
    url_query_args = parse_qs( url_parts.query ) # parse our query args
    pcmd_list = list( url_query_args[ "pcmd" ][0] ) # split into list for editing
    pcmd_list[ 9 ] = "0" # disable Thunder display
    
    pcmd_list[ 10 ] = "1" # enable Snow display
    pcmd_list[ 11 ] = "1" # enable Snow display
    pcmd_list[ 12 ] = "1" # enable Snow display
    pcmd_list[ 13 ] = "1" # enable Snow display
    
    url_query_args[ "pcmd" ] = "".join( pcmd_list ) # save it back
    fixed_url = urlunsplit( SplitResult( scheme="",
                                         netloc="",
                                         path = url_parts.path,
                                         query = urlencode( url_query_args, True ),
                                         fragment="" ) ) # re-join url parts
    return fixed_url


app = Flask(__name__)

app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def handler_index():
    """Return a friendly HTTP greeting."""
#    return 'Hello miniweather'
    return render_template( "base.tpl", is_index=True )


@app.route('/redir')
def handler_redir():
    """just redirect form GET query to /zip/* GET"""
    return redirect( "/zip/%s" % request.args.get( "zip" ) , code=302 ) # temp redir


@app.route('/zip/<zip>')
def handler_zip( zip ):
    """Return weather forecast for a particular US postal zip code."""
    
    z = Zip.get_by_id( zip )
    
    if not z:
        print "cache miss for zip:", zip
        response = requests.post( "http://forecast.weather.gov/zipcity.php", data={ "inputstring": zip } )
        
        if response.status_code != 200:
            return render_template( "base.tpl", message="sorry, data from weather.gov is temporarily unavailable" ), 404
        
        match = re.search( '<a href="(MapClick.php\?[^"]+)"><img src="newimages/medium/hourlyweather.png"', response.text )
        if not match:
            return render_template( "base.tpl", message="invalid zip code" ), 404
        
        response2 = requests.get( "http://forecast.weather.gov/%s" % match.group( 1 ) )
        if response2.status_code != 200:
            return render_template( "base.tpl", message="sorry, no map data for that zip code" ), 404
        
        match2 = re.search( '<img src="(meteograms/Plotter.php\?[^"]+)"', response2.text )
        if not match2:
            return render_template( "base.tpl", message="sorry, no weather data for that zip code" ), 404
        
        ## tweak image display settings..
        fixed_url = hide_thunder( match2.group( 1 ) )
        
        z = Zip( id = zip, img_url = fixed_url )
        
        vars = parse_qs( urlsplit( response.url ).query )
        print "DEBUG: vars:", vars
        z.state = vars[ "state" ][0]
        z.city  = vars[ "CityName" ][0]
        
        print "caching zip:", z
        z.put()
    
    ## display snow in winter..
    month = int( datetime.now().strftime("%m") )
    if month >= 10 or month <= 3: # winter..
        z.img_url = show_snow( z.img_url )
	
	return render_template( "base.tpl", city = z.city, state = z.state, zip = zip, img_url = z.img_url )


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

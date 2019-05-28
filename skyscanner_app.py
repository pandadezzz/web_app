from flask import Flask, jsonify, render_template, request
import unirest
import json
from datetime import datetime,timedelta
from time import strftime

api_key = '1c3b759866msh08fc8fcca0665b0p1efcfdjsn3fe94d77020c'
refurl = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0"


headers={
	"X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
	"X-RapidAPI-Key": api_key,
	"Content-Type": "application/x-www-form-urlencoded"
}

def create_Range(start_date,end_date):
  #return list of range of date
  st = datetime.strptime(start_date,"%Y-%m-%d")
  et = datetime.strptime(end_date,"%Y-%m-%d")
  days = (et-st).days
  res = [start_date]
  d=st
  for x in range(days):
	d+=timedelta(days=1)
	res.append(d.strftime("%Y-%m-%d"))
	
	return res

#dates
out_date_start = "2019-10-01"
out_date_end = "2019-10-02"

out_range = create_Range(out_date_start,out_date_end)

in_date_start = "2019-11-01"
in_date_end = "2019-11-02"

in_range = create_Range(in_date_start,in_date_end)

#destinations
origin_place = "SFO-sky" 
destination_place = "LHR-sky"


#print range

prices = []

for out_date in out_range:
	for in_date in in_range:
		# params=params
		query= "/US/USD/en-US/"+origin_place+"/"+destination_place+"/"+out_date+"/1"
		
		#optional params
		params={
			"inboundDate": in_date,
			"cabinClass": "economy",
			"children": 0,
			"infants": 0,
			"Country": "US",
			"currency": "USD",
			"locale": "en-US",
			"originPlace": origin_place,
			"destinationPlace": destination_place,
			"outboundDate": out_date,
			"adults": 1
		}

		r_post = unirest.post(refurl,headers=headers,params=params)
		session_id= r_post.headers["Location"].split('/')[-1]
		print out_date,in_date

		response = unirest.get("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/"+session_id+"?pageIndex=0&pageSize=10",
			headers={
			"X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
			"X-RapidAPI-Key": "1c3b759866msh08fc8fcca0665b0p1efcfdjsn3fe94d77020c"
			}
		)
		
		price = [(out_date,in_date),response.body]
		prices.append(price)

		#for x in response.body["Itineraries"]:
		#  print x["PricingOptions"][0]

legs = {}
carriers = {}
agents = {}
places = {}

for p in prices:
	
	#getting leg 
	for leg in p[1]["Legs"]:
		id = leg["Id"]
		legs[id]=leg

	for carrier in p[1]["Carriers"]:
		id = carrier["Id"]
		carrier[id]=carrier
	
	for agent in p[1]["Agents"]:
		id = agent["Id"]
		agents[id]=agent
	
	for place in p[1]["Places"]:
		id = place["Id"]
		places[id]=place
  
  
	day = p[0]
	print(day)
	Itineraries = p[1]["Itineraries"]
	min_price = None
	#in_leg_info,out_leg_info


	for it in Itineraries:
	for pricingOptions in it["PricingOptions"]:
		cur_price = pricingOptions['Price']
		if min_price ==None:
			out_leg_info= it["OutboundLegId"]
			in_leg_info= it["InboundLegId"]
			book_url = pricingOptions["DeeplinkUrl"]
			min_price = cur_price
	  	else:
			if cur_price<min_price:
			#update required
			min_price = cur_price
			out_leg_info= it["OutboundLegId"]
			in_leg_info= it["InboundLegId"]
			book_url = pricingOptions["DeeplinkUrl"]
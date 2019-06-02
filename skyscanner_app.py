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

def get_data(data):
	#return data of flight info given parameters

	out_date_start,out_date_end,in_date_start,in_date_end,origin_place,destination_place=data
	res =[]
	in_range = create_Range(in_date_start,in_date_end)
	out_range = create_Range(out_date_start,out_date_end)
	# print in_range, out_range
	for out_date in out_range:
		for in_date in in_range:
			# making sure return date is after out date
			out_d = datetime.strptime(out_date,"%Y-%m-%d")
			return_d = datetime.strptime(in_date,"%Y-%m-%d")
			if(return_d>out_d):
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
				# print out_date,in_date

				response = unirest.get("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/"+session_id+"?pageIndex=0&pageSize=10",
					headers={
					"X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
					"X-RapidAPI-Key": api_key
					}
				)
				
				day_response = [(out_date,in_date),response.body]
				res.append(day_response)
	return res

def get_cheapest(data):
	#finding the cheapest data given flight data

	legs = {}
	carriers = {}
	agents = {}
	places = {}

	for p in data:
		
		#get leg info. contains flight information like duration, time etc. 
		for leg in p[1]["Legs"]:
			id = leg["Id"]
			legs[id]=leg

		#get carrier info
		for carrier in p[1]["Carriers"]:
			id = carrier["Id"]
			carriers[id]=carrier
		
		#get agent info
		for agent in p[1]["Agents"]:
			id = agent["Id"]
			agents[id]=agent
		
		#get places info
		for place in p[1]["Places"]:
			id = place["Id"]
			places[id]=place
		
		day = p[0]
		print(day)
		Itineraries = p[1]["Itineraries"]
		min_price = None
		out_leg_info,in_leg_info,book_url="","",""

		for it in Itineraries:
			for pricingOptions in it["PricingOptions"]:
				cur_price = pricingOptions['Price']
				if min_price ==None:
					#initilize
					out_leg_id= it["OutboundLegId"]
					in_leg_id= it["InboundLegId"]
					book_url = pricingOptions["DeeplinkUrl"]
					min_price = cur_price
				else:
					if cur_price<min_price:
						#update required
						min_price = cur_price
						out_leg_id= it["OutboundLegId"]
						in_leg_id= it["InboundLegId"]
						book_url = pricingOptions["DeeplinkUrl"]

		#with leg_id we can get flight details
		#get outbound information
		out_carrier_id = legs[out_leg_id]["Carriers"][0]
		# print(carriers)
		out_carrier = carriers[out_carrier_id]["Name"]
		out_departure = legs[out_leg_id]["Departure"]
		out_arrival = legs[out_leg_id]["Arrival"]
		out_carrier_img=carriers[out_carrier_id]["ImageUrl"]

		#get inbound information
		in_carrier_id = legs[in_leg_id]["Carriers"][0]
		in_carrier = carriers[in_carrier_id]["Name"]
		in_departure = legs[in_leg_id]["Departure"]
		in_arrival = legs[in_leg_id]["Arrival"]
		in_carrier_img=carriers[in_carrier_id]["ImageUrl"]

	res = {}

	#genearl info
	res["min_price"]=min_price
	res["book_url"]=book_url

	res["out_carrier"]=out_carrier
	res["out_departure"]=out_departure
	res["out_arrival"]=out_arrival
	res["out_carrier_img"]=out_carrier_img

	res["in_carrier"]=out_arrival
	res["in_departure"]=in_departure
	res["in_arrival"]=in_arrival
	res["in_carrier_img"]=in_carrier_img

	return res
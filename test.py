from skyscanner.skyscanner import Flights

flights_service = Flights('ha177649362715475514428886582394')
result = flights_service.get_result(
    country='UK',
    currency='GBP',
    locale='en-GB',
    originplace='SIN-sky',
    destinationplace='KUL-sky',
    outbounddate='2016-07-28',
    inbounddate='2016-07-31',
    adults=1).parsed

print(result)
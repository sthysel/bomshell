# -*- encoding: utf-8 -*-

"""
All current forecasts, observations, advices and warnings are at:   ftp2.bom.gov.au/anon/gen/fwo/
Current analysis and forecast charts are at:  ftp2.bom.gov.au/anon/gen/difacs/
Current satellite imagery is at:  ftp2.bom.gov.au/anon/gen/gms/
Current radar images are at:  ftp2.bom.gov.au/anon/gen/radar/
An archive of Volcanic Ash Advisories are at:  ftp2.bom.gov.au/anon/gen/vaac/

catalog sits here
http://reg.bom.gov.au/catalogue/data/SMSRPR09.json

Albany Airport
http://www.bom.gov.au/fwo/IDW60801/IDW60801.94802.json

ftp://ftp.bom.gov.au/anon/home/adfd/spatial/
IDM00001 – forecast districts
IDM00003 – marine zones
IDM00004 – rainfall districts
IDM00005 – tropical cyclone service areas
IDM00006 – high seas forecast areas
IDM00007 – fire weather districts
IDM00013 – point places (precis, fire, marine)
IDM00014 – metropolitan and other forecast areas
IDM00015 – ocean wind warning areas
IDR00006 – radar coverage
IDR00007 – radar location
"""

ftp_root = 'ftp://ftp.bom.gov.au/anon/gen/'

sources = {
    'forecast': ftp_root + 'fwo',
    'observation': ftp_root + 'fwo',
    'advice': ftp_root + 'fwo',
    'warning': ftp_root + 'fwo',
    'chart': ftp_root + 'difacs',
    'satellite': ftp_root + 'gms',
    'radar': ftp_root + 'radar',
    'ash': ftp_root + 'vaac',
}

catalog_url = 'http://reg.bom.gov.au/catalogue/data/SMSRPR09.json'

"""
All current forecasts, observations, advices and warnings are at:   ftp2.bom.gov.au/anon/gen/fwo/
Current analysis and forecast charts are at:  ftp2.bom.gov.au/anon/gen/difacs/
Current satellite imagery is at:  ftp2.bom.gov.au/anon/gen/gms/
Current radar images are at:  ftp2.bom.gov.au/anon/gen/radar/
An archive of Volcanic Ash Advisories are at:  ftp2.bom.gov.au/anon/gen/vaac/

catalog sits here
http://reg.bom.gov.au/catalogue/data/SMSRPR09.json
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

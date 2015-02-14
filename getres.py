# -*- coding: utf-8 -*-
import math
import json
import unicodecsv as csv
import urllib
import urllib2

url = "https://rnp.ine.mx/rnp/usuario/buscarProveedor_JsonResult"
data = {
  'searchRfc':'',
  'searchRnpId':'',
  'searchStartDate':'',
  'searchFinishDate':'',
  'searchEntidad':0,
  'startLimit':0,
  'captchaText':'undefined',
}

def get_data(num):
  data['startLimit'] = num
  req_data = urllib.urlencode(data)
  request = urllib2.Request(url, req_data)
  response = urllib2.urlopen(request)
  return response.read()


print "Querying page number..."
db_info =  json.loads(get_data(-1))
total_results = int(db_info['totalResults'])
res_per_page = int(db_info['maxResults'])
total_pages = int(math.ceil(total_results / res_per_page))

print "%d pages found" % total_pages

full_json = []

for i in range(0,total_pages+1):
  print "Querying for page %d..." % i
  req_resp = get_data(i)
  json_resp = json.loads(req_resp)
  for i in range(0,len(json_resp['data'])):
    full_json.append(json_resp['data'][i])

print "Creating csv..."

outfile = csv.writer(open("output.csv", "wb+"))
outfile.writerow(['entidad','estatus','fechaAlta','rfc','razonSocial','estatusSat','rnp'])

for r in full_json:
  outfile.writerow([r['entidad'], r['estatus'], r['fechaAlta'], r['rfc'], r['razonSocial'], r['estatusSat'], r['rnp']])

print "Done"

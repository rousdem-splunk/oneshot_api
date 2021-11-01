import utils
import sys
import urllib
import httplib2
import credentials
import json
import re

baseurl = credentials.baseurl
username = credentials.username
password = credentials.password

# f = open('output-ind.json','w')

myhttp = httplib2.Http(disable_ssl_certificate_validation=True)

try:
#
#  Connect to the Splunk server
#
  cmdurl = '/services/auth/login'

  serverResponse = myhttp.request(baseurl + cmdurl,
                                 'POST', headers={},
    body=urllib.urlencode({'username':username, 'password':password,
                           'output_mode':'json'}))[1]
  parsed_json = json.loads(serverResponse)
  sessionKey = parsed_json['sessionKey']
#
#
#
  cmdurl = '/services/search/jobs'
#
#
#
  searchStr = 'search index=_internal source=*splunkd.log earliest=-1d'

#
#
#
  serverResponse = myhttp.request(baseurl + cmdurl, 'POST',
    headers={'Authorization': 'Splunk %s' % sessionKey},
              body=urllib.urlencode(
                {'output_mode':'json',
                'exec_mode':'oneshot',
                 'search': searchStr,
                 'count':1}))[1]        # rousdem set this to limit results

#  f.write(serverResponse)
  parsed_json = json.loads(serverResponse)

  with open("log.txt", 'w') as f:
    f.write('type = {0}'.format(type(serverResponse)))
    f.write(serverResponse)

  with open("data_file.json", "w") as write_file:
      json.dump(parsed_json, write_file)


#
#
#

  list = parsed_json['results']
#
#
#
  underscore = re.compile('_[a-z]+')
  for result in list:
    print "Result: "
    for field, value in result.items():
      if underscore.match(field) is None:
        print "     ", field, ": ", value
except Exception, err:
    sys.stderr.write('Error: %s\n' % str(err))



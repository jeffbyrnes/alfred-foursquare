#!/usr/bin/env python
# encoding: utf-8

import sys
from workflow import Workflow, web
import codecs
import urllib
from unidecode import unidecode


def main(wf):

    reload(sys)
    sys.setdefaultencoding('utf8')
    query = wf.args[0].encode('utf8')

    try:

        with codecs.open('location', 'r', 'utf-8') as fname:
            location = urllib.quote(unidecode(fname.read()))

    except IOError:
        err = 'Set a location before performing any search.'
        wf.add_item(valid=True, title=err, icon='error.png')
        wf.send_feedback()
        return


    r = web.get('https://api.foursquare.com/v2/venues/explore?client_id=31LH3BDKDYDKSHEUTTMSOL45BU10AEVGEFHA1GXMGJ4ICR1O&client_secret=OESNNGSFQB2KEI2ZJOMSYFDAGGV15XCT2DJSJ4MCIA4AQQRG&v=20160718&near=' + location + '&limit=50&query=' + urllib.quote(query))
    r.raise_for_status()
    data = r.json()
    results = len(data['response']['groups'][0]['items'])
    url_part = query.replace(' ', '-')

    wf.add_item(valid=True, title=query, arg='https://foursquare.com/explore?=' + urllib.quote(query))

    for i in xrange(results):
        name = data['response']['groups'][0]['items'][i]['venue']['name']
        address = data['response']['groups'][0]['items'][i]['venue']['location'].get('address', '(address missing)')
        city = data['response']['groups'][0]['items'][i]['venue']['location'].get('city', '(city missing)')
        state = data['response']['groups'][0]['items'][i]['venue']['location'].get('state', '(state missing)')
        phone = data['response']['groups'][0]['items'][i]['venue']['contact'].get('formattedPhone', 'missing')
        url = 'https://foursquare.com/v/url_part' + '/' + data['response']['groups'][0]['items'][i]['venue']['id']

        wf.add_item(valid=True, title=name, subtitle=address + ', ' + city + ', ' + state + ' | Phone: ' + phone, arg=url)

    wf.send_feedback()

if __name__ == '__main__':

    wf = Workflow()
    sys.exit(wf.run(main))

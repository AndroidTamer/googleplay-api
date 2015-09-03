#!/usr/bin/python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import io

from googleplay import GooglePlayAPI
from helpers import sizeof_fmt

if (len(sys.argv) < 2):
    print("Usage: %s packagename [filename]")
    print("Download an app.")
    print("If filename is not present, will write to '<packagename>_<versioncode>.apk'.")
    sys.exit(0)

packagename = sys.argv[1]

filename = None
if (len(sys.argv) == 3):
    filename = sys.argv[2]

# read config from config.py
config = helpers.read_config()

# connect to GooglePlayStore
api = GooglePlayAPI(config['ANDROID_ID'])
api.login(config['GOOGLE_LOGIN'], config['GOOGLE_PASSWORD'], config['AUTH_TOKEN'])

# Get the version code and the offer type from the app details
m = api.details(packagename)
doc = m.docV2
vc = doc.details.appDetails.versionCode
ot = doc.offer[0].offerType

if filename == None:
    filename = "%s_%s.apk" % (packagename, vc)

# Download
print("Downloading to file %s with size %s..." % (filename, sizeof_fmt(doc.details.appDetails.installationSize)))
data = api.download(packagename, vc, ot)
io.open(filename, "wb").write(data)
print("Done")


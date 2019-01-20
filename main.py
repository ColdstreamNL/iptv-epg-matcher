## needs massive work on the actual stuff it does now, needs cleaning m3u items with some regex and probably some
## common stuff like 1080P, VIP, whatever and probably a phase where it does leveitherm based fixing?

import difflib
import xml.etree.ElementTree as ET
from typing import List

from m3u.channel import Channel
from m3u.m3u import M3u

m3u = M3u()
channels: List[Channel] = m3u.parse('list.m3u')

# Simple XML parsing
tree = ET.parse('xmltv.xml')
root = tree.getroot()

# Simple channel-id grabbing from XML
for channel in root.findall('channel'):
    id = channel.get('id')

# Old code that will need massive changes
# Loop channels and find the best suit
for channel in channels:
    best = {
        'CHANNEL_NAME' : '',
        'percentage' : 0
    }

    for el in root.findall('channel'):
        id = el.get('id')

        # just ignore if don't have more than 3 chars (i'm lazy)
        if len(id) <= 3:
            continue

        # Get similiarity
        percentage = difflib.SequenceMatcher(None, channel.CHANNEL_NAME.lower(), id.lower() ).ratio()

        # If higher than what we have now, save it
        if percentage > best['percentage'] and percentage >= 0.50:
            best['CHANNEL_NAME'] = id
            best['percentage'] = percentage
    
    # overwrite tvg-id and channel-name
    channel.TVG_ID = best['CHANNEL_NAME']
    channel.CHANNEL_NAME = best['CHANNEL_NAME']

# Output
m3u.buildFile(channels, 'list_out.m3u')
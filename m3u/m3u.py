from .channel import Channel
import re

# lets start with the regex a little better
M3U_START_MARKER = "#EXTM3U"
M3U_INFO_MARKER = "#EXTINF:"
DURATION_REGEX = re.compile(".*#EXTINF:(.*?)[ |,].*", re.IGNORECASE)
TVG_ID_REGEX = re.compile(".*tvg-id=\"(.?|.+?)\".*", re.IGNORECASE)
TVG_NAME_REGEX = re.compile(".*tvg-name=\"(.?|.+?)\".*", re.IGNORECASE)
TVG_LOGO_REGEX = re.compile(".*tvg-logo=\"(.?|.+?)\".*", re.IGNORECASE)
GROUP_TITLE_REGEX = re.compile(".*group-title=\"(.?|.+?)\".*", re.IGNORECASE)
CHANNEL_NAME_REGEX = re.compile(".*,(.+?)$", re.IGNORECASE)
# probably compile some regex for channel cleaning?
# example
# TVG_NAME_CLEANER = re.compile("\(\w.+?:\W)\")

class M3u:
    def parse(self, filename):

        channels = []

        # read file line by line
        with open(filename) as file:
            for line in file:

                # if first line, skip it
                if line == M3U_INFO_MARKER: continue

                # if is url, add to last one channel
                if not line.startswith(M3U_INFO_MARKER):
                    if len(channels) == 0: continue

                    last_channel = channels[-1]

                    last_channel.url = line

                # if its channel info line
                else:

                    # Parse major groups
                    DURATION = DURATION_REGEX.search(line)
                    TVG_ID = TVG_ID_REGEX.search(line)
                    TVG_NAME = TVG_NAME_REGEX.search(line)
                    TVG_LOGO = TVG_LOGO_REGEX.search(line)
                    GROUP_TITLE = GROUP_TITLE_REGEX.search(line)
                    CHANNEL_NAME = CHANNEL_NAME_REGEX.search(line)

                    # Add channel instance to array
                    channels.append(Channel(
                        DURATION.group(1),
                        TVG_ID.group(1),
                        TVG_NAME.group(1),
                        TVG_LOGO.group(1),
                        GROUP_TITLE.group(1),
                        CHANNEL_NAME.group(1)
                    ))

                # testing a few things. ignore for now
                # tst1 = channels[-1].CHANNEL_NAME
                # CLEAN_CHANNELNAME = tst1.split('.*?: ')[-1].replace("NL:", '')
                # print(CLEAN_CHANNELNAME)

            return channels

    def buildFile(self, channels, outputFile):

        str = "#EXTM3U\n"

        for channel in channels:

            str += '#EXTINF:-1 tvg-ID="' + channel.tvgId + '" tvg-name="' + channel.tvgName + '" tvg-logo="' + channel.tvgLogo + '" group-title="' + channel.groupTitle + '",' + channel.name + '\n'
            str += channel.url

        with open(outputFile, 'a') as file:
            file.write(str)

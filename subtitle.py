import pysubs2
import os
import io


class Subtitle:
    def __init__(self, subs):
        self.subs = subs

    def generate(self):
        return self.__subtitle()

    def __subtitle(self):
        # load the subtitle ass file
        subs = pysubs2.SSAFile.from_string(self.subs)

        # remove miscellaneous events
        subs.remove_miscellaneous_events()

        # remove styles
        subs.styles.clear()

        new_events = []
        for i, e in enumerate(subs.events):
            # if time now is first than time before
            before = subs.events[i - 1]
            if i > 0 and e.start < subs.events[i - 1].end:
                if len(e.plaintext.strip()) <= 3 and len(before.plaintext.strip()) <= 3:
                    continue

            e.plaintext = e.plaintext.replace("<i>", "").replace("</i>", "")

            new_events.append(e)

        subs.events = new_events

        return subs.to_string(format_="vtt")
        # create temporary open w file
        # with io.BytesIO() as fp:
        #     fp.write(subs.to_string(format_="vtt").encode("utf-8"))
        #     return self.__repair(fp)


if __name__ == "__main__":
    with open("subtitle.ass", "r") as fp:
        subs = Subtitle(fp.read())
        print(subs.generate())

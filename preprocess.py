import re

def preprocess(test_str):
    # eyes = "[8:=;]"
    # nose = "['`\-]?"

    x = re.sub(r"http(s?+)", "", test_str) # Get rid of http because data has it on its own
    x = re.sub(r"(www)?+\w+(com)\S*", "<URL>", x)
    x = re.sub(r"/", " / ", x) # Force splitting words appended with slashes (once we tokenized the URLs, of course)
    x = re.sub(r"u/[A-Za-z0-9_-]+", "<USER>", x) #u/(username) format on Reddit
    # :) smile: (8|:|=|;)('|`|\\|-)*)+
    # (: smile: \(+('|`|\\|-)*(8|:|=|;)
    x = re.sub(r"((8|:|=|;)('|`|\\|-)*)+|\(+('|`|\\|-)*(8|:|=|;)", "<SMILE>", x)
    x = re.sub(r"(8|:|=|;)('|`|\\|-)*p+", "<LOLFACE>", x)
    # :( sad: (8|:|=|;)('|`|\\|-)*)*\(+
    # ): sad: ()+)('|`|\\|-)*)*(8|:|=|;))
    # (8|:|=|;)('|`|\\|-)*\(+
    # \(+('|`|\\|-)*(8|:|=|;)
    x = re.sub(r"((8|:|=|;)('|`|\\|-)*[(]+|()+('|`|\\|-)*(8|:|=|;))", "<SADFACE>", x)
    x = re.sub(r"(8|:|=|;)('|`|\\|-)*(\/|l*)+", "<NEUTRALFACE>", x)
    x = re.sub(r"<3","<HEART>", x)
    x = re.sub(r"[-+]?[.\d]*[\d]+[:,.\d]*/", "<NUMBER>", x)
    x = re.sub(r"([!?.]){2,}/", repeat_sub(x), x) # Mark punctuation repeats
    x = re.sub(r"\b(\S*?)(.)\2{2,}\b", elongate_sub(x), x)

    return x


def repeat_sub(str):
    # Mark punctuation repeats
    repeat = re.findall(r"([!?.]){2,}", str)
    new_str = ""
    for r in repeat:
        new_str += r[0]
    x = re.sub(r"([!?.]){2,}", new_str + " <REPEAT>", str) 
    return x


def elongate_sub(str):
    # Mark elongated words
    repeat = re.split(r"\b(\S*?)(.)\2{2,}\b", str)
    x = re.sub(r"\b(\S*?)(.)\2{2,}\b", repeat[0] + " <ELONG>", str)
    return x

# data has already been .lower()ed
# def downcase_sub(str):
#     return str.lower() + " <ALLCAPS>"
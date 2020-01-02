from flask import Flask, render_template, redirect, json, url_for, request, abort
import datetime
import json
import time

_counter = 0

def AVSystemGetBitString():
    _counter ++ 1
    if (_counter%5 == 0 ):
        return "011"
    return "10"

def MotionSystemGetBitString():
    _counter ++ 1
    if (_counter%5 == 0 ):
        return "0001000"
    return "01000"

def HandsSystemGetBitString():
    _counter ++ 1
    if (_counter%5 == 0 ):
        return "001100"
    return "011"

def LocomotionSystemGetBitString():
    _counter ++ 1
    if (_counter%5 == 0 ):
        return "1001000"
    return "1100"

app = Flask(__name__)

# Returns list of a system's component names or index (int) of color statuses. Parameters must be strings.
def parseJSON(systemType, statusType):
    json_data = json.loads(open("system_status.json").read())
    result = json_data[systemType][statusType]
    if type(result) == int:
        return result
    else:
        for x in range(len(result)):
            result[x] = result[x].encode('ascii', 'ignore')
        return result

jsonTest1 = parseJSON("AudioVisualSystem", "StatusNames")
jsonTest2 = parseJSON("AudioVisualSystem", "StatusGreen")

AVS_STATUS_BITSET_1 = "01"
AVS_STATUS_BITSET_2 = "10100"


# Find current date and time
def now():
    now = datetime.datetime.fromtimestamp(int(time.time())).strftime('%m-%d %H:%M:%S')
    return now

# statusNames: list of a system's components (i.e. camera, microphone, audio for Audiovisual)
# bitSet: a string of ones and zeroes that indicate if a component is working or not.
def parseData(statusNames, bitSet):
    result = []
    index = 0
    if len(statusNames) == len(bitSet):
        for bit in bitSet:
            if bit == '1':
                result.append(statusNames[index])
                index += 1
        result = ', '.join(result)
    else:
        limit = min(len(statusNames), len(bitSet))
        # how many extra errors as a result of the different two parameter lengths
        errorNum = max(len(statusNames), len(bitSet)) - limit
        for bit in bitSet[:limit]:
            if bit == '1':
                result.append(statusNames[index])
            index += 1
        result = ', '.join(result)
        nameLen = "(" + str(len(statusNames)) + ")"
        bitSetLen = "(" + str(len(bitSet)) + ")"
        result += "\nWarning: There is a difference in the lengths of statusNames " + nameLen + " \nand bitSet " + bitSetLen + "."
    return result

# Creates color icon that indicates if a system is working, partially working, or not working at all
def iconColor(greenIndex, yellowIndex, redIndex, bitSet):
    if bitSet[greenIndex] == "1":
        return "material-icons cell statusOK"
    elif bitSet[yellowIndex] == "1":
        return "material-icons cell FuckedButNotTooMuch"
    else:
        return "material-icons cell Fubar"

# Shows last run of a system (timestamp, attributes, optional warning)
def history():
    count = 0
    previousMsg = parseData(systemType, statusType)
    if count == 0:
        return ""
        count += 1
    else:
        return previousMsg

AVS_STATUS_GREEN = parseJSON("AudioVisualSystem", "StatusGreen")
AVS_STATUS_YELLOW = parseJSON("AudioVisualSystem", "StatusYellow")
AVS_STATUS_RED = parseJSON("AudioVisualSystem", "StatusRed")
test1 = parseData(parseJSON("AudioVisualSystem", "StatusNames"), AVS_STATUS_BITSET_1)
test2 = iconColor(AVS_STATUS_GREEN, AVS_STATUS_YELLOW, AVS_STATUS_RED, AVS_STATUS_BITSET_2)
test3 = parseData(parseJSON("AudioVisualSystem", "StatusNames"), AVSystemGetBitString())
test4 = parseData(parseJSON("MotionControlSystem", "StatusNames"), MotionSystemGetBitString())
test5 = iconColor(AVS_STATUS_GREEN, AVS_STATUS_YELLOW, AVS_STATUS_RED, HandsSystemGetBitString())
test6 = iconColor(AVS_STATUS_GREEN, AVS_STATUS_YELLOW, AVS_STATUS_RED, LocomotionSystemGetBitString())

@app.route('/')
def index():
    return render_template('index.html', AVS_STATUS_COLOR=test2, AVS_STATUS_PRINT=now() + " " + test3,
    MOTION_STATUS_COLOR=test2, MOTION_STATUS_PRINT= now() + " " + test4,
    HANDS_STATUS_COLOR=test5, HANDS_STATUS_PRINT=now() + " " + test1,
    LOCOMOTION_STATUS_COLOR=test6, LOCOMOTION_STATUS_PRINT=now() + " " + test1)

if __name__ == "__main__":
    app.run(debug=True)

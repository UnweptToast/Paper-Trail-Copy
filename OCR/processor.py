def isAmountForced(line):
    line = line.strip()
    line = line.replace("$", "")
    line = line.replace(",", "")
    if len(line.split(".")) > 2:
        lines = line.split(".")
        newLine = ""
        for i in range(0,len(lines)-1):
            newLine += lines[i]
        newLine += "."+lines[len(lines)-1]
        line = newLine

    if "." not in line:
        return False
    else:
        nums = line.split(".")
        if len(nums) != 2:
            return False
        elif len(nums[1]) == 2 and nums[1].isdigit() and nums[0].isdigit():
            return True
        else:
            return False
        
def getRawValueForced(num):
    oldNum = num
    num = num.strip()
    num = num.replace("$", "")
    num = num.replace(",", "")
    if len(num.split(".")) > 2:
        lines = num.split(".")
        newLine = ""
        for i in range(0,len(lines)-1):
            newLine += lines[i]
        newLine += ("."+lines[len(lines)-1])
        num = newLine
    return float(num)

def findMax(nums):
    high = nums[0]
    for i in nums:
        if i > high:
            high = i
    return high

def getTotal(lines):
    totals = []
    for i in range(0, len(lines)):
        try:
            index = lines[i].lower().index("total")
            if i < len(lines)-1:
                if isAmountForced(lines[i+1]):
                    totals.append(getRawValueForced(lines[i+1]))
        except:
            continue

    if len(totals) >= 1:
        return findMax(totals)
    else:
        for i in lines:
            if isAmountForced(i):
                # try:
                totals.append(getRawValueForced(i))
                # except:
                #     print("ERRORRR: couldnt convert string to value:", i)
    if len(totals) >= 1:
        return findMax(totals)
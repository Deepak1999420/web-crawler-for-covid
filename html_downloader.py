import requests
country_list = []
continent_list = []
f1 = open("worldometers_countrylist.txt", "rt")        # open country list provided for assignment
f1_content = f1.read()
f1.seek(0)
file_len = len(f1.readlines())  # read lines from given file
count = 0
f1.seek(0)  # seek to 0


def replacer(str1):
    return "-".join(str1.split())      #as hypens are in website urls


for line in f1:
    count = count + 1    # creating data such that can be used in link i.e. refining
    temp1 = line
    line = line[0:len(line)-1:1]
    if line.endswith(":"):
        line = line[0:len(line)-1]
        continent_list.append(line)
    elif line == "Oceania" or line == "Africa" or line == "South America" or line == "Asia":
        continent_list.append(line)
    elif line.endswith("-"):
        print("", end="")
    elif line == "":
        print("", end="")
    else:
        if line == "USA":
            line = "us"
        elif line == "Vietnam":
            line = "viet-nam"
        elif count == file_len:
            line = temp1
        line = replacer(line)
        country_list.append(line)

print("\033[0;35mdownloading main web page\033[0m")
q = requests.get("https://www.worldometers.info/coronavirus/")    # get command for get html page from given url
f2 = open(f"world.html", "w+", errors='ignore')
print(f2.write(q.text))
for i in range(len(country_list)):
    print(f"\033[0;33mdownloading html page of {country_list[i]}\033[0m")                # get command for get html page from given url
    q = requests.get(f"https://www.worldometers.info/coronavirus/country/{country_list[i]}/")
    f2 = open(f"zz{country_list[i]}.html", "w+", errors='ignore')
    print(f2.write(q.text))



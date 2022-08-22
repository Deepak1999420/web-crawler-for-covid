import ply.yacc as yacc
import ply.lex as lex
from datetime import date
import os
f_ptr1 = open("world.html", "r+", errors='ignore')
f_ptr2 = open("21cs60r10_world.txt", "w+", errors='ignore')  #file contain yestarday data
f_ptr3 = open("21cs60r10_logs.txt", "w+", errors='ignore')


'''for i in range(8066):  # <table id="main_table_countries_yesterday" class="table table-bordered table-hover main_table_countries" style="width:100%;margin-top: 0px !important;display:none;">
    f_ptr1.readline()
for i in range(5880):
    f_ptr2.write(f_ptr1.readline())'''


FLAG =0
for l1 in f_ptr1:
    if l1 == '<div class="tab-pane " id="nav-yesterday" role="tabpanel" aria-labelledby="nav-yesterday-tab">\n':
        FLAG = 1
    elif l1 == '<div class="tab-pane " id="nav-yesterday2" role="tabpanel" aria-labelledby="nav-yesterday2-tab">\n':
        FLAG = 0
    if FLAG == 1:
        f_ptr2.write(l1)

t1 = []
continent = {}          # continent data
world = []         # world data
crawl_countries = ['France', 'UK', 'Russia', 'Italy', 'Germany', 'Spain', 'Poland', 'Netherlands', 'Ukraine', 'Belgium', 'us', 'Mexico', 'Canada', 'Cuba', 'Costa-Rica', 'Panama', 'India', 'Turkey', 'Iran', 'Indonesia', 'Philippines', 'Japan', 'Israel', 'Malaysia', 'Thailand', 'viet-nam', 'Iraq', 'Bangladesh', 'Pakistan', 'Brazil', 'Argentina', 'Colombia', 'Peru', 'Chile', 'Bolivia', 'Uruguay', 'Paraguay', 'Venezuela', 'South-Africa', 'Morocco', 'Tunisia', 'Ethiopia', 'Libya', 'Egypt', 'Kenya', 'Zambia', 'Algeria', 'Botswana', 'Nigeria', 'Zimbabwe', 'Australia', 'Fiji', 'Papua-New-Guinea', 'New-Caledonia', 'New-Zealand']
index_countries = ['france', 'uk', 'russia', 'italy', 'germany', 'spain', 'poland', 'netherlands', 'ukraine', 'belgium', 'usa', 'mexico', 'canada', 'cuba', 'costa rica', 'panama', 'india', 'turkey', 'iran', 'indonesia', 'philippines', 'japan', 'israel', 'malaysia', 'thailand', 'vietnam', 'iraq', 'bangladesh', 'pakistan', 'brazil', 'argentina', 'colombia', 'peru', 'chile', 'bolivia', 'uruguay', 'paraguay', 'venezuela', 'south africa', 'morocco', 'tunisia', 'ethiopia', 'libya', 'egypt', 'kenya', 'zambia', 'algeria', 'botswana', 'nigeria', 'zimbabwe', 'australia', 'fiji', 'papua new guinea', 'new caledonia', 'new zealand']
countries_info = {}  # countries data
att1 = []   # for task 2.2
att2 = []
att3 = []
att4 = []
att_uni = []
for i in range(50):
    att_uni.append(t1)
date_wise_data = []         # contain data for task 2.2
date_dict ={}
f_ptr2.close()
tokens = (
    'ONOBR',
    'NAME',
    'CNOBR',
    'OTD',
    'CCLOSE',
    'WORLDOPEN',
    'WORLDCLOSE',
    'CTROPEN',
    'CTRGCLOSE',
    'CTRCLOSE',
    'CTROP',
    'CTRCLS',
    'TACTVCASE',
    'TDAILYDEATH',
    'TNEWCASE',
    'TNEWRCVR',
    'THEEND',

)


def t_ONOBR(t):
    r'<nobr>'
    return t


def t_WORLDOPEN(t):
    r'<td></td>\s<td\sstyle="text-align:left;">World</td>'
    return t


def t_WORLDCLOSE(t):
    r'<td></td>\s<td></td>\s<td></td>\s<td\sstyle="display:none"\sdata-continent="all">All</td>'
    return t


def t_CTROPEN(t):
    r'<td\sstyle="font-weight:\sbold;\sfont-size:15px;\stext-align:left;"><a\sclass="mt_a"\shref="country/[a-zA-Z\-]+/">'
    return t


def t_CTRGCLOSE(t):
    r'<td\sstyle="display:none"'
    return t


def t_CTRCLOSE(t):
    r'</a></td>\n'
    return t


def t_CTROP(t):
    r'<td\sstyle="(f|t)[^>]*>(<a[^>]*>)*'
    return t


def t_CCLOSE(t):
    r'<td></td>'
    return t


def t_OTD(t):
    r'<td>'
    return t


def t_CNOBR(t):
    r'</nobr>\n</td>'
    return t


def t_CTRCLS(t):
    r'(</a>\s)*</td>\n'   #
    return t


def t_TACTVCASE(t):
    r"name:\s'Currently\sInfected'[^\[]*\["
    return t


def t_TDAILYDEATH(t):
    r"name:\s'Daily\sDeaths'[^\[]*\["
    return t


def t_TNEWCASE(t):
    r"name:\s'Daily\sCases'[^\[]*\["
    return t


def t_TNEWRCVR(t):
    r"name:\s'New\sRecoveries'[^\[]*\["
    return t


def t_THEEND(t):
    r'\][\s]+\}'           #
    return t


def t_NAME(t):
    r"[A-Za-z0-9':\.\-()\+,/\0]+"
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    t.lexer.skip(1)


def p_start(t):
    '''start : conti
              | worldd
              | countries
              | actvcase
              | dailydeath
              | newcase
              | newrcvr
             '''


def p_conti(t):
    'conti :  ONOBR pname CNOBR yname CCLOSE'
    t[4] = t[4].replace(" ", "")
    t[4] = t[4].replace("+", "")
    t[4] = t[4].replace(",", "")
    ls = t[4].split(';')
    continent[t[2].lower()] = ls

def p_countries(t):
    'countries : CTROPEN pname CTRCLOSE ctrname CTRGCLOSE'
    t[4] = t[4].replace(" ", "")
    t[4] = t[4].replace("+", "")
    t[4] = t[4].replace(",", "")
    ls = t[4].split(';')
    countries_info[t[2].lower()] = ls

def p_pname(t):
    'pname : NAME'
    t[0] = t[1]


def p_pname_multi(t):
    'pname : NAME pname'
    t[0] = t[1] + ' ' + t[2]


def p_yname(t):
    'yname : OTD pname CTRCLS'
    t[0] = t[2]


def p_multi_yname(t):
    'yname : OTD pname CTRCLS yname'
    t[0] = t[2] + ";" + t[4]


def p_ctrname(t):
    'ctrname : CTROP pname CTRCLS'
    t[0] = t[2]


def p_multi_ctrname(t):
    'ctrname : CTROP pname CTRCLS ctrname'
    t[0] = t[2] + ";" + t[4]


def p_worldd(t):
    'worldd : WORLDOPEN wname WORLDCLOSE'
    strr = t[2]
    strr = strr.replace(" ", "")
    strr = strr.replace("+", "")
    strr = strr.replace(",", "")
    lst = strr.split(';')
    world.append(lst)


def p_wname(t):
    'wname : OTD pname CTRCLS'
    t[0] = t[2]


def p_multi_wname(t):
    'wname : OTD pname CTRCLS wname'
    t[0] = t[2] + ";" + t[4]


def p_actvcase(t):
    'actvcase : TACTVCASE pname THEEND'
    t[0] = t[2]
    t[2] = t[2].replace("+", "")
    t[2] = t[2].replace("-", "")
    t[2] = t[2].replace("null", "0")
    att1.append(t[2].split(','))


def p_dailydeath(t):
    'dailydeath : TDAILYDEATH pname THEEND'
    t[0] = t[2]
    t[2] = t[2].replace("+", "")
    t[2] = t[2].replace("-", "")
    t[2] = t[2].replace("null", "0")
    att2.append(t[2].split(','))


def p_newcase(t):
    'newcase : TNEWCASE pname THEEND'
    t[0] = t[2]
    t[2] = t[2].replace("+", "")
    t[2] = t[2].replace("-", "")
    t[2] = t[2].replace("null", "0")
    att4.append(t[2].split(','))


def p_newrcvr(t):
    'newrcvr : TNEWRCVR pname THEEND'
    t[0] = t[2]
    t[2] = t[2].replace("+", "")
    t[2] = t[2].replace("-", "")
    t[2] = t[2].replace("null", "0")
    att3.append(t[2].split(','))


def p_error(t):
    pass


lexer = lex.lex()
texts = open("21cs60r10_world.txt", "r+", errors='ignore').read()
lexer.input(str(texts))
parser = yacc.yacc()
parser.parse(str(texts))
fair_countries_info = []

for iteM in countries_info.keys():
    iteM.replace("-", " ")
    iteM = iteM.lower()
    if iteM == "us":
        iteM = "usa"
    fair_countries_info.append(iteM)

set1 = set(fair_countries_info)
set2 = set(index_countries)
set3 = set2 - set1
length = 0
length1 = 0
length2 = 0
length3 = 0
country_counter = 0
country_counter1 = 0
graph4_countries = {}
graph1_countries = {}
graph2_countries = {}
graph3_countries = {}
fair_countries = []
fair_countries1 = []
fair_countries2 = []
fair_countries3 = []
for item in crawl_countries:
    print(f" \033[0;35mfetching data from website of -->\033[0;33m {index_countries[country_counter]}...................\033[0m")
    f1 = open(f"zz{item}.html", "r", errors='ignore').read()
    lexer.input(str(f1))
    parser.parse(str(f1))
    if len(att3) == length + 1:
        graph4_countries[index_countries[country_counter]] = att3[length]
        fair_countries.append(index_countries[country_counter])
        length = length + 1
    if len(att2) == length2 + 1:
        graph2_countries[index_countries[country_counter]] = att2[length2]
        fair_countries2.append(index_countries[country_counter])
        length2 = length2 + 1
    if len(att4) == length3 + 1:
        graph3_countries[index_countries[country_counter]] = att4[length3]
        fair_countries3.append(index_countries[country_counter])
        length3 = length3 + 1
    country_counter += 1


att_temp = []
[att_temp.append(x) for x in att1 if x not in att_temp]
for item in index_countries:
    if item == "peru":
        continue
    else:
        graph1_countries[item] = att_temp[country_counter1]
        country_counter1 += 1
        fair_countries1.append(item)



def country_index_finder(arg1):
    counter = -1
    for k in index_countries:
        counter += 1
        if k == arg1:
            return counter
    return 5000


def date_index(arg1):
    dd = int(input(f"Enter {arg1} which day  [numeric values]\n"))
    mm = int(input(f"Enter {arg1} which  month \n"))
    yy = int(input(f"Enter {arg1} which year \n"))
    d1 = date(year=yy, month=mm, day=dd)
    d2 = date(year=2020, month=2, day=15)
    return ((d1 -d2).days)

while(1):
    print("\n\n \033[0;33menter '1' for part1(task 2) ,\033[0;32m'2' for 2nd part[for percentage change and nearest country],\033[0;31m '3' for terminate program \033[0m")
    opt1 = int(input())
    if opt1 == 3:
        break
    if opt1 == 1:
        print("\n\033[0;33menter 1 for world info, \033[0;32m2 for continent , \033[0;31m3 for country info\033[0m")
        semi_opt1 = int(input())
        if semi_opt1 == 2:
            cont_name = str(input("enter the name of continent\n"))
            cont_name = cont_name.lower()
            if cont_name not in list(continent.keys()):
                print("!! write continent spelling correctly for reference")
                print(list(continent.keys()))
                continue
            print(f"total cases --> {continent[cont_name][0]} | new cases --> {continent[cont_name][1]} | total deaths --> {continent[cont_name][2]} | new deaths --> {continent[cont_name][3]} | total recovered --> {continent[cont_name][4]} | new recovered --> {continent[cont_name][5]} | active cases --> {continent[cont_name][6]} | serious cases --> {continent[cont_name][7]} | total case per million --> N/A | deaths per million --> N/A | ")
            f_ptr3.write(f"continent\tAll fields\t\ttotal cases --> {continent[cont_name][0]} | new cases --> {continent[cont_name][1]} | total deaths --> {continent[cont_name][2]} | new deaths --> {continent[cont_name][3]} | total recovered --> {continent[cont_name][4]} | new recovered --> {continent[cont_name][5]} | active cases --> {continent[cont_name][6]} | serious cases --> {continent[cont_name][7]} | total case per million --> N/A | deaths per million --> N/A | \n")
        elif semi_opt1 == 1:
            print(f"total cases --> {world[0][0]} | new cases --> {world[0][1]} | total deaths --> {world[0][2]} | new deaths --> {world[0][3]} | total recovered --> {world[0][4]} | new recovered --> {world[0][5]} | active cases --> {world[0][6]} | serious cases --> {world[0][7]} | total case per million --> {world[0][8]} | deaths per million --> {world[0][9]} | ")
            f_ptr3.write(f"World\t All fields\t\ttotal cases --> {world[0][0]} | new cases --> {world[0][1]} | total deaths --> {world[0][2]} | new deaths --> {world[0][3]} | total recovered --> {world[0][4]} | new recovered --> {world[0][5]} | active cases --> {world[0][6]} | serious cases --> {world[0][7]} | total case per million --> {world[0][8]} | deaths per million --> {world[0][9]} | \n")
        elif semi_opt1 == 3:
                country_name = str(input("enter the name of country \n"))
                country_name = country_name.lower()
                if country_name not in fair_countries_info:
                    print("!!All fields are not provided for this country on website so this part (Task 2.1->countries) not working properly for given countries !!")
                    print(set3)
                    continue
                print(f"total cases --> {countries_info[country_name][0]} | new cases --> {countries_info[country_name][1]} | total deaths --> {countries_info[country_name][2]} | new deaths --> {countries_info[country_name][3]} | total recovered --> {countries_info[country_name][4]} | new recovered --> {countries_info[country_name][5]} | active cases --> {countries_info[country_name][6]} | serious cases --> {countries_info[country_name][7]} | total case per million --> {countries_info[country_name][8]} | deaths per million --> {countries_info[country_name][9]} | total test --> {countries_info[country_name][10]} | test per million --> {countries_info[country_name][11]} | population --> {countries_info[country_name][12]} | ")
                f_ptr3.write(f"Country\t All fields\t\ttotal cases --> {countries_info[country_name][0]} | new cases --> {countries_info[country_name][1]} | total deaths --> {countries_info[country_name][2]} | new deaths --> {countries_info[country_name][3]} | total recovered --> {countries_info[country_name][4]} | new recovered --> {countries_info[country_name][5]} | active cases --> {countries_info[country_name][6]} | serious cases --> {countries_info[country_name][7]} | total case per million --> {countries_info[country_name][8]} | deaths per million --> {countries_info[country_name][9]} | total test --> {countries_info[country_name][10]} | test per million --> {countries_info[country_name][11]} | population --> {countries_info[country_name][12]} | \n")
        else:
            print("Invalid option ):[Try again ]")
    elif opt1 == 2:
        country_name = str(input("Enter the name of country \n"))
        country_name = country_name.lower()
        index_c = country_index_finder(country_name)
        if index_c == 5000:
            print("!! check country spelling or may have space between like (south africa)  try again !! ")
        else:
            choice  = int(input("\033[0;33mEnter '1' for change in active cases, \033[0;32m'2' for change in daily death, \033[0;31m'3' change in new cases ,\033[0;35m '4' change in new recovered cases \033[0m\n"))
            if choice < 1 or choice > 4:
                print("not a valid option ): try again !!")
                continue
            index_d_s = date_index("from")
            index_d_d = date_index("Till")
            if index_d_s < 1 or index_d_d < 1:
                print("date before 16 feb 2020 is not valid ")
            else:
                if choice == 4:
                    if country_name not in fair_countries:
                        print("this graph (Recovered cases) is only available on below mentioned countries website only")
                        print(fair_countries)
                        continue
                    if int(graph4_countries[country_name][index_d_s]) == 0:
                        print("denominator part is 0 so adding 0.001 in it for calculation ")
                    ratio1 = (int(graph4_countries[country_name][index_d_s])-int(graph4_countries[country_name][index_d_d]))/((int(graph4_countries[country_name][index_d_s])) + 0.0001)
                    print(f"% change ---> {ratio1 * -100}")
                    b = "useless"
                    best = 100000000.6
                    ratio2 = 1.1
                    for k in fair_countries:
                        if k == country_name:
                            continue
                        ratio2 = (int(graph4_countries[k][index_d_s])-int(graph4_countries[k][index_d_d]))/((int(graph4_countries[k][index_d_s])) + 0.001)
                        ratio_diff = ratio1 - ratio2
                        if ratio_diff < 0:
                            if best > -1 * ratio_diff:
                                best = -1 * ratio_diff
                                b = k
                        else:
                            if best > ratio_diff:
                                best = ratio_diff
                                b = k

                    print(f"closest country --> {b}")
                    f_ptr3.write(f"Country({country_name})\t[change in recovered cases]\t% change ---> {ratio1 * -100}\n")
                elif choice == 1:
                    if country_name not in fair_countries1:
                        print("this graph is only available for below mentioned countries website only")
                        print(fair_countries1)
                        continue
                    if int(graph1_countries[country_name][index_d_s]) == 0:
                        print("denominator part is 0 so adding 0.001 in it for calculation ")
                    ratio1 = (int(graph1_countries[country_name][index_d_s])-int(graph1_countries[country_name][index_d_d]))/((int(graph1_countries[country_name][index_d_s])) + 0.0001)
                    print(f"% change ---> {ratio1 * -100}")
                    b = "useless"
                    best = 100000000.6
                    ratio2 = 1.1
                    for k in fair_countries1:
                        if k == country_name:
                            continue
                        ratio2 = (int(graph1_countries[k][index_d_s])-int(graph1_countries[k][index_d_d]))/((int(graph1_countries[k][index_d_s])) + 0.001)
                        ratio_diff = ratio1 - ratio2
                        if ratio_diff < 0:
                            if best > -1 * ratio_diff:
                                best = -1 * ratio_diff
                                b = k
                        else:
                            if best > ratio_diff:
                                best = ratio_diff
                                b = k

                    print(f"closest country --> {b}")
                    f_ptr3.write(f"Country({country_name})\t[change in active cases]\t% change ---> {ratio1 * -100}\n")
                elif choice == 2:
                    if country_name not in fair_countries2:
                        print("this graph is only available for below mentioned countries website only")
                        print(fair_countries2)
                        continue
                    if int(graph2_countries[country_name][index_d_s]) == 0:
                        print("denominator part is 0 so adding 0.001 in it for calculation ")
                    ratio1 = (int(graph2_countries[country_name][index_d_s])-int(graph2_countries[country_name][index_d_d]))/((int(graph2_countries[country_name][index_d_s])) + 0.0001)
                    print(f"% change ---> {ratio1 * -100}")
                    b = "useless"
                    best = 100000000.6
                    ratio2 = 1.1
                    for k in fair_countries2:
                        if k == country_name:
                            continue
                        ratio2 = (int(graph2_countries[k][index_d_s])-int(graph2_countries[k][index_d_d]))/((int(graph2_countries[k][index_d_s])) + 0.001)
                        ratio_diff = ratio1 - ratio2
                        if ratio_diff < 0:
                            if best > -1 * ratio_diff:
                                best = -1 * ratio_diff
                                b = k
                        else:
                            if best > ratio_diff:
                                best = ratio_diff
                                b = k

                    print(f"closest country --> {b}")
                    f_ptr3.write(f"Country({country_name})\t[change in daily death ]\t% change ---> {ratio1 * -100}\n")
                else:
                    if country_name not in fair_countries3:
                        print("this graph is only available for below mentioned countries website only")
                        print(fair_countries3)
                        continue
                    if int(graph3_countries[country_name][index_d_s]) == 0:
                        print("denominator part is 0 so adding 0.001 in it for calculation ")
                    ratio1 = (int(graph3_countries[country_name][index_d_s])-int(graph3_countries[country_name][index_d_d]))/((int(graph3_countries[country_name][index_d_s])) + 0.0001)
                    print(f"% change ---> {ratio1 * -100}")
                    b = "useless"
                    best = 100000000.6
                    ratio2 = 1.1
                    for k in fair_countries3:
                        if k == country_name:
                            continue
                        ratio2 = (int(graph3_countries[k][index_d_s])-int(graph3_countries[k][index_d_d]))/((int(graph3_countries[k][index_d_s])) + 0.001)
                        ratio_diff = ratio1 - ratio2
                        if ratio_diff < 0:
                            if best > -1 * ratio_diff:
                                best = -1 * ratio_diff
                                b = k
                        else:
                            if best > ratio_diff:
                                best = ratio_diff
                                b = k

                    print(f"closest country --> {b}")
                    f_ptr3.write(f"Country({country_name})\t[change in new cases]\t% change ---> {ratio1 * -100}\n")
    else :
        print("Invalid option ): [Try again ]")

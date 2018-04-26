import os
import sys
import requests
from bs4 import BeautifulSoup
import re


def parse(soup):

    strings = ""
    terms = ""
    
    web_contents = soup.stripped_strings

    for line in web_contents:
        strings += "\n" + line


    possible_content_dict = {}

    possible_content_dict = {
                    "possible_beginnings" :
                        {
                            "0" : ["Definitions", "Preamble", "Permission to use", "MICROSOFT .NET LIBRARY"], #Declare
                            "1" : ["rights reserved", "License agreement"],  #Ignore
                            "2" : ["License", "license", "Copyright (c)"]
                        },

                    "possible_endings" :
                        {
                            "0" : ["Copy lines", "Copy permalink", "View git blame", "GitHub, Inc", "Jump to Line", "END OF TERMS AND CONDITIONS", \
                                   "extent permitted by applicable law"]
                        },

                    "junk_values" :
                        {
                            "0" : ["Copy lines", "Copy permalink", "View git blame", "GitHub, Inc", "Jump to Line", "Opensource.org"]
                        }
                }
        
    is_copyright = False
    is_terms = False
    is_begin_terms = False

    str_split_dict = {}
    str_split_dict["0"] = strings.splitlines()
    str_split_dict["1"] = strings.split("\n")
    
    for index in str_split_dict:
        
        #For license terms with copyrights!
        for line in str_split_dict[index]:
            
            if line == ".":
                continue
            
            re_exp = re.compile('[Cc][Oo][Pp][Yy][Rr][Ii][Gg][Hh][Tt] (\([Cc@]\)|\w+|[^notice]).*')
            re_exp_junk = re.compile('[Cc][Oo][Pp][Yy][Rr][Ii][Gg][Hh][Tt] \<YEAR\>*')


            #---------------------Beginnning of GitHub----------------------------------------
            if re_exp.search(line) != None or re_exp_junk.search(line) != None:
                if terms == "" and is_copyright == False:
                    is_copyright = True
                    continue
            
            if any(val in line for val in possible_content_dict["possible_beginnings"]["0"]) == True:
                is_begin_terms == True
                terms += str(line)
            elif any(val in line for val in possible_content_dict["possible_beginnings"]["1"]) == True:
                is_begin_terms == True
            elif any(val in line for val in possible_content_dict["possible_beginnings"]["2"]) == True:
                is_begin_terms == True                
            elif any(val in line for val in possible_content_dict["junk_values"]["0"]) == True:
                break
            elif terms != "" and any(val in line for val in possible_content_dict["possible_endings"]["0"]) == True:
                terms += "\n"+str(line)
                break
            else:
                if is_copyright == True or is_begin_terms == True:
                    terms += "\n"+str(line)
                else:
                    continue
            #---------------------End of GitHub------------------------------------------------
      
        #print(terms)
        #------------------------Beginning of single string block----------------------------
        if len(terms) < 50:
            
            if line == ".":
                continue
            
            is_terms = False
            terms = ""
            
            for line in str_split_dict[index]:
                #print(line)
                if re.match('(.*?!)[Ll][Ii][Cc][Ee][Nn][Cc][Ee]$', line) != None:
                    is_terms = True
                    continue
                elif any(val in line for val in possible_content_dict["possible_beginnings"]["0"]) == True:
                    terms += str(line)
                    is_begin_terms = True
                elif is_begin_terms == False and any(val in line for val in possible_content_dict["possible_beginnings"]["1"]) == True:
                    is_begin_terms = True
                elif is_begin_terms == False and any(val in line for val in possible_content_dict["possible_beginnings"]["2"]) == True:
                    is_begin_terms = True    
                elif any(val in line for val in possible_content_dict["junk_values"]["0"]) == True:
                    break
                elif terms != "" and any(val in line for val in possible_content_dict["possible_endings"]["0"]) == True:
                    terms += "\n"+str(line)
                    is_terms == True
                    break
                else:
                    if is_terms == True or is_begin_terms == True:
                        terms += "\n" + str(line)
                    else:
                        continue
        #------------------------End of single string block--------------------------------
        if len(terms) > 400:
            break
        
    print(terms)  
    return True




def main():

    url = input("Enter URL name: ")
    req = requests.get(url)

    soup = BeautifulSoup(req.content,'html.parser')
    
    license_text = parse(soup)
    

  

if __name__ == "__main__":
    main()

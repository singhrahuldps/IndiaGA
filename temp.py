file1 = open('Party List.txt', 'r')
file2 = open('party_list.txt', 'w')
for each in file1:
    file2.write("<option value=\""+each.strip()+"\">"+each.strip()+"</option>\n")
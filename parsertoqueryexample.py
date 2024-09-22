import queryattempt
query = "dance_ability"
operator = ">"
info = 3
query2 = "dance_ability"
operator2 = "<"
info2 = 5
#listqueries = [query, operator, info]
#print(listqueries)
listqueries = [query, operator, info, query2, operator2, info2]


queryattempt.make_query(listqueries) # calls function make_query in queryattempt.py



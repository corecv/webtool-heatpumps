# def cashflows2(oudverbruik, nieuwverbruik,investering):
#     print("###berekening cashflows###")
#     i=0
#     cashflow = []
#     discountedCashFlow = []
#     developmentVerbruik = 0.03  #elk jaar 3% meer verbruik dan het jaar voordien
#     developmentCost = 0.19 #elk jaar stijgt de prijs met 5%
#     kostHuidig = totVerbruikskost(oudverbruik) #initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
#     kostNieuw = totVerbruikskost(nieuwverbruik)

#     onderhoud = 100 #jaarlijkse kost onderhoud
#     cashflow.append(-1*investering)
#     discountedCashFlow.append(-1*investering)
#     while cashflow[i] < 0 or cashflow[i-1] < 0:
#         cashflow.append(cashflow[i] + kostHuidig - kostNieuw - onderhoud)
#         # cashflow[i] = kostHuidig - kostNieuw - onderhoud

#         oudverbruik = {key:value*(1+ developmentVerbruik) for (key,value) in oudverbruik.items()}
#         nieuwverbruik = {key:value*(1+developmentVerbruik) for (key,value) in nieuwverbruik.items()}
#         kostHuidig = totVerbruikskost(oudverbruik) #initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
#         kostNieuw = totVerbruikskost(nieuwverbruik)
#         kostHuidig = kostHuidig*(1+developmentCost)
#         kostNieuw = kostNieuw*(1+developmentCost)
#         discountedCashFlow.append(discountedCashFlow[i-1] + kostHuidig - kostNieuw - onderhoud)   #mogelijks fout: doet hetzelfde als de cashflow lijst 5 lijnen erboven, enkel een plaats verschoven
#         # discountedCashFlow[i] = kostHuidig - kostNieuw - onderhoud   #mogelijks fout: doet hetzelfde als de cashflow lijst 5 lijnen erboven, enkel een plaats verschoven
#         i += 1
#     # print(cashflow)
#     # print(discountedCashFlow)
#     return discountedCashFlow

# # cashtest = cashflows2({"aardgas":20000},{"electriciteit":8000},5000)
# #functie om de cashflow en discounted cashflow(in en output per jaar) voor een bepaalde periode te berekenen.
# def cashflows(oudverbruik, nieuwverbruik,investering):  #de cashflow per jaar berekenen, periode is het aantal jaar. Eerste waarde is het jaar 0 = de investering
#     print("###berekening cashflows###")
#     periode = 100 #jaar
#     cashflow = [None]*periode
#     discountedCashFlow = [None]*periode
#     developmentVerbruik = 0.03  #elk jaar 3% meer verbruik dan het jaar voordien
#     developmentCost = 0.19 #elk jaar stijgt de prijs met 5%
#     kostHuidig = totVerbruikskost(oudverbruik) #initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
#     kostNieuw = totVerbruikskost(nieuwverbruik)

#     onderhoud = 100 #jaarlijkse kost onderhoud
#     cashflow[0] = -1*investering
#     discountedCashFlow[0] = -1*investering
#     for i in range(1,len(cashflow)):
#         cashflow[i] = cashflow[i-1] + kostHuidig - kostNieuw - onderhoud
#         # cashflow[i] = kostHuidig - kostNieuw - onderhoud

#         oudverbruik = {key:value*(1+ developmentVerbruik) for (key,value) in oudverbruik.items()}
#         nieuwverbruik = {key:value*(1+developmentVerbruik) for (key,value) in nieuwverbruik.items()}
#         kostHuidig = totVerbruikskost(oudverbruik) #initieel verbruikskost berekenen van huidige situatie, deze wordt dan geupdate met de percentuele stijging hierboven
#         kostNieuw = totVerbruikskost(nieuwverbruik)
#         kostHuidig = kostHuidig*(1+developmentCost)
#         kostNieuw = kostNieuw*(1+developmentCost)
#         discountedCashFlow[i] = discountedCashFlow[i-1] + kostHuidig - kostNieuw - onderhoud   #mogelijks fout: doet hetzelfde als de cashflow lijst 5 lijnen erboven, enkel een plaats verschoven
#         # discountedCashFlow[i] = kostHuidig - kostNieuw - onderhoud   #mogelijks fout: doet hetzelfde als de cashflow lijst 5 lijnen erboven, enkel een plaats verschoven

#     # print(cashflow)
#     # print(discountedCashFlow)
#     return discountedCashFlow

# #functie berekent de payback periode op basis van de investering en cashflows.       
# def payback_of_investment(investment, cashflows): #payback periode berekenen op basis van investering en cashflow per jaar
#     print("###terugverdientijd berekenen###")
#     """The payback period refers to the length of time required 
#        for an investment to have its initial cost recovered.
       
#        >>> payback_of_investment(200.0, [60.0, 60.0, 70.0, 90.0])
#        3.1111111111111112
#     """
#     print(cashflows)
#     total, years, cumulative = 0.0, 0, []
#     # if not cashflows or (sum(cashflows) < investment):
#     #     raise Exception("insufficient cashflows, did you fill in a negative value for yearly use or cost per kWh?")  #deze error kan ook aageven als het geen interesante investering is, als tvt> x aantal jaar 
#     for cashflow in cashflows:
#         total += cashflow
#         if total < investment:
#             years += 1
#         cumulative.append(total)
#     print("cumul",cumulative)

#     A = years
#     B = investment - cumulative[years-1]
#     C = cumulative[years] - cumulative[years-1]
# #    print(A + round((B/C),3),"years")
#     months = round((B/C)*12)
# #    print(A,"years and",months,"months")
#     return [A,months]

# #roept de payback functie op, deze wordt opgeroepen in de vergelijking
# def payback(cashflows): #functie om de payback periode op te roepen
#     """The payback period refers to the length of time required
#        for an investment to have its initial cost recovered.
       
#        (This version accepts a list of cashflows)
       
#        >>> payback([-200.0, 60.0, 60.0, 70.0, 90.0])
#        3.1111111111111112
#     """
#     investment, cashflow = cashflows[0], cashflows[1:]
#     print(cashflow)
#     if investment < 0 : investment = -investment
#     return payback_of_investment(investment, cashflow)

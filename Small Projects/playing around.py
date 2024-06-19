stats_init = [43,30,55,97,40,65]
stats_new = []

print(sum(stats_init))


for i in range(len(stats_init)):
    stats_new.append(round(stats_init[i] * 500 / sum(stats_init)))

if sum(stats_new) != 500:
    correction_value = 500 - sum(stats_new)
    stats_new[stats_new.index(max(stats_new))] = stats_new[stats_new.index(max(stats_new))] + correction_value
    
    
print(stats_new)
print(sum(stats_new))
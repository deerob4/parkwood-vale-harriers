# Base values arrived at by doing CPH / 80
calories_per_hour = {
	'swimming': {
		'backstroke': 413, # 5.1625
		'breaststroke': 590, # 7.375
		'butterfly': 649, # 8.1125
		'freestyle-slow': 413, # 5.1625
		'freestyle-fast': 590 # 7.375
	},
	'running': {
		'5mph': 472, # 5.9
		'6mph': 590, # 7.375
		'7mph': 679, # 8.4875
		'8mph': 797, # 9.9625
		'9mph': 885, # 11.0625
		'10mph': 944 # 11.8
	},
	'cycling': {
		'leisure': 236, # 2.95
		'gentle': 354, # 4.425
		'moderate': 472, # 5.9
		'vigorous': 590, # 6.125
		'very-fast': 708, # 8.85
		'racing': 944 # 11.8
	}
}

weight = int(input('\nEnter your weight: '))
sport = input('What sport did you do? ')
method = input('What method did you use? ')
hours = int(input('How many hours did you do it for? '))

exam_calories = int(calories_per_hour[sport][method])
base_figure = (exam_calories / 80) * weight
total = base_figure * hours

print('\n{0} calories burnt!\n'.format(total))
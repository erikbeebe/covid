import requests
import sys

if len(sys.argv) < 3:
    print("\nUsage: {} <country> <days>\n".format(sys.argv[0]))
    sys.exit(1)

COUNTRY = sys.argv[1]
DAYS = int(sys.argv[2])

death_source = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
deaths = [z for z in death_source.text.replace('\r','').split('\n') if z.startswith(','+COUNTRY+',')][0].split(',')[-DAYS:]
dates = [z for z in death_source.text.replace('\r','').split('\n')][0].split(',')[-DAYS:]

infection_source = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
infections = [z for z in infection_source.text.replace('\r','').split('\n') if z.startswith(','+COUNTRY+',')][0].split(',')[-DAYS:]

print("{:8} | {:6} | {:7} {:8} | {:11} | {:6} | {:6}  {:6} {:10}".format("Date", "Cases", "(+/-)", "%Incr", "Mortality", "Deaths", "(+/-)", "%Incr", ""))
print("-" * 80)

for i in enumerate(zip(infections, deaths)):
    idx = i[0]

    _infections = int(i[1][0])
    _deaths = int(i[1][1])

    last_infection_count = 0
    last_death_count = 0
    infection_increase = 0
    death_increase = 0
    infection_increase_count = 0
    death_increase_total = 0

    if idx > 0:
        last_infection_count = int(infections[idx-1])
        last_death_count = int(deaths[idx-1])

    if last_infection_count > 0:
        infection_increase = round(_infections/last_infection_count*100-100, 1)
        infection_increase_count = _infections-last_infection_count
    if last_death_count > 0:
        death_increase = round(_deaths/last_death_count*100-100, 1)
        death_increase_total = _deaths-last_death_count

    infection_meter = int((infection_increase/10)) * "="
    death_meter = int((death_increase/10)) * "="

    mortality_rate = round(_deaths/_infections*100, 1)

    print("{:8} | {:6d} | {:7} {:7}% | {:10}% | {:6} | {:6}  {:6}% {:10}".format(dates[idx], _infections, '('+str(infection_increase_count)+')', infection_increase, mortality_rate, deaths[idx], '('+str(death_increase_total)+')', death_increase, death_meter))

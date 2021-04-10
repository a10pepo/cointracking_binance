




from classes import Event
from utils import parse_file,generate_file

events=[]


def main():
    events.extend(parse_file("Files/Trading/"))
    events.extend(parse_file("Files/Deposits/"))
    events.extend(parse_file("Files/Buy/"))
    events.extend(parse_file("Files/Staking/"))
    events.extend(parse_file("Files/Conversions/"))
    events.extend(parse_file("Files/Airdrops/"))
    generate_file(events)

main()

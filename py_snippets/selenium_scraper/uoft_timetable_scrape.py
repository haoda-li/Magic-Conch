import re, requests, csv, argparse


def scrape(path="courses.txt", year="20199"):
    with open(path, "r") as f:
        courses = [line[:-1] for line in f]

    data = {'course': [], 'lecture': [], 'capacity': [], 'size': [], 'waitlist': []}
    f = open("./course_avalibility.csv", "w", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(['course', 'lecture', 'prof', 'avaliable', 'class_size', 'waitlist'])
    for course in courses:
        print("current", course, "       ", end="\r")
        r = requests.get("https://timetable.iit.artsci.utoronto.ca/api/{year}/courses?code={code}".format(year=year, code=course))
        if r.status_code == 200:
            try:
                info = r.json()
                for course_v in info.values():
                    code = course_v['code']
                    for section in course_v['meetings'].values():
                        if section['teachingMethod'] == "LEC":
                            prof = section.get('instructors')
                            if prof:
                                prof = list(prof.values())[0]
                                prof = prof.get("firstName", "") + " " + prof.get("lastName", "")
                            else:
                                prof = "N.A."
                            writer.writerow([code,
                                       section['teachingMethod'] + section['sectionNumber'],
                                       prof,
                                       section.get('enrollmentCapacity', "Cancelled"),
                                       section.get('actualEnrolment', "Cancelled"),
                                       section.get("actualWaitlist", "Cancelled")])
            except Exception as e:
                # print(e)
                continue
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape UofT time table')
    parser.add_argument('-p', help='Give a text file of courses, one course for each line', metavar="path")
    parser.add_argument('-y', help='The scraping year(term) in format of [YEAR][9|5], 9 is regular term, 5 is summer term', metavar="year")
    args = parser.parse_args()
    path = args.p.replace("\\", "/") if args.p else "courses.txt"
    year = args.y if args.y else "20199"
    scrape(path, year)
    
    
    
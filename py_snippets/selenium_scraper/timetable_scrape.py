import re, requests, csv, argparse


def scrape_UT(path="courses.txt", year="20199"):
    with open(path, "r") as f:
        courses = [line[:-1] for line in f]

    f = open("./course_avalibility.csv", "w", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(['course', 'section', 'lecture', 'prof', 'avaliable', 'class_size', 'waitlist'])
    for course in courses:
        print("current", course, "       ", end="\r")
        r = requests.get("https://timetable.iit.artsci.utoronto.ca/api/{year}/courses?code={code}".format(year=year, code=course))
        if r.status_code == 200:
            try:
                info = r.json()
                for course_v in info.values():
                    code = course_v['code']
                    course_section = course_v['section']
                    for section in course_v['meetings'].values():
                        if section['teachingMethod'] == "LEC":
                            prof = section.get('instructors')
                            if prof:
                                prof = list(prof.values())[0]
                                prof = prof.get("firstName", "") + " " + prof.get("lastName", "")
                            else:
                                prof = "N.A."
                            writer.writerow([code,
                                       course_section,
                                       section['teachingMethod'] + section['sectionNumber'],
                                       prof,
                                       section.get('enrollmentCapacity', "Cancelled"),
                                       section.get('actualEnrolment', "Cancelled"),
                                       section.get("actualWaitlist", "Cancelled")])
            except Exception as e:
                # print(e)
                continue
    f.close()
    
def scrape_UWaterloo(path="courses.txt", year="1205"):
    with open(path, "r") as f:
        courses = [line[:-1] for line in f]

    data = {'course': [], 'lecture': [], 'capacity': [], 'size': [], 'waitlist': []}
    f = open("./course_avalibility.csv", "w", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(['course', 'section', 'prof', 'avaliable', 'class_size', 'waitlist'])
    for course in courses:
        subject, number = re.search("[A-Z]+", course)[0], re.search("[0-9]+", course)[0]
        print("current", course, "       ", end="\r")
        r = requests.get(f"https://api.uwaterloo.ca/v2/courses/{subject}/{number}/schedule.json?key={key}&term={year}")
        if r.status_code == 200:
            try:
                info = r.json()['data']
                for course in info:
                    section = course['section']
                    if section[:3] == "LEC" \
                    and len(course['classes']) > 0 \
                    and not course['classes'][0]['date']['is_cancelled']:
                        capacity = course['enrollment_capacity']
                        available = capacity - course['enrollment_total']
                        waitlist = course['waiting_total']
                        class_ = course['classes'][0]
                        prof = "; ".join(class_['instructors'])
                        writer.writerow([f"{subject}{number}",
                                         section,
                                         prof,
                                         available,
                                         capacity, 
                                         waitlist
                                        ])
            except Exception as e:
                print(e, course)
                continue
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape UofT or UWaterloo time table')
    parser.add_argument('-p', help='Give a text file of courses, one course for each line', metavar="path")
    parser.add_argument('-y', help='For UofT: The scraping year(term) in format of [YEAR][9|5], 9 is regular term, 5 is summer term,\nFor Waterloo: the term ID provided from their website', metavar="year")
    parser.add_argument('-u', help='The University, currently UT or UWaterloo', metavar="university")
    parser.add_argument('-k', help="The API key for UWaterloo's API, you can request a key here https://uwaterloo.ca/api/register", metavar="key")
    args = parser.parse_args()
    university = args.u if args.u else "UT"
    path = args.p.replace("\\", "/") if args.p else "courses.txt"
    year = args.y if args.y else "20199"
    if not args.k and university in ["UWaterloo", "UW"]:
        print("Provide a valid API key")
        exit()
    key = args.k
    if university == "UT":
        scrape_UT(path, year)
    elif university == "UWaterloo" or university == "UW":
        scrape_UWaterloo(path, year)
    
    
    
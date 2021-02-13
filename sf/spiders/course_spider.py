"""Define a scrapy spider to crawl course data from stanford website.

Start crawling: scrapy crawl course -O courses.json --nolog
Use && sed '2q;d' to print the first item for easier debugging.
"""
import re
import scrapy


def get_study_area(course_number):
    area_number = int(course_number[1] if len(course_number) > 2 else 0)
    study_area = [
        'Introductory, miscellaneous', 'Hardware Systems',
        'Artificial Language', 'Numerical Analysis', 'Software Systems',
        'Mathematical Foundations of Computing', 'Analysis of Algorithms',
        'Computational Biology and Interdisciplinary Topics', '',
        'Independent Study and Practicum'
    ][area_number]
    return study_area


def get_difficulty(course_number):
    difficulty_number = int(course_number[0]) if len(course_number) > 2 else 0
    difficulty = [
        'service', 'basic undergraduate', 'advanced undergraduate',
        'advanced graduate', 'experimental', 'graduate seminars'
    ][difficulty_number]
    return difficulty


class CourseSpider(scrapy.Spider):
    name = "course"
    start_urls = [
        "https://explorecourses.stanford.edu/print?filter-catalognumber-CS=on\
    &filter-departmentcode-CS=on\
    &filter-coursestatus-Active=on&filter-catalognumber-CS=on\
    &q=CS&descriptions=on"
    ]

    def parse(self, response):
        for course in response.css('div.searchResult'):
            code = re.sub(r'[: ]', '',
                          course.css('span.courseNumber::text').get())
            number = re.findall(r'\d+', code)[0]
            yield {
                'code': code,
                'area': get_study_area(number),
                'difficulty': get_difficulty(number),
                'title': course.css('span.courseTitle::text').get(),
                'description': course.css('div.courseDescription::text').get()
            }
            #yield {'title': title, 'descriptions': descriptions, 'code': code}

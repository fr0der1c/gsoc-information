import requests
import csv
from bs4 import BeautifulSoup

url = 'https://summerofcode.withgoogle.com/archive/2017/organizations/'
root_domain = 'https://summerofcode.withgoogle.com'
header_info = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate'
}

s = requests.session()
request = s.get(url=url, headers=header_info)


def list2str(lst):
    string = ''
    for each in lst:
        string += each + ','
    return string[:len(string) - 1]


soup = BeautifulSoup(request.content, 'html.parser')
selector = 'a[class="organization-card__link"]'

with open('GSoC 2017 organizations.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Organization name', 'Category', 'Description', 'Technologies', 'Topics', 'Link'])

    for i in soup.select(selector):
        href = i['href']
        org_id = href[-17:-1]
        href = root_domain + href
        org_name = i.select('h4')[0].string
        org_description = i.select('.organization-card__tagline')[0].string
        print(org_id, href, org_name, org_description)

        # get sub page
        request2 = s.get(url=href, headers=header_info)
        soup2 = BeautifulSoup(request2.content, 'html.parser')
        headings = soup2.select('.org__meta-heading')

        technologies = [each.string for each in headings[0].find_next_sibling('ul').find_all('li')]
        # print(technologies)

        topics = [each.string for each in headings[1].find_next_sibling('ul').find_all('li')]
        topics.pop(0)
        # print(topics)

        category = headings[1].find_next_sibling('ul').find('li').find('a').string
        # print(category)

        writer.writerow([org_name,
                         category,
                         org_description,
                         list2str(technologies),
                         list2str(topics),
                         href])

    print('Finished.')

from bs4 import BeautifulSoup


with open("test.html", "r") as file:
    content = file.read()
    soup = BeautifulSoup(content, "lxml")

    link_tags = soup.find_all("a")

    for tag in link_tags:
        print(tag.text)

from requests_html import HTMLSession, HTML

class Topic:

    def __init__(self, title: str, author: str, url: str, base_url: str, session: HTMLSession):
        self.title = title
        self.author = author
        self.url = url
        self.base_url = base_url
        self.session = session

    def setPage(self, page: int) -> None:
        """
        Set the page of the topic
        """
        url_list = self.url.split("-")
        url_list[3] = str(page)
        self.url = "-".join(url_list)

    def getMessages(self, page: int) -> list:
        """
        Get the messages of a topic
        """
        self.setPage(page)
        content = self.session.get(self.base_url + self.url).html

        messages = []
        for bloc_message in content.find(".bloc-message-forum"):
            bloc_message_html = HTML(html=bloc_message.html)

            for bloc_pseudo in bloc_message_html.find(".bloc-pseudo-msg"):
                author = bloc_pseudo.text

            for bloc_contenu in bloc_message_html.find(".bloc-contenu"):
                content = bloc_contenu.text

            for bloc_date in bloc_message_html.find(".bloc-date-msg"):
                date = bloc_date.text

            messages.append(Message(author, content, date))

        return messages

    def sendMessage(self, message: str):
        """
        Post a message on a topic
        """
        url = self.base_url + self.url
        content = self.session.get(url).html
        form_html = HTML(html=content.find(".js-form-session-data", first=True).html)
        inputTags = form_html.find("input")
        headers = {
            "fs_session": inputTags[0].attrs["value"],
            "fs_timestamp":  inputTags[1].attrs["value"],
            "fs_version":  inputTags[2].attrs["value"],
            inputTags[3].attrs["name"]: inputTags[3].attrs["value"],
            "g_recaptcha_response": "",
            "form_alias_rang": "1",

            "message_topic": message
        }

        post = self.session.post(url, data=headers).text
        post_html = HTML(html=post)

        if post_html.find(".alert", first=True):
                return False

        return True

    def getPages(self) -> int:
        """
        Get the number of pages of a topic
        """
        content = self.session.get(self.base_url + self.url).html.find(".bloc-liste-num-page", first=True).text
        try:
            return int(content.split(" ")[1].replace("»", "").replace(".", ""))
        except IndexError:
            return 1

    def getOnlines(self) -> int:
        """
        Get the number of people on a topic
        """
        content = self.session.get(self.base_url + self.url).html.find(".nb-connect-fofo", first=True).text
        return content.split(" ")[0]

class Message:

    def __init__(self, author: str, message: str, date: str):
        self.author = author
        self.message = message
        self.date = date

class JVC:

    BASE_URL = 0
    BASE_URL_FORUM = 1
    FORUM_1825 = 2
    PM_URL = 3

    BASE_URLS = {
        BASE_URL: "https://www.jeuxvideo.com",
        BASE_URL_FORUM: "https://www.jeuxvideo.com/forums/",
        FORUM_1825: "https://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm",
        PM_URL: "https://www.jeuxvideo.com/messages-prives/nouveau.php"
    }

    def __init__(self, cookie: str, forum: int):
        self.cookie = cookie
        self.base_url = self.BASE_URLS[forum]

        self.session = HTMLSession()
        self.session.cookies.update({
            "coniunctio": self.cookie
        })

    def getTopics(self, page: int) -> list:
        """
        Get a list of the topics
        """
        url_list = self.base_url.split("-")
        url_list[5] = str((page-1)*25 + 1)
        url = "-".join(url_list)

        topics = []
        for element in self.session.get(url).html.find("li"):
            if "data-id" in element.attrs:
                element_html = HTML(html=element.html)
                title = element_html.find(".topic-title", first=True).text
                author = element_html.find(".topic-author", first=True).text
                url = next(iter(element_html.find(".lien-jv", first=True).links))

                topics.append(Topic(title, author, url, self.BASE_URLS[self.BASE_URL], self.session))

        return topics

    def getTopic(self, url: str) -> Topic:
        """
        Get a topic by its url
        """
        base_url = self.BASE_URLS[self.BASE_URL_FORUM]
        content = self.session.get(base_url + url).html
        title = content.find("#bloc-title-forum", first=True).text
        author = content.find(".bloc-pseudo-msg", first=True).text

        return Topic(title, author, url, base_url, self.session)

    def createTopic(self, title: str, message: str) -> bool:
        """
        Create a topic and returns a Topic
        To implement: polls
        """
        content = self.session.get(self.base_url).html
        form_html = HTML(html=content.find(".js-form-session-data", first=True).html)
        inputTags = form_html.find("input")
        headers = {
            "fs_session": inputTags[0].attrs["value"],
            "fs_timestamp":  inputTags[1].attrs["value"],
            "fs_version":  inputTags[2].attrs["value"],
            inputTags[3].attrs["name"]: inputTags[3].attrs["value"],
            "g_recaptcha_response": "",
            "form_alias_rang": "1",

            "titre_topic": title,
            "message_topic": message
        }

        post = self.session.post(self.base_url, data=headers).text
        post_html = HTML(html=post)

        if post_html.find(".alert", first=True):
                return False

        return True

    def sendMessage(self, participants: list, title: str, message: str):
        """
        Send a message to the participants
        """
        url = self.BASE_URLS[self.PM_URL]
        content = self.session.get(url).html
        form_html = HTML(html=content.find(".js-form-session-data", first=True).html)
        inputTags = form_html.find("input")
        headers = {
            "fs_session": inputTags[0].attrs["value"],
            "fs_timestamp":  inputTags[1].attrs["value"],
            "fs_version":  inputTags[2].attrs["value"],
            inputTags[3].attrs["name"]: inputTags[3].attrs["value"],
            "g_recaptcha_response": "",
            "form_alias_rang": "1",

            "conv_titre": title,
            "message": message
        }
        for participant in participants:
            headers["participants[" + participant + "]"] = participant

        post = self.session.post(url, data=headers).text
        post_html = HTML(html=post)

        if post_html.find(".alert", first=True):
                return False

        return True

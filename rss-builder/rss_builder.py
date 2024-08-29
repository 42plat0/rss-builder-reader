import xml.etree.ElementTree as ET

class RSS:
    def __init__(self, **kwargs):
        self.rss_content = kwargs

    def __add_children(self, item, content):

        for tag in content:
            if type(content[tag]) is list:
                categories = content[tag]
                for category_name in categories:
                    category = ET.SubElement(item, 'category')
                    category.text = category_name
                continue
            item_element = ET.SubElement(item, tag)
            item_element.text = content[tag]

        return item


    def __create_xml(self):
        tree = ET.Element("rss")

        channel = ET.SubElement(tree, "channel")

        for tag in self.rss_content:
            content = self.rss_content[tag]
            if content is not None:
                if type(content) is list and len(content) > 0:
                    for iterable_content in content:
                        if type(iterable_content) is dict: # Means that its items:
                            item = ET.SubElement(channel, 'item')
                            self.__add_children(item, iterable_content)

                        elif type(iterable_content) is str:
                            category_name = iterable_content

                            category = ET.SubElement(channel, 'category')
                            category.text = category_name
                else:
                    element = ET.SubElement(channel, tag)
                    element.text = content

        return ET.tostring(tree)
    
    def build(self):
        return self.__create_xml()

'''    
    usage:
    
        rss = RSS(
            title='Dummy', 
            description='Dummy Description', 
            link='https://dummy.com', 
            category=["Newspapers", "Some random category"], 
            copyright=None, 
            docs=None, 
            pubDate=None, 
            rating=None, 
            skipDays=None, 
            skipHours=None, 
            textInput=None, 
            ttl=None, 
            webMaster=None, 
            items=[
                {
                    "title": "Some title",
                    "link": "https://some-link.com/path",
                    "description": "Some description",
                    "category": ["one category", "other category"]
                }
            ]
        ) 
'''



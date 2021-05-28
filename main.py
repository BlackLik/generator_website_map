from xml.etree.ElementTree import VERSION
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import requests
import time, datetime
import os


def ask_for_url():
    global url
    url =  input('Напиши свой домен: ') # "http://crawler-test.com/" https://www.google.com/ https://vk.com/ https://yandex.ru/
    
    global response
    cheching = url[-1]
    
    try:
        if cheching != "/":
            url += "/"
        response = requests.get(url)
        start_crawling()
    except:
        print("Не вереный домен. Пример домена: https://www.google.com/")


def start_crawling():
    #os.system('cls')
    print('Ищу')
    global checked_links
    checked_links = []
    global more_repead_links
    more_repead_links = []
    checked_links.append(url)
    crawling_web_pages()


def crawling_web_pages():
    global response
    global more_repead_links
    # Если надо более продвинутый, то надо поменять for на while, но тогда некоторые ссылки могут не корректно отображаться
    #control = 0
    #while control < len(checked_links):
    for control in range(len(checked_links)):
        try:
            response = requests.get(checked_links[control])
            source_code = response.text
            soup = BeautifulSoup(source_code, 'html.parser')
            new_links = [w.get('href') for w in soup.find_all('a')]
            for counter in range(len(new_links)):
                # Проверка на протокол
                if 'http' not in new_links[counter] or 'https' not in new_links[counter]:
                    # Создание харатекристик для каждой ссылки
                    verify = new_links[counter][0]
                    if verify == '/':
                        new_links[counter] = new_links[counter][:1].replace('/', '') + new_links[counter][1:]
                        
                    # Вхожденя домена на релетивные ссылки
                    new_links[counter] = url + new_links[counter]
            for counter in range(len(new_links)):
                # Расскоментировать если надо использовать while
                """root_now = new_links[counter].split('/')
                page_now = str(root_now[-1])
                root_now = root_now[:-1]
                u = new_links[counter].replace(page_now, '')
                print(new_links)"""
                # Фильтрация
                #u                   not in more_repead_links   and 
                if  '#'                 not in new_links[counter]   and \
                    '.jpg'              not in new_links[counter]   and \
                    '.pdf'              not in new_links[counter]   and \
                    new_links[counter]  not in checked_links        and \
                    '/'.join(new_links[counter].split('/')[:-1])  not in more_repead_links    and \
                    new_links[counter].startswith(url):
                        
                        if counter > 0:
                            root_last = new_links[counter-1].split('/')
                            page_last = str(root_last[-1])
                            name_page_last = page_last.split('?')[0]
                            root_last = root_last[:-1]

                            root_now = new_links[counter].split('/')
                            page_now = str(root_now[-1])
                            name_page_now = page_now.split('?')[0]
                            root_now = root_now[:-1]
                            """if root_last == root_now and len(name_page_last) == len(name_page_now):
                                u = new_links[counter].replace(page_now, '')
                                more_repead_links.append(u)
                                break"""
                            
                            checked_links.append(new_links[counter])
                            os.system('cls')
                            print(str(control)+' / '+str(len(checked_links)))
                            print(str(control)+" Ползает по вебсайту & "+str(len(checked_links))+' страниц сайтов найдено')
                            # Корретный url
                            print(new_links[counter])
                        else:
                            # Создание харатекристик для каждой ссылки
                            checked_links.append(new_links[counter])
                            os.system('cls')
                            print(str(control)+' / '+str(len(checked_links)))
                            print(str(control)+" Ползает по вебсайту & "+str(len(checked_links))+' страниц сайтов найдено')
                            # Корретный url
                            print(new_links[counter])
            
            # Расскоментировать если надо использовать while
            #control += 1
            #os.system('cls')
            #print(str(control)+' / '+str(len(checked_links)))
            #print(str(control)+" Ползает по вебсайту & "+str(len(checked_links))+' страниц сайтов надено')
            # Корретный url
            #print(checked_links[control])
        except:
            #control += 1
            #print(control)
            pass
    
    creating_sitemap()


def creating_sitemap():
    os.system('cls')
    print('Все страницы найдены.\nСоздаю файл')
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for link in range(len(checked_links)):
        urls = ET.SubElement(urlset, 'url')
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        ET.SubElement(urls, 'loc').text = str(checked_links[link])
        ET.SubElement(urls, 'lastmod').text = str(today)
        count_prior = str(checked_links[link]).split('/')[3:]
        prior = round((1.0 - float(len(count_prior))*0.2 + 0.2), 2)
        if prior < .1:
            prior = .1
        ET.SubElement(urls, 'priority').text = str(prior)
    tree = ET.ElementTree(urlset)
    indent(urlset)
    site_name = url.split('/')[2]
    tree.write(site_name+'.xml', encoding="UTF-8", xml_declaration=True)
    print('Всего ссылок найдено %s' % str(len(checked_links)))
    print("Я создал карту сайта :D")


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == "__main__":
    start = time.time()
    ask_for_url()
    print("Работала {:.2f} секунд".format(time.time() - start))


from bs4 import BeautifulSoup
import codecs
import requests
import os
from unidecode import unidecode
import csv


# ------------------------------page_counter---------------------------------------
def page_counter(min_price='1', max_price='144040000'):
    page_counts = 0
    for x in range(20):
        url = f'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?price[min]={min_price}&' \
              f'price[max]={max_price}&pageno={x}&sortby=20 '
        site = requests.get(url)
        soup = BeautifulSoup(site.text, 'lxml')
        page_content = soup.find('div', id='content').find('ul', class_='c-listing__items js-plp-products-list')
        try:
            if page_content.div.div.div.p.text == 'جستجو برای این ترکیب از فیلترها با هیچ کالایی هم‌خوانی نداشت.':
                break
        except:
            page_counts += 1
    return page_counts - 1


# ------------------------------Get_links---------------------------------------

path = os.getcwd().replace('/', '\\')
file_path = str(path + '\\links.txt')
if not os.path.exists(file_path):
    create_io = codecs.open(file_path, "x", 'utf-8')
    create_io.close()
io = codecs.open(file_path, 'w', 'utf-8')

laptop_links = []


def get_links(min_price='1', max_price='144040000', page_num='1'):
    global laptop_links
    url = f'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?' \
          f'price[min]={min_price}&price[max]={max_price}&pageno={page_num}&sortby=20'
    web_site_loader = requests.get(url)
    soup_loader = BeautifulSoup(web_site_loader.text, 'lxml')
    site_table = soup_loader.find('ul', class_='c-listing__items js-plp-products-list')
    site_laptops = site_table.find_all('li')
    for item in site_laptops:
        try:
            laptop_link = 'https://www.digikala.com' + item.div.a.attrs['href']
            laptop_links.append(laptop_link)
            io.write(laptop_link)
            io.write('\n')
        except:
            pass
    io.close()


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def replace_p_to_en(st: str, li_p: list, li_e: list):
    for item in li_p:
        if item in st:
            index = li_p.index(item)
            new_string = st.replace(item, li_e[index])
            return new_string


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


path_csv = os.getcwd().replace('/', '\\')
file_path_csv = str(path_csv + '\\information.csv')
if not os.path.exists(file_path_csv):
    create_io_csv = codecs.open(file_path_csv, "x", 'utf-8')
    csv_writer = csv.writer(create_io_csv, delimiter=',')
    csv_writer.writerow(['Name', 'CPU', 'Ram', 'GPU', 'Weight', 'Screen', 'Price', 'Link'])
    create_io_csv.close()


def info_writer(laptop_link, laptop_name, laptop_cpu, laptop_ram, laptop_graphic, laptop_weight, laptop_screen,
                laptop_price):
    path = os.getcwd().replace('/', '\\')
    file_path = str(path + '\\information.txt')
    if not os.path.exists(file_path):
        create_io = codecs.open(file_path, "x", 'utf-8')
        create_io.close()
    with codecs.open(file_path, 'a', 'utf-8') as io:
        io.write(f'-----{laptop_name}-----\n')
        io.write(f'CPU: {laptop_cpu}\n')
        io.write(f'Ram: {laptop_ram}\n')
        io.write(f'GPU: {laptop_graphic}\n')
        io.write(f'Weight: {laptop_weight}\n')
        io.write(f'Screen: {laptop_screen}\n\n')
        io.write(f'Price: {laptop_price}\n\n')
        io.write(f'Link: {laptop_link}\n')
        io.write('--------------------\n\n\n\n')
        io.close()
    csv_path = os.getcwd().replace('/', '\\')
    csv_file_path = str(csv_path + '\\information.csv')
    with codecs.open(csv_file_path, 'a', 'utf-8') as io_csv:
        writer_csv = csv.writer(io_csv, delimiter=',')
        writer_csv.writerow(
            [laptop_name, laptop_cpu, laptop_ram, laptop_graphic, laptop_weight, laptop_screen, laptop_price,
             laptop_link])
        io_csv.close()


# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
def get_info(address):
    global laptop_price
    site = requests.get(address)
    soup = BeautifulSoup(site.text, 'lxml')
    page_content = soup.find('div', id='content')
    table = page_content.find('div', id='tabs').find('div', class_='c-box c-box--tabs p-tabs__content'). \
        find('div', class_='c-params').article
    # ---------------------------------laptop_name------------------------------------------
    try:
        laptop_name = page_content.find('div', class_='o-page c-product-page').find('h1', class_='c-product__title') \
            .text.strip()
    except:
        laptop_name = 'None'
    # -------------------------------------laptop_weight----------------------------------------
    try:
        laptop_weight = table.find_all('section')[0].find_all('li')[1].find('div',
                                                                            class_='c-params__list-value').text.strip()
        laptop_weight = replace_p_to_en(laptop_weight, ['کیلوگرم', 'گرم'], ['Kg', 'g'])
    except:
        laptop_weight = 'None'
    # ---------------------------------------laptop_cpu------------------------------------------
    try:
        laptop_cpu_comp = table.find_all('section')[1].find_all('li')[0] \
            .find('div', class_='c-params__list-value').find('a', class_='btn-link-spoiler js-wiki-link').text.strip()
    except:
        laptop_cpu_comp = 'None'
    try:
        laptop_cpu_seri = table.find_all('section')[1].find_all('li')[1]. \
            find('div', class_='c-params__list-value').text.strip()
    except:
        laptop_cpu_seri = 'None'
    try:
        laptop_cpu_model = table.find_all('section')[1].find_all('li')[2].find('div',
                                                                               class_='c-params__list-value').text.strip()
    except:
        laptop_cpu_model = 'None'
    laptop_cpu = laptop_cpu_comp + '-' + laptop_cpu_seri + '-' + laptop_cpu_model
    # ------------------------------------------laptop_ram------------------------------------
    try:
        laptop_ram = table.find_all('section')[2].find_all('li')[0]. \
                         find('div', class_='c-params__list-value').text.strip() + ' - ' + \
                         table.find_all('section')[2].find_all('li')[1].\
                         find('div', class_='c-params__list-value').text.strip()
    except:
        laptop_ram = 'None'
    laptop_ram = replace_p_to_en(laptop_ram, ['گیگابایت'], ['GB'])
    # ------------------------------------------laptop_disk---------------------------------------
    try:
        laptop_disk_space = table.find_all('section')[3].find_all('li')[1].\
            find('div', class_='c-params__list-value').text.strip()
    except:
        laptop_disk_space = 'None'
    laptop_disk_space = replace_p_to_en(laptop_disk_space,
                                        ['هارد دیسک', 'یک ترابایت', 'دو ترابایت', 'سه ترابایت', 'چهار ترابایت'],
                                        ['HDD', '1 TB', '2 TB', '3 TB', '4 TB'])
    try:
        laptop_disk = table.find_all('section')[3].find_all('li')[0].\
                          find('div', class_='c-params__list-value').text.strip() + ' - ' + laptop_disk_space
    except:
        laptop_disk = 'None'
    laptop_disk = replace_p_to_en(laptop_disk, ['هارد دیسک', 'یک ترابایت', 'دو ترابایت', 'سه ترابایت', 'چهار ترابایت'],
                                  ['HDD', '1 TB', '2 TB', '3 TB', '4 TB'])

    # -------------------------------------------laptop_graphic-------------------------------------
    try:
        laptop_graphic = table.find_all('section')[4].find_all('li')[0].\
                             find('div', class_='c-params__list-value').text.strip() + ' - ' + \
                             table.find_all('section')[4].find_all('li')[1].\
                             find('div', class_='c-params__list-value').text.strip() + '-' + \
                             table.find_all('section')[4].find_all('li')[2].\
                             find('div', class_='c-params__list-value').text.strip()
    except:
        laptop_graphic = 'None'
    # ------------------------------------------------laptop_screen--------------------------------
    try:
        laptop_screen = table.find_all('section')[5].find_all('li')[0].find('div',
                                                                            class_='c-params__list-value').text.strip()
    except:
        laptop_screen = 'None'
    laptop_screen = replace_p_to_en(laptop_screen, ['اینچ'], ['Inch'])
    # ------------------------------------------------laptop_price--------------------------------

    try:
        laptop_price = page_content.find('div', class_='c-product__seller-price-pure js-price-value').text.strip()
        laptop_price = unidecode(laptop_price)
    except:
        pass
    info_writer(address, laptop_name, laptop_cpu, laptop_ram, laptop_graphic, laptop_weight, laptop_screen,
                laptop_price)


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


minimum_price = input('Enter minimum price(default = 0)')
maximum_price = input('Enter maximum price(default = 144040000)')
pages = page_counter(minimum_price, maximum_price)
print(pages, 'pages were found')
for page in range(pages):
    try:
        get_links(minimum_price, maximum_price, str(page + 1))
    except:
        pass
print(len(laptop_links), 'links found')
print('analysing........')
for link in laptop_links:
    get_info(link)
    index = laptop_links.index(link) + 1
    print(str(index) + ' of ' + str(len(laptop_links)) + ' completed.')
laptop_links.clear()

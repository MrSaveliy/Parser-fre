from parse_kapitalkz import get_source
from parse_kapitalkz import get_source_nex


import time


# print('Ввидите имя или компанию для парса')
# name = input().replace(" ", "+")
# name_2 = name.lower().replace("+", "_")

start = time.time()
# name_list = ['Владимир Ким', 'kaz minerals limited', 'nova resources b.v.',
#                 'Vostok Cooper B.V.', 'Vostok Holdings Ltd', 'Folin Universal Trust',
#                 'ТОО «Корпорация Казахмыс»']
# name_list = ['Тимур Кулибаев','Joint Resources', 'Кристалл Менеджмент', 'Каспий нефть',
#                'Шубарколь Премиум']
# name_list = ['Холдинговая Группа Алмэкс', 'Astana IT University','ШубаркольПремиум']
# name_list = ['Вячеслав Ким', 'Алсеко', 'Астана-ЕРЦ', 'Kaspi.kz']
#
# name_list = ['Нурлан Смагулов', 'Астана Групп', 'Астана Моторс', 'ТРЦ MEGA',
#                'MEGA Alma-Ata', 'MEGA Park', 'MEGA Silk Way']
# name_list = ['Александр Машкевич', 'Eurasian National Resources corporation',
#              'Евразийская финансовая компания', 'Евразийский банк']

if __name__ == '__main__':
   for i in name_list:
      name = i.replace(" ", "+")
      page = 1
      while True:
         get_source(url=f"https://kapital.kz/search/default/index?q={name}&page={str(page)}&per-page=10", name=name)
         if get_source_nex(url=f"https://kapital.kz/search/default/index?q={name}&page={str(page)}&per-page=10") == None:
            break
         page += 1
      print('Количество страниц =', page)

end = time.time()
total = round((end-start)/60, 1)
print('Время выполнения парса =', total , 'минут')
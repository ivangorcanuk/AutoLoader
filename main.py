# import easygui
# from selenium import webdriver
# import time
# import random
# from fake_useragent import UserAgent
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# url = "https://www.instagram.com"
#
# # options
# options = webdriver.FirefoxOptions()  # создали объект опций
#
# #useragent
# useragent = UserAgent()  # не получается!!
# options.set_preference("general.useragent.override", 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0')
#
# options.add_argument("--headless")  # сделали фоновый режим
#
# driver = webdriver.Firefox(options=options)
#
# #executable_path='C:\\Users\\user\\PycharmProjects\\AutoUploader\\DriverFireFox\\geckodriver'
# #"https://www.whatismybrowser.com/detect/what-is-my-user-agent"  ссылка на просмотр моего user-agent
#
# try:
#
#     # driver.get(url="https://stepik.org/")
#     #
#     # time.sleep(10)
#     #
#     # driver.find_element(By.ID, "ember452").click()
#     #
#     # time.sleep(5)
#     #
#     # city_input = driver.find_element(By.ID, "id_login_email")
#     # city_input.send_keys('ivangorcanuk464@gmail.com')
#     #
#     # time.sleep(5)
#     #
#     # city_input = driver.find_element(By.ID, "id_login_password")
#     # city_input.send_keys('iwaniwan1998')
#     #
#     # time.sleep(5)
#     #
#     # city_input.send_keys(Keys.ENTER)
#     #
#     # time.sleep(5)
#     #
#     # driver.find_element(By.XPATH, "//button[@class='rubricator-onboarding__popup-btn']").click()
#     #
#     # time.sleep(5)
#     #
#     # driver.find_element(By.XPATH,
#     #                     "//button[@class='navbar__profile-toggler st-button_style_none']").click()  # клинул на профиль
#     #
#     # time.sleep(5)
#     #
#     # driver.find_element(By.LINK_TEXT, "Настройки").click()  # клинул настройки
#     #
#     # time.sleep(5)
#     #
#     # driver.find_element(By.XPATH,
#     #                     "//button[@class='user-edit__image-upload btn-link ']").click()  # клинул загрузить фото
#     #
#     # time.sleep(500)
#     #
#     # # city_input = WebDriverWait(driver, 10).until(
#     # #     EC.visibility_of_element_located((By.XPATH, "//input[@class='input js-input']"))
#     # # )
#     # #
#     # # city = input('Введите город: ')
#     # #
#     # # city_input.send_keys(city)
#     # # time.sleep(1)
#     # # city_input.send_keys(Keys.ENTER)
#     # #
#     # # # Ждем загрузки информации о погоде
#     # # weather = WebDriverWait(driver, 10).until(
#     # #     EC.visibility_of_element_located((By.XPATH, "//div[@class='weather-value']"))
#     # # )
#     # # print(weather.text)
#     #
#     # # #driver.get(url="https://www.whatismybrowser.com/detect/what-is-my-user-agent")
#     # # driver.get(url="https://gismeteo.by/")
#     # # time.sleep(1)
#     # #
#     # # driver.find_element(By.CLASS_NAME, "search-form").click()
#     # #
#     # # time.sleep(5)
#     # #
#     # # city_input = driver.find_element(By.XPATH, "//input[@class='input js-input']")
#     # # city_input.send_keys('Москва')
#     # # time.sleep(5)
#     # #
#     # # city_input.send_keys(Keys.ENTER)
#     # # time.sleep(5)
#     # #
#     # # weather = driver.find_element(By.XPATH, "//div[@class='weather-value']")
#     # # print(weather.text)
# #
# # except Exception as ex:
# #     print(ex)
# # finally:
# #     driver.close()
# #     driver.quit()

import tkinter as tk
from PIL import Image, ImageTk


def merge_images(image_paths):
    list_images = list()
    # Загружаем все изображения
    images = [Image.open(image_path) for image_path in image_paths]

    for image in images:
        img = image.resize((100, 100), Image.Resampling.LANCZOS)
        list_images.append(img)

    # Получаем ширину и высоту для нового изображения
    total_width = sum(image.width for image in list_images)
    max_height = max(image.height for image in list_images)

    # Создаём новое изображение для склеивания
    new_image = Image.new('RGB', (total_width, max_height))

    # Склеиваем изображения
    x_offset = 0
    for image in list_images:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.width

    return new_image


# Главная функция
def main():
    # Создаем главное окно
    root = tk.Tk()
    root.title("Склеенные изображения")

    # Укажите пути к изображениям
    image_paths = [
        "C:/Users/user/OneDrive/Рабочий стол/image/image1.png",
        "C:/Users/user/OneDrive/Рабочий стол/image/image2.png",
        "C:/Users/user/OneDrive/Рабочий стол/image/image3.png"
    ]

    # Склеиваем изображения
    merged_image = merge_images(image_paths)

    # Преобразуем в формат для Tkinter
    photo = ImageTk.PhotoImage(merged_image)

    # Создаем Label и устанавливаем изображение
    label_image = tk.Label(root, image=photo)
    label_image.pack(pady=20)

    # Запускаем основной цикл
    root.mainloop()

if __name__ == "__main__":
    main()
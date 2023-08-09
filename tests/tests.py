import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CLASS_TAB_ACTIVE = 'rt-tab--active'
fake = Faker()


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Firefox()

    # Переходим на страницу авторизации
    driver.implicitly_wait(10)
    driver.get('https://b2c.passport.rt.ru')

    yield driver

    driver.quit()


def test_phone_tab_active(driver):
    """
    Проверка, что находимся на форме авторизации и изначально выделена вкладка "Телефон"
    """
    auth_title = driver.find_element(By.CLASS_NAME, 'card-container__title')

    assert auth_title.text == 'Авторизация'

    tab_phone = driver.find_element(By.ID, 't-btn-tab-phone')

    assert CLASS_TAB_ACTIVE in tab_phone.get_attribute('class').split()


def test_change_active_tab_to_email(driver):
    """
    Проверка, что при вводе E-Mail и переключении в поле ввода пароля становится активна вкладка "Почта"
    """
    input_username = driver.find_element(By.ID, 'username')

    send_keys(driver=driver, element=input_username, value=fake.email())

    input_password = driver.find_element(By.ID, 'password')
    input_password.click()

    tab_mail = driver.find_element(By.ID, 't-btn-tab-mail')

    assert CLASS_TAB_ACTIVE in tab_mail.get_attribute('class').split()


def test_change_active_tab_to_login(driver):
    """
    Проверка, что при вводе логина и переключении в поле ввода пароля становится активна вкладка "Логин"
    """
    input_username = driver.find_element(By.ID, 'username')

    send_keys(driver=driver, element=input_username, value=fake.user_name())

    input_password = driver.find_element(By.ID, 'password')
    input_password.click()

    tab_login = driver.find_element(By.ID, 't-btn-tab-login')

    assert CLASS_TAB_ACTIVE in tab_login.get_attribute('class').split()


def test_username_placeholder_value_for_phone_tab(driver):
    """
    Проверка, что placeholder поля ввода "Имя пользователя" при выделенной вкладке "Телефон" имеет
    значение "Мобильный телефон"
    """
    tab_phone = driver.find_element(By.ID, 't-btn-tab-phone')
    tab_phone.click()

    input_username = driver.find_element(By.ID, 'username')
    input_username_parent = input_username.find_element(By.XPATH, '..')

    placeholder = input_username_parent.find_element(By.CLASS_NAME, 'rt-input__placeholder')

    assert placeholder.text == 'Мобильный телефон'


def test_username_placeholder_value_for_email_tab(driver):
    """
    Проверка, что placeholder поля ввода "Имя пользователя" при выделенной вкладке "Почта" имеет
    значение "Электронная почта"
    """
    tab_mail = driver.find_element(By.ID, 't-btn-tab-mail')
    tab_mail.click()

    input_username = driver.find_element(By.ID, 'username')
    input_username_parent = input_username.find_element(By.XPATH, '..')

    placeholder = input_username_parent.find_element(By.CLASS_NAME, 'rt-input__placeholder')

    assert placeholder.text == 'Электронная почта'


def test_username_placeholder_value_for_login_tab(driver):
    """
    Проверка, что placeholder поля ввода "Имя пользователя" при выделенной вкладке "Логин" имеет
    значение "Логин"
    """
    tab_login = driver.find_element(By.ID, 't-btn-tab-login')
    tab_login.click()

    input_username = driver.find_element(By.ID, 'username')
    input_username_parent = input_username.find_element(By.XPATH, '..')

    placeholder = input_username_parent.find_element(By.CLASS_NAME, 'rt-input__placeholder')

    assert placeholder.text == 'Логин'


def test_username_placeholder_value_for_ls_tab(driver):
    """
    Проверка, что placeholder поля ввода "Имя пользователя" при выделенной вкладке "Лицевой счёт" имеет
    значение "Лицевой счёт"
    """
    tab_ls = driver.find_element(By.ID, 't-btn-tab-ls')
    tab_ls.click()

    input_username = driver.find_element(By.ID, 'username')
    input_username_parent = input_username.find_element(By.XPATH, '..')

    placeholder = input_username_parent.find_element(By.CLASS_NAME, 'rt-input__placeholder')

    assert placeholder.text == 'Лицевой счёт'


def test_password_placeholder_value(driver):
    """
    Проверка, что placeholder поля ввода "Пароль" имеет значение "Пароль"
    """
    input_password = driver.find_element(By.ID, 'password')
    input_password_parent = input_password.find_element(By.XPATH, '..')

    placeholder = input_password_parent.find_element(By.CLASS_NAME, 'rt-input__placeholder')

    assert placeholder.text == 'Пароль'


def test_change_password_input_type_from_password_to_text(driver):
    """
    Проверка поля ввода "Пароль": при нажатии на иконку отображения пароля он отображается (type поля
    ввода "Пароль" меняется на text)
    """
    input_password = driver.find_element(By.ID, 'password')
    input_password_parent = input_password.find_element(By.XPATH, '..')

    assert input_password.get_property('type') == 'password'

    svg = input_password_parent.find_element(By.TAG_NAME, 'svg')
    svg.click()

    assert input_password.get_property('type') == 'text'


def test_change_icon_in_password_input(driver):
    """
    Проверка поля ввода "Пароль": при нажатии на иконку отображения пароля изображение меняется
    """
    input_password = driver.find_element(By.ID, 'password')
    input_password_parent = input_password.find_element(By.XPATH, '..')

    svg = input_password_parent.find_element(By.TAG_NAME, 'svg')
    img_old = svg.find_element(By.TAG_NAME, 'path')
    img_old_content = img_old.get_attribute('d')

    svg.click()

    img_new = svg.find_element(By.TAG_NAME, 'path')
    img_new_content = img_new.get_attribute('d')

    assert img_new_content != img_old_content


def test_tab_mail_after_refresh(driver):
    """
    Проверка, что после перехода на вкладку "Почта" она остается активна после перезагрузки страницы
    """
    tab_mail = driver.find_element(By.ID, 't-btn-tab-mail')
    tab_mail.click()

    assert CLASS_TAB_ACTIVE in tab_mail.get_attribute('class').split()

    driver.refresh()

    tab_mail = driver.find_element(By.ID, 't-btn-tab-mail')

    assert CLASS_TAB_ACTIVE in tab_mail.get_attribute('class').split()


def test_tab_login_after_refresh(driver):
    """
    Проверка, что после перехода на вкладку "Логин" она остается активна после перезагрузки страницы
    """
    tab_login = driver.find_element(By.ID, 't-btn-tab-login')
    tab_login.click()

    assert CLASS_TAB_ACTIVE in tab_login.get_attribute('class').split()

    driver.refresh()

    tab_login = driver.find_element(By.ID, 't-btn-tab-login')

    assert CLASS_TAB_ACTIVE in tab_login.get_attribute('class').split()


def test_tab_ls_after_refresh(driver):
    """
    Проверка, что после перехода на вкладку "Лицевой счет" она остается активна после перезагрузки страницы
    """
    tab_ls = driver.find_element(By.ID, 't-btn-tab-ls')
    tab_ls.click()

    assert CLASS_TAB_ACTIVE in tab_ls.get_attribute('class').split()

    driver.refresh()

    tab_ls = driver.find_element(By.ID, 't-btn-tab-ls')

    assert CLASS_TAB_ACTIVE in tab_ls.get_attribute('class').split()


def test_check_warning_message_if_ls_not_set(driver):
    """
    При переходе на вкладку "Лицевой счет", переключении фокуса на поле "Лицевой счет", а потом на поле "Пароль"
    появляется надпись "Проверьте, пожалуйста, номер лицевого счета"
    """
    tab_ls = driver.find_element(By.ID, 't-btn-tab-ls')
    tab_ls.click()

    input_username = driver.find_element(By.ID, 'username')
    input_username.click()

    input_password = driver.find_element(By.ID, 'password')
    input_password.click()

    span = driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[2]/span[1]'
    )

    assert span.text == 'Проверьте, пожалуйста, номер лицевого счета'


def test_redirect_reset_cred_phone(driver):
    """
    Проверка перехода на форму восстановления пароля:
     * Проверяем, что активна вкладка "Телефон"
     * Выполняем переход на форму восстановления пароля
     * Проверяем, что вкладка "Телефон" активна
    """
    tab_phone = driver.find_element(By.ID, 't-btn-tab-phone')

    assert CLASS_TAB_ACTIVE in tab_phone.get_attribute('class').split()

    forgot_password = driver.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    # Ожидаем перехода на форму восстановления пароля
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'card-container__title'), 'Восстановление пароля')
    )

    reset_tab_phone = driver.find_element(By.ID, 't-btn-tab-phone')

    assert CLASS_TAB_ACTIVE in reset_tab_phone.get_attribute('class').split()


def test_redirect_reset_cred_email(driver):
    """
    Проверка перехода на форму восстановления пароля:
     * Переходим на вкладку "Почта"
     * Выполняем переход на форму восстановления пароля
     * Проверяем, что вкладка "Почта" активна
    """
    tab_mail = driver.find_element(By.ID, 't-btn-tab-mail')
    tab_mail.click()

    assert CLASS_TAB_ACTIVE in tab_mail.get_attribute('class').split()

    forgot_password = driver.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    # Ожидаем перехода на форму восстановления пароля
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'card-container__title'), 'Восстановление пароля')
    )

    reset_tab_mail = driver.find_element(By.ID, 't-btn-tab-mail')

    assert CLASS_TAB_ACTIVE in reset_tab_mail.get_attribute('class').split()


def test_redirect_reset_cred_login(driver):
    """
    Проверка перехода на форму восстановления пароля:
     * Переходим на вкладку "Логин"
     * Выполняем переход на форму восстановления пароля
     * Проверяем, что вкладка "Логин" активна
    """
    tab_login = driver.find_element(By.ID, 't-btn-tab-login')
    tab_login.click()

    assert CLASS_TAB_ACTIVE in tab_login.get_attribute('class').split()

    forgot_password = driver.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    # Ожидаем перехода на форму восстановления пароля
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'card-container__title'), 'Восстановление пароля')
    )

    reset_tab_login = driver.find_element(By.ID, 't-btn-tab-login')

    assert CLASS_TAB_ACTIVE in reset_tab_login.get_attribute('class').split()


def test_redirect_reset_cred_ls(driver):
    """
    Проверка перехода на форму восстановления пароля:
     * Переходим на вкладку "Лицевой счет"
     * Выполняем переход на форму восстановления пароля
     * Проверяем, что вкладка "Лицевой счет" активна
    """
    tab_ls = driver.find_element(By.ID, 't-btn-tab-ls')
    tab_ls.click()

    assert CLASS_TAB_ACTIVE in tab_ls.get_attribute('class').split()

    forgot_password = driver.find_element(By.ID, 'forgot_password')
    forgot_password.click()

    # Ожидаем перехода на форму восстановления пароля
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'card-container__title'), 'Восстановление пароля')
    )

    reset_tab_ls = driver.find_element(By.ID, 't-btn-tab-ls')

    assert CLASS_TAB_ACTIVE in reset_tab_ls.get_attribute('class').split()


def test_redirect_to_agreement(driver):
    """
    Проверка перехода на пользовательское соглашение
    """
    agreement_link = driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[4]/a[1]')
    agreement_link.click()

    # Ожидаем переход
    WebDriverWait(driver, 10).until(EC.url_changes("https://b2c.passport.rt.ru/sso-static/agreement/agreement.html4"))


def test_redirect_to_registration(driver):
    """
    Проверка перехода на форму регистрации
    """
    register_link = driver.find_element(By.ID, 'kc-register')
    register_link.click()

    # Ожидаем переход
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'card-container__title'), 'Регистрация')
    )


def send_keys(driver, element, value):
    """
    FIX проблемы с усечением ввода через send_keys:
        https://stackoverflow.com/questions/18483419/selenium-sendkeys-drops-character-with-chrome-driver
    """
    element.clear()

    for i in range(len(value)):
        element.send_keys(value[i])
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element_value((By.ID, 'username'), value[:i+1])
        )

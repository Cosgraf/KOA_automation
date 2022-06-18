from numpy import uint8
import pyautogui
import cv2
import time
import pyperclip
import numpy as np
from PIL import ImageGrab
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\Documents\KOA\Tesseract\tesseract.exe'

ID_POSITIONS = {'mail': (818, 300), 'password': (818, 375)}
LOADING_TIME = 6
START_UP_SCREENS = {'small': (1580, 246), 'medium': (1713, 225), 'event': (1834, 121), 'daily_delivery': (689, 888)}
POINTS_SCREEN_INSIDE = {'point1': ((589, 690), (66, 61, 61)),
                        'point2': ((526, 515), (85, 77, 76)),
                        'point3': ((812, 1031), (76, 68, 68))}
ALLIANCE = {'button': (1151, 994),
            'exit_window': (1834, 121),
            'exit_tab': (127, 74),
            'territory': (1066, 490),
            'territory_tab': (177, 372),
            'territory_gather': (1656, 258),
            'researches': (1350, 490),
            'researches_choices': [(373, 840), (373, 591), (373, 342)],
            'research_star_y_offset': 173,
            'research_star_color': (109, 214, 239),
            'exit_donation': (1508, 185),
            'donate': (1382, 859),
            'donate_color': (151, 114, 57),  # (104, 78, 39), end color
            'donate_for_gold': (1162, 718),
            'donate_for_gold_color': (32, 94, 54),
            'no_donation_pos': (1282, 754),
            'no_donation_color': (0, 0, 240),
            'over_20_donation_pos_1': (1337, 755),
            'over_20_donation_color_1': (109, 102, 92),
            'over_20_donation_pos_2': (1328, 755),
            'over_20_donation_color_2': (113, 106, 96),
            'donation_bug': (1170, 740),
            'donation_bug_color': (112, 80, 30),
            'chests_menu': (1350, 700),
            'chests_tab': (907, 73),
            'chests_open': (233, 700),
            'chests_opened_color': (61, 115, 149),  # 61 115 149 golden / 140, 106, 53 blue
            'help': (1643, 700),
            'help_button': (962, 931),
            }

MAILS = {'button': (1538, 988),
         'new_mail_color': (32, 38, 152),
         'messages': (281, 169),
         'war': (281, 281),
         'alliance': (281, 398),
         'system': (281, 512),
         'report': (281, 623),
         'mark_read': (1255, 991),
         }

ACCOUNT_PARAM = {'account_nb_pos': [(590, 231), (984, 231), (590, 372), (984, 372), (590, 505), (984, 505)],
                 'px_connect_button': 942,
                 'min_max_py_connect_button': (298, 700),
                 'connect_button_color': (9, 144, 248)
                 }

EXIT_ACCOUNT_POS = {'profile': (111, 105),
                    'parameters': (111, 985),
                    'account': (771, 428),
                    'change_account': (950, 680),
                    'kings_account': (949, 431),
                    }

ACCOUNT_FUNPLUS = {'admissible_error_height_check': 10,
                   'scroll_height': -300,
                   'scroll_y_pos': 800,
                   "switch_account_funplus": (438, 452),
                   'current_account': ((280, 346), (650, 390)),  # corner1 x, corner 1 y, corner2 x, corner 2 y
                   'x_pos_check_valid_character': 1800,
                   'character_height': 176,
                   'check_height_character': 150,
                   'change_char': (1234, 921),
                   'char_name_xmin': 820,
                   'char_name_xmax': 1314,
                   'max_char_for_character': 12,
                   'offset_char_name_box': (-40, 0),
                   'x_pos_check_valid_account': 1028,
                   'account_more': (1381, 649),
                   'account_name_xmin': 1200,
                   'account_name_xmax': 1550,
                   'offset_account_name_box': (-70, -30),
                   'check_height_account': 186,
                   }

DAILY_DELIVERY = {'war_aid_center': (1633, 168),
                  "days": [(1153, 615), (1345, 615), (1532, 615), (1068, 845), (1247, 845), (1433, 845), (1613, 845)]
                  }


def click(px_x, px_y):
    mouse_pos = pyautogui.position()
    pyautogui.click(px_x, px_y)
    pyautogui.moveTo(*mouse_pos)
    time.sleep(0.6)


def click_repeat(px_x, px_y, rep):
    mouse_pos = pyautogui.position()
    for i in range(rep):
        pyautogui.click(px_x, px_y)
        time.sleep(0.15)
    pyautogui.moveTo(*mouse_pos)


def what_is_color(image, px_x, px_y):
    print(px_x, px_y)
    # print(image[px_y, px_x, :])
    print(image.getpixel((px_x, px_y)))


def scroll(pos_ini, x_scroll, y_scroll, scroll_time=0.5):
    pyautogui.moveTo(pos_ini[0], pos_ini[1])
    pyautogui.drag(x_scroll, y_scroll, scroll_time, button='left')


def match_color_in_image(image, px_x, px_y, color, display=False):
    # b, g, r = image[px_y, px_x, :]
    r, g, b = image.getpixel((px_x, px_y))
    difference = np.sqrt((b - color[0]) ** 2 + (g - color[1]) ** 2 + (r - color[2]) ** 2)
    if display:
        print(color, "and", image.getpixel((px_x, px_y)))
        print(difference)
    if difference < 10:
        return True
    return False


def image_to_txt_crop(corner1, corner2):
    image = ImageGrab.grab()
    txt_image = np.array(image.crop((corner1[0], corner1[1], corner2[0], corner2[1])).convert('RGB'))
    txt_image = txt_image[:, :, ::-1].copy()
    gray = cv2.cvtColor(txt_image.astype(uint8), cv2.COLOR_BGR2GRAY)
    # ret, thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
    # morph_img = cv2.morphologyEx(thresh_img, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('blur', thresh_img)
    # cv2.waitKey()
    # mail_value = pytesseract.image_to_string(morph_img, lang='eng', config='--psm 10')
    txt_value = pytesseract.image_to_string(gray, lang='eng', config='--psm 10')
    return txt_value


def detect_items_in_list(x_detection):
    image = ImageGrab.grab()
    front_up_y = []
    front_down_y = []
    r = g = b = 0
    for j in range(image.height):
        prev_r, prev_g, prev_b = r, g, b
        r, g, b = image.getpixel((x_detection, j))
        if r == g == b == 255 and prev_r != 255:
            front_up_y.append(j)
        elif (g != 255 or r != 255 or b != 255) and prev_r == prev_g == prev_b == 255:
            front_down_y.append(j)

    center_y_items = np.floor((np.array(front_down_y) + np.array(front_up_y)) / 2)

    return front_up_y, front_down_y, center_y_items


def prepare_names(names):
    dict_names = {}
    for name in names:
        identical_char = 0
        for name_to_test in names:
            identical_char_tmp = 0
            if name != name_to_test:
                min_len = min(len(name), len(name_to_test))
                for i in range(min_len):
                    char1, char2 = name[i], name_to_test[i]
                    if char1 == char2:
                        identical_char_tmp += 1
                    else:
                        break
            if identical_char_tmp > identical_char:
                identical_char = identical_char_tmp
        char_to_test = identical_char + 1
        dict_names[name] = char_to_test - 1
    return dict_names


def select_items_names(x_detect_items, dict_names_searched, x_min, x_max, offset_y, check_valid, error_height_check,
                       max_char_to_test=None, del_stars=False):
    names_to_test = list(dict_names_searched.keys())
    # for name, char_to_test in dict_names_searched.items():
    #     names_to_test.append(name[:12])
    front_up, front_down, center_y_items = detect_items_in_list(x_detect_items)
    # print(front_up)
    # print(front_down)
    # print(center_y_items)
    item_names = []
    to_scroll = False
    name_found = (None, 0, 0)
    for i, center in enumerate(center_y_items):
        if abs(check_valid - (front_down[i] - front_up[i])) < error_height_check:
            text = image_to_txt_crop((x_min, center + offset_y[0]), (x_max, center + offset_y[1]))
            # print(text)
            if text[-1:] == "\n":
                text = text[:-1]
            if text not in item_names:
                item_names.append(text)
            for name_to_test in names_to_test:
                # print(name_to_test, text)
                if max_char_to_test is None:
                    real_test_name = name_to_test
                else:
                    real_test_name = name_to_test[:max_char_to_test]
                if del_stars:
                    real_test_name = real_test_name.replace('*', '')
                    text = text.replace('*', '')
                # print(real_test_name, text)
                if text.startswith(real_test_name):
                    name_found = (name_to_test, x_min, center)
                    break
            if name_found[0] is not None:
                break
        elif i == len(center_y_items) - 1:
            to_scroll = True

    return to_scroll, name_found, item_names


def enter_ids(mail, password):
    click(*ID_POSITIONS['mail'])
    pyperclip.copy(mail)
    pyautogui.hotkey("ctrl", "v")
    click(*ALLIANCE['button'])
    click(*ID_POSITIONS['password'])
    pyautogui.typewrite(password)


def change_account(identification):
    click(ACCOUNT_FUNPLUS["switch_account_funplus"][0], ACCOUNT_FUNPLUS["switch_account_funplus"][1])
    click(*ACCOUNT_FUNPLUS["account_more"])
    dict_id = prepare_names([identification])
    to_scroll, name_found, item_names = select_items_names(ACCOUNT_FUNPLUS['x_pos_check_valid_account'], dict_id,
                                               ACCOUNT_FUNPLUS['account_name_xmin'],
                                               ACCOUNT_FUNPLUS['account_name_xmax'],
                                               ACCOUNT_FUNPLUS['offset_account_name_box'],
                                               ACCOUNT_FUNPLUS['check_height_account'],
                                               ACCOUNT_FUNPLUS['admissible_error_height_check'], del_stars=True)
    if name_found[0] is None:
        while to_scroll:
            scroll((ACCOUNT_FUNPLUS['x_pos_check_valid_character'], ACCOUNT_FUNPLUS['scroll_y_pos']), 0,
                   ACCOUNT_FUNPLUS['scroll_height'])
            time.sleep(0.5)
            to_scroll, name_found, item_names = select_items_names(ACCOUNT_FUNPLUS['x_pos_check_valid_account'], dict_id,
                                                       ACCOUNT_FUNPLUS['account_name_xmin'],
                                                       ACCOUNT_FUNPLUS['account_name_xmax'],
                                                       ACCOUNT_FUNPLUS['offset_account_name_box'],
                                                       ACCOUNT_FUNPLUS['check_height_account'],
                                                       ACCOUNT_FUNPLUS['admissible_error_height_check'], del_stars=True)
            if name_found[0] is not None:
                break

    if name_found[0] is None:
        not_found = list(dict_id.keys())
        print('ERROR: identification was not found', not_found, "in", item_names)
    click(name_found[1], name_found[2])


def exit_start_up_screens():
    inter = 0
    while True:
        time.sleep(LOADING_TIME)
        click(*START_UP_SCREENS['daily_delivery'])
        click(*START_UP_SCREENS['event'])
        click(*START_UP_SCREENS['event'])
        click(*START_UP_SCREENS['medium'])
        click(*START_UP_SCREENS['small'])
        if is_start_up_screen_position():
            return
        inter += 1
        if inter > 5:
            raise Exception("STOPPED DURING EXIT START UP SCREENS")


def is_start_up_screen_position():
    image = ImageGrab.grab()
    pos_points = [POINTS_SCREEN_INSIDE['point1'][0],
                  POINTS_SCREEN_INSIDE['point2'][0],
                  POINTS_SCREEN_INSIDE['point3'][0]]
    points_color = [POINTS_SCREEN_INSIDE['point1'][1],
                    POINTS_SCREEN_INSIDE['point2'][1],
                    POINTS_SCREEN_INSIDE['point3'][1]]
    match = 0
    for point, color in zip(pos_points, points_color):
        px_y, px_x = point
        r, g, b = image.getpixel((px_x, px_y))
        if (b, g, r) == color:
            match += 1
    if match == len(pos_points):
        return True
    return False


def detect_star_donation(image):
    for choice in ALLIANCE['researches_choices']:
        px_star = choice[0]
        py_star = choice[1] - ALLIANCE['research_star_y_offset']
        r, g, b = image.getpixel((px_star, py_star))
        if r > 150 and g > 150:
            return choice
    return ALLIANCE['researches_choices'][1]


def do_donations():
    click(*ALLIANCE['button'])
    click(*ALLIANCE['researches'])
    time.sleep(1)
    image = ImageGrab.grab()
    choice = detect_star_donation(image)
    click(*choice)
    while True:
        # pyautogui.screenshot(path)
        # time.sleep(1)
        # image = cv2.imread(path)
        image = ImageGrab.grab()
        # print(not match_color_in_image(image, *ALLIANCE['no_donation_pos'], ALLIANCE['no_donation_color']))
        # print(match_color_in_image(image, *ALLIANCE['donate'], ALLIANCE['donate_color']))
        if (match_color_in_image(image, *ALLIANCE['donate'], ALLIANCE['donate_color']) and
                not match_color_in_image(image, *ALLIANCE['no_donation_pos'], ALLIANCE['no_donation_color']) and
                (match_color_in_image(image, *ALLIANCE['over_20_donation_pos_1'],
                                      ALLIANCE['over_20_donation_color_1']) or
                 match_color_in_image(image, *ALLIANCE['over_20_donation_pos_2'],
                                      ALLIANCE['over_20_donation_color_2']))):
            click_repeat(*ALLIANCE['donate'], 5)
        else:
            if match_color_in_image(image, *ALLIANCE['donate_for_gold'], ALLIANCE['donate_for_gold_color']):
                break
            elif match_color_in_image(image, *ALLIANCE['donation_bug'], ALLIANCE['donation_bug_color']):
                # BUG OOPS MUST CLICK BLUE BUTTON
                click(*ALLIANCE['donate_for_gold'])
                break
            else:
                break
    for i in range(3):
        click(*ALLIANCE['exit_window'])


def do_territory_rss_gathering():
    click(*ALLIANCE['button'])
    click(*ALLIANCE['territory'])
    click(*ALLIANCE['territory_tab'])
    time.sleep(1)
    click(*ALLIANCE['territory_gather'])
    click(*ALLIANCE['exit_window'])


def do_chest_collect():
    click(*ALLIANCE['button'])
    click(*ALLIANCE['chests_menu'])
    click(*ALLIANCE['chests_tab'])
    image = ImageGrab.grab()
    while match_color_in_image(image, *ALLIANCE['chests_open'], ALLIANCE['chests_opened_color']):
        click(*ALLIANCE['chests_open'])
        click(*ALLIANCE['chests_open'])
        image = ImageGrab.grab()
    click(*ALLIANCE['exit_window'])


def do_help():
    click(*ALLIANCE['button'])
    click(*ALLIANCE['help'])
    click(*ALLIANCE['help_button'])
    click(*ALLIANCE['exit_window'])


def do_alliance_rotation():
    exit_start_up_screens()
    do_territory_rss_gathering()
    do_donations()
    do_chest_collect()
    do_help()
    do_mails()


def do_donation_only():
    exit_start_up_screens()
    do_territory_rss_gathering()
    do_donations()


def detect_connect_button(image):
    for i in range(*ACCOUNT_PARAM['min_max_py_connect_button']):
        if match_color_in_image(image, ACCOUNT_PARAM['px_connect_button'], i, ACCOUNT_PARAM['connect_button_color']):
            return ACCOUNT_PARAM['px_connect_button'], i


def exit_account():
    click(*EXIT_ACCOUNT_POS['profile'])
    click(*EXIT_ACCOUNT_POS['parameters'])
    click(*EXIT_ACCOUNT_POS['account'])
    click(*EXIT_ACCOUNT_POS['change_account'])
    click(*EXIT_ACCOUNT_POS['kings_account'])


def do_daily_delivery():
    exit_start_up_screens()
    click(*DAILY_DELIVERY['war_aid_center'])
    for day in DAILY_DELIVERY['days']:
        click(*day)
    time.sleep(4)
    click(*START_UP_SCREENS['event'])
    click(*START_UP_SCREENS['event'])


def do_mails():
    click(*MAILS['button'])
    time.sleep(0.5)
    image = ImageGrab.grab()
    item_positions = [MAILS['messages'], MAILS['war'], MAILS['alliance'], MAILS['system'], MAILS['report']]
    for pos in item_positions:
        if match_color_in_image(image, *pos, MAILS['new_mail_color']):
            click(*pos)
            click(*MAILS['mark_read'])
            # click(*MAILS['mark_read'])
            click(*pos)
    click(*START_UP_SCREENS['event'])


def rotate_accounts_and_do(identification, character_names, function_to_do, param_fct=None):
    dict_characters = prepare_names(character_names)

    current_acc_name = image_to_txt_crop(ACCOUNT_FUNPLUS['current_account'][0], ACCOUNT_FUNPLUS['current_account'][1])[:-1]
    if ' ' in current_acc_name:
        current_acc_name = current_acc_name.split(' ')[-1]
    if not identification.startswith(current_acc_name):
        change_account(identification)

    while len(dict_characters) != 0:
        to_scroll, name_found, item_names = select_items_names(ACCOUNT_FUNPLUS['x_pos_check_valid_character'], dict_characters,
                                                   ACCOUNT_FUNPLUS['char_name_xmin'], ACCOUNT_FUNPLUS['char_name_xmax'],
                                                   ACCOUNT_FUNPLUS['offset_char_name_box'],
                                                   ACCOUNT_FUNPLUS['check_height_character'],
                                                   ACCOUNT_FUNPLUS['admissible_error_height_check'],
                                                   ACCOUNT_FUNPLUS['max_char_for_character'])
        if name_found[0] is None:
            while to_scroll:
                scroll((ACCOUNT_FUNPLUS['x_pos_check_valid_character'], ACCOUNT_FUNPLUS['scroll_y_pos']), 0,
                       ACCOUNT_FUNPLUS['scroll_height'])
                time.sleep(0.5)
                to_scroll, name_found, item_names = select_items_names(ACCOUNT_FUNPLUS['x_pos_check_valid_character'],
                                                           dict_characters,
                                                           ACCOUNT_FUNPLUS['char_name_xmin'],
                                                           ACCOUNT_FUNPLUS['char_name_xmax'],
                                                           ACCOUNT_FUNPLUS['offset_char_name_box'],
                                                           ACCOUNT_FUNPLUS['check_height_character'],
                                                           ACCOUNT_FUNPLUS['admissible_error_height_check'],
                                                           ACCOUNT_FUNPLUS['max_char_for_character'])
                if name_found[0] is not None:
                    break

        if name_found[0] is None:
            not_found = list(dict_characters.keys())
            print('ERROR: Names in the list were not found', not_found)
            break
        del dict_characters[name_found[0]]

        click(name_found[1], name_found[2])
        click(ACCOUNT_FUNPLUS["change_char"][0], ACCOUNT_FUNPLUS["change_char"][1])

        time.sleep(LOADING_TIME)
        if param_fct is not None:
            function_to_do(param_fct)
        else:
            function_to_do()
        exit_account()
        time.sleep(0.5)


def rotate_accounts_and_do_old(identifications, function_to_do, try_captcha, param_fct=None):
    """DEPRECATED"""
    for account_nb in identifications[2]:
        account_pos = ACCOUNT_PARAM['account_nb_pos'][account_nb]
        enter_ids(identifications[0], identifications[1])
        try_captcha()
        time.sleep(1)
        image = ImageGrab.grab()
        r, g, b = image.getpixel((account_pos[0], account_pos[1]))
        if r == g == b:
            break
        click(*account_pos)

        click(*detect_connect_button(image))

        time.sleep(LOADING_TIME)
        if param_fct is not None:
            function_to_do(param_fct)
        else:
            function_to_do()
        exit_account()
        time.sleep(0.5)

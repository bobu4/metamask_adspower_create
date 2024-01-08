import time, os, sys
import glob
import traceback
import os
import string
import platform


def line_control(file_txt):
    # Удаление пустых строк
    with open(file_txt) as f1:
        lines = f1.readlines()
        non_empty_lines = (line for line in lines if not line.isspace())
        with open(file_txt, "w") as n_f1:
            n_f1.writelines(non_empty_lines)


def path_to_ads_folder():
    # Определение ОС пользователя
    # if platform.system() == 'Darwin':
    #     # Mac operating system
    #     folder_name = "adspower_global/cwd_global/source"
    #     username = getpass.getuser()
    #     path = os.path.join("/Users/", username + "/Library/Application Support/", folder_name)
    #     if os.path.exists(path):
    #         return path

    if True:
        # Other operating systems (Windows)
        drives = [drive for drive in string.ascii_uppercase if os.path.exists(drive + ":")]
        folder_name = ".ADSPOWER_GLOBAL"
        for drive in drives:
            path = drive + ":" + "\\" + folder_name
            if os.path.exists(os.path.join(path)):
                return path


def cache_folder_exist():
    path_to_cache = path_to_ads_folder() + r"/cache"
    if os.path.exists(path_to_cache):
        return
    else:
        return 0


def get_profile_cache_path(prof_id, path_from_ads_settings):
    folder_path = glob.glob(fr"{path_from_ads_settings}/cache/{prof_id}*")

    if folder_path:
        path_to_profile = folder_path[0].replace("\\", "/")
        path = fr'{path_to_profile}/extensionCenter/nkbihfbeogaeaoehlefnkodbefgpgknn/runtime-lavamoat.js'
    else:
        return 0
    return path


def runtime_lavamoat_cache_editor(path):

    with open(path, 'r', encoding="utf-8") as read:
        lines = read.readlines()

    key_edt = False
    # Изменяет переменную scuttleGlobalThis на значение false/true
    with open(path, 'w', encoding="utf-8") as read:
        for line in lines:
            if line.startswith('    } = {"scuttleGlobalThis":{"enabled":true,"scuttlerName":"SCUTTLER","exceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","WeakSet","Event","Image","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","JSON","Date","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}}'):
                line = '    } = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","WeakSet","Event","Image","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","JSON","Date","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}}'
                key_edt = True
            elif line.startswith('    } = {"scuttleGlobalThis":{"enabled":false,"scuttlerName":"SCUTTLER","exceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","WeakSet","Event","Image","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","JSON","Date","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}}'):
                line = '    } = {"scuttleGlobalThis":{"enabled":true,"scuttlerName":"SCUTTLER","exceptions":["toString","getComputedStyle","addEventListener","removeEventListener","ShadowRoot","HTMLElement","Element","pageXOffset","pageYOffset","visualViewport","Reflect","Set","Object","navigator","harden","console","WeakSet","Event","Image","/cdc_[a-zA-Z0-9]+_[a-zA-Z]+/iu","performance","parseFloat","innerWidth","innerHeight","Symbol","Math","DOMRect","Number","Array","crypto","Function","Uint8Array","String","Promise","JSON","Date","__SENTRY__","appState","extra","stateHooks","sentryHooks","sentry"]}}'
                key_edt = False
            read.write(line)

    return key_edt


def fix(prof_id):

    path_from_ads_settings = path_to_ads_folder()
    if path_from_ads_settings is None:
        print(f'Adspower не установлен/Не найден путь. Обратитесь к разрабочику')
        sys.exit(0)
    if cache_folder_exist() == 0:
        print(f'Папка /Cache/ не была обнаружена. Обратитесь к разрабочику')
        sys.exit(0)

    try:
        path = get_profile_cache_path(prof_id, path_from_ads_settings)
        # if path == 0:
        #     print(f'{0}. < {prof_id} >  cache not found or wrong id')
        key_edt = runtime_lavamoat_cache_editor(path)
        # if key_edt is True:
        #     print(f'{0}. < {prof_id} >  fixed')
        # elif key_edt is False:
        #     print(f'{0}. < {prof_id} >  unfixed')

    except FileNotFoundError:
        # traceback.print_exc()
        # time.sleep(.3)
        print(f' < {prof_id} >  runtime-lavamoat.js not found')

    except Exception as ex:
        traceback.print_exc()
        time.sleep(.3)
        print(f' < {prof_id} >  Unexpected error. Обратитесь к разработчику.')

# ======================================================================================================================
# Created by Desti
# ======================================================================================================================

# 📌 Что это и зачем?

Репозиторий содержит инструкцию по установке **XKeen Mihomo** и мои персональные настройки для панели.  
Здесь также находится скрипт для автоматического парсинга IP голосового чата Discord — удобно для формирования списков IP-адресов в формате `ip-sets`.

<p align="center">

  <picture>
    <img width="100%" height="100%" src="https://github.com/cazmusw/MihomoInstallKenetic/blob/main/icons/Demo.png?raw=true">
  </picture>
  
</p>

---

## 🔧 Что внутри
- Инструкция по установке **XKeen Mihomo**.
- Мои настройки панели (конфиги, шаблоны).
- Скрипт `ParseDiscordDomains.py` — автоматический парсер доменов/айпи, связанный с голосовым чатом Discord.
- Папка `ip-sets` — место, куда сохраняются полученные результаты.

---

## 🚀 Как запустить скрипт парсинга IP голосового чата Discord

Откройте терминал и выполните:

```bash
  pip install aiofiles tqdm
  py .\scripts\ParseDiscordDomains.py
```

После выполнения скрипта результаты будут сохранены в папке `ip-sets`.

## 🚀 Установка XKeen

**1) Форматирование USB накопителя в Ext4**
- Скачайте [DiskGenius](https://www.diskgenius.com/dyna_download/?software=DGEng6011645_x64.zip)
- Запусти и найди свою флешку.
- Удали старые разделы (ПКМ → Delete All Partitions).
- Создай новый → Create New Partition.
- В поле File System Type выбери Linux Ext4.
- Нажми Save All → Yes для подтверждения.


**2) В роутере Keenetic установите нужные компоненты [OPKG](https://help.keenetic.com/hc/ru/articles/213968029-Установка-внешних-Opkg-пакетов-для-версий-NDMS-2-11-и-более-ранних). Основным и обязательным является компонент "**Поддержка открытых пакетов**".**

- [x] Интерфейс USB
- [x] Файловая система Ext
- [x] Общий доступ к файлам и принтерам по протоколу SMB
- [x] Поддержка открытых пакетов
- [x] Прокси-сервер DNS-over-TLS
- [x] Прокси-сервер DNS-over-HTTPS
- [ ] Протокол IPv6
- [x] Модули ядра подсистемы Netfilter
- [ ] Сервер SSH

**3) Теперь нужно установить репозиторий системы пакетов [Entware](https://forum.keenetic.net/topic/4299-entware/).**

> [!NOTE]
> **Справка**: Для моделей 4G (KN-1212), Omni (KN-1410), Extra (KN-1710/1711/1713), Giga (KN-1010/1011), Ultra (KN-1810), Viva (KN-1910/1912/1913), Giant (KN-2610), Hero 4G (KN-2310/2311), Hopper (KN-3810) и Zyxel Keenetic II / III, Extra, Extra II, Giga II / III, Omni, Omni II, Viva, Ultra, Ultra II используйте для установки архив **mipsel** — [mipsel-installer.tar.gz](https://bin.entware.net/mipselsf-k3.4/installer/mipsel-installer.tar.gz)
>
> Для моделей Ultra SE (KN-2510), Giga SE (KN-2410), DSL (KN-2010), Skipper DSL (KN-2112), Duo (KN-2110), Ultra SE (KN-2510),  Hopper DSL (KN-3610) и Zyxel Keenetic DSL, LTE, VOX используйте для установки архив **mips** — [mips-installer.tar.gz](https://bin.entware.net/mipssf-k3.4/installer/mips-installer.tar.gz)
>
> Для моделей Peak (KN-2710), Ultra (KN-1811), Giga (KN-1012), Hopper (KN-3811) и Hopper SE (KN-3812) используйте архив **aarch64** — [aarch64-installer.tar.gz](https://bin.entware.net/aarch64-k3.10/installer/aarch64-installer.tar.gz)

<br>

Подключите уже подготовленный накопитель c файловой системой [EXT4](https://help.keenetic.com/hc/ru/articles/115005875145-Использование-файловой-системы-EXT4-на-USB-накопителях) к USB-порту роутера. Диск должен отобразиться на странице "Приложения" в разделе "Диски и принтеры".

<p align="center">
  <a href="http://192.168.1.1/apps" target="_blank" rel="noopener noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Corvus-Malus/XKeen-docs/raw/main/images/Dark/Keenetic-apps-Dark.png">
      <img width="100%" height="100%" src="https://github.com/Corvus-Malus/XKeen-docs/raw/main/images/Light/Keenetic-apps-Light.jpg">
    </picture>
  </a>
</p>

На компьютере с помощью файлового менеджера подключитесь к диску по сети (в ОС Windows можно использовать Проводник). В настройках роутера предварительно должно быть включено приложение "[Сервер SMB](https://help.keenetic.com/hc/ru/articles/360000812220-Сервер-SMB-доступ-к-файлам-и-принтерам)" для доступа к подключаемым USB-дискам по сети.

В корне раздела диска создайте директорию **install**, куда положите файл **mipsel-installer.tar.gz**.

<p align="center">
  <a href="http://192.168.1.1/apps/device/Media0" target="_blank" rel="noopener noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Corvus-Malus/XKeen-docs/raw/main/images/Dark/Explorer-install-Dark.jpg">
      <img width="100%" height="100%" src="https://github.com/Corvus-Malus/XKeen-docs/raw/main/images/Light/Explorer-install-Light.jpg">
    </picture>
  </a>
</p>
<br>
В поле "Накопитель" выберите диск OPKG (метка EXT4-раздела)

Нажмите **Сохранить**.

**4) Скачайте [Termius](https://termi.us/win)**

